"""Esse arquivo contém todas as funções relacionadas aos ônibus da Unicamp.
"""

from data.bus_schedule import BUS_SCHEDULER
from modules.time_utils import is_business_day, is_time_valid, is_weekday_valid


MAX_BUSINESSDAY_BUSES = 72
MAX_WEEKEND_BUSES = 35


# --------------------- #
#  Validation functions
# --------------------- #

def is_bus_num_valid(num: int, weekday: int) -> bool:
    if is_business_day(weekday):
        return 0 < num <= MAX_BUSINESSDAY_BUSES
    return 0 < num <= MAX_WEEKEND_BUSES


def validate_bus_entries(weekday: int, time: str, n_buses: int) -> None:
    if not is_weekday_valid(weekday):
        raise ValueError(f"{weekday} -> It is not a valid weekday (0-9).")

    if not is_time_valid(time):
        raise ValueError(f"{time} -> It is not a valid time format or range.")

    if not is_bus_num_valid(n_buses, weekday):
        raise ValueError(f"{n_buses} -> It is negative or exceeds the maximum number of buses.")


# --------------------- #
#    "Get" functions
# --------------------- #

def get_weekdays_schedule(weekday: int) -> dict[str, list[str]]:
    day_type = "business_day" if is_business_day(weekday) else "weekend"
    return BUS_SCHEDULER[day_type]


def get_next_buses(time: str, schedule: dict, num_buses: int) -> list[tuple]:
    # Initializes the list with the immediate next bus from the given time.
    next_buses = [(schedule[time].next_departure, schedule[time].next_return)]

    remaining_dep_buses = schedule[time].remaining_dep_buses
    remaining_ret_buses = schedule[time].remaining_ret_buses

    num_buses -= 1 # Adjust to pick the exact asked amount
    for i in range(0, num_buses):
        departure_bus = remaining_dep_buses[i] if i < len(remaining_dep_buses) else "-"
        return_bus = remaining_ret_buses[i] if i < len(remaining_ret_buses) else "-"

        ended_bus_list = (departure_bus == return_bus == "-")
        if not ended_bus_list:
            next_buses.append((departure_bus, return_bus))
        else:
            return next_buses

    return next_buses
