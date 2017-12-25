import sqlite3
import datetime
import datetime as dt


def get_stations():
    db = sqlite3.connect('rrdata.db')
    cursor = db.cursor()
    cursor.execute('select * from stations')
    stations = cursor.fetchall()
    return stations
