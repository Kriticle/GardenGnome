# import the module
import python_weather
import asyncio
import csv


def getDict(crop):
    seedListFile = open('D:\GitHub Things\kritisHackHub2022\hackhub2022\static\seedList.csv', newline='')
    seedList = csv.DictReader(seedListFile)
    for row in seedList:
        if row["seedName"] == crop:
            return (row)


async def getweather():
    # declare the client. format defaults to metric system (celcius, km/h, etc.)
    client = python_weather.Client()

    # fetch a weather forecast from a city
    weather = await client.find("Ghaziabad")

    # returns the current day's forecast
    global curTemp, curHumid, curSky
    # print("Current Temperature:",weather.forecasts[0].temperature,"|| Current Humidity:",weather.current.humidity, "|| Sky status:",weather.forecasts[0].sky_text)
    curTemp = weather.forecasts[0].temperature
    curHumid = weather.current.humidity
    curSky = weather.forecasts[0].sky_text

    # close the wrapper once done
    await client.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(getweather())
    #cropDict = getDict(crop)


def tempCompare(crop, city):
    global seedList, curTemp
    curTemp = asyncio.run(getCurTemp(city))
    row = getDict(crop)
    if int(row["tempHigh"]) >= curTemp >= int(row["tempLow"]):
        return "Ideal temperature"
    elif curTemp > int(row["tempHigh"]):
        return "Temperature higher than ideal. Use air conditioning"
    else:
        return "Temperature lower than ideal. Use heating"


def humiCompare(crop, city):
    global seedList, curHumid
    curHumid = asyncio.run(getCurHum(city))
    row = getDict(crop)
    if int(row["humHigh"]) >= curHumid >= int(row["humLow"]):
        return "Ideal humidity"
    elif curTemp > int(row["humHigh"]):
        return "Humidity higher than ideal. Use dehumidifier"
    else:
        return "Humidity lower than ideal. Use humidifier"


def skytextCompare(crop, city):
    global curSky
    curSky = asyncio.run(getCurSky(city))
    skyTextGradient = {"Clear": 0, "Mostly Sunny": 1, "Partly Cloudy": 2, "Mostly Cloudy": 3, "Cloudy": 4}
    row = getDict(crop)
    ideal_sunlight = row["seedSunlight"]
    curSky_int = skyTextGradient[curSky]
    conditionDict = {"high": [0, 1],
                     "moderate": [2, 3],
                     "low": [4, ]}
    ideal_cursky = conditionDict[ideal_sunlight]
    if curSky_int in ideal_cursky:
        return "The sunlight is ideal you are good to go"

    elif curSky_int > max(ideal_cursky):
        return "Not sunny enough. Consider moving to sunlight"


    else:
        print("Too sunny. Consider moving to shade")


async def getCurHum(city):
    client = python_weather.Client()
    weather = await client.find(city)
    curHumid = weather.current.humidity
    return curHumid
    await client.close()


async def getCurTemp(city):
    client = python_weather.Client()
    weather = await client.find(city)
    curTemp = weather.forecasts[0].temperature
    return curTemp
    await client.close()


async def getCurSky(city):
    client = python_weather.Client()
    weather = await client.find(city)
    curSky = weather.forecasts[0].sky_text
    return curSky
    await client.close()


def idealTempRange(crop):
    return str(getDict(crop)["tempLow"]) + 'C-' + str(getDict(crop)["tempHigh"]) + 'C'


def idealHumRange(crop):
    return str(getDict(crop)["humLow"]) + "%-" + str(getDict(crop)["humHigh"]) + "%"


def idealSky(crop):
    return str(getDict(crop)["seedSunlight"])

# dict key format: {seedName,tempLow,tempHigh,humLow,humHigh,seedSunlight}
skytextCompare("Guava","Ghaziabad")