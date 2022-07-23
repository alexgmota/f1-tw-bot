import requests
import json 
import datetime

def getRaceSchedule():
    res = requests.get(f'https://ergast.com/api/f1/current/next.json')
    response = json.loads(res.text)
    return response["MRData"]["RaceTable"]["Races"][0]

def parseDates(date, time):
    dateArray = date.split("-")
    timeArray = time[0:-1].split(":")
    dateArray = [int(num) for num in dateArray] 
    timeArray = [int(num) for num in timeArray] 
    return datetime.datetime(dateArray[0], dateArray[1], dateArray[2], hour=timeArray[0]+2, minute=timeArray[1], second=timeArray[2])

def getRaceDate(data):
    return parseDates(data['date'], data['time'])
    
def getQualiDate(data):
    qualy = data["Qualifying"]
    return parseDates(qualy['date'], qualy['time'])

def getFP1Date(data):
    fp = data["FirstPractice"]
    return parseDates(fp['date'], fp['time'])

def getFP2Date(data):
    fp = data["SecondPractice"]
    return parseDates(fp['date'], fp['time'])

def getFP3Date(data):
    fp = data["ThirdPractice"]
    return parseDates(fp['date'], fp['time'])


if __name__ == '__main__':
    data = getRaceSchedule()
    print(getFP1Date(data))
    print(getFP2Date(data))
    print(getFP3Date(data))
    print(getQualiDate(data))
    print(getRaceDate(data))