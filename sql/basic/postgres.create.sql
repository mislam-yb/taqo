DROP TABLE IF EXISTS t1 CASCADE;
DROP TABLE IF EXISTS t2 CASCADE;
DROP TABLE IF EXISTS t3 CASCADE;
DROP TABLE IF EXISTS ts2 CASCADE;
DROP TABLE IF EXISTS ts3 CASCADE;

CREATE TABLE t1(k1 int,
                k2 text,
                v1 int,
                v2 text,
                PRIMARY KEY(k1, k2));
CREATE INDEX ON t1(v1, k2);
COPY t1 FROM '$DATA_PATH/data/t1.csv' DELIMITER ',';

CREATE TABLE t2(k1 int,
                k2 text,
                v1 int,
                v2 text,
                PRIMARY KEY(k1, k2));
CREATE INDEX ON t2(v1, k2);
COPY t2 FROM '$DATA_PATH/data/t2.csv' DELIMITER ',';

CREATE TABLE t3(k1 int,
                k2 text,
                v1 int,
                v2 text,
                PRIMARY KEY(k1, k2));
CREATE INDEX ON t3(v1, k2);
COPY t3 FROM '$DATA_PATH/data/t3.csv' DELIMITER ',';

CREATE TABLE ts2(k1 int,
                 k2 text,
                 v1 int,
                 v2 text,
                 PRIMARY KEY(k1, k2));
CREATE INDEX ON ts2(v1, k2);
COPY ts2 FROM '$DATA_PATH/data/ts2.csv' DELIMITER ',';

CREATE TABLE ts3(k1 int,
                 k2 text,
                 v1 int,
                 v2 text,
                 PRIMARY KEY(k1, k2));
CREATE INDEX ON ts3(v1, k2);
COPY ts3 FROM '$DATA_PATH/data/ts3.csv' DELIMITER ',';