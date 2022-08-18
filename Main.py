import sys
import requests
import json
from ChampStandings import (
    getConstructorStandings,
    getDriversStandings,
    makeConstStandImg,
    makeDriverStandImg,
)
from CircuitLastPoles import makeLastPolesMsg
from CircuitLastWinners import makeLastWinnersMsg
from QualyComparator import makeQualyComparationMsg
from QualyResults import makeQualyResultsMsg
from RaceComparator import makeRaceComparationMsg
from RacePace import makeRaceGraph
from RaceResults import makeRaceResultsMsg

from Schedule import makeScheduleTweet
from twitterManager import postImageTweet, postTextTweet


def actions(opc):
    sw = {
        "1": tweetSchedule,
        "2": tweetStandings,
        "3": tweetLastWinners,
        "4": tweetQualyComparator,
        "5": tweetQualyResults,
        "6": tweetRacePace,
        "7": tweetLastPoles,
        "8": tweetRaceResults,
        "9": tweetRaceComparator,
    }
    action = sw.get(opc)
    try:
        action()
    except:
        print("\tIntroduce una opción valida")


def tweetSchedule():
    txt, img = makeScheduleTweet()
    postImageTweet(txt + "\n\n [Test]", [img])


def tweetStandings():
    img = [
        makeDriverStandImg(getDriversStandings()),
        makeConstStandImg(getConstructorStandings()),
    ]
    txt = f"🏆 Standings after {getLastRaceName()} 🏆"
    postImageTweet(txt + "\n\n [Test]", img)


def getLastRaceName():
    res = requests.get(f"https://ergast.com/api/f1/current/last.json")
    response = json.loads(res.text)
    return response["MRData"]["RaceTable"]["Races"][0]["raceName"]


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
    txt = f"🏆 Top 5 Race pace 🏆\n\n{getLastRaceName()}"
    postImageTweet(txt + "\n\n [Test]", [img])


def tweetRaceResults():
    txt, img = makeRaceResultsMsg()
    postImageTweet(txt + "\n\n [Test]", img)


def tweetRaceComparator():
    postTextTweet(makeRaceComparationMsg())


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(
            "\t Options:\n\n"
            + "\t\t 1. Tweet schedule\n"
            + "\t\t 2. Tweet standings\n"
            + "\t\t 3. Tweet Last Winners\n"
            + "\t\t 4. Tweet Qualy Mates Comparation\n"
            + "\t\t 5. Tweet Qualy Results Graph\n"
            + "\t\t 6. Tweet Race Pace Graph\n"
            + "\t\t 7. Tweet Last Pole sitters\n"
            + "\t\t 8. Tweet Race Results\n"
            + "\t\t 9. Tweet Race Comparator\n"
        )
        opc = input("\t Select an option: ")
        actions(opc)
