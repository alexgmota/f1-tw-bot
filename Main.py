import sys
import requests
import json 
from ChampStandings import getConstructorStandings, getDriversStandings, makeConstStandImg, makeDriverStandImg
from CircuitLastPoles import makeLastPolesMsg
from CircuitLastWinners import makeLastWinnersMsg
from QualyComparator import makeQualyComparationMsg
from QualyResults import makeQualyResultsMsg
from RacePace import makeRaceGraph

from Schedule import makeScheduleTweet
from twitterManager import postImageTweet, postTextTweet

def actions(opc):
    match opc:
        case '1': 
            tweetSchedule()
        case '2': 
            tweetStandings()
        case '3':
            tweetLastWinners()
        case '4':
            tweetQualyComparator()
        case '5':
            tweetQualyResults()
        case '6':
            tweetRacePace()
        case '7': 
            tweetLastPoles()
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

def tweetLastWinners():
    postTextTweet(makeLastWinnersMsg() + "\n\n [Test]")

def tweetLastPoles():
    postTextTweet(makeLastPolesMsg() + "\n\n [Test]")

def tweetQualyComparator():
    postTextTweet(makeQualyComparationMsg() + "\n\n [Test]")

def tweetQualyResults():
    txt, img = makeQualyResultsMsg()
    postImageTweet(txt + "\n\n [Test]", [img])

def tweetRacePace():
    img = makeRaceGraph()
    txt = f'🏆 Top 5 Race pace 🏆\n\n{getLastRaceName()}'
    postImageTweet(txt + "\n\n [Test]", [img])

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print(
            '\t Options:\n\n' +
            '\t\t 1. Tweet schedule\n' +
            '\t\t 2. Tweet standings\n' +
            '\t\t 3. Tweet Last Winner\n' +
            '\t\t 4. Tweet Qualy Mates Comparation\n' +
            '\t\t 5. Tweet Qualy Results Graph\n' + 
            '\t\t 6. Tweet Race Pace Graph\n' +
            '\t\t 7. Tweet Last Pole sitters\n'
        )
        opc = input('\t Select an option: ')
        actions(opc)
