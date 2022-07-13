from config import Config
from models.factory import get_test_model
from tests.regression.report import RegressionReport
from tests.abstract import AbstractTest
from utils import get_optimizer_score_from_plan, calculate_avg_execution_time, evaluate_sql


class RegressionTest(AbstractTest):

    def __init__(self):
        super().__init__()
        self.report = RegressionReport()

    @staticmethod
    def evaluate_queries_for_version(conn, queries):
        version_queries = []
        with conn.cursor() as cur:
            counter = 1
            for first_version_query in queries:
                try:
                    print(
                        f"Evaluating query {first_version_query.query[:40]}... [{counter}/{len(queries)}]")
                    evaluate_sql(cur, first_version_query.get_explain())
                    first_version_query.execution_plan = '\n'.join(
                        str(item[0]) for item in cur.fetchall())
                    first_version_query.optimizer_score = get_optimizer_score_from_plan(
                        first_version_query.execution_plan)

                    calculate_avg_execution_time(cur, first_version_query,
                                                 int(Config().num_retries))

                    version_queries.append(first_version_query)
                except Exception as e:
                    raise e
                finally:
                    counter += 1

        return version_queries

    def evaluate(self):
        self.start_db()

        conn = None

        try:
            conn = self.connect_to_db()

            with conn.cursor() as cur:
                evaluate_sql(cur, 'SELECT VERSION();')
                first_version = cur.fetchone()[0]

            # evaluate original query
            model = get_test_model()
            created_tables = model.create_tables(conn)
            queries = model.get_queries(created_tables)

            first_version_queries = self.evaluate_queries_for_version(conn, queries)

            conn.close()

            self.switch_version()

            # reconnect
            conn = self.connect_to_db()

            with conn.cursor() as cur:
                evaluate_sql(cur, 'SELECT VERSION();')
                second_version = cur.fetchone()[0]

            self.report.define_version(first_version, second_version)

            second_version_queries = self.evaluate_queries_for_version(conn, queries)

            for first_version_query, second_version_query in zip(first_version_queries,
                                                                 second_version_queries):
                self.report.add_query(first_version_query, second_version_query)
        finally:
            # publish current report
            self.report.build_report()
            self.report.publish_report("regression")

            # close connection
            conn.close()

            # stop yugabyte
            self.stop_db()
