"""
Esse arquivo contém todas as funções relacionadas aos ônibus da Unicamp.
"""
from timeUtils import *
from busSchedule import *

def getDayBusSchedule(weekday:str=CURRENT_WEEKDAY):
    dayType = getDayType(weekday)
    if weekday == 'Domingo':
        return dayTypes[dayType][0][:25], dayTypes[dayType][1][:25]
    else:
        return dayTypes[dayType][0], dayTypes[dayType][1]

def hasAvailableBus(time:datetime.time, busSchedule:list):
    if time < busSchedule[-1]:
        return True
    return False

def nextBusFromTime(busSchedule:list, time:datetime=CURRENT_TIME):
    time = time.time()
    for busTime in busSchedule:
        if time <= strToDatetime(busTime):
            return busTime

def getAvailableBusSchedule(busSchedule:list, time:datetime.time=CURRENT_TIME):
    time = time.time()
    availableBusSchedule = []

    for busTime in busSchedule:
        if time >= strToDatetime(busTime):
            availableBusSchedule.append(busTime)

    return availableBusSchedule