"""
Esse arquivo contém todas as funções relacionadas aos ônibus da Unicamp.
"""
from busSchedule import *
from time_utils import *

# Funções auxiliares

def getDayBusSchedule(weekday:str=CURRENT_WEEKDAY) -> tuple:
    """Retorna uma tupla com as listas de ida e volta dos ônibus dependendo do dia atual."""
    day_type = is_business_day(weekday)
    day_type = "business day" if day_type else "weekend"

    if weekday == 'domingo':
        return dayTypes[day_type][0][:25], dayTypes[day_type][1][:25]

    return dayTypes[day_type][0], dayTypes[day_type][1]

def hasAvailableBus(time:datetime, busSchedule:list) -> bool:
    """Checa se há ônibus disponível no dia após o horário em que a função foi chamada."""
    return time < busSchedule[-1]

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
        timeForNextDepartureBus1 = calc_time_diff(nextDepartureBusTime1, CURRENT_DATETIME)
        if nextReturnBusTime2:
            timeForNextDepartureBus2 = calc_time_diff(nextDepartureBusTime2, CURRENT_DATETIME)
        else:
            timeForNextDepartureBus2 = None
    else:
        timeForNextDepartureBus1 = None
        timeForNextDepartureBus2 = None

    # Tempo restante para os horários - VOLTA
    if nextReturnBusTime1:
        timeForNextReturnBus1 = calc_time_diff(nextReturnBusTime1, CURRENT_DATETIME)
        if nextReturnBusTime2:
            timeForNextReturnBus2 = calc_time_diff(nextReturnBusTime1, CURRENT_DATETIME)
        else:
            timeForNextReturnBus2 = None
    else:
        timeForNextReturnBus1 = None
        timeForNextReturnBus2 = None

    # Substituir horários com valor None por "Acabaram os ônibus por hoje!"
    times = [
        [dt_to_str(nextDepartureBusTime1), timeForNextDepartureBus1],
        [dt_to_str(nextDepartureBusTime2), timeForNextDepartureBus2],
        [dt_to_str(nextReturnBusTime1), timeForNextReturnBus1],
        [dt_to_str(nextReturnBusTime2), timeForNextReturnBus2]
    ]

    timesOutput = []
    for time in times:
        if time[0] == None:
            time = r"Acabaram os ônibus por hoje\!"
        else:
            time = f"{time[0]} \({time[1]}\)"
        timesOutput.append(time)

    # String formatada
    next2busText = f"""
🚌 HORÁRIOS DOS PRÓXIMOS ÔNIBUS

⌚ Horário atual: {dt_to_str(CURRENT_DATETIME)}

➡️ IDA \(Moradia \-\> Unicamp\):
    01\) \) \) \) \) \) \) \) \) \) \) \) \) \) \) \) ) \) ) ) \) ) ) \) ) ) \) ) ) \) ) ) \) ) ) \) ) ) \) ) ) \) {timesOutput[0]}
    02\) {timesOutput[1]}

⬅️ VOLTA \(Unicamp \-\> Moradia\):
    01\) {timesOutput[2]}
    02\) {timesOutput[3]}
"""
    return next2busText

def createAvailableBusListMessage(busSchedule:list) -> str:
    """Cria uma string com todos os horários do dia de ônibus, riscando os horários que já passaram e destacando o próximo."""

    nextBus = nextBusFromNow(busSchedule)
    availableBusScheduleListText = "LISTA DE ÔNIBUS DISPONÍVEIS\n\n"

    pos = 0
    for time in busSchedule:

        # Ônibus que já passaram
        if time < nextBus:
            time = dt_to_str(time)
            pos += 1
            if pos % 3 == 0:
                availableBusScheduleListText += f'~{time}~\n'
            else:
                availableBusScheduleListText += f'~{time}~  \|  '

        # Próximo ônibus
        elif time == nextBus:
            pos += 1
            if pos % 3 == 0:
                availableBusScheduleListText += f'*{dt_to_str(nextBus)}*\n'
            else:
                availableBusScheduleListText += f'*{dt_to_str(nextBus)}*  \|  '

        # Ônibus que ainda não passaram
        else:
            time = dt_to_str(time)
            pos += 1
            if pos % 3 == 0:
                availableBusScheduleListText += f'{time}\n'
            else:
                availableBusScheduleListText += f'{time}  \|  '

    return availableBusScheduleListText