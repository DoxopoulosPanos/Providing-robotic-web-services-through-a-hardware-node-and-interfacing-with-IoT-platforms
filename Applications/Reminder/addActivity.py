#!/usr/bin/python2

import requests
import createDB as r


if __name__ == "__main__":

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    resource = 'http://localhost:8080/Mashape/RemindersNLP'
    phrase = 'remind me to take my medicine in 2 minutes'
    #phrase = 'remind me to do the exercise every 2 minutes'
    timezone = 'Europe/Athens'      #or timezone = 'GMT+03:00'

    #print("Request with params:\n{0}", headers)
    response = requests.get(resource, headers=headers, params={'phrase': phrase, 'timezone': timezone})
    print("Response: {0}", response.text)

    result = response.json()
    # day, year, month, hour, minute, weekday
    activityName = result['body']
    day = int(result['day'])
    year = int(result['year'])
    month = int(result['month'])
    hour = int(result['hour'])
    minute = int(result['minute'])
    recurring = result['recurring']
    if (recurring == 'yes'):
        repeat = result['repeat']
    else:
        repeat = 'no'


    if result['status'] == 'FUTURE':
        r.AddActivity(activityName, year,month,day,hour,minute, recurring, repeat)
        print('activity added')
