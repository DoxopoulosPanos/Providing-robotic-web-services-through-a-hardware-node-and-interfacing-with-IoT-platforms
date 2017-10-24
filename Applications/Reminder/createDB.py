import sqlite3,time, datetime, calendar
from datetime import date


db = sqlite3.connect("my_database.sql") #you can put whatever ... created if not exist
conn = db.cursor()

conn.execute("CREATE TABLE IF NOT EXISTS Activities (timestamp int, name text, recurrence text, repeatence text);")

def AddActivity(activityName, year, month, day, hour, minutes, recurring, repeat):
    #today = datetime.date.today()
    #now = datetime.datetime.now()
    #reminderAt = datetime.datetime(year, month, day, hour, minutes)
    reminderAt = time.mktime((year,month,day,hour,minutes,0,0,0,-1))
    conn.execute("INSERT INTO Activities (timestamp, name, recurrence, repeatence) VALUES (?,?,?,?)",(reminderAt,activityName, recurring, repeat))
    db.commit()
    #conn.execute("INSERT INTO Activities (timestamp,name) VALUES (?,?)",(time.time(),activityName))
    #db.commit()

def AddActivityByTimestamp(activityName, reminderAt, recurring, repeat):
    #today = datetime.date.today()
    #now = datetime.datetime.now()
    #reminderAt = datetime.datetime(year, month, day, hour, minutes)
    #reminderAt = time.mktime((year,month,day,hour,minutes,0,0,0,-1))
    conn.execute("INSERT INTO Activities (timestamp, name, recurrence, repeatence) VALUES (?,?,?,?)",(reminderAt,activityName, recurring, repeat))
    db.commit()

def GetAllActivitiesOnDate(year, month, day):
    start_time = time.mktime((year,month,day,0,0,0,0,0,-1))
    end_time = time.mktime((year,month,day,23,59,0,0,0,-1)) #use 1 for last  argument if you live somewhere with dst
    conn.execute("SELECT * FROM Activities WHERE timestamp > ? AND timestamp < ?",(start_time,end_time))
    return conn.fetchall()

#def GetAllRecurringActivities(year, month, day):
#    start_time = time.mktime((year,month,day,0,0,0,0,0,-1))
#    end_time = time.mktime((year,month,day,23,59,0,0,0,-1)) #use 1 for last  argument if you live somewhere with dst
#    my_date = date.today()
#    today = calendar.day_name[my_date.weekday()]
#    conn.execute("SELECT * FROM Activities WHERE timestamp > ? AND timestamp < ? AND recurring == ? AND weekday = ?",(start_time,end_time,'yes',today))
#    return conn.fetchall()


#check the database
#print(reminder.GetAllActivitiesOnDate(2017,9,18))

#https://stackoverflow.com/questions/15627656/a-good-way-to-store-date-based-data-using-python
