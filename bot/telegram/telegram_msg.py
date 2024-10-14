import dataclasses as dc
from datetime import datetime as dt

from telebot.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)

from bot.data.texts import *
from bot.modules.bus import (get_next_buses, get_weekdays_schedule,
                             validate_bus_entries)
from bot.modules.restaurants import (get_available_restaurants, get_menu,
                                     get_next_restaurant_opening_time,
                                     get_restaurants_from_the_day, ra, rs, ru,
                                     validate_menu_entries)
from bot.modules.time_utils import get_time_remaining


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
    weekday: int | None = None, time: str | None = None, n_buses: int = 1,
) -> str:
    if weekday is None:
        weekday = dt.now().weekday()

    if time is None:
        time = dt.now().strftime("%H:%M")

    validate_bus_entries(weekday, time, n_buses)

    schedule = get_weekdays_schedule(weekday)
    next_buses = get_next_buses(time, schedule, n_buses)

    header = f"+{'-'*13}+{'-'*13}+|{'IDA':^13}|{'VOLTA':^13}|+{'-'*13}+{'-'*13}+"

    body = ""
    for pair in next_buses:
        dep_bus = pair[0] if pair[0] is not None else "-"
        ret_bus = pair[1] if pair[1] is not None else "-"
        body += f"\n|{dep_bus:^13}|{ret_bus:^13}|"

    footer = f"\n+{'-'*13}+{'-'*13}+"

    return header + body + footer


def create_menu_msg(
    date: str | None = None,
    menu_number: int = 0
) -> str:

    if date is None:
        date = dt.now().strftime("%Y-%m-%d")

    validate_menu_entries(date, menu_number)

    menu_keywords = ["tudo", "tradicional", "vegano"]
    # BUG: Porque nas duas primeiras linhas tem mais de um get_menu e na outra não?
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

def create_get_restaurants_available_msg() -> str:
    date = dt.now().strftime("%H:%M")
    weekday = dt.now().weekday()
    restaurants = get_available_restaurants(date, weekday)

    if restaurants and len(restaurants) > 1:
        restaurant_msgs = [
            (
                f"O {r.name} está aberto! Ele fecha às {r.schedule[1]} em " +
                get_time_remaining(dt.strptime(date, "%H:%M"), r.schedule[1])
            )
            for r in restaurants
        ]

        return "\n".join(restaurant_msgs) + "\n"

    elif restaurants:
        return (
            f"O {restaurants[0].name} está aberto! Ele fecha às {restaurants[0].schedule[1]} em " +
            get_time_remaining(dt.strptime(date, "%H:%M"), restaurants[0].schedule[1])
        )

    else:
        restaurants = get_restaurants_from_the_day(weekday)
        restaurants_info = []

        for r in restaurants:
            next_opening_time = get_next_restaurant_opening_time(date, r)
            if next_opening_time:
                restaurants_info.append((next_opening_time, r.name))

        if not restaurants_info:
            return "Não há restaurantes disponíveis no momento."

        restaurant_info_msgs = [
            f"{r_i[1]} abre em {r_i[0]}"
            for r_i in restaurants_info
        ]

        return f"Não há restaurantes disponíveis no momento.\n" + "\n".join(restaurant_info_msgs)

def create_message(res_name: str) -> tuple[str, str]:
    breakfast = "Não há"
    restaurant = ra if res_name == "/ra" else rs

    # Restaurantes com café da manhã
    if res_name == "/ru":
        restaurant = ru
        breakfast = f"{restaurant.schedule['breakfast'][0]} às {restaurant.schedule['breakfast'][1]}"

    lunch = f"{restaurant.schedule['lunch'][0]} às {restaurant.schedule['lunch'][1]}"
    dinner = f"{restaurant.schedule['dinner'][0]} às {restaurant.schedule['dinner'][1]}"

    return (
        f"*{restaurant.name}*\n"
        f"{restaurant.address}\n"
        f"*Horários* (dia útil)\n"
        f"Café da manhã: {breakfast}\n"
        f"Almoço: {lunch}\n"
        f"Jantar: {dinner}\n"
    ), restaurant.image_path

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
