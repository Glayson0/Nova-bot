"""
Esse arquivo contém todas as funções relacionadas aos ônibus da Unicamp.
"""
from timeUtils import *
from busSchedule import *

def getDayBusSchedule(weekday:str=CURRENT_WEEKDAY) -> tuple:
    """Retorna uma tupla com as listas de ida e volta dos ônibus dependendo do dia atual."""
    dayType = getDayType(weekday)
    if weekday == 'Domingo':
        return dayTypes[dayType][0][:25], dayTypes[dayType][1][:25]
    else:
        return dayTypes[dayType][0], dayTypes[dayType][1]

def hasAvailableBus(time:datetime, busSchedule:list) -> bool:
    """Checa se há ônibus disponível no dia após o horário em que a função foi chamada."""
    if time < busSchedule[-1]:
        return True
    return False

def nextBusFromNow(busSchedule:list, time:datetime=CURRENT_DATETIME) -> datetime:
    """Retorna o horário em datetime do próximo ônibus a partir do horário em que a função foi chamada."""
    for busTime in busSchedule:
        if time <= busTime:
            return busTime

def getAvailableBusSchedule(busSchedule:list, time:datetime=CURRENT_DATETIME) -> list:
    """Retorna uma lista com apenas os ônibus disponíveis no dia a partir do horário em que a função foi chamada."""
    availableBusSchedule = []

    for busTime in busSchedule:
        if time >= busTime:
            availableBusSchedule.append(busTime)

    return availableBusSchedule