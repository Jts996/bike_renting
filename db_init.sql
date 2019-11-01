/*
History:
-based on previous versions to create first copy 10/10/2019
-added back accounts table after review requirement with pay and charge mechanisum 10/10/2019
-added create_date field under users table for housekeeping 11/10/2019
-added user user_role table initial setup 11/10/2019
*/

/*users table contains user registration and authentication information*/
CREATE TABLE IF NOT EXISTS "users" (
	"user_id"	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	"email"	INTEGER NOT NULL UNIQUE,
	"phone_number"	INTEGER,
	"name"	TEXT,
	"password"	TEXT NOT NULL,
	"role_id"	INTEGER NOT NULL,
	"create_date"	TEXT NOT NULL,
	FOREIGN KEY("role_id") REFERENCES "user_roles"("role_id")
);

/*
user_roles table contains user role in system 
1-customer
2-operator
3-manager
*/
CREATE TABLE IF NOT EXISTS "user_roles" (
	"role_id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"description"	TEXT
);

/*orders table contains RENT/RETURN transaction details*/
CREATE TABLE IF NOT EXISTS "orders" (
	"order_id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"user_id"	INTEGER NOT NULL,
	"bike_id"	INTEGER NOT NULL,
	"start_datetime"	TEXT NOT NULL,
	"end_datetime"	TEXT,
	"amount"	REAL DEFAULT 0,
	FOREIGN KEY("bike_id") REFERENCES "bikes"("bike_id"),
	FOREIGN KEY("user_id") REFERENCES "users"("user_id")
);

/*bikes table contains bike info. and it's corresponding location
status can be DEFECT/AVAILABLE/PENDING_ACTION/INUSE
*/
CREATE TABLE IF NOT EXISTS "bikes" (
	"bike_id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"status"	TEXT NOT NULL,
	"parked_bike_station"	INTEGER,
	"loc_lat"	INTEGER,
	"loc_long"	INTEGER,
	FOREIGN KEY("parked_bike_station") REFERENCES "bike_stations"("station_id")
);

/*bike_stations table contains bike station info. including it's location,
bikes are parked there before RETURN action*/
CREATE TABLE IF NOT EXISTS "bike_stations" (
	"station_id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"post_code"	TEXT,
	"loc_lat"	INTEGER NOT NULL,
	"loc_long"	INTEGER NOT NULL,
	"bike_rack_number"	INTEGER NOT NULL
);

/*defect_report table contains defects reported by customers
status can be REP_DEFECT/REP_INVESTIGATE/FIXED */
CREATE TABLE IF NOT EXISTS "defect_report" (
	"report_id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"user_id"	INTEGER NOT NULL,
	"bike_id"	INTEGER NOT NULL,
	"category"	INTEGER NOT NULL,
	"details"	BLOB,
	"report_datetime"	TEXT NOT NULL,
	"status"	TEXT NOT NULL,
	FOREIGN KEY("user_id") REFERENCES "users"("user_id"),
	FOREIGN KEY("bike_id") REFERENCES "bikes"("bike_id")
);

/*accounts table contains balance of users*/
CREATE TABLE IF NOT EXISTS "accounts" (
	"user_id"	INTEGER NOT NULL PRIMARY KEY UNIQUE,
	"card_info"	TEXT,
	"total_amount"	REAL NOT NULL DEFAULT 0,
	"last_topup_datetime"	TEXT,
	"last_topup_amount"	REAL,
	FOREIGN KEY("user_id") REFERENCES "users"("user_id")
);

/*user role table initializaton*/
INSERT INTO user_roles (role_id, description) VALUES (1, 'Customer');
INSERT INTO user_roles (role_id, description) VALUES (2, 'Operator');
INSERT INTO user_roles (role_id, description) VALUES (3, 'Manager');

/*bike stations testing data loading*/
INSERT INTO bike_stations (station_id,post_code,loc_lat,loc_long,bike_rack_number) VALUES (1, 'G40BA',55.86729,-4.25006,10);
INSERT INTO bike_stations (station_id,post_code,loc_lat,loc_long,bike_rack_number) VALUES (2, 'G25RJ',55.86248,-4.26362,15);
INSERT INTO bike_stations (station_id,post_code,loc_lat,loc_long,bike_rack_number) VALUES (3, 'G11XQ',55.86125,-4.24471,8);
INSERT INTO bike_stations (station_id,post_code,loc_lat,loc_long,bike_rack_number) VALUES (4, 'G59TA',55.85254,-4.25184,20);

/*bikes testing data loading*/
INSERT INTO bikes (bike_id,status,parked_bike_station,loc_lat,loc_long) VALUES (1001,'A',1,55.86729,-4.25006);
INSERT INTO bikes (bike_id,status,parked_bike_station,loc_lat,loc_long) VALUES (1002,'A',1,55.86729,-4.25006);
INSERT INTO bikes (bike_id,status,parked_bike_station,loc_lat,loc_long) VALUES (1003,'A',1,55.86729,-4.25006);
INSERT INTO bikes (bike_id,status,parked_bike_station,loc_lat,loc_long) VALUES (1004,'A',1,55.86729,-4.25006);
INSERT INTO bikes (bike_id,status,parked_bike_station,loc_lat,loc_long) VALUES (1005,'A',2,55.86248,-4.26362);
INSERT INTO bikes (bike_id,status,parked_bike_station,loc_lat,loc_long) VALUES (1006,'A',2,55.86248,-4.26362);
INSERT INTO bikes (bike_id,status,parked_bike_station,loc_lat,loc_long) VALUES (1007,'A',3,55.86125,-4.24471);
INSERT INTO bikes (bike_id,status,parked_bike_station,loc_lat,loc_long) VALUES (1008,'A',3,55.86125,-4.24471);
INSERT INTO bikes (bike_id,status,parked_bike_station,loc_lat,loc_long) VALUES (1009,'A',4,55.85254,-4.25184);
INSERT INTO bikes (bike_id,status,parked_bike_station,loc_lat,loc_long) VALUES (1010,'A',4,55.85254,-4.25184);
INSERT INTO bikes (bike_id,status,parked_bike_station,loc_lat,loc_long) VALUES (1011,'A',4,55.85254,-4.25184);
INSERT INTO bikes (bike_id,status,parked_bike_station,loc_lat,loc_long) VALUES (1012,'D',4,55.85254,-4.25184);
INSERT INTO bikes (bike_id,status,parked_bike_station,loc_lat,loc_long) VALUES (1013,'U',4,55.86222,-4.25555);
INSERT INTO bikes (bike_id,status,parked_bike_station,loc_lat,loc_long) VALUES (1014,'U',4,55.85321,-4.24184);
INSERT INTO bikes (bike_id,status,parked_bike_station,loc_lat,loc_long) VALUES (1015,'U',4,55.85123,-4.25384);

/*defect ticket testing data loading*/
INSERT INTO defect_report (user_id,bike_id,category,details,report_datetime,status) VALUES (1,1012,'Others','no brake','2019-10-14 13:30','RD');
INSERT INTO defect_report (user_id,bike_id,category,details,report_datetime,status) VALUES (1,1013,'Others','broken chair','2019-10-15 12:30','RI');
INSERT INTO defect_report (user_id,bike_id,category,details,report_datetime,status) VALUES (1,1014,'Others','broken light','2019-10-18 11:30','DF');
INSERT INTO defect_report (user_id,bike_id,category,details,report_datetime,status) VALUES (1,1015,'Others','not function','2019-10-12 12:30','RD');
INSERT INTO defect_report (user_id,bike_id,category,details,report_datetime,status) VALUES (1,1007,'Others','wonderful','2019-10-11 16:30','RD');
