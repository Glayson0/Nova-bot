"""Esse arquivo contém todas as funções relacionadas à manipulação de tempo.
"""

from datetime import datetime
from re import match


def is_business_day(day: int) -> bool:
    """Receives days as int, Monday = 0, Tuesday = 1, ..., Sunday = 6
    and Returns True if it is a business day, False otherwise
    """
    return day < 5


def is_time_valid(time: str) -> bool:
    time_pattern = r"^\d{2}:\d{2}$"
    is_valid_time_pattern = match(time_pattern, time)

    if not is_valid_time_pattern:
        return False

    hours, minutes = map(int, time.split(':'))
    is_valid_time_range = 0 <= hours < 24 and 0 <= minutes < 60

    if not is_valid_time_range:
        return False
    
    return True


def is_weekday_valid(weekday: int) -> bool:
    return 0 <= weekday <= 9


def is_date_valid(date: str) -> bool:
    try:
        datetime.strptime(date, '%m-%d')
        return True
    except ValueError:
        return False
    
def get_time_remaining(date: str) -> str:
    """Receives a date in "HH-MM" format and returns the time remaining until that date.
    """
    date = datetime.strptime(date, '%H:%M')
    now = datetime.now()
    
    time_remaining = date - now
    
    return str(time_remaining)

def write_time_in_portuguese(time: str) -> str:
    """Receives a time in "HH:MM" format and returns it in portuguese.
    """
    hours, minutes = map(int, time.split(':'))
    
    if hours == 0:
        return f"{minutes} minutos"
    elif hours == 1:
        return f"1 hora e {minutes} minutos"
    elif minutes == 0:
        return f"{hours} horas"
    else:
        return f"{hours} horas e {minutes} minutos"