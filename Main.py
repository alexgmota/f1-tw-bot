from datetime import datetime
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

from Schedule import Schedule
from TelemetryAnalizer import makeTelemetryMsg
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
        "10": tweetTelemetryComparison,
    }
    action = sw.get(opc)
    try:
        action()
    except Exception as e:
        print("\tSe ha producido un error")
        print(e)


def tweetSchedule():
    txt, img = Schedule().makeScheduleTweet()
    postImageTweet(txt, [img])


def tweetStandings():
    img = [
        makeDriverStandImg(getDriversStandings()),
        makeConstStandImg(getConstructorStandings()),
    ]
    txt = f"🏆 Standings after {getLastRaceName()} 🏆"
    postImageTweet(txt, img)


def getLastRaceName():
    res = requests.get(f"https://ergast.com/api/f1/current/last.json")
    response = json.loads(res.text)
    return response["MRData"]["RaceTable"]["Races"][0]["raceName"]


def tweetLastWinners():
    postTextTweet(makeLastWinnersMsg())


def tweetLastPoles():
    postTextTweet(makeLastPolesMsg())


def tweetQualyComparator():
    postTextTweet(makeQualyComparationMsg())


def tweetQualyResults():
    txt, img = makeQualyResultsMsg()
    postImageTweet(txt, [img])


def tweetRacePace():
    img = makeRaceGraph()
    txt = f"🏆 Top 5 Race pace 🏆\n\n{getLastRaceName()}"
    postImageTweet(txt, [img])


def tweetRaceResults():
    txt, img = makeRaceResultsMsg()
    postImageTweet(txt, img)


def tweetRaceComparator():
    postTextTweet(makeRaceComparationMsg())


def tweetTelemetryComparison():
    txt, img = makeTelemetryMsg()
    postImageTweet(txt, img)


def isRaceWeek():
    raceDate = Schedule().getRaceDate()
    now = datetime.now()
    return (
        raceDate.strftime("%d %m") == now.strftime("%d %m") 
        or raceDate.strftime("%W") == now.strftime("%W")
    )


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(
            "\t Options:\n\n"
            + "\t\t  1. Tweet schedule\n"
            + "\t\t  2. Tweet standings\n"
            + "\t\t  3. Tweet Last Winners\n"
            + "\t\t  4. Tweet Qualy Mates Comparation\n"
            + "\t\t  5. Tweet Qualy Results Graph\n"
            + "\t\t  6. Tweet Race Pace Graph\n"
            + "\t\t  7. Tweet Last Pole sitters\n"
            + "\t\t  8. Tweet Race Results\n"
            + "\t\t  9. Tweet Race Comparator\n"
            + "\t\t 10. Tweet Telemetry Comparison\n"
        )
        opc = input("\t Select an option: ")
        actions(opc)
    else:
        if isRaceWeek():
            for i in sys.argv[1:]:
                actions(i)
