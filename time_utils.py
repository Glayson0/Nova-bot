"""Esse arquivo contém todas as funções relacionadas à manipulação de tempo.
"""

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
