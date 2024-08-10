"""Este arquivo é para a construção do bot para o Telegram"""

import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, \
    KeyboardButton
from telebot.replymarkup import ReplyKeyboardMarkup

from bus import get_day_bus_schedule, create_available_bus_list_message, \
    create_next_bus_message
from texts import start_text, help_text, onibus_text, bandejao_text, \
    cardapio_text
from time_utils import CURRENT_WEEKDAY
from bus_schedule import BUS_FULL_SCHEDULE_PHOTO

# Fazer conexão com a API do bot do Telegram
CHAVE_API = "7141300367:AAHBHEelfnAig53EVxqq0oabZrRz15CjIJ8"
bot = telebot.TeleBot(CHAVE_API, parse_mode='MarkdownV2')

"""NOTAS:
- O parâmetro "messagem" é um objeto mensagem enviada pelo usuário;
- Todas as funções podem ser chamadas a qualquer momento no chat pelos seus
respectivos comandos;
- Há uma hierarquia vertical para a chamada das funções que têm o
message_handler. Ou seja, por exemplo: se houver mais de uma função com o
mesmo trigger, apenas aquela que está mais acima será ativada.

"""


# --------------------- #
#        Comandos
# --------------------- #

# Comando /start
@bot.message_handler(commands=["start"])
def start(mensagem):

    # Botões
    start_button = InlineKeyboardMarkup(row_width=1)
    start_button.add(InlineKeyboardButton('/help', callback_data="cb_help"))

    # Envio de mensagem
    bot.send_message(mensagem.chat.id,
                     f'👋 Olá, {mensagem.chat.first_name}\! Como vai?')
    bot.send_message(mensagem.chat.id, start_text, reply_markup=start_button)


# Comando /help
@bot.message_handler(commands=["help"])
def help(mensagem):

    """envia uma mensagem no chat com 3 comandos principais para ajudar o
    usuário.
    """

    # Botões
    help_buttons = InlineKeyboardMarkup(row_width=1)
    help_buttons.add(
        InlineKeyboardButton('Comandos ônibus', callback_data='cb_onibus'),
        InlineKeyboardButton('Comandos bandejao', callback_data='cb_bandejao'),
        InlineKeyboardButton('Todos os comandos', callback_data='cb_tudo'),
    )

    # Envio de mensagem
    bot.send_message(mensagem.chat.id,
                     r'Entendido\! Aqui está uma lista com os comandos principais:')
    bot.send_message(mensagem.chat.id, help_text, reply_markup=help_buttons)


# --------------------- #
#        Ônibus
# --------------------- #


# Comando /onibus
@bot.message_handler(commands=["onibus"])
def onibus(mensagem):
    """Envia uma mensagem no chat listando todos os comandos relacionados com
    os ônibus da moradia.
    """

    # Botões
    onibus_buttons = InlineKeyboardMarkup(row_width=2)
    onibus_buttons.add(
        InlineKeyboardButton('Próximo ônibus',
                             callback_data="cb_o_prox"),
        InlineKeyboardButton('Todos os ônibus de IDA',
                             callback_data="cb_o_todos_ida"),
        InlineKeyboardButton('Todos os ônibus de VOLTA',
                             callback_data="cb_o_todos_volta")
    )

    # Envio de mensagem
    bot.reply_to(mensagem,
                 r'Okay\! Aqui estão os comandos para os ônibus da moradia:')
    bot.send_message(mensagem.chat.id, onibus_text,
                     reply_markup=onibus_buttons)


# Comando /oTodos
@bot.message_handler(commands=["oTodos"])
def o_todos(mensagem):
    """Envia uma foto no chat da tabela de horários dos ônibus da moradia."""

    bot.send_message(mensagem.chat.id,
                     'Aqui está a foto com todos os horários dos ônibus da moradia:')
    bot.send_photo(mensagem.chat.id, BUS_FULL_SCHEDULE_PHOTO)


# Comando /oProx
@bot.message_handler(commands=["oProx"])
def o_prox(mensagem):
    next_2_bus_text = create_next_bus_message()

    # Envio da mensagem no chat
    bot.reply_to(mensagem,
                 r"Claro\! Aqui estão os horários dos próximos ônibus da moradia:")
    bot.send_message(mensagem.chat.id, next_2_bus_text)


