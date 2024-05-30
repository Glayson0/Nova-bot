"""
Este arquivo contém funções responsáveis pela criação dos menus disponíveis
na interação com o bot.
"""

from datetime import datetime
from bandejao import *
from timeUtils import *

# Importação de bibliotecas
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

class Message:
    """
    Classe para criação de mensagens.
    """
    def __init__(self, text: str, buttons: dict):
        self.text = text
        self.buttons = buttons

##
##   MENSAGENS GERAIS
##

# Mensagem Start
startText = f"""
Eu me chamo Nova e sou um bot criado por alunos da Unicamp\!

Meu objetivo é fornecer informações dos ônibus da moradia e dos restaurantes da Unicamp de forma rápida e fácil\.

Clique no botão que apareceu no lugar do seu teclado ou digite /home para ver o menu principal\.
"""

startButtons = {
    "Home": "home"
}

startMessage = Message(startText, startButtons)

# Mensagem menu Home
menuHomeText = """Menu *Principal* 🏠

Escolha entre as opções abaixo para acessar os menus de cada categoria do bot\!

\- _Menu ônibus_: alterna para o menu com os comandos relacionados aos ônibus da moradia\.
\- _Menu restaurantes_: alterna para o menu com os comandos relacionados aos restaurantes da Unicamp\.
"""

menuHomeButtons = {
    'Menu ônibus': 'callback_menuOnibus',
    'Menu restaurantes': 'callback_menuRestaurantes',

    "Home": "callback_home"
}

menuHomeMessage = Message(menuHomeText, menuHomeButtons)

menuHomeButtons_telegram = InlineKeyboardMarkup()
menuHomeButtons_telegram.add(InlineKeyboardButton(text='Menu ônibus', callback_data='menuOnibus'))
menuHomeButtons_telegram.add(InlineKeyboardButton(text='Menu restaurantes', callback_data='menuRestaurantes'))

##
##  MENSAGENS ÔNIBUS DA MORADIA
##

# Mensagem menu ônibus da moradia
menuOnibusText = """Menu *Ônibus* 🚌

\- _Próximos ônibus_: Ver os próximos 2 ônibus de ida e de volta

\- _Tabela de horários_: Ver a foto do pdf com todos os horários de ônibus

\- _Lista dos ônibus de ida_: Ver todos os horários de ônibus de IDA do dia \(Moradia \-\> Unicamp\)

\- _Lista dos ônibus de Volta_: Ver todos os horários de ônibus de VOLTA dia \(Unicamp \-\> Moradia\)
"""

menuOnibusButtons = {
    "Próximos ônibus": "callback_oProximosOnibus",
    "Tabela de horários": "callback_oTabelaDeHorarios",
    "Lista dos ônibus de ida": "callback_oTodosOnibusIda",
    "Lista dos ônibus de volta": "callback_oTodosOnibusVolta",

    "Home": "callback_home"
}

menuOnibusMessage = Message(menuOnibusText, menuOnibusButtons)

menuOnibusButtons_telegram = InlineKeyboardMarkup()
menuOnibusButtons_telegram.add(
    InlineKeyboardButton(text='Próximos ônibus', callback_data='oProx'),
    InlineKeyboardButton(text='Tabela de horários', callback_data='oTodos')
)
menuOnibusButtons_telegram.add(
    InlineKeyboardButton(text='Lista dos ônibus de ida', callback_data='oTodosIda'),
    InlineKeyboardButton(text='Lista dos ônibus de volta', callback_data='oTodosVoolta')
)

menuOnibusButtons_telegram.add(InlineKeyboardButton(text='Home', callback_data='home'))

# Mensagem Próximos ônibus

# Mensagem Tabela de horários

# Mensagem Lista dos ônibus de ida

# Mensagem Lista dos ônibus de volta

##
##  MENSAGENS RESTAURANTES
##

