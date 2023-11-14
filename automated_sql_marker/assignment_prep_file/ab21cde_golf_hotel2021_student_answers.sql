/* Golfing database */

/* Under each comment modify and/or add the relevant code - DO NOT REMOVE THE COMMENTS */

/* Task 1 - correct the errors in this script file */

DROP VIEW ab21cde_golfing_history CASCADE  CONSTRAINTS;  ---------------Renamed to golfing_history to match naming in the question.
DROP TABLE ab21cde_hotel_staff CASCADE CONSTRAINTS;
DROP TABLE ab21cde_booking CASCADE CONSTRAINTS;  -----------------------*1-Missing CONSTRAINTS keyword
DROP TABLE ab21cde_golfer CASCADE  CONSTRAINTS;
DROP TABLE ab21cde_room CASCADE  CONSTRAINTS;
DROP TABLE ab21cde_hotel CASCADE  CONSTRAINTS;

CREATE TABLE ab21cde_hotel  --------------------------------------------*2-"hotel" table not created
(hotel_numb NUMBER(2) NOT NULL PRIMARY KEY,
name VARCHAR2(30),
street VARCHAR2(20),
town VARCHAR2(20),
region VARCHAR2(20),
postcode VARCHAR2(8),
tel_numb VARCHAR2(13));

CREATE TABLE ab21cde_room
(room_numb NUMBER(4) NOT NULL,                                   			
hotel_numb NUMBER(2) NOT NULL REFERENCES ab21cde_hotel(hotel_numb),
room_type VARCHAR2(1),
tariff NUMBER(5,2),
PRIMARY KEY(room_numb, hotel_numb));                            

CREATE TABLE ab21cde_golfer  --------------------------------------------*3-Missing "TABLE" in declaration of "CREATE TABLE" 
(golfer_numb NUMBER(6) NOT NULL PRIMARY KEY,
firstname VARCHAR2(25),
surname VARCHAR2(25),
street VARCHAR2(20),
town VARCHAR2(20),  ----------------------------------------------------*4-Missing town, datatype and constraint.
region VARCHAR2(20),
postcode VARCHAR2(8),
tel_numb VARCHAR2(13));  -----------------------------------------------*5-tel_numb Should be of type varchar2

CREATE TABLE ab21cde_booking
(hotel_numb NUMBER(2) NOT NULL REFERENCES ab21cde_hotel(hotel_numb),
golfer_numb NUMBER(6) NOT NULL REFERENCES ab21cde_golfer(golfer_numb),
date_from DATE NOT NULL,  -----------------------------------------------*6-NOT NULL AND data type incorrectly ordered
date_to DATE, -----------------------------------------------------------*7-date_to incorrectly labeled as date_from
room_numb NUMBER(4),  ---------------------------------------------------*8-room_numb should be '4' numbers in length not '2'
PRIMARY KEY(hotel_numb, golfer_numb, date_from));               



/* Task 2 - Add below your SQL INSERT commands to insert all the data into your tables */

--=======================hotel insert statements

INSERT INTO ab21cde_hotel
VALUES(1, 'the grange', 'abernethy road', 'wentworth', 'surrey', 'gu25 3lx', '01344-84672');

INSERT INTO ab21cde_hotel
VALUES (2, 'cock and bull', 'stirling street', 'troon', 'ayrshire', 'ka10 6ep', '01292-43245');

INSERT INTO ab21cde_hotel
VALUES (3, 'the nineteenth tee', 'golf avenue', 'carnoustie', 'angus', 'dd7 8fd', '01241-820654');

INSERT INTO ab21cde_hotel
VALUES (4, 'the grand', 'main street', 'lytham st annes', 'lancashire', 'fy8 3pc', '01253-724432');

INSERT INTO ab21cde_hotel
VALUES(5, 'putters delight', 'market street', 'st andrews', 'fife', 'ky16 8pq', '01334-888834');

INSERT INTO ab21cde_hotel
VALUES(6, 'the lost ball', 'petticoat lane', 'turnberry', 'ayrshire', 'ka26 9lh', '01655-331543');

