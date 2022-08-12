import sys
import requests
import json 
from ChampStandings import getConstructorStandings, getDriversStandings, makeConstStandImg, makeDriverStandImg
from CircuitLastWinners import makeLastWinnersMsg
from QualyComparator import makeQualyComparationMsg
from QualyResults import makeQualyResultsMsg

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

def tweetQualyComparator():
    postTextTweet(makeQualyComparationMsg() + "\n\n [Test]")

def tweetQualyResults():
    txt, img = makeQualyResultsMsg()
    postImageTweet(txt + "\n\n [Test]", [img])

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print(
            '\t Options:\n\n' +
            '\t\t 1. Tweet schedule\n' +
            '\t\t 2. Tweet standings\n' +
            '\t\t 3. Tweet Last Winner\n' +
            '\t\t 4. Tweet Qualy Mates Comparation\n' +
            '\t\t 5. Tweet Qualy Results Graph\n'
        )
        opc = input('\t Select an option: ')
        actions(opc)
