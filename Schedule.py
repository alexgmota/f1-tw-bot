import requests
import datetime
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


class Schedule:

    path = "./images/Schedule.png"
    templatePath = "./templates/scheduleTemplate.jpg"
    xCenter = 540
    firstColumn = 90
    secondColumn = 645
    firstRow = 400
    secondRow = 603
    dateFormat = "%a %d - %H:%M"
    off = 68

    def __init__(self) -> None:
        self.data = self.getRaceSchedule()

    def getRaceSchedule(self):
        response = requests.get(f"https://ergast.com/api/f1/current/next.json").json()
        return response["MRData"]["RaceTable"]["Races"][0]

    def getLastRaceSchedule(self):
        res = requests.get(f'https://ergast.com/api/f1/current/last.json').json()
        self.data =  res["MRData"]["RaceTable"]["Races"][0]
        return self

    def parseDates(self, date, time):
        dateArray = date.split("-")
        timeArray = time[0:-1].split(":")
        dateArray = [int(num) for num in dateArray]
        timeArray = [int(num) for num in timeArray]
        return datetime.datetime(
            dateArray[0],
            dateArray[1],
            dateArray[2],
            hour=timeArray[0] + 2, # Spanish Time Zone is +
            minute=timeArray[1],
            second=timeArray[2],
        )

    def getRaceDate(self):
        return self.parseDates(self.data["date"], self.data["time"])

    def getQualiDate(self):
        qualy = self.data["Qualifying"]
        return self.parseDates(qualy["date"], qualy["time"])

    def getFP1Date(self):
        fp = self.data["FirstPractice"]
        return self.parseDates(fp["date"], fp["time"])

    def getFP2Date(self):
        fp = self.data["SecondPractice"]
        return self.parseDates(fp["date"], fp["time"])

    def getFP3Date(self):
        fp = self.data["ThirdPractice"]
        return self.parseDates(fp["date"], fp["time"])

    def makeScheduleImg(self):
        img = Image.open(self.templatePath)
        self.drawer = ImageDraw.Draw(img)

        self.drawTitle()
        self.drawFreePractice()
        self.drawQualy()
        self.drawRace()

        img.save(self.path)
        print("Schedule image saved (schedule.png)")

    def drawTitle(self):
        fontBold = ImageFont.truetype("./fonts/Roboto_Slab/static/RobotoSlab-Bold.ttf", 72)
        fontMediumBig = ImageFont.truetype("./fonts/Roboto_Slab/static/RobotoSlab-Medium.ttf", 60)

        self.drawer.text((self.xCenter, 170), self.data["raceName"], font=fontBold, anchor="mm")
        self.drawer.text(
            (self.xCenter, 250),
            self.data["Circuit"]["circuitName"],
            font=fontMediumBig,
            anchor="mm",
        )

    def drawFreePractice(self):
        fontSmall = ImageFont.truetype("./fonts/Roboto_Slab/static/RobotoSlab-Medium.ttf", 38)
        fontBoldSmall = ImageFont.truetype("./fonts/Roboto_Slab/static/RobotoSlab-SemiBold.ttf", 45)

        self.drawer.text((self.firstColumn, self.firstRow), "Free Practice 1", font=fontBoldSmall)
        self.drawer.text(
            (self.firstColumn, self.firstRow + self.off),
            self.getFP1Date().strftime(self.dateFormat),
            font=fontSmall,
        )

        self.drawer.text((self.secondColumn, self.firstRow), "Free Practice 2", font=fontBoldSmall)
        self.drawer.text(
            (self.secondColumn, self.firstRow + self.off),
            self.getFP2Date().strftime(self.dateFormat),
            font=fontSmall,
        )

        self.drawer.text((self.firstColumn, self.secondRow), "Free Practice 3", font=fontBoldSmall)
        self.drawer.text(
            (self.firstColumn, self.secondRow + self.off),
            self.getFP3Date().strftime(self.dateFormat),
            font=fontSmall,
        )

    def drawQualy(self):
        fontBoldSmall = ImageFont.truetype("./fonts/Roboto_Slab/static/RobotoSlab-SemiBold.ttf", 45)
        fontSmall = ImageFont.truetype("./fonts/Roboto_Slab/static/RobotoSlab-Medium.ttf", 38)

        self.drawer.text((self.secondColumn, self.secondRow), "Qualifying", font=fontBoldSmall)
        self.drawer.text(
            (self.secondColumn, self.secondRow + self.off),
            self.getQualiDate().strftime(self.dateFormat),
            font=fontSmall,
        )

    def drawRace(self):
        fontBig = ImageFont.truetype("./fonts/Roboto_Slab/static/RobotoSlab-SemiBold.ttf", 55)
        fontSmall = ImageFont.truetype("./fonts/Roboto_Slab/static/RobotoSlab-Medium.ttf", 38)

        self.drawer.text((self.xCenter, 820), "Race", font=fontBig, anchor="mm")
        self.drawer.text(
            (self.xCenter, 890),
            self.getRaceDate().strftime(self.dateFormat),
            font=fontSmall,
            anchor="mm",
        )

    def makeScheduleTweet(self):
        self.makeScheduleImg()
        return f"🚨 {self.data['raceName']} Schedule 🚨\n\n *Hora española 🇪🇦", self.path


if __name__ == "__main__":
    Schedule().makeScheduleTweet()