--=======================room insert statements
INSERT INTO ab21cde_room
VALUES(108, 1, 'f', 105);
INSERT INTO ab21cde_room
VALUES(118, 1, 'd', 125);
INSERT INTO ab21cde_room
VALUES(123, 1, 'd', 125);
INSERT INTO ab21cde_room
VALUES(203, 1, 'f', 115);
INSERT INTO ab21cde_room
VALUES(205, 1, 's', 95);
INSERT INTO ab21cde_room
VALUES(18, 2, 's', 110);
INSERT INTO ab21cde_room
VALUES(21, 2, 's', 110);
INSERT INTO ab21cde_room
VALUES(32, 2, 'd', 120);
INSERT INTO ab21cde_room
VALUES(45, 2, 'd', 125);
INSERT INTO ab21cde_room
VALUES(46, 2, 'f', 135);
INSERT INTO ab21cde_room
VALUES(54, 2, 'f', 140);
INSERT INTO ab21cde_room
VALUES(1, 3, 's', 80);
INSERT INTO ab21cde_room
VALUES(2, 3, 's', 80);
INSERT INTO ab21cde_room
VALUES(3, 3, 'd', 90);
INSERT INTO ab21cde_room
VALUES(4, 3, 'd', 95);
INSERT INTO ab21cde_room
VALUES(5, 3, 'f', 105);
INSERT INTO ab21cde_room
VALUES(6, 3, 'f', 10);
INSERT INTO ab21cde_room
VALUES(201,	4, 's', 85);
INSERT INTO ab21cde_room
VALUES(202,	4, 's', 90);
INSERT INTO ab21cde_room
VALUES(203,	4, 's', 85);
INSERT INTO ab21cde_room
VALUES(212,	4, 'd', 10);
INSERT INTO ab21cde_room
VALUES(213,	4, 'd', 105);
INSERT INTO ab21cde_room
VALUES(220,	4, 'f', 120);
INSERT INTO ab21cde_room
VALUES(201,	5, 's', 65);
INSERT INTO ab21cde_room
VALUES(203,	5, 's', 65);
INSERT INTO ab21cde_room
VALUES(205,	5, 's', 75);
INSERT INTO ab21cde_room
VALUES(320,	5, 'f', 85);
INSERT INTO ab21cde_room
VALUES(321,	5, 'f', 85);
INSERT INTO ab21cde_room
VALUES(322,	5, 'f', 85);
INSERT INTO ab21cde_room
VALUES(10, 6, 'd', 95);
INSERT INTO ab21cde_room
VALUES(11, 6, 'd', 85);
INSERT INTO ab21cde_room
VALUES(12, 6, 'd', 90);
INSERT INTO ab21cde_room
VALUES(21, 6, 's', 75);
INSERT INTO ab21cde_room
VALUES(22, 6, 's', 78);
INSERT INTO ab21cde_room
VALUES(31, 6, 'f', 110);

--=======================golfer insert statements
INSERT INTO ab21cde_golfer
VALUES(1001, 'james', 'bolan', '65 somerset drive', 'felling', 'tyne and wear', 'sr1 3yt', '01915-562345');
INSERT INTO ab21cde_golfer
VALUES(1002, 'david', 'hanratty', '23 high street', 'kinghorn', 'fife', 'kh7 2as', NULL);
INSERT INTO ab21cde_golfer
VALUES(1003, 'helen', 'davis', '17 new lane', 'windygates', 'fife', 'ky3 4ds', '01856-674567');
INSERT INTO ab21cde_golfer
VALUES(1004, 'brian', 'jones', '47 stratton street', 'milton keynes', 'buckinghamshire', 'br1 6bg', '01812-454456');
INSERT INTO ab21cde_golfer
VALUES(1005, 'jean', 'simmons', '56 lime street', 'bolton', 'lancashire', 'bt2 9gh', '01877-236543');
INSERT INTO ab21cde_golfer
VALUES(1006, 'margaret', 'thompson', '33 roker avenue', 'sunderland', 'tyne and wear', 'sr2 8rt', NULL);
INSERT INTO ab21cde_golfer
VALUES(1007, 'john', 'brown', '6 leafy grove', 'rothbury', 'northumberland', 'ns8 3jl', '01915-123678');
INSERT INTO ab21cde_golfer
VALUES(1008, 'mark', 'abingdon', '17 new lane', 'harleston', 'norfolk', 'nr6 2fr', '01824-32356');

