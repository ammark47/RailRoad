import sqlite3
import datetime
import datetime as dt


def get_stations():
    db = sqlite3.connect('rrdata.db')
    cursor = db.cursor()
    cursor.execute('select * from stations')
    stations = cursor.fetchall()
    return stations

def get_all_available_trains(dep_date,outgoing_station,destination_station):
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
