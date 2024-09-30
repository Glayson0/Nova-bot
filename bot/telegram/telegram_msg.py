import dataclasses as dc
from datetime import datetime as dt

from telebot.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)

from bot.data.texts import *
from bot.modules.bus import (get_next_buses, get_weekdays_schedule,
                             validate_bus_entries)
from bot.modules.restaurants import (get_menu, validate_menu_entries,
                                     get_available_restaurants,
                                     get_restaurants_from_the_day,
                                     get_next_restaurant_opening_time, ru, ra, rs)

from bot.modules.time_utils import (get_time_remaining,
                                    write_time_in_portuguese)

@dc.dataclass
class Message_Layout:
    short_text: str
    text: str
    inline_markup: InlineKeyboardMarkup
    inline_keyboard: list[InlineKeyboardButton]
    reply_markup: ReplyKeyboardMarkup
    reply_keyboard: list[KeyboardButton]

    def __post_init__(self):
        for button in self.inline_keyboard:
            self.inline_markup.add(button)
        for button in self.reply_keyboard:
            self.reply_markup.add(button)


def create_next_buses_msg(
    weekday: int | None = None,
    time: str | None = None,
    n_buses: int = 1,
) -> str:
    if weekday is None:
        weekday = dt.now().weekday()
        
    if time is None:
        time = dt.now().strftime("%H:%M")

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


def create_menu_msg(
    date: str | None = None,
    menu_number: int = 0
) -> str:
    
    if date is None:
        date = dt.now().strftime("%Y-%m-%d")

    validate_menu_entries(date, menu_number)

    menu_keywords = ["tudo", "tradicional", "vegano"]
    MENU_CREATOR = {
        "tradicional": (get_menu(0, date), get_menu(2, date)),
        "vegano": (get_menu(1, date), get_menu(3, date)),
        "tudo": (
            get_menu(0, date),
            get_menu(2, date),
            get_menu(1, date),
            get_menu(3, date),
        ),
    }

    menus = MENU_CREATOR[menu_keywords[menu_number]]

    menu_message = ""
    for menu in menus:
        menu_message += f"{str(menu)}\n\n"

    return menu_message

def create_get_restaurants_available_msg():
    date = dt.now().strftime("%Y-%m-%d")
    weekday = dt.now().weekday()
    restaurants = get_available_restaurants(date, weekday)
    
    if restaurants and len(restaurants) > 1:
        return f"{'\n'.join(f'O {r.name} está aberto! Ele fecha às {r.schedule[1]} em {write_time_in_portuguese(get_time_remaining(r.schedule[1]))}' for r in restaurants)}\n"
    elif restaurants:
        return f"O {restaurants[0].name} está aberto! Ele fecha às {restaurants[0].schedule[1]} em {write_time_in_portuguese(get_time_remaining(restaurants[0].schedule[1]))}"
    else:
        restaurants = get_restaurants_from_the_day(weekday)
        restaurants_info = []
        
        for r in restaurants:
            next_opening_time = get_next_restaurant_opening_time(date, r)
            restaurants_info.append((next_opening_time, r.name)) if next_opening_time else None
                
        if restaurants_info:
            return f"""Não há restaurantes disponíveis no momento.
                {'\n'.join(f'{r_i[0]} abre em {write_time_in_portuguese(r_i[1])}' for r_i in restaurants_info)}
                """
        else:
            return f"Não há restaurantes disponíveis no momento."
        
        
def create_ru_msg() -> tuple[str, str]:
    breakfast = f"{ru.schedule["breakfast"][0]} às {ru.schedule["breakfast"][1]}"
    lunch = f"{ru.schedule["lunch"][0]} às {ru.schedule["lunch"][1]}"
    dinner = f"{ru.schedule["dinner"][0]} às {ru.schedule["dinner"][1]}"
    
    msg = f"""{ru.name}
{ru.address}

- Horários (dia útil)
Café da manhã: {breakfast}
Almoço: {lunch}
Jantar: {dinner}
"""
    return msg, ru.image_path
    
    
