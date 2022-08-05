from pyparsing import line
import requests
import json 
import numpy as np
import matplotlib.pyplot as plt

from DriverInfo import getDriverColor, getDriverFamilyName

def compareLapTimesNormalized(driverId1, driverId2):
    dr1LapTimes, laps1 = normalizeLapTime(getDriverLapTimes(driverId1))
    dr2LapTimes, laps2 = normalizeLapTime(getDriverLapTimes(driverId2))

    plt.style.use('./templates/mystyle.mplstyle')
    plt.figure(figsize=[10, 5])
    plt.title(f'{getDriverFamilyName(driverId1)} vs {getDriverFamilyName(driverId2)}')
    plt.xlabel('Laps')
    plt.ylabel('Lap Time (sec)')
    
    plt.plot(laps1, dr1LapTimes, label=getDriverFamilyName(driverId1), color=getDriverColor(driverId1))
    plt.plot(laps2, dr2LapTimes, label=getDriverFamilyName(driverId2), linestyle='dashed', color=getDriverColor(driverId2))

    plt.legend()
    plt.savefig('./images/lap_times_normalized.png', dpi=300)
    plt.close()
    print('Lap time figure saved (lap_times_normalized.png)')

def normalizeLapTime(arr):
    lapTimes = list(map(strToSec, arr))
    lapTimesNormalized = []
    laps = []
    avgLapTime = np.average(np.array(lapTimes))
    for i in range(0, len(lapTimes)):
        if lapTimes[i] < avgLapTime * 1.075:
            lapTimesNormalized.append(lapTimes[i])
            laps.append(i)
    return lapTimesNormalized[1:], laps[1:]
    
def strToSec(s):
    mins = int(s.split(":")[0])
    secs = int(s.split(":")[1].split(".")[0])
    msec = int(s.split(":")[1].split(".")[1])
    return mins * 60 + secs + msec / 1000

def getDriverLapTimes(driverId):
    limit = 30
    laps = getLaps(driverId)
    lapTimes = []
    for offset in range(0, laps, limit):
        res = requests.get(f'https://ergast.com/api/f1/current/last/drivers/{driverId}/laps.json?limit={limit}&offset={offset}')
        response = json.loads(res.text)
        lapArray = response['MRData']['RaceTable']['Races'][0]['Laps']
        for i in lapArray:
            lapTimes.append(i['Timings'][0]['time'])
    return lapTimes


def getLaps(driverId):
    res = requests.get('https://ergast.com/api/f1/current/last/drivers/' + driverId + '/laps.json')
    response = json.loads(res.text)
    return int(response["MRData"]["total"])


if __name__ == '__main__':
    compareLapTimesNormalized('alonso', 'ocon')
