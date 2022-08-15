from difflib import restore
from lib2to3.pgen2.driver import Driver
from unittest import result
import requests
import json

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


def getRaceResults():
    res = requests.get(f"https://ergast.com/api/f1/current/last/results.json")
    response = json.loads(res.text)
    results = response["MRData"]["RaceTable"]["Races"][0]["Results"]
    positions = []
    for driver in results:
        positions.append(
            (
                driver["position"],
                driver["Driver"]["givenName"][0]
                + ". "
                + driver["Driver"]["familyName"]
            )
        )
    return positions, response["MRData"]["RaceTable"]['Races'][0]['raceName']

def makeRaceResultsImg(results, raceName):
    img = Image.open('./templates/raceResults.jpg')
    drawer = ImageDraw.Draw(img)
    fontNames = ImageFont.truetype('./fonts/Roboto_Slab/static/RobotoSlab-Medium.ttf', 58)
    drawer.text((819, 180), raceName, font=ImageFont.truetype('./fonts/Roboto_Slab/static/RobotoSlab-Bold.ttf', 84), anchor="mm")
    offset = 0; x = 310
    for i in results:
        drawer.text((x, 365 + offset), i[1], font=fontNames)
        offset += 171
        if i[0] == "10":
            offset = 0
            x += 695
    path = './images/RaceResults.png'
    img.save(path)
    img.close()
    print('Race result image saved (RaceResults.png)')
    return path

def makeRaceResultsMsg():
    results, raceName = getRaceResults()
    img = [makeRaceResultsImg(results, raceName)]
    txt = f'🏆 {raceName} Results 🏆\n'
    return txt, img

if __name__ == "__main__":
    results, raceName = getRaceResults()
    makeRaceResultsImg(results, raceName)
