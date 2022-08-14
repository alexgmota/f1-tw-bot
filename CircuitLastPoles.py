import requests
import json

from CircuitLastWinners import getNextCircuit

def getLastCircuitPoles(circuitId):
    limit = 30
    races = []
    url = f'https://ergast.com/api/f1/circuits/{circuitId}/qualifying/1.json?limit={limit}'
    res = requests.get(url)
    response = json.loads(res.text)
    for i in response['MRData']['RaceTable']['Races']:
        races.append((i['season'], i['QualifyingResults'][0]['Driver']['givenName'] + " " + i['QualifyingResults'][0]['Driver']['familyName']))
    for offset in range(limit, int(response['MRData']["total"]), limit):
        res = requests.get(url + f'&offset={offset}')
        response = json.loads(res.text)
        for i in response['MRData']['RaceTable']['Races']:
            races.append((i['season'], i['QualifyingResults'][0]['Driver']['givenName'] + " " + i['QualifyingResults'][0]['Driver']['familyName']))

    return races[-5:]


def makeLastPolesMsg():
    circuit = getNextCircuit()
    res = f"🥇 Last {circuit['circuitName']} Pole sitters: 🥇\n\n"
    lastPoles = getLastCircuitPoles(circuit['circuitId'])
    for i in lastPoles[::-1]:
        res += f"    {i[0]} - {i[1]}\n"
    print(res)
    return res

if __name__ == '__main__':
    makeLastPolesMsg()