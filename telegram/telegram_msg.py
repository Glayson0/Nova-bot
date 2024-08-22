import dataclasses as dc
from datetime import datetime as dt
from modules.bus import validate_bus_entries, get_weekdays_schedule, get_next_buses
from modules.restaurants import get_menu, validate_menu_entries
from data.texts import *

from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)


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


def create_menu_msg(
    date: str = dt.now().strftime("%Y-%m-%d"), menu_number: int = 0
) -> str:

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
