import requests
import json

# http://ergast.com/api/f1/current/constructorStandings

def getDriversStandings():
    res = requests.get(f'http://ergast.com/api/f1/current/driverStandings.json')
    response = json.loads(res.text)
    return response["MRData"]["StandingsTable"]["StandingsLists"][0]["DriverStandings"]

def getConstructorStandings():
    res = requests.get(f'http://ergast.com/api/f1/current/constructorStandings.json')
    response = json.loads(res.text)
    return response["MRData"]["StandingsTable"]["StandingsLists"][0]["ConstructorStandings"]

if __name__ == '__main__':

    print(json.dumps(getConstructorStandings(), indent=2))