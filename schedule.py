import requests
import json 
import datetime
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

def getRaceSchedule():
    res = requests.get(f'https://ergast.com/api/f1/current/next.json')
    response = json.loads(res.text)
    return response["MRData"]["RaceTable"]["Races"][0]

def parseDates(date, time):
    dateArray = date.split("-")
    timeArray = time[0:-1].split(":")
    dateArray = [int(num) for num in dateArray] 
    timeArray = [int(num) for num in timeArray] 
    return datetime.datetime(dateArray[0], dateArray[1], dateArray[2], hour=timeArray[0]+2, minute=timeArray[1], second=timeArray[2])

def getRaceDate(data):
    return parseDates(data['date'], data['time'])
    
def getQualiDate(data):
    qualy = data["Qualifying"]
    return parseDates(qualy['date'], qualy['time'])

def getFP1Date(data):
    fp = data["FirstPractice"]
    return parseDates(fp['date'], fp['time'])

def getFP2Date(data):
    fp = data["SecondPractice"]
    return parseDates(fp['date'], fp['time'])

def getFP3Date(data):
    fp = data["ThirdPractice"]
    return parseDates(fp['date'], fp['time'])

def makeScheduleImg(data):
    img = Image.open('./templates/scheduleTemplate.jpg')
    drawer = ImageDraw.Draw(img)
    fontBold = ImageFont.truetype('./fonts/Roboto_Slab/static/RobotoSlab-Bold.ttf', 72)
    fontMediumBig = ImageFont.truetype('./fonts/Roboto_Slab/static/RobotoSlab-Medium.ttf', 60)
    fontMediumSmall = ImageFont.truetype('./fonts/Roboto_Slab/static/RobotoSlab-Medium.ttf', 38)
    fontSemiBoldBig = ImageFont.truetype('./fonts/Roboto_Slab/static/RobotoSlab-SemiBold.ttf', 55)
    fontSemiBoldSmall = ImageFont.truetype('./fonts/Roboto_Slab/static/RobotoSlab-SemiBold.ttf', 45)

    #Title
    drawer.text((110, 120), data['raceName'], font=fontBold)
    drawer.text((110, 200), data["Circuit"]["circuitName"], font=fontMediumBig)

    # FP
    drawer.text((90, 400), 'Free Practice 1', font=fontSemiBoldSmall)
    drawer.text((90, 468), getFP1Date(data).strftime('%a %d - %H:%M'), font=fontMediumSmall)

    drawer.text((645, 400), 'Free Practice 2', font=fontSemiBoldSmall)
    drawer.text((645, 468), getFP2Date(data).strftime('%a %d - %H:%M'), font=fontMediumSmall)

    drawer.text((90, 605), 'Free Practice 3', font=fontSemiBoldSmall)
    drawer.text((90, 675), getFP3Date(data).strftime('%a %d - %H:%M'), font=fontMediumSmall)

    # Qualy
    drawer.text((645, 605), 'Qualifying', font=fontSemiBoldSmall)
    drawer.text((645, 675), getQualiDate(data).strftime('%a %d - %H:%M'), font=fontMediumSmall)

    # Race
    drawer.text((470, 780), 'Race', font=fontSemiBoldBig)
    drawer.text((420, 860), getRaceDate(data).strftime('%a %d - %H:%M'), font=fontMediumSmall)

    img.save('./images/schedule.png')
    print("Schedule image saved (schedule.png)")

def makeScheduleTweet():
    data = getRaceSchedule()
    makeScheduleImg(data)
    return f"🚨 {data['raceName']} Schedule 🚨\n*Hora española 🇪🇦", './images/schedule.png'



if __name__ == '__main__':
    makeScheduleTweet()