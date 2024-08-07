"""
Esse arquivo contém todas as funções relacionadas aos ônibus da Unicamp.
"""
from timeUtils import *
from busSchedule import *

# Funções auxiliares

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
    if hasAvailableBus(CURRENT_DATETIME, busSchedule):
        for busTime in busSchedule:
            if time <= busTime:
                return busTime
    return None

def getAvailableBusSchedule(busSchedule:list, time:datetime=CURRENT_DATETIME) -> list:
    """Retorna uma lista com apenas os ônibus disponíveis no dia a partir do horário em que a função foi chamada."""
    availableBusSchedule = []

    for busTime in busSchedule:
        if time >= busTime:
            availableBusSchedule.append(busTime)

    return availableBusSchedule

# Funções principais

def createNextBusMessage() -> str:
    """Cria uma string com os horários dos conjuntos ida-volta dos ônibus da moradia."""
    departureBusSchedule, returnBusSchedule = getDayBusSchedule(CURRENT_WEEKDAY)

    # Obtenção dos próximo 2 horários dos ônibus
    nextDepartureBusTime1 = nextBusFromNow(departureBusSchedule)
    nextDepartureBusTime2 = nextBusFromNow(departureBusSchedule, nextDepartureBusTime1)
    nextReturnBusTime1 = nextBusFromNow(returnBusSchedule)
    nextReturnBusTime2 = nextBusFromNow(returnBusSchedule, nextReturnBusTime1)

    # Tempo restante para os horários - IDA
    if nextReturnBusTime1:
        timeForNextDepartureBus1 = calculateTimeDifference(nextDepartureBusTime1, CURRENT_DATETIME)
        if nextReturnBusTime2:
            timeForNextDepartureBus2 = calculateTimeDifference(nextDepartureBusTime2, CURRENT_DATETIME)
        else:
            timeForNextDepartureBus2 = None
    else:
        timeForNextDepartureBus1 = None
        timeForNextDepartureBus2 = None

    # Tempo restante para os horários - VOLTA
    if nextReturnBusTime1:
        timeForNextReturnBus1 = calculateTimeDifference(nextReturnBusTime1, CURRENT_DATETIME)
        if nextReturnBusTime2:
            timeForNextReturnBus2 = calculateTimeDifference(nextReturnBusTime1, CURRENT_DATETIME)
        else:
            timeForNextReturnBus2 = None
    else:
        timeForNextReturnBus1 = None
        timeForNextReturnBus2 = None

    # Substituir horários com valor None por "Acabaram os ônibus por hoje!"
    times = [
        [datetimeToStr(nextDepartureBusTime1), timeForNextDepartureBus1], 
        [datetimeToStr(nextDepartureBusTime2), timeForNextDepartureBus2], 
        [datetimeToStr(nextReturnBusTime1), timeForNextReturnBus1], 
        [datetimeToStr(nextReturnBusTime2), timeForNextReturnBus2]
    ]

    timesOutput = []
    for time in times:
        if time[0] == None:
            time = "Acabaram os ônibus por hoje\!"
        else:
            time = f"{time[0]} \({time[1]}\)"
        timesOutput.append(time)

    print(timesOutput)

    # String formatada
    next2busText = f"""
Ida \(Moradia \-\> Unicamp\):
01\) {timesOutput[0]}
02\) {timesOutput[1]}

Volta \(Unicamp \-\> Moradia\):
01\) {timesOutput[2]}
02\) {timesOutput[3]}
"""
    return next2busText

def createAvailableBusListMessage(busSchedule:list) -> str:
    """Cria uma string com todos os horários do dia de ônibus, riscando os horários que já passaram e destacando o próximo."""

    nextBus = nextBusFromNow(busSchedule)
    availableBusScheduleListText = ""

    pos = 0
    for time in busSchedule:

        # Ônibus que já passaram
        if time < nextBus: 
            time = datetimeToStr(time)
            pos += 1
            if pos % 3 == 0:
                availableBusScheduleListText += f'~{time}~\n'
            else:
                availableBusScheduleListText += f'~{time}~  \|  '
        
        # Próximo ônibus
        elif time == nextBus:
            pos += 1
            if pos % 3 == 0:
                availableBusScheduleListText += f'*{datetimeToStr(nextBus)}*\n'
            else:
                availableBusScheduleListText += f'*{datetimeToStr(nextBus)}*  \|  '
        
        # Ônibus que ainda não passaram
        else:
            time = datetimeToStr(time)
            pos += 1
            if pos % 3 == 0:
                availableBusScheduleListText += f'{time}\n'
            else:
                availableBusScheduleListText += f'{time}  \|  '

    return availableBusScheduleListText