"""
Esse arquivo contém todas as funções relacionadas à manipulação de tempo.
"""

from datetime import datetime, timedelta


# Funções para as variáveis globais
def translate_week_day(weekday: str) -> str:
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

def is_business_day (day: str) -> str:
    """Retorna se o dia é útil ou é não-util."""
    if day in 'Segunda Terça Quarta Quinta Sexta':
        return "working day"

    return "non working day"

# Variáveis globais
CURRENT_DATETIME = datetime.now()  # tipo: datetime (YYYY-MM-DD HH:MM:SS.mmmmm)

CURRENT_TIME = CURRENT_DATETIME.time()  # tipo: datetime (YYYY-MM-DD HH:MM:SS.mmmmm)

CURRENT_WEEKDAY = translate_week_day(CURRENT_DATETIME.strftime('%A'))

CURRENT_DAY_TYPE = is_business_day(CURRENT_WEEKDAY)

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

    timeDelta = endTime - timedelta(hours=startTime.hour, minutes=startTime.minute)

    if formated:
        if timeDelta.hour > 0:
            return f'{timeDelta.hour} hr e {timeDelta.minute} min'
        else:
            return f'{timeDelta.minute} min'
    else:
        return timeDelta