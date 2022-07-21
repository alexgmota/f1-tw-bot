from cProfile import label
from email.errors import MessageDefect
from posixpath import split
import requests
import json 
import numpy as np
import matplotlib.pyplot as plt

def compareLapTimes(driverId1, driverId2):
    dr1LapTimes = normalizeLapTime(getDriverLapTimes(driverId1))
    dr2LapTimes = normalizeLapTime(getDriverLapTimes(driverId2))

    plt.title(f'{driverId1} vs {driverId2}')
    plt.plot(np.arange(0, len(dr1LapTimes), 1), dr1LapTimes, label=driverId1)
    plt.plot(np.arange(0, len(dr2LapTimes), 1), dr2LapTimes, label=driverId2)
    plt.legend()

    plt.savefig('./images/my_plot.png')

def normalizeLapTime(arr):
    return list(map(strTomsec, arr))
    
def strTomsec(s):
    min = int(s.split(":")[0])
    sec = int(s.split(":")[1].split(".")[0])
    msec = int(s.split(":")[1].split(".")[1])
    return min * 60 * 1000 + sec *  1000 + msec

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
    compareLapTimes('alonso', 'ocon')