--=======================booking insert statements
INSERT INTO ab21cde_booking
VALUES(1, 1002, '14-Nov-19', '21-Nov-19', 118);
INSERT INTO ab21cde_booking
VALUES(3, 1007, '04-Jun-19', '09-Jun-19', 4);
INSERT INTO ab21cde_booking
VALUES(3, 1005, '02-Feb-20', '05-Feb-20', 6);
INSERT INTO ab21cde_booking
VALUES(2, 1004, '23-Oct-19', '25-Oct-19', 32);
INSERT INTO ab21cde_booking
VALUES(6, 1001, '12-Jan-20', '15-Jan-20', 21);
INSERT INTO ab21cde_booking
VALUES(5, 1002, '01-Jul-19', '05-Jul-19', 320);
INSERT INTO ab21cde_booking
VALUES(6, 1005, '28-Feb-20', '03-Mar-20', 12);
INSERT INTO ab21cde_booking
VALUES(2, 1006, '07-Dec-19', '11-Dec-19', 45);
INSERT INTO ab21cde_booking
VALUES(1, 1008, '12-Jan-20', '13-Jan-20', 203);
INSERT INTO ab21cde_booking
VALUES(4, 1002, '09-Oct-19', '13-Oct-19', 220);
INSERT INTO ab21cde_booking
VALUES(3, 1003, '11-Apr-20', '18-Apr-20', 2);
INSERT INTO ab21cde_booking
VALUES(1, 1004, '17-Mar-20', '21-Mar-20', 118);
INSERT INTO ab21cde_booking
VALUES(6, 1001, '19-May-20', '22-May-20', 31);

/* Task 3 - Enter each your SQL query to answer each question under the relevant comment */

/* Task 3 - Question 1 */

SELECT surname, firstname, town, postcode, region
FROM ab21cde_golfer
WHERE initcap(region) <> 'Northumberland';

/* Task - 3 - Question 2 - Mark [3] */

SELECT surname, firstname, date_from, date_to
FROM golfer g, booking b
WHERE b.golfer_numb = g.golfer_numb
ORDER BY surname DESC, date_from ASC;

/* Task 3 - Question 3 - Mark [4] */

SELECT name, count(room_numb) golfing_rooms, max(tariff) maximum, min(tariff) minimum, round(avg(tariff), 2) average
FROM hotel h, room r
WHERE r.hotel_numb = h.hotel_numb
GROUP BY name
ORDER BY name ASC;

/* Task 3 - Question 4 - Mark [5]*/

CREATE TABLE hotel_staff
(staff_numb NUMBER(4) NOT NULL PRIMARY KEY,
surname VARCHAR2(25) NOT NULL,
initials VARCHAR2(2),
hotel_numb NUMBER(2) REFERENCES hotel(hotel_numb),
position VARCHAR2(15) NOT NULL,
salary NUMBER(6) NOT NULL);

/* Task 3 - Question 5 - Mark [1]*/

INSERT INTO hotel_staff
VALUES(1, 'Baker', 'ML', 3, 'Manager', 75000);

/* Task 3 - Question 6 - Mark [1]*/
INSERT INTO hotel_staff
VALUES(2, 'Butler', 'R', 1, 'Reception', 22000);


/* Task 3 - Question 7 - Mark [7]*/

SELECT golfer_numb, substr(firstname,1,1)||', '|| surname fullname, substr(tel_numb,1,5)||' '||substr(tel_numb,7,13) telephone_no
FROM golfer
WHERE tel_numb <> 'NULL';

/* Task 3 - Question 8 [8] */

CREATE VIEW golfing_history AS
SELECT golfer_numb, count(room_numb) bookings
FROM booking
GROUP BY golfer_numb
ORDER BY bookings ASC;

/* Task 3 - Question 9 - Mark [9]*/

SELECT bk.golfer_numb, bk.date_from, h.name, bk.room_numb
FROM booking bk
JOIN hotel h ON bk.hotel_numb = h.hotel_numb
JOIN golfing_history gh1 ON bk.golfer_numb = gh1.golfer_numb
WHERE gh1.bookings = (SELECT min(gh2.bookings)
                      FROM golfing_history gh2)
ORDER BY bk.date_from DESC;

/* Task 3 - Question 10 - Mark [10] */

ALTER TABLE golfer
MODIFY surname VARCHAR2(30) NOT NULL;

/* Task 3 - Question 12 - Mark [6]*/
ALTER TABLE golfer
MODIFY firstname NOT NULL;

/* Task 3 - Question 13 - Mark [6]*/
ALTER TABLE booking
ADD CONSTRAINT fk_bkg_rm_no FOREIGN KEY (room_numb, hotel_numb) REFERENCES room(room_numb, hotel_numb)

/* commit to db */
COMMIT