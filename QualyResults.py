import requests
import json 
import numpy as np
import matplotlib.pyplot as plt
from DriverInfo import getDriversCode, getDriversTeamColor

from DriverLapsComparator import strToSec

def getQualyLapTimes():
    res = requests.get('https://ergast.com/api/f1/current/last/qualifying.json')
    response = json.loads(res.text)
    lapTimes = []
    for i in response["MRData"]["RaceTable"]["Races"][0]['QualifyingResults']:
        lapTimes.append((i['Driver']['driverId'], getHigherQualyTime(i)))
    lapTimes.sort(key=comparator)
    return lapTimes, response["MRData"]["RaceTable"]["Races"][0]['raceName']


def getHigherQualyTime(qualyResult):
    try:
        time = getQ3Time(qualyResult)
    except:
        time = getLowerQualyTime(qualyResult)
    return strToSec(time)
def comparator(x):
    return x[1]

def getLowerQualyTime(qualyResult):
    try: 
        return getQ2Time(qualyResult)
    except:
        return getQ1Time(qualyResult)

def getQ3Time(qualyResult):
    return qualyResult['Q3']

def getQ2Time(qualyResult):
    return qualyResult['Q2']

def getQ1Time(qualyResult):
    return qualyResult['Q1']

def makeQualyGraph():
    times, raceName = getQualyLapTimes()
    driversId = list(map(getDrivers, times))
    normalizedTimes = normalizeQualyTimes(list(map(getTimes, times)))
    drivers = getDriversCode(driversId)
    colors = getDriversTeamColor(driversId)
    plt.style.use('./templates/mystyle.mplstyle')
    plt.figure(figsize=[10, 5])
    plt.title(f'Qualy Results\n{raceName}')
    plt.xlabel('Leader gap in %')
    
    plt.barh(drivers[::-1], normalizedTimes[::-1], color=colors[::-1])
    path = './images/qualyTimes.png'
    plt.savefig(path, dpi=300)
    plt.close()
    print('Figure qualy saved (qualyTimes.png)')
    return path


def getDrivers(i):
    return i[0]

def getTimes(i):
    return i[1]

def normalizeQualyTimes(times):
    normalizedTimes = [0]
    for i in times[1:]:
        normalizedTimes.append((i/times[0] - 1) * 100)
    return normalizedTimes

def makeQualyResultsMsg():
    img = makeQualyGraph()
    txt = "📈 Qualifying Results 📉\n"
    return txt, img

if __name__ == '__main__':
    makeQualyGraph()