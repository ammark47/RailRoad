import sqlite3
import datetime
import datetime as dt


def get_stations():
    db = sqlite3.connect('rrdata.db')
    cursor = db.cursor()
    cursor.execute('select * from stations')
    stations = cursor.fetchall()
    return stations

def get_available_trains(dep_date,outgoing_station,destination_station):
    direction = get_direction(int(outgoing_station),int(destination_station))

    db = sqlite3.connect('rrdata.db')
    cursor = db.cursor()

    cursor.execute("SELECT seats_free.train_id, seats_free.seat_free_date, stops_at.time_in FROM seats_free INNER JOIN "
                             " stops_at ON seats_free.train_id = stops_at.train_id WHERE seats_free.seat_free_date = '{}' and "
                             " stops_at.station_id = '{}' and seats_free.segment_id = '{}' "
                   "and seats_free.train_id in (SELECT train_id FROM trains WHERE train_direction = '{}')".format(dep_date,outgoing_station,destination_station,direction))
    return cursor.fetchall()

def get_direction(outgoing_station,destination_station):
    if outgoing_station - destination_station < 0:
        return 0 #south
    else:
        return 1 #north

def get_seats_free(start_station,end_station,date,tickets):
    db = sqlite3.connect('rrdata.db')
    cursor = db.cursor()
    start_station = int(start_station)
    end_station = int(end_station)


    for x in range(start_station,end_station):
       sf_free = cursor.execute("SELECT freeseat-1 FROM seats_free WHERE segment_id = '{}' AND  seat_free_date = '{}'".format(x,date)).fetchone()

       if sf_free[0] < 0:
           return False

    return True

def decrease_seats_free(train_num,date,outgoing_station,destination_station,tickets):
    db = sqlite3.connect('rrdata.db')
    cursor = db.cursor()
    if int(outgoing_station) < int(destination_station):
        start = outgoing_station
        end = destination_station
    else:
        start = destination_station
        end = outgoing_station
    for x in range(start,end+1):
        print(x)
        cursor.execute("UPDATE seats_free SET sf_free = sf_free -'{}' WHERE train_num = '{}' and sf_segment_id = '{}' "
                       "and sf_date = '{}'".format(tickets,train_num,x,date))
        db.commit()

def get_destination_stations(outgoing_station,destination_station):
    db= sqlite3.connect('rrdata.db')
    cursor = db.cursor()
    start = cursor.execute("SELECT station_name FROM stations WHERE station_id = '{}'".format(outgoing_station)).fetchone()
    end =  cursor.execute("SELECT station_name FROM stations WHERE station_id = '{}'".format(destination_station)).fetchone()
    result = (start[0],end[0])
    return result