# Comando /oTodosIda
@bot.message_handler(commands=["oTodosIda"])
def o_todos_ida(message):

    departure_bus_schedule, _ = get_day_bus_schedule(CURRENT_WEEKDAY)
    available_bus_schedule_list_text = create_available_bus_list_message(
        departure_bus_schedule)

    # Envio de mensagem
    bot.reply_to(message,
                 r'Ta bom\! Aqui está a lista dos ônibus de Ida de hoje\!')
    bot.send_message(message.chat.id, available_bus_schedule_list_text)


# Comando /oTodosVolta
@bot.message_handler(commands=["oTodosVolta"])
def o_todos_volta(message):

    _, return_bus_schedule = get_day_bus_schedule(CURRENT_WEEKDAY)
    available_bus_schedule_list_text = create_available_bus_list_message(
        return_bus_schedule)

    # Envio de mensagem
    bot.reply_to(message,
                 r'Ta bom\! Aqui está a lista dos ônibus de Ida de hoje\!')
    bot.send_message(message.chat.id, available_bus_schedule_list_text)


# --------------------- #
#      Restaurantes
# --------------------- #


# Comando /bandejão
@bot.message_handler(commands=["bandejao"])
def bandejao(mensagem):
    """envia uma mensagem no chat listando todos os comandos relacionados com
    os restaurantes da Unicamp.
    """

    # Botões
    bandejao_buttons = InlineKeyboardMarkup(row_width=2)
    bandejao_buttons.add(
        InlineKeyboardButton('Horários de cada restaurante',
                             callback_data='cb_bHoras'),
        InlineKeyboardButton('Ver cardápio do dia',
                             callback_data='cb_bCardapio'),
        InlineKeyboardButton('Tempo para a próxima refeição',
                             callback_data='cb_bJaPode'))

    # Envio de mensagem
    bot.reply_to(mensagem, r'Certo\! Aqui estão os comandos para o bandejão:')
    bot.send_message(mensagem.chat.id, bandejao_text,
                     reply_markup=bandejao_buttons)


# Comando /bCardapio
@bot.message_handler(commands=["bCardapio"])
def b_cardapio(mensagem):
    """Envia uma mensagem no chat com as opções de cardápio (Tradicional e
    Vegano) para o usuário escolher.
    """

    # Botões
    cardapio_buttons = ReplyKeyboardMarkup(resize_keyboard=True)
    cardapio_buttons.add(KeyboardButton('/bTradicional'))
    cardapio_buttons.add(KeyboardButton('/bVegano'))

    # Envio de mensagem
    bot.reply_to(mensagem, r'Ta bom\! Qual cardápio deseja ver?')
    bot.send_message(mensagem.chat.id, cardapio_text,
                     reply_markup=cardapio_buttons)

# --------------------- #
#        Handlers
# --------------------- #


def verify(mensagem):
    """Retorna True para a chegada de toda e qualquer mensagem.
    """
    return True


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "cb_help":
        bot.answer_callback_query(help(call.message))

    elif call.data == "cb_onibus":
        bot.answer_callback_query(onibus(call.message))

    elif call.data == "cb_bandejao":
        bot.answer_callback_query(bandejao(call.message))

    elif call.data == "cb_bCardapio":
        bot.answer_callback_query(help(call.message))


@bot.message_handler(func=verify)  # Função ativada por verify()
def unknown_command(mensagem):
    """Essa função deve ser a última de todas, porque ela é ativada para
    QUALQUER mensagem.
    Ela é responsável por pegar todas as mensagens que não caíram nas funções
    anteriores.
    """

    # Botões
    help_button = ReplyKeyboardMarkup(resize_keyboard=True)
    help_button.add(KeyboardButton('/help'))

    # Envio de mensagem
    bot.reply_to(mensagem, r'Hmmm, eu não conheço esse comando\.')
    bot.send_message(mensagem.chat.id, 
                     r'Digite /help ou clique no botão abaixo para ver os comandos disponíveis\.',
                     reply_markup=help_button)


bot.polling()
