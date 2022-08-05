import json

def getData():
    with open('utils.json') as file:
        return json.load(file)

def getDriversCode(arr):
    data = getData()
    res = []
    for driver in arr:
        res.append(data[driver]['code'])
    return res

def getDriverCode(driverId):
    data = getData()
    return data[driverId]['code']

def getDriversTeamColor(arr):
    data = getData()
    res = []
    for driver in arr:
        res.append(data[driver]['teamColor'])
    return res

def getDriverColor(driverId):
    data = getData()
    return data[driverId]['color']

def getDriverFamilyName(driverId):
    data = getData()
    return data[driverId]['familyName']