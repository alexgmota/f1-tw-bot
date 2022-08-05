import requests
import json

from DriverInfo import getDriverCode

def getQualyPositions(driverId):
    res = requests.get(f'https://ergast.com/api/f1/current/drivers/{driverId}/qualifying.json')
    response = json.loads(res.text)
    races = response["MRData"]["RaceTable"]["Races"]
    qualyPositions = []
    for race in races:
        qualyPositions.append(int(race["QualifyingResults"][0]["position"]))
    return qualyPositions

def compareQualiPositions(driverId1, driverId2):
    results1 = getQualyPositions(driverId1)
    results2 = getQualyPositions(driverId2)
    count1 = count2 = 0
    for i in range(0, len(results1)):
        if results1[i] > results2[i]:
            count2 += 1
        else:
            count1 += 1
    
    return ((getDriverCode(driverId1), count1), (getDriverCode(driverId2), count2))

def makeQualyComparationMsg():
    res = "Comparación de compañeros en clasificación: \n\n"
    for i in getTeamMates():
        aux = compareQualiPositions(i[0], i[1])
        res += f"\t{aux[0][0]} {aux[0][1]} - {aux[1][1]} {aux[1][0]}\n"
    print(res)
    return res

def getTeamMates():
    return [
        ('leclerc', 'sainz'),
        ('max_verstappen', 'perez'),
        ('hamilton', 'russell'),
        ('alonso', 'ocon'),
        ('norris', 'ricciardo'),
        ('bottas', 'zhou'),
        ('gasly', 'tsunoda'),
        ('mick_schumacher', 'kevin_magnussen'),
        ('vettel', 'stroll'),
        ('albon', 'latifi')
    ]

if __name__ == '__main__':
    makeQualyComparationMsg()
    