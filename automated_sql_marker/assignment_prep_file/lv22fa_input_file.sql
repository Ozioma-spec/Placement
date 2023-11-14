/* Golfing database */

/* sections to mark identifier */
/* <task: 1 - questions: 1, 3     , 5, 5, 7> */
/* <task: 2 - questions: 2, 4, 6, 8, 9> */
/* <task: 3 - questions: 10, 20, 30, 5, 15> */

/* Under each comment modify and/or add the relevant code - DO NOT REMOVE THE COMMENTS */

/* Task 1 - correct the errors in this script file */

DROP VIEW golfer_history CASCADE  CONSTRAINTS;
DROP TABLE hotel_staff CASCADE CONSTRAINTS;
DROP TABLE booking CASCADE;
DROP TABLE golfer CASCADE  CONSTRAINTS;
DROP TABLE room CASCADE  CONSTRAINTS;
DROP TABLE hotel CASCADE  CONSTRAINTS;

CREATE TABLE room
(room_numb NUMBER(4) NOT NULL,
hotel_numb NUMBER(2) NOT NULL REFERENCES hotel(hotel_numb),
room_type VARCHAR2(1),
tariff NUMBER(5,2),
PRIMARY KEY(room_numb, hotel_numb));

CREATE  golfer
(golfer_numb NUMBER(6) NOT NULL PRIMARY KEY,
firstname VARCHAR2(25),
surname VARCHAR2(25),
street VARCHAR2(20),
region VARCHAR2(20),
postcode VARCHAR2(8),
tel_numb NUMBER(13));

CREATE TABLE booking
(hotel_numb NUMBER(2) NOT NULL REFERENCES hotel(hotel_numb),
golfer_numb NUMBER(6) NOT NULL REFERENCES golfer(golfer_numb),
date_from NOT NULL DATE,
date_from DATE,
room_numb NUMBER(2),
PRIMARY KEY(hotel_numb, golfer_numb, date_from));

/* Task 2 - Add below your SQL INSERT commands to insert all the data into your tables */

/* Task 3 - Enter each your SQL query to answer each question under the relevant comment */

/* Task 3 - Question 1 */
in t3q1
/* Task 3 - Question 2 */
in t3q2
/* Task 3 - Question 3 */
in t3q3
/* Task 3 - Question 4 */
in t3q4
/* Task 3 - Question 5 */
in t3q5
/* Task 3 - Question 6 */
in t3q6
/* Task 3 - Question 7 */
in t3q7
/* Task 3 - Question 8 */
in t3q8
/* Task 3 - Question 9 */

COMMIT;