# Mensagem menu restaurantes
menuRestaurantesText = """Menu *Restaurantes* 🍽️

Geral
\- _Horários_: Ver os horários dos três restaurantes

\- _Cardápios_: Ver o cardápio de almoço e jantar

\- _Já pode ao mossar?_: Ver se já tá podendo

Restaurantes
\- _RU_: Ver informações do RU

\- _RA_: Ver informações do RA

\- _RS_: Ver informações do RS
"""

menuRestaurantesButtons = {
    "Horários": "callback_rHorarios",
    "Cardápios": "callback_rCardápios",
    "RU": "callback_ru",
    "RA": "callback_ra",
    "RS": "callback_rs",

    "Home": "callback_home"
}

menuRestaurantesMessage = Message(menuRestaurantesText, menuRestaurantesButtons)

menuRestaurantesButtons_telegram = InlineKeyboardMarkup()

menuRestaurantesButtons_telegram.add(InlineKeyboardButton(text='Já pode ao mossar?', callback_data='bJaPode'))

menuRestaurantesButtons_telegram.add(
    InlineKeyboardButton(text='Horários', callback_data='bHoras'),
    InlineKeyboardButton(text='Cardápios', callback_data='bCardapios')
)
menuRestaurantesButtons_telegram.add(
    InlineKeyboardButton(text='RU', callback_data='ru'),
    InlineKeyboardButton(text='RA', callback_data='ra'),
    InlineKeyboardButton(text='RS', callback_data='rs')
)
menuRestaurantesButtons_telegram.add(InlineKeyboardButton(text='Home', callback_data='home'))

# Menu cardápios
cardapiosText = """Menu *Cardápios* 📋

    \- /bTradicional: Cardápio tradicional

    \- /bVegano: Cardápio vegano
"""

cardapiosButtons = {
    "Cardápio Tradicional": "callback_cardapioTradicional",
    "Cardápio Vegano": "callback_cardapioVegano",

    "Home": "home"
}

cardapiosMessage = Message(cardapiosText, cardapiosButtons)

# Botões
cardapiosButtons_telegram = InlineKeyboardMarkup()
cardapiosButtons_telegram.add(
    InlineKeyboardButton(text='Cardápio Tradicional', callback_data='bTradicional'),
    InlineKeyboardButton(text='Cardápio Vegano', callback_data='bVegano')
)
cardapiosButtons_telegram.add(InlineKeyboardButton(text='Home', callback_data='home'))

# Mensagem Cardápio Tradicional
def cardapioTradicional(date: datetime) -> object:

    currentWeekDay = getWeekDay(date)

    if currentWeekDay == "Domingo":
            almocoTradicional = getCardapio(date, currentWeekDay)[0]
        
        # Texto da mensagem do bot  
            cardapioTradicionalText = f"""
        Cardápio *Tradicional* 🥩

    \-\> *Almoço*
        *Proteína*: {almocoTradicional.proteina}
        *Base*: {almocoTradicional.base}
        *Complemento*: {almocoTradicional.complemento}
        *Salada*: {almocoTradicional.salada}
        *Fruta*: {almocoTradicional.fruta}
        *Suco*: {almocoTradicional.suco}
        
    \-\> *Jantar*
        Não tem jantar aos domingos\!
    """

    else:
        almocoTradicional = getCardapio(tempoAtual, currentWeekDay)[0]
        jantarTradicional = getCardapio(tempoAtual, currentWeekDay)[1]

        # Texto da mensagem do bot
        cardapioTradicionalText = f"""
        Cardápio *Tradicional* 🥩

    \-\> *Almoço*
        *Proteína*: {almocoTradicional.proteina}
        *Base*: {almocoTradicional.base}
        *Complemento*: {almocoTradicional.complemento}
        *Salada*: {almocoTradicional.salada}
        *Fruta*: {almocoTradicional.fruta}
        *Suco*: {almocoTradicional.suco}

    \-\> *Jantar*
        *Proteína*: {jantarTradicional.proteina}
        *Base*: {jantarTradicional.base}
        *Complemento*: {jantarTradicional.complemento}
        *Salada*: {jantarTradicional.salada}
        *Fruta*: {jantarTradicional.fruta}
        *Suco*: {jantarTradicional.suco}
        """