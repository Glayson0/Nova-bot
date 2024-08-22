"""Este arquivo é para a construção do bot para o Telegram"""

import logging

import telebot  # Biblioteca pyTelegramBotAPI para acessar a API do bot do Telegram
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from bus import create_next_buses_msg
from bus_schedule import BUS_FULL_PHOTO
from restaurants_info import *
from texts import *
from time_utils import *

# Logging configuration
logging.basicConfig(level=logging.INFO)

# Make connection with bot's API
API_TOKEN = "7141300367:AAHBHEelfnAig53EVxqq0oabZrRz15CjIJ8"
bot = telebot.TeleBot(API_TOKEN, parse_mode='MarkdownV2')

# Constants
WELCOME_MESSAGE = '*👋 Olá, {first_name}\! Como vai?\nSeja bem\-vindo\!\n*{start_text}'
HELP_MESSAGE = escape_msg('Entendido! Aqui está uma lista com os comandos principais:')
ONIBUS_MESSAGE = escape_msg('Okay! Aqui estão os comandos para os ônibus da moradia:')
UNKNOWN_COMMAND_MESSAGE = escape_msg('Hmmm, eu não conheço esse comando.')
HELP_PROMPT_MESSAGE = escape_msg('Digite /help ou clique no botão abaixo para ver os comandos disponíveis.')
ERROR_MESSAGE = escape_msg('Ocorreu um erro ao processar sua solicitação. Tente novamente mais tarde.')


# --------------------- #
#        Commands
# --------------------- #

# /start
@bot.message_handler(commands=["start"])
def start_menu(mensagem: Message) -> None:
    try:
        # Buttons
        start_button = InlineKeyboardMarkup(row_width=1)
        start_button.add(InlineKeyboardButton('Help', callback_data="cb_help"))

        # Send message
        welcome_message = WELCOME_MESSAGE.format(first_name=mensagem.chat.first_name, start_text=start_text)
        bot.send_message(mensagem.chat.id, welcome_message, reply_markup=start_button)
    except Exception as e:
        logging.error(f"Error in start command: {e}")


# /help
@bot.message_handler(commands=["help"])
def help_menu(mensagem: Message) -> None:
    """Essa função envia uma mensagem no chat com 3 comandos principais para ajudar o usuário.
    """

    try:
        # Buttons
        help_buttons = InlineKeyboardMarkup(row_width=1)
        help_buttons.add(
            InlineKeyboardButton('Comandos ônibus', callback_data='cb_onibus'), 
            # InlineKeyboardButton('Comandos bandejao', callback_data='cb_bandejao'),
            InlineKeyboardButton('Todos os comandos', callback_data='cb_tudo'),
        )

        # Send message
        bot.send_message(mensagem.chat.id, HELP_MESSAGE)
        bot.send_message(mensagem.chat.id, help_text, reply_markup=help_buttons)
    except Exception as e:
        logging.error(f"Error in help command: {e}")


# --------------------- #
#          Bus
# --------------------- #

# /onibus
@bot.message_handler(commands=["onibus"])
def onibus(mensagem: Message) -> None:
    """Essa função envia uma mensagem no chat listando todos os comandos relacionados com os ônibus da moradia.
    """

    try:
        # Buttons
        onibus_buttons = InlineKeyboardMarkup(row_width=2)
        onibus_buttons.add(
            InlineKeyboardButton('Próximo ônibus', callback_data="cb_oProx"),
            InlineKeyboardButton('Todos os ônibus do dia', callback_data="cb_oTodos"),
            InlineKeyboardButton('Foto oficial dos horários', callback_data="cb_oFoto")
        )

        # Send message
        bot.reply_to(mensagem, ONIBUS_MESSAGE)
        bot.send_message(mensagem.chat.id, onibus_text, reply_markup=onibus_buttons)
    except Exception as e:
        logging.error(f"Error in onibus command: {e}")


# /oProx
@bot.message_handler(commands=["oProx"])
def oProx(mensagem: Message) -> None:
    """Envia uma tabela de IDA e VOLTA no chat com os N números de ônibus fornecidos.
    Default: 3
    """
    # Get the num of buses
    try:
        _, num_buses = mensagem.text.split()
        num_buses = int(num_buses)
    except ValueError:
        num_buses = 3
        
    try:
        # Create message
        next_buses_text = "Horários\n" + create_next_buses_msg(n_buses=num_buses)
        next_buses_text = format_msg(next_buses_text, "```")

        # Send message
        bot.reply_to(mensagem, r"Claro\! Aqui estão os horários dos próximos ônibus da moradia:")
        bot.send_message(mensagem.chat.id, next_buses_text)
    except Exception as e:
        logging.error(f"Error in oProx command: {e}")


# /oFoto
@bot.message_handler(commands=["oFoto"])
def oFoto(mensagem: Message) -> None:
    """Envia uma foto no chat da tabela de horários dos ônibus da moradia.
    """

    # Send message
    try:
        bot.send_message(mensagem.chat.id, 'Aqui está a foto oficial de todos os horários dos ônibus da moradia:')
        bot.send_photo(mensagem.chat.id, BUS_FULL_PHOTO)
    except Exception as e:
        logging.error(f"Error in oTodos command: {e}")


# Comando /oTodos
@bot.message_handler(commands=["oTodos"])
def oTodos(mensagem: Message) -> None:
    """Envia uma foto no chat da tabela de horários dos ônibus da moradia.
    """
    try:
        # Create message
        MAX_BUSES = 72
        all_buses_text = "Horários\n" + create_next_buses_msg(time='00:00', n_buses=MAX_BUSES)
        all_buses_text = format_msg(all_buses_text, "```")

        # Send message
        bot.reply_to(mensagem, r"Claro\! Aqui estão os horários de todos os ônibus do dia de hoje da moradia:")
        bot.send_message(mensagem.chat.id, all_buses_text)
    except Exception as e:
        logging.error(f"Error in oProx command: {e}")


# --------------------- #
#        Callback
# --------------------- #

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call) -> None:
    try:
        ##  Others

        if call.data == "cb_help":
            bot.answer_callback_query(help_menu(call.message))

        ##   Bus

        elif call.data == "cb_onibus":
            bot.answer_callback_query(onibus(call.message))

        elif call.data == "cb_oProx":
            bot.answer_callback_query(oProx(call.message))

        elif call.data == "cb_oFoto":
            bot.answer_callback_query(oFoto(call.message))

        elif call.data == "cb_oTodos":
            bot.answer_callback_query(oTodos(call.message))

        ##   Bandejão

        ##   Restaurants

    except Exception as e:
        logging.error(f"Error in callback query: {e}")


def verify(mensagem: Message) -> bool:
    """Essa função retorna True para a chegada de toda e qualquer mensagem.
    """
    return True


@bot.message_handler(func=verify)
def handle_unknown_message(mensagem: Message) -> None:
    """Essa função deve ser a última de todas, porque ela é ativada para QUALQUER mensagem.
    Ela é responsável por pegar todas as mensagens que não caíram nas funções anteriores.
    """

    try:
        # Buttons
        help_button = InlineKeyboardMarkup(row_width=1)
        help_button.add(InlineKeyboardButton('/help', callback_data="cb_help"))

        # Envio de mensagem
        bot.reply_to(mensagem, UNKNOWN_COMMAND_MESSAGE)
        bot.send_message(mensagem.chat.id, HELP_PROMPT_MESSAGE, reply_markup=help_button)
    except Exception as e:
        logging.error(f"Error in unknownCommand: {e}")

bot.polling()