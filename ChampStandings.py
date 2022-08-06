import requests
import json
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


def getDriversStandings():
    res = requests.get(f'http://ergast.com/api/f1/current/driverStandings.json')
    response = json.loads(res.text)
    standings = []
    for i in response["MRData"]["StandingsTable"]["StandingsLists"][0]["DriverStandings"]:
        standings.append((i['position'], i['points'], i['Driver']['givenName'][0] + ". " + i['Driver']['familyName']))
    return standings



def getConstructorStandings():
    res = requests.get(f'http://ergast.com/api/f1/current/constructorStandings.json')
    response = json.loads(res.text)
    standings = []
    for i in response["MRData"]["StandingsTable"]["StandingsLists"][0]["ConstructorStandings"]:
        standings.append((i['position'], i['points'], i['Constructor']['name']))
    return standings


def makeConstStandImg(standings):
    img = Image.open('./templates/constructorsStandings.jpg')
    drawer = ImageDraw.Draw(img)
    fontNames = ImageFont.truetype('./fonts/Roboto_Slab/static/RobotoSlab-Medium.ttf', 72)
    fontPoints = ImageFont.truetype('./fonts/Roboto_Slab/static/RobotoSlab-Regular.ttf', 72)
    offset = 0
    for i in standings:
        drawer.text((380, 353 + offset), i[2], font=fontNames)
        drawer.text((1260, 353 + offset), "{:3d}".format(int(i[1])), font=fontPoints)
        offset += 171
    path = './images/ConstructorStandings.png'
    img.save(path)
    img.close()
    print('Constructor Standings image saved (ConstructorStandings.png)')
    return path

def makeDriverStandImg(standings):
    img = Image.open('./templates/driverStandings.jpg')
    drawer = ImageDraw.Draw(img)
    fontNames = ImageFont.truetype('./fonts/Roboto_Slab/static/RobotoSlab-Medium.ttf', 48)
    fontPoints = ImageFont.truetype('./fonts/Roboto_Slab/static/RobotoSlab-Regular.ttf', 48)
    offset = 0; x = 305
    for i in standings[:20]:
        drawer.text((x, 375 + offset), i[2], font=fontNames)
        drawer.text((x + 378, 375 + offset), "{:3d}".format(int(i[1])), font=fontPoints)
        offset += 171
        if i[0] == "10":
            offset = 0
            x = 1000
    path = './images/DriverStandings.png'
    img.save(path)
    img.close()
    print('Drivers Standings image saved (DriverStandings.png)')
    return path



if __name__ == '__main__':
    makeConstStandImg(getConstructorStandings())
    makeDriverStandImg(getDriversStandings())
