import requests
import json

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
    
    return ((driverId1, count1), (driverId2, count2))

if __name__ == '__main__':
    print(compareQualiPositions('leclerc', 'sainz'))
    print(compareQualiPositions('max_verstappen', 'perez'))
    print(compareQualiPositions('hamilton', 'russell'))
    print(compareQualiPositions('alonso', 'ocon'))
    print(compareQualiPositions('norris', 'ricciardo'))
    print(compareQualiPositions('gasly', 'tsunoda'))
    print(compareQualiPositions('albon', 'latifi'))
    print(compareQualiPositions('mick_schumacher', 'kevin_magnussen'))
    print(compareQualiPositions('vettel', 'stroll'))
    print(compareQualiPositions('bottas', 'zhou'))
    