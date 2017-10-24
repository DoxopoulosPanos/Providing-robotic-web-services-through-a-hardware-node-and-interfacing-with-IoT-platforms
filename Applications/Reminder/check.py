import createDB as r
import datetime
import time
import re
import calendar
import requests
import json

#r.AddActivity("Jumping Jacks", 2017, 8, 3, 17, 3)
#time.sleep(10)
#r.AddActivity("Push Ups")

today = datetime.datetime.today()
now = datetime.datetime.now()
activities = r.GetAllActivitiesOnDate(today.year, today.month,today.day)
#activities = r.GetAllActivitiesOnDate(2012,10,5)
print "Found %d Entries"%len(activities)
for activity in activities:
    temp = time.localtime(int(activity[0]))
    print temp.tm_year
    print temp.tm_mday
    print "Activity %s @ %s"%(activity[1],time.strftime("%x %X",time.localtime(int(activity[0]))))
print("\n\n\n")
print activities

while(True):
    activities = r.GetAllActivitiesOnDate(today.year, today.month,today.day)
    today = datetime.datetime.today()
    now = datetime.datetime.now()
    for activity in activities:
        temp = time.localtime(int(activity[0]))
        if (now.year ==  temp.tm_year) & (now.month == temp.tm_mon) & (now.day == temp.tm_mday) & (now.hour == temp.tm_hour)& (now.minute == temp.tm_min):
            print "Activity %s @ %s"%(activity[1],time.strftime("%x %X",time.localtime(int(activity[0]))))
            #start REMEDES if needed
            if 'exercise' in activity[1]:
                print 'starting exercise'
                REMEDEScall = requests.put('http://192.168.3.101:8008/ProxyMC/startAutomaticExercise', headers={"Content-Type": "application/json"}, params={'username':'guest'}, data = json.dumps({"training":0, "totalTime": 30, "brightness": 50, "minDist": 0, "maxDist": 0.2, "minAct": 1, "maxAct":5, "minDelay":1, "maxDelay":2, "validColors": ["ff0000"], "invalidColors": ["00ff00"], "type": "continuous", "templateId": None, "diffpads":1}))
                REMEDESresults = REMEDEScall.json()
                #print REMEDESresults
                print REMEDESresults['comments']
            #if activity is recurring, add the same activity again
            if activity[2]=='yes':
                activity3 = re.split(',', activity[3])
                if activity3[0] == 'MINUTES':
                    temp_delta = datetime.timedelta(minutes=int(activity3[1]))
                elif activity3[0] == 'HOURS':
                    temp_delta = datetime.timedelta(hours=int(activity3[1]))
                elif activity3[0] == 'DAYS':
                    temp_delta = datetime.timedelta(days=int(activity3[1]))
                elif activity3[0] == 'WEEKS':
                    temp_delta = datetime.timedelta(weeks=int(activity3[1]))
                elif activity3[0] == 'MONTHS':
                    daysOfCurrentMonth = calendar.monthrange(now.year, now.month)[1]
                    temp_delta = datetime.timedelta(days = daysOfCurrentMonth*int(activity3[1]))
                elif activity3[0] == 'YEARS':
                    temp_delta = datetime.timedelta(days = 365*int(activity3[1]))
                else:  #elif activity3[0] == 'MONDAYS' or activity3[0] == 'TUESDAYS' or activity3[0] == 'WEDNESDAYS' or activity3[0] == 'THURSDAYS' or activity3[0] == 'FRIDAYS' or activity3[0] == 'SATURDAYS' or activity3[0] == 'SUNDAYS':
                    temp_delta = datetime.timedelta(days = 7)
                temp_time = activity[0] +  temp_delta.seconds + (temp_delta.days*24*60*60)  #add minutes
                r.AddActivityByTimestamp(activityName = activity[1], reminderAt = temp_time, recurring = activity[2], repeat = activity[3])
                print('activity added')
    time.sleep(60) #wait for 1 minute
