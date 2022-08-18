import re
import requests
import json

from DriverInfo import getDriverCode, getDrivers, getTeamMates


def getRacePositions():
    races = getPastRaces()
    results = {}
    for race in races:
        res = requests.get(
            f"https://ergast.com/api/f1/current/circuits/{race}/results.json"
        )
        response = json.loads(res.text)
        current = {}
        for pos in response["MRData"]["RaceTable"]["Races"][0]["Results"]:
            current[pos["Driver"]["driverId"]] = getPosition(pos)
        results[race] = current
    return results


def getPosition(pos):
    if pos["status"] in ["Finished", "Front wing"] or pos["status"][0] == "+":
        return int(pos["position"])
    return 21


def getPastRaces():
    res = requests.get(f"https://ergast.com/api/f1/current/results/1/races.json")
    response = json.loads(res.text)
    races = []
    for race in response["MRData"]["RaceTable"]["Races"]:
        races.append(race["Circuit"]["circuitId"])
    return races


def compareRacePositions():
    results = getRacePositions()
    battle = {}
    [battle.setdefault(i, 0) for i in getDrivers()]
    for race in results:
        for mates in getTeamMates():
            if validComparison(mates, results, race):
                battle[compareDrivers(mates, results[race])] += 1
    return battle


def validComparison(mates, results, race):
    return (
        mates[0] in results[race].keys()
        and mates[1] in results[race].keys()
        and (results[race][mates[0]] != 21 or results[race][mates[1]] != 21)
    )


def compareDrivers(mates, race):
    if race[mates[0]] < race[mates[1]]:
        return mates[0]
    return mates[1]


def makeRaceComparationMsg():
    txt = "🏎️ Race Results Teammates Comparison: 🏎️\n\n"
    res = compareRacePositions()
    for i in getTeamMates():
        txt += f"   {getDriverCode(i[0])}  {res[i[0]]:2d}  - {res[i[1]]:2d}  {getDriverCode(i[1])}\n"
    print(txt)
    return txt


if __name__ == "__main__":
    makeRaceComparationMsg()
