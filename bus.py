"""Esse arquivo contém todas as funções relacionadas aos ônibus da Unicamp.
"""

import datetime as dt
from bus_schedule import BUS_SCHEDULER
from time_utils import is_business_day


def get_weekdays_schedule(weekday: int = dt.datetime.now().weekday()) -> dict[str, list[str]]:
    day_type = "business_day" if is_business_day(weekday) else "weekend"
    return BUS_SCHEDULER[day_type]


def get_next_buses(time: str, schedule: dict, num_buses: int = 0) -> list[tuple]:
    next_buses = [(schedule[time].next_departure, schedule[time].next_return)]
    dep_buses_exist = len(schedule[time].remaining_dep_buses)
    ret_buses_exist = len(schedule[time].remaining_ret_buses)
    
    for i in range(num_buses):
        next_dep_bus = str(schedule[time].remaining_dep_buses[i]) if dep_buses_exist else "-"
        next_ret_bus = str(schedule[time].remaining_ret_buses[i]) if ret_buses_exist else "-"
        next_buses.append((next_dep_bus, next_ret_bus))

    return next_buses


def create_next_buses_msg(time: str = dt.datetime.now().strftime("%H:%M"), n_buses: int = 1) -> str:
    schedule = get_weekdays_schedule()
    next_buses = get_next_buses(time, schedule, n_buses)

    # Cabeçalho
    header = f"""+{'-'*7}+{'-'*7}+
|{'IDA':^7}|{'VOLTA':^7}|
+{'-'*7}+{'-'*7}+"""
    
    # Corpo
    body = ""
    for pair in next_buses:
        dep_bus = pair[0] if pair[0] is not None else '-'
        ret_bus = pair[1] if pair[1] is not None else '-'
        body += f"\n|{dep_bus:^7}|{ret_bus:^7}|"

    # Fim
    footer = f"""\n+{'-'*7}+{'-'*7}+"""

    return header + body + footer