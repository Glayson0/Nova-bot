"""Esse arquivo contém todas as funções relacionadas aos ônibus da Unicamp.
"""
from bus_schedule import day_types
from time_utils import CURRENT_DATETIME, CURRENT_WEEKDAY, is_business_day, \
    calc_time_diff, dt_to_str
from datetime import datetime


# Funções auxiliares
def get_day_bus_schedule(weekday: str = CURRENT_WEEKDAY) -> tuple:
    """Retorna uma tupla com as listas de ida e volta dos ônibus dependendo do
    dia atual.
    """
    day_type = is_business_day(weekday)
    day_type = "business day" if day_type else "weekend"

    if weekday == 'domingo':
        return day_types[day_type][0][:25], day_types[day_type][1][:25]

    return day_types[day_type][0], day_types[day_type][1]


def has_available_bus(time: datetime, bus_schedule: list) -> bool:
    """Checa se há ônibus disponível no dia após o horário em que a função foi
    chamada.
    """
    return time < bus_schedule[-1]


def next_bus_from_now(bus_schedule: list,
                      time: datetime = CURRENT_DATETIME) -> datetime:
    """Retorna o horário em datetime do próximo ônibus a partir do horário em
    que a função foi chamada.
    """
    if has_available_bus(CURRENT_DATETIME, bus_schedule):
        for busTime in bus_schedule:
            if time <= busTime:
                return busTime

    return None


def get_available_bus_schedule(bus_schedule: list,
                               time: datetime = CURRENT_DATETIME) -> list:
    """Retorna uma lista com apenas os ônibus disponíveis no dia a partir do
    horário em que a função foi chamada.
    """
    available_bus_schedule = []

    for bus_time in bus_schedule:
        if time >= bus_time:
            available_bus_schedule.append(bus_time)

    return available_bus_schedule

# Funções principais


def createNextBusMessage() -> str:
    """Cria uma string com os horários dos conjuntos ida-volta dos ônibus da
    moradia.
    """
    departure_bus_schedule, return_bus_schedule = \
        get_day_bus_schedule(CURRENT_WEEKDAY)

    # Obtenção dos próximo 2 horários dos ônibus
    next_departure_bus_time_1 = next_bus_from_now(departure_bus_schedule)
    next_departure_bus_time_2 = next_bus_from_now(departure_bus_schedule,
                                                  next_departure_bus_time_1)
    next_return_bus_time_1 = next_bus_from_now(return_bus_schedule)
    next_return_bus_time_2 = next_bus_from_now(return_bus_schedule,
                                               next_return_bus_time_1)

    # Tempo restante para os horários - IDA
    if next_return_bus_time_1:
        time_for_next_departure_bus_1 = calc_time_diff(next_return_bus_time_1,
                                                       CURRENT_DATETIME)
        if next_return_bus_time_2:
            time_for_next_departure_bus_2 = calc_time_diff(
                next_return_bus_time_2, CURRENT_DATETIME)
        else:
            time_for_next_departure_bus_2 = None
    else:
        time_for_next_departure_bus_1 = None
        time_for_next_departure_bus_2 = None

    # Tempo restante para os horários - VOLTA
    if next_return_bus_time_1:
        time_for_next_return_bus_1 = calc_time_diff(next_return_bus_time_1,
                                                    CURRENT_DATETIME)
        if next_return_bus_time_2:
            time_for_next_return_bus_1 = calc_time_diff(next_return_bus_time_1,
                                                        CURRENT_DATETIME)
        else:
            time_for_next_return_bus_2 = None
    else:
        time_for_next_return_bus_1 = None
        time_for_next_return_bus_2 = None

    # Substituir horários com valor None por "Acabaram os ônibus por hoje!"
    times = [
        [dt_to_str(next_departure_bus_time_1), time_for_next_departure_bus_1],
        [dt_to_str(next_departure_bus_time_2), time_for_next_departure_bus_2],
        [dt_to_str(next_return_bus_time_1), time_for_next_return_bus_1],
        [dt_to_str(next_return_bus_time_2), time_for_next_return_bus_2]
    ]

    times_output = []
    for time in times:
        if time[0] is None:
            time = r"Acabaram os ônibus por hoje\!"
        else:
            time = f"{time[0]} \({time[1]}\)"
        times_output.append(time)

    # String formatada
    next_2_bus_text = f"""
🚌 HORÁRIOS DOS PRÓXIMOS ÔNIBUS

⌚ Horário atual: {dt_to_str(CURRENT_DATETIME)}

➡️ IDA \(Moradia \-\> Unicamp\):
    01\) \) \) \) \) \) \) \) \) \) \) \) \) \) \) \) ) \) ) ) \) ) ) \) ) ) \) ) ) \) ) ) \) ) ) \) ) ) \) ) ) \) {timesOutput[0]}
    02\) {times_output[1]}

⬅️ VOLTA \(Unicamp \-\> Moradia\):
    01\) {times_output[2]}
    02\) {times_output[3]}
"""
    return next_2_bus_text


def create_available_bus_list_message(bus_schedule: list) -> str:
    """Cria uma string com todos os horários do dia de ônibus, riscando os
    horários que já passaram e destacando o próximo.
    """

    next_bus = next_bus_from_now(bus_schedule)
    available_bus_schedule_list_text = "LISTA DE ÔNIBUS DISPONÍVEIS\n\n"

    pos = 0
    for time in bus_schedule:

        # Ônibus que já passaram
        if time < next_bus:
            time = dt_to_str(time)
            pos += 1
            if pos % 3 == 0:
                available_bus_schedule_list_text += f'~{time}~\n'
            else:
                available_bus_schedule_list_text += f'~{time}~  \|  '

        # Próximo ônibus
        elif time == next_bus:
            pos += 1
            if pos % 3 == 0:
                available_bus_schedule_list_text += \
                    f'*{dt_to_str(next_bus)}*\n'
            else:
                available_bus_schedule_list_text += \
                    f'*{dt_to_str(next_bus)}*  \|  '

        # Ônibus que ainda não passaram
        else:
            time = dt_to_str(time)
            pos += 1
            if pos % 3 == 0:
                available_bus_schedule_list_text += f'{time}\n'
            else:
                available_bus_schedule_list_text += f'{time}  \|  '

    return available_bus_schedule_list_text
