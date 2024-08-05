"""
Esse arquivo contém todas as funções relacionadas à manipulação de tempo.
"""

from datetime import datetime, timedelta

# Funções para as variáveis globais
def translateWeekday(weekday:str) -> str:
    """Traduz o dia da semana do inglês para português brasileiro."""

    translation_map = {
        "Monday": "Segunda",
        "Tuesday": "Terça",
        "Wednesday": "Quarta",
        "Thursday": "Quinta",
        "Friday": "Sexta",
        "Saturday": "Sábado",
        "Sunday": "Domingo"
    }
    
    return translation_map.get(weekday, weekday)

def getDayType(day:str) -> str:
    """Retorna se o dia é útil ou é não-util."""
    if day in 'Segunda Terça Quarta Quinta Sexta':
        return "working day"
    return "non working day"

# Variáveis globais
global CURRENT_DATETIME
CURRENT_DATETIME = datetime.now()  # tipo: datetime (YYYY-MM-DD HH:MM:SS.mmmmm)

global CURRENT_TIME
CURRENT_TIME = CURRENT_DATETIME.time()  # tipo: datetime (YYYY-MM-DD HH:MM:SS.mmmmm)

global CURRENT_WEEKDAY
CURRENT_WEEKDAY = translateWeekday(CURRENT_DATETIME.strftime('%A'))

global CURRENT_DAY_TYPE
CURRENT_DAY_TYPE = getDayType(CURRENT_WEEKDAY)

# Funções
def datetimeToStr(time: datetime) -> str:
    """Converte variáveis do tipo datetime para string no formato '%H:%M'"""
    return datetime.strftime(time, '%H:%M')

def strToTime(time:str):
    """Essa função converte horários do tipo str no formato '%H:%M' para datetime no formato 'ano-mês-dia hora:minuto'"""
    time = datetime.strptime(time, '%H:%M')
    return datetime.time(time)

def strToDatetime(time:str):
    """Essa função converte horários do tipo str no formato '%H:%M' para datetime no formato 'ano-mês-dia hora:minuto'"""
    time = datetime.strptime(time, '%H:%M')
    return datetime(CURRENT_DATETIME.year, CURRENT_DATETIME.month, CURRENT_DATETIME.day, time.hour, time.minute)

def calculateTimeDifference(endTime, startTime, formated=True) -> datetime:
    """Essa função calcula a diferença de tempo entre dois horários do tipo datetime"""

    if type(endTime) == str:
        endTime = strToDatetime(endTime)
    if type(startTime) == str:
        startTime = strToDatetime(startTime)

    timeDelta = endTime - timedelta(hours=startTime.hour, minutes=startTime.minute)

    if formated:
        if timeDelta.hour > 0:
            return f'{timeDelta.hour} hr e {timeDelta.minute} min'
        else:
            return f'{timeDelta.minute} min'
    else:
        return timeDelta