

DROP TABLE IF EXISTS financial;
CREATE TABLE financial (
time TIMESTAMP PRIMARY KEY,
Open double precision, 
High double precision, 
Low	 double precision, 
Close double precision, 
Adj_Close double precision,
Volume double precision
);



DROP TABLE IF EXISTS financial2;
CREATE TABLE financial2 (
time TIMESTAMP PRIMARY KEY,
Open double precision, 
High double precision, 
Low	 double precision, 
Close double precision, 
Adj_Close double precision,
Volume double precision
);