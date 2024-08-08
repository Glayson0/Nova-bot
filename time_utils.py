"""
Esse arquivo contém todas as funções relacionadas à manipulação de tempo.
"""

from datetime import datetime, timedelta

# Use locale to set the default locale
# that converts literals to portuguese

def is_business_day (day: int) -> bool:
    """
        Receives days as int, Monday = 0, Tuesday = 1, ..., Sunday = 6
        and Returns True if it is a business day, False otherwise
    """
    return day < 5

# Variáveis globais
CURRENT_DATETIME = datetime.now()  # tipo: datetime (YYYY-MM-DD HH:MM:SS.mmmmm)

CURRENT_TIME = CURRENT_DATETIME.time()  # tipo: datetime (YYYY-MM-DD HH:MM:SS.mmmmm)

CURRENT_WEEKDAY = CURRENT_DATETIME.strftime('%A')

CURRENT_DAY_TYPE = is_business_day(CURRENT_DATETIME.weekday())

# Funções
def dt_to_str(time: datetime) -> str:
    """Converte variáveis do tipo datetime para string no formato '%H:%M'"""
    return datetime.strftime(time, '%H:%M')

def str_to_time(time: str) -> datetime:
    """Essa função converte horários do tipo str no formato '%H:%M' para datetime no formato 'ano-mês-dia hora:minuto'"""
    return datetime.strptime(time, '%H:%M')

def calc_time_diff(
    endTime: str | datetime, startTime: str | datetime, formated: bool = True
) -> datetime:
    """Essa função calcula a diferença de tempo entre dois horários do tipo datetime"""

    if type(endTime) == str:
        endTime = str_to_time(endTime)

    if type(startTime) == str:
        startTime = str_to_time(startTime)

    time_diff = endTime - timedelta(hours=startTime.hour, minutes=startTime.minute)

    if formated:
        if time_diff.hour:
            return time_diff.strftime("%H hr e %M min")

        return time_diff.strftime("%M min")
    
    return time_diff
