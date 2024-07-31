"""
Esse arquivo contém os horários de funcionamento dos restaurantes da Unicamp.
"""

from datetime import datetime
from timeUtils import *

# Dicionários das refeições com cada restaurante e seus respectivos horários de abertura e fechamento

cafeLocalidades = {
    'RU': ['07:30','08:30']
}

almocoLocalidades = {
    'RU': ['10:30','14:00'],
    'RA': ['11:15','14:00'],
    'RS': ['11:00','14:00']
}

jantarLocalidades = {
    'RU': ['17:30','19:45'],
    'RA': ['17:30','19:00'],
    'RS': ['17:30','19:00']
}
