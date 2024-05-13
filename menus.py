"""
Este arquivo contém funções responsáveis pela criação dos menus disponíveis
na interação com o bot.
"""

# Importação de bibliotecas
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Classe Menu para a criação das mensagens-menu
class Menu:
    def __init__(self, text, buttons) -> None:
        self.text = text
        self.buttons = buttons
        pass




# Menu Home
textoHome = """
Menu *Principal* 🏠

Escolha entre as opções abaixo para acessar os menus de cada categoria do bot\!

\- _Menu ônibus_: alterna para o menu com os comandos relacionados aos ônibus da moradia\.
\- _Menu restaurantes_: alterna para o menu com os comandos relacionados aos restaurantes da Unicamp\.
"""

botoesHome = InlineKeyboardMarkup()
botoesHome.add(InlineKeyboardButton(text='Menu ônibus', callback_data='menuOnibus'))
botoesHome.add(InlineKeyboardButton(text='Menu restaurantes', callback_data='menuRestaurantes'))

menuHome = Menu(textoHome, botoesHome)




# Menu ônibus da moradia
textoOnibus = """
Menu *Ônibus* 🚌

\- _Próximos ônibus_: Ver os próximos 2 ônibus de ida e de volta

\- _Tabela de horários_: Ver a foto do pdf com todos os horários de ônibus

\- _Lista dos ônibus de ida_: Ver todos os horários de ônibus de IDA do dia \(Moradia \-\> Unicamp\)

\- _Lista dos ônibus de Volta_: Ver todos os horários de ônibus de VOLTA dia \(Unicamp \-\> Moradia\)
"""

botoesOnibus = InlineKeyboardMarkup()
botoesOnibus.add(
    InlineKeyboardButton(text='Próximos ônibus', callback_data='oProx'),
    InlineKeyboardButton(text='Tabela de horários', callback_data='oTodos')
)
botoesOnibus.add(
    InlineKeyboardButton(text='Lista dos ônibus de ida', callback_data='oTodosIda'),
    InlineKeyboardButton(text='Lista dos ônibus de volta', callback_data='oTodosVoolta')
)

botoesOnibus.add(InlineKeyboardButton(text='Home', callback_data='home'))

menuOnibus = Menu(textoOnibus, botoesOnibus)




# Menu restaurantes
textoRestaurantes = """
Menu *Restaurantes* 🍽️

Geral
\- _Horários_: Ver os horários dos três restaurantes

\- _Cardápios_: Ver o cardápio de almoço e jantar

\- _Já pode ao mossar?_: Ver se já tá podendo

Restaurantes
\- _RU_: Ver informações do RU

\- _RA_: Ver informações do RA

\- _RS_: Ver informações do RS
"""

botoesRestaurantes = InlineKeyboardMarkup()

botoesRestaurantes.add(InlineKeyboardButton(text='Já pode ao mossar?', callback_data='bJaPode'))

botoesRestaurantes.add(
    InlineKeyboardButton(text='Horários', callback_data='bHoras'),
    InlineKeyboardButton(text='Cardápios', callback_data='bCardapios')
)
botoesRestaurantes.add(
    InlineKeyboardButton(text='RU', callback_data='ru'),
    InlineKeyboardButton(text='RA', callback_data='ra'),
    InlineKeyboardButton(text='RS', callback_data='rs')
)
botoesRestaurantes.add(InlineKeyboardButton(text='Home', callback_data='home'))

menuRestaurantes = Menu(textoRestaurantes, botoesRestaurantes)



# Menu cardápios
# Texto da mensagem do bot
textoCardapios = """
Menu *Cardápios* 📋

    \- /bTradicional: Cardápio tradicional

    \- /bVegano: Cardápio vegano
"""

# Botões
botoesCardapios = InlineKeyboardMarkup()
botoesCardapios.add(
    InlineKeyboardButton(text='Cardápio Tradicional', callback_data='bTradicional'),
    InlineKeyboardButton(text='Cardápio Vegano', callback_data='bVegano')
)
botoesCardapios.add(InlineKeyboardButton(text='Home', callback_data='home'))

menuCardapios = Menu(textoCardapios, botoesCardapios)