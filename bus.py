"""Esse arquivo contém todas as funções relacionadas aos ônibus da Unicamp.
"""

from datetime import datetime as dt
from bus_schedule import BUS_SCHEDULER
from time_utils import is_business_day, is_time_valid, is_weekday_valid


##
##  Constants
## 

MAX_BUSINESSDAY_BUSES = 72
MAX_WEEKEND_BUSES = 35


##
##  Validation functions
## 

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


##
##  'get' functions
## 

def get_weekdays_schedule(weekday: int) -> dict[str, list[str]]:
    day_type = "business_day" if is_business_day(weekday) else "weekend"
    return BUS_SCHEDULER[day_type]


def get_next_buses(time: str, schedule: dict, num_buses: int) -> list[tuple]:
    # Initializes the list with the immediate next bus from the given time.
    next_buses = [(schedule[time].next_departure, schedule[time].next_return)]

    remaining_dep_buses = schedule[time].remaining_dep_buses
    remaining_ret_buses = schedule[time].remaining_ret_buses

    for i in range(1, num_buses):
        departure_bus = remaining_dep_buses[i] if i < len(remaining_dep_buses) else "-"
        return_bus = remaining_ret_buses[i] if i < len(remaining_ret_buses) else "-"

        ended_bus_list = (departure_bus == return_bus == "-")
        if not ended_bus_list:
            next_buses.append((departure_bus, return_bus))
        else:
            return next_buses

    return next_buses


##
##  Create message
## 

def create_next_buses_msg(
    weekday: int = dt.now().weekday(),
    time: str = dt.now().strftime("%H:%M"),
    n_buses: int = 1,
) -> str:

    validate_bus_entries(weekday, time, n_buses)

    schedule = get_weekdays_schedule(weekday)
    next_buses = get_next_buses(time, schedule, n_buses)

    header = f"""+{'-'*7}+{'-'*7}+
|{'IDA':^7}|{'VOLTA':^7}|
+{'-'*7}+{'-'*7}+"""

    body = ""
    for pair in next_buses:
        dep_bus = pair[0] if pair[0] is not None else "-"
        ret_bus = pair[1] if pair[1] is not None else "-"
        body += f"\n|{dep_bus:^7}|{ret_bus:^7}|"

    footer = f"""\n+{'-'*7}+{'-'*7}+"""

    return header + body + footer


##
##  Run
## 

if __name__ == "__main__":
    manual_test = int(input("- Método de inserção de dados:\n[0] Hora atual  |  [1] Manual\nSua opção: "))

    if manual_test:
        print("- Inserir valores:")

        weekday = int(input("Dia da semana: "))
        time = input("Horário: ")
        num_buses = int(input("Qntd de ônibus: "))

        print(create_next_buses_msg(weekday, time, num_buses))
    else:
        print("- Utilizando o horário e dia atuais.")

        print(create_next_buses_msg())
