SELECT * FROM p_timepass;
SET SQL_SAFE_UPDATES=0;

USE TIMEPASS;

SELECT * FROM C1;

SELECT DISTINCT(COURSE) FROM C1;

UPDATE C1 SET COURSE = NULL WHERE COURSE NOT IN ("Data Analytics","Machine Learning","Web Developmet","Data Analysis","Web Development");

UPDATE C1 SET COURSE = "Web Development" WHERE COURSE = "Web Developmet";

SELECT * FROM C1;