from datetime import date, timedelta, time
import datetime
import sqlite3 as sql
import xlrd

with sql.connect("rrdata.db") as con:
    cur = con.cursor()

    cur.execute("DROP TABLE if EXISTS passengers")
    cur.execute("CREATE TABLE passengers ("
                "passenger_id INTEGER PRIMARY KEY,"
                "fname varchar(30) NOT NULL,"
                "lname varchar(100) NOT NULL,"
                "email varchar(100) NOT NULL,"
                "password varchar(100) NOT NULL,"
                "preferred_billing_address varchar(100) DEFAULT NULL,"
                "preferred_card_number varchar(16) NOT NULL)")

    cur.execute("DROP TABLE if EXISTS segments")
    cur.execute("CREATE TABLE segments ("
                "segment_id INTEGER PRIMARY KEY,"
                "seg_n_end int(11) DEFAULT NULL,"
                "seg_s_end int(11) DEFAULT NULL,"
                "seg_fare decimal(7,2) NOT NULL )")

    cur.execute("DROP TABLE if EXISTS seats_free")
    cur.execute("CREATE TABLE seats_free ("
                "train_id int NOT NULL,"
                "segment_id int NOT NULL,"
                "seat_free_date DEFAULT NULL,"
                "freeseat int(11) NOT NULL,"
                "FOREIGN KEY (train_id) REFERENCES trains (train_id),"
                "FOREIGN KEY (segment_id) REFERENCES segments (segment_id)"
                ")")

    cur.execute("DROP TABLE if EXISTS stations")
    cur.execute("CREATE TABLE stations ("
                "station_id INTEGER PRIMARY KEY,"
                "station_name varchar(40) NOT NULL,"
                "station_symbol char(3) NOT NULL )")

    cur.execute("DROP TABLE if EXISTS stops_at")
    cur.execute("CREATE TABLE stops_at ("
                "train_id int DEFAULT NULL,"
                "station_id int DEFAULT NULL,"
                "time_in char NOT NULL,"
                "time_out char NOT NULL )")

    cur.execute("DROP TABLE if EXISTS trains")
    cur.execute("CREATE TABLE trains ("
                "train_id int NOT NULL,"
                "train_start int NOT NULL,"
                "train_end int NOT NULL,"
                "train_direction tinyint(1) NOT NULL,"
                "train_days tinyint(1) NOT NULL)")

    cur.execute("DROP TABLE if EXISTS trips")
    cur.execute("CREATE TABLE trips ("
                "trip_id INTEGER PRIMARY KEY,"
                "trip_date date DEFAULT NULL,"
                "trip_time TIME DEFAULT NULL,"
                "start int(11) NOT NULL,"
                "end int(11) NOT NULL,"
                "train_id int(11) NOT NULL,"
                "passenger_id int NOT NULL,"
                "fare decimal(7,2) NOT NULL,"
                "payment_method boolean NOT NULL, "
                "FOREIGN KEY (train_id) REFERENCES trains (train_id),"
                "FOREIGN KEY (start) REFERENCES segments (segment_id),"
                "FOREIGN KEY (end) REFERENCES segments (segment_id),"
                "FOREIGN KEY (passenger_id) REFERENCES passengers (passenger_id))")



    # data for stations
    cur.execute("""INSERT INTO stations (station_id, station_name, station_symbol) VALUES


                (1, 'Boston - North Station', 'BON'),
                (2 , 'Boston - South Station, MA', 'BOS'),
                (3, 'Boston - Back Bay Station, MA', 'BBY'),
                (4, 'Route 128, MA', 'RTE'),
                (5, 'Providence, RI', 'PVD'),
                (6, 'Kingston, RI', 'KIN'),
                (7, 'Westerly, RI', 'WLY'),
                (8, 'Mystic, CT', 'MYS'),
                (9, 'New London, CT', 'NLC'),
                (10, 'Old Saybrook, CT', 'OSB'),
                (11, 'New Haven, CT', 'NHV'),
                (12, 'Bridgeport, CT', 'BRP'),
                (13, 'Stamford, CT', 'STM'),
                (14, 'New Rochelle, NY', 'NRO'),
                (15, 'New York - Penn Station, NY', 'NYP'),
                (16, 'Newark, NJ', 'NWK'),
                (17, 'Newark - International Airport', 'EWR'),
                (18, 'Metropark, NJ', 'MET'),
                (19, 'Trenton, NJ', 'TRE'),
                (20, 'Philadelphia - 30th Street Sta', 'PHL'),
                (21, 'Wilmington - Joseph R. Biden J', 'WIL'),
                (22, 'Aberdeen, MD', 'ABE'),
                (23, 'Baltimore - Penn Station, MD', 'BAL'),
                (24, 'BWI Marshall Airport, MD', 'BWI'),
                (25, 'New Carrollton, MD', 'NCR'),
                (26, 'Washington - Union Station, DC', 'WAS')""")

    cur.execute("""INSERT INTO trains VALUES
                (1,1,25,0,1),
                (2,1,25,0,1),
                (3,1,25,0,1),
                (4,1,25,0,1),
                (5,1,25,0,1),
                (6,1,25,0,1),
                (7,1,25,0,1),
                (8,1,25,0,1),
                (9,1,25,0,1),
                (10,1,25,0,1),
                (11,1,25,0,1),
                (12,1,25,0,1),
                (13,25,1,1,1),
                (14,25,1,1,1),
                (15,25,1,1,1),
                (16,25,1,1,1),
                (17,25,1,1,1),
                (18,25,1,1,1),
                (19,25,1,1,1),
                (20,25,1,1,1),
                (21,25,1,1,1),
                (22,25,1,1,1),
                (23,25,1,1,1),
                (24,25,1,1,1),
                (25,1,25,0,0),
                (26,1,25,0,0),
                (27,1,25,0,0),
                (28,1,25,0,0)""")


    cur.execute("""INSERT INTO segments VALUES
                    (1,1,2,2.82),
                    (2,2,3,4.7),
                    (3,3,4,11.75),
                    (4,4,5,9.87),
                    (5,5,6,6.11),
                    (6,6,7,5.17),
                    (7,7,8,7.05),
                    (8,8,9,8.93),
                    (9,9,10,15.51),
                    (10,10,11,10.34),
                    (11,11,12,12.69),
                    (12,12,13,9.87),
                    (13,13,14,13.63),
                    (14,14,15,7.99),
                    (15,15,16,2.35),
                    (16,16,17,6.11),
                    (17,17,18,10.81),
                    (18,18,19,12.69),
                    (19,19,20,9.87),
                    (20,20,21,12.69),
                    (21,21,22,11.75),
                    (22,22,23,6.11),
                    (23,23,24,6.58),
                    (24,24,25,7.05)""")

def insert_stops_at():
    book = xlrd.open_workbook("stops_at_updated.xls")
    sheet = book.sheet_by_name("source")

    query = """INSERT INTO stops_at (train_id, station_id, time_in, time_out)
            VALUES (?,?,?,?)"""


    for r in range(0, sheet.nrows):
        train_id = int(sheet.cell(r,0).value)
        station_id = int(sheet.cell(r,1).value)

        y = sheet.cell(r,2).value
        y = int(y * 24 * 3600) # convert to number of seconds
        time_in = str(time(y//3600, (y%3600)//60, y%60)) # hours, minutes, seconds

        x = sheet.cell(r,3).value
        x = int(x * 24 * 3600) # convert to number of seconds
        time_out = str(time(x//3600, (x%3600)//60, x%60)) # hours, minutes, seconds

        values = (train_id, station_id, time_in, time_out)

        cur.execute(query, values)
        con.commit()

insert_stops_at()

def insert_seats_free():
    book = xlrd.open_workbook("seats_free.xlsx")
    sheet = book.sheet_by_name("source")

    query = """INSERT INTO seats_free (train_id, segment_id, seat_free_date, freeseat)
            VALUES (?,?,?,?)"""


    for r in range(0, sheet.nrows):
        try:
            train_id = int(sheet.cell(r,0).value)
            segment_id = int(sheet.cell(r,1).value)

            seat_free_date = str(xlrd.xldate.xldate_as_datetime(sheet.cell(r,2).value, book.datemode))

            freeseat = sheet.cell(r,3).value

            values =  (train_id, segment_id, seat_free_date, freeseat)
            print(values)
            cur.execute(query, values)
            con.commit()
        except:
            pass



insert_seats_free()