def create_ra_msg() -> tuple[str, str]:
    lunch = f"{ra.schedule["lunch"][0]} às {ra.schedule["lunch"][1]}"
    dinner = f"{ra.schedule["dinner"][0]} às {ra.schedule["dinner"][1]}"
    
    msg = f"""{ra.name}
{ra.address}

Horários (dia útil)
Café da manhã: Não há
Almoço: {lunch}
Jantar: {dinner}
"""

    return msg, ra.image_path


def create_rs_msg() -> tuple[str, str]:
    breakfast = f"{rs.schedule["breakfast"][0]} às {rs.schedule["breakfast"][1]}"
    lunch = f"{rs.schedule["lunch"][0]} às {rs.schedule["lunch"][1]}"
    dinner = f"{rs.schedule["dinner"][0]} às {rs.schedule["dinner"][1]}"
    
    msg = f"""{rs.name}
{rs.address}

- Horários (exceto domingos)
Café da manhã (somente dias não-úteis): {breakfast}
Almoço: {lunch}
Jantar: {dinner}
"""
    return msg, rs.image_path


# --------------------- #
#    Message objects
# --------------------- #

start_message = Message_Layout(
    START_SHORT_TEXT,
    START_TEXT,
    InlineKeyboardMarkup(row_width=1),
    [
        InlineKeyboardButton("Ir para a Home", callback_data="cb_home")
    ],
    ReplyKeyboardMarkup(resize_keyboard=True),
    [
        KeyboardButton("/home")
    ],
)


home_message = Message_Layout(
    MENU_SHORT_TEXT,
    MENU_TEXT,
    InlineKeyboardMarkup(row_width=2),
    [
        InlineKeyboardButton("Comandos ônibus", callback_data="cb_onibus"),
        InlineKeyboardButton("Comandos bandejao", callback_data="cb_bandejao"),
        InlineKeyboardButton("Todos os comandos", callback_data="cb_tudo"),
    ],
    ReplyKeyboardMarkup(resize_keyboard=True, row_width=2),
    [KeyboardButton("/onibus"), KeyboardButton("/bandejao"), KeyboardButton("/tudo")],
)


unknown_message = Message_Layout(
    UNKNOWN_SHORT_TEXT,
    UNKNOWN_TEXT,
    InlineKeyboardMarkup(row_width=1),
    [
        InlineKeyboardButton("Ir para a Home", callback_data="cb_home")
    ],
    ReplyKeyboardMarkup(resize_keyboard=True),
    [
        KeyboardButton("/home")
    ]
)


onibus_message = Message_Layout(
    BUS_SHORT_TEXT,
    BUS_TEXT,
    InlineKeyboardMarkup(row_width=2),
    [
        InlineKeyboardButton("Próximo ônibus", callback_data="cb_oProx"),
        InlineKeyboardButton("Todos os ônibus do dia", callback_data="cb_oTodos"),
        InlineKeyboardButton("Foto oficial dos horários", callback_data="cb_oFoto"),
        InlineKeyboardButton("Ir para a Home", callback_data="cb_home")
    ],
    ReplyKeyboardMarkup(resize_keyboard=True, row_width=2),
    [
        KeyboardButton("/oProx"),
        KeyboardButton("/oTodos"),
        KeyboardButton("/oFoto"),
    ],
)


bandejao_message = Message_Layout(
    BANDEJAO_SHORT_TEXT,
    BANDEJAO_TEXT,
    InlineKeyboardMarkup(row_width=2),
    [
        InlineKeyboardButton("Cardápio Tradicional", callback_data="cb_bCardapio1"),
        InlineKeyboardButton("Cardápio Vegano", callback_data="cb_bCardapio2"),
        InlineKeyboardButton("Ambos cardápios", callback_data="cb_bCardapio0"),
        InlineKeyboardButton("Ir para a Home", callback_data="cb_home")
    ],
    ReplyKeyboardMarkup(resize_keyboard=True, row_width=2),
    [
        KeyboardButton("/bCardapio 1"),
        KeyboardButton("/bCardapio 2"),
        KeyboardButton("/bCardapio 0"),
    ],
)
