"""Esse arquivo contém todas as funções relacionadas aos ônibus da Unicamp.
"""
import datetime as dt

from bus_schedule import *
from time_utils import *


# Funções auxiliares
def next_bus_from_now() -> tuple[str, str]:
    """Retorna o horário em datetime do próximo ônibus a partir do horário em que a função foi chamada."""
    day_type = is_business_day(dt.datetime.now().weekday())
    day_type = "business_day" if day_type else "weekend"

    return BUS_SCHEDULER[day_type]

# Funções principais
def create_next_bus_message(time:str) -> str:
    todays_schedule = next_bus_from_now()
    next_buses = todays_schedule[time]

    next2busesText = f"""+{'-'*7}+{'-'*7}+
|{'IDA':^7}|{'VOLTA':^7}|
+{'-'*7}+{'-'*7}+
{next_buses}
+{'-'*7}+{'-'*7}+
"""
    return next2busesText