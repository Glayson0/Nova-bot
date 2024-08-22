import requests
from bs4 import BeautifulSoup
from datetime import datetime as dt
from modules.time_utils import is_date_valid
import dataclasses as dc

MENU_PATH = "https://www.prefeitura.unicamp.br/apps/cardapio/index.php?d={date}"


@dc.dataclass
class Menu:
    food_list: list[str]
    menu_type: str

    protein: str = dc.field(init=False)
    base: str = dc.field(init=False)
    complement: str = dc.field(init=False)
    salad: str = dc.field(init=False)
    dessert: str = dc.field(init=False)
    drink: str = dc.field(init=False)

    def __post_init__(self):
        self.protein = self.food_list[0]
        self.base = self.food_list[1]
        self.complement = self.food_list[2]
        self.salad = self.food_list[3]
        self.dessert = self.food_list[4]
        self.drink = self.food_list[5]

    def __str__ (self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        menu_types = ["🔴 Almoço Tradicional", "🟢 Almoço Vegano", "🔴 Jantar Tradicional", "🟢 Jantar Vegano"]
        message = (
            f"*{menu_types[self.menu_type]}*\n"
            f"*Proteína:* {self.protein}\n"
            f"*Base:* {self.base}\n"
            f"*Complemento:* {self.complement}\n"
            f"*Salada:* {self.salad}\n"
            f"*Sobremesa:* {self.dessert}\n"
            f"*Bebida:* {self.drink}\n"
        )
        return message


@dc.dataclass
class Restaurant:
    name: str
    schedule: dict[str:tuple]
    open_at_weekend: bool


def clean_and_split_menu(protein: str, menu_items: str) -> list[str]:

    food_list = menu_items.split("\r\n")
    food_list = food_list[1:3]
    food_list.insert(0, protein)

    for i in range(len(food_list)):
        food_list[i] = food_list[i].strip()
        
    aux_list = food_list[-1].split('                    ')
    food_list.pop(-1)
    aux_list[-1] = aux_list[-1].replace(" Observações:", "")

    food_list += aux_list

    for i in range(len(food_list)):
        food_list[i] = food_list[i].strip()

    return [food.capitalize() for food in food_list]


def get_menu(
        menu_type: int,
        date: str
) -> Menu:
    """
    Get the menu for a specific date and menu type.

    Args:
        date (str): The date in "YYYY-MM-DD" format.
        menu_type (int): The menu type: 0 = traditional lunch, 1 = traditional dinner, 2 = vegan lunch, 3 = vegan dinner.

    Returns:
        Menu: The menu for the specified date and menu type.
    """
    response = requests.get(MENU_PATH.format(date=date))
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all menu items
    proteins = soup.find_all(class_="menu-item-name")
    menu_items = soup.find_all(class_="menu-item-description")

    # All menus
    all_menus = []
    for i in range(len(proteins)):
        all_menus.append(clean_and_split_menu(proteins[i].text, menu_items[i].text))

    return Menu(all_menus[menu_type], menu_type)


def is_menu_number_valid(menu_number: int):
    return 0 <= menu_number <= 2

def validate_menu_entries(date: str, menu_number: int):
    if not is_date_valid(date):
        return ValueError(f"{menu_number} -> It is not a valid date 'MM-DD'.")
    if not is_menu_number_valid(menu_number):
        return ValueError(f"{menu_number} -> It is not a valid menu number (0-2).")


ru = Restaurant(
    "RU", 
    {"breakfast": ('07:30', '08:30'),
    "lunch": ('10:30', '14:00'),
    "dinner": ('17:30', '19:45')},
    False)

ra = Restaurant(
    "RA",
    {"breakfast": None,
    "lunch": ('11:15','14:00'),
    "dinner": ('17:30','19:00')
    },
    False)

rs = Restaurant(
    "RS",
    {"breakfast": None,
    "lunch": ('11:00','14:00'),
    "dinner": ('17:30','19:00')
    },
    True)
