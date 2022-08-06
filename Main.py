import sys
import requests
import json 
from ChampStandings import getConstructorStandings, getDriversStandings, makeConstStandImg, makeDriverStandImg

from Schedule import makeScheduleTweet
from twitterManager import postImageTweet

def actions(opc):
    match opc:
        case '1': 
            tweetSchedule()
        case '2': 
            tweetStandings()
        case _: 
            print('\tIntroduce una opcion valida')

def tweetSchedule():
    txt, img = makeScheduleTweet()
    postImageTweet(txt + "\n\n [Test]", [img])

def tweetStandings():
    img = [
        makeDriverStandImg(getDriversStandings()),
        makeConstStandImg(getConstructorStandings())
        ]
    txt = f'🏆 Standings after {getLastRaceName()} 🏆'
    postImageTweet(txt + "\n\n [Test]", img)
    

def getLastRaceName():
    res = requests.get(f'https://ergast.com/api/f1/current/last.json')
    response = json.loads(res.text)
    return response['MRData']['RaceTable']['Races'][0]['raceName']


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print(
            '\t Options:\n\n' +
            '\t\t 1. Tweet schedule\n' +
            '\t\t 2. Tweet standings\n' +
            '\t\t 3. Tweet \n'
        )
        opc = input('\t Select an option: ')
        actions(opc)
