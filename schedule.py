import requests
import json 
import datetime

def parseDates(date, time):
    dateArray = date.split("-")
    timeArray = time[0:-1].split(":")
    dateArray = [int(num) for num in dateArray] 
    timeArray = [int(num) for num in timeArray] 
    print(dateArray, timeArray)
    return datetime.datetime(dateArray[0], dateArray[1], dateArray[2], hour=timeArray[0]+2, minute=timeArray[1], second=timeArray[2])

if __name__ == '__main__':
    res = requests.get(f'https://ergast.com/api/f1/current/next.json')
    response = json.loads(res.text)
    nextRace = response["MRData"]["RaceTable"]["Races"][0]
    print(parseDates(nextRace['date'], nextRace['time']))