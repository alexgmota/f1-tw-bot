from textwrap import indent
import requests
import json

def getLastCircuitWinners(circuitId):
    limit = 30
    races = []
    res = requests.get(f'https://ergast.com/api/f1/circuits/{circuitId}/results/1.json?limit={limit}')
    response = json.loads(res.text)
    for i in response['MRData']['RaceTable']['Races']:
        races.append((i['season'], i['Results'][0]['Driver']['givenName'] + " " + i['Results'][0]['Driver']['familyName']))
    for offset in range(limit, int(response['MRData']["total"]), limit):
        res = requests.get(f'https://ergast.com/api/f1/circuits/{circuitId}/results/1.json?limit={limit}&offset={offset}')
        response = json.loads(res.text)
        for i in response['MRData']['RaceTable']['Races']:
            races.append((i['season'], i['Results'][0]['Driver']['givenName'] + " " + i['Results'][0]['Driver']['familyName']))

    return races[-5:]

def getNextCircuitId():
    res = requests.get(f'https://ergast.com/api/f1/current/next.json')
    response = json.loads(res.text)
    return response['MRData']['RaceTable']['Races'][0]['Circuit']['circuitId']

if __name__ == '__main__':
    print(getLastCircuitWinners(getNextCircuitId()))