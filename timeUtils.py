"""
Esse arquivo contém todas as funções relacionadas à manipulação de tempo.
"""

from datetime import datetime, timedelta

# Funções para as variáveis globais
def getTranslatedWeekday(weekday:str) -> str:
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
        return "dia util"
    return "dia não-util"

# Variáveis globais
global CURRENT_TIME
CURRENT_TIME = datetime.now()  # tipo: datetime (YYYY-MM-DD HH:MM:SS.mmmmm)

global CURRENT_WEEKDAY
CURRENT_WEEKDAY = getTranslatedWeekday(CURRENT_TIME.strftime('%A'))

global CURRENT_DAY_TYPE
CURRENT_DAY_TYPE = getDayType(CURRENT_WEEKDAY)

# Funções
def datetimeToStr(h: datetime) -> str:
    """Converte variáveis do tipo datetime para string no formato '%H:%M'"""

    return datetime.strftime(h, '%H:%M')

def strToDatetime(h:str) -> datetime:
    """Essa função converte horários do tipo str no formato '%H:%M' para datetime no formato 'ano-mês-dia hora:minuto'"""

    h = datetime.strptime(h, '%H:%M')
    return datetime(CURRENT_TIME.year, CURRENT_TIME.month, CURRENT_TIME.day, h.hour, h.minute)

def getTimeDifference(startTime, endTime) -> datetime:
    """Essa função calcula a diferença de tempo entre dois horários do tipo datetime"""

    if type(startTime) == str:
        startTime = strToDatetime(startTime)
    if type(endTime) == str:
        endTime = strToDatetime(endTime)

    return startTime - timedelta(hours=endTime.hour, minutes=endTime.minute)