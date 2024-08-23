"""Este arquivo é para a construção do bot para o Telegram
"""

import logging

import telebot  # Biblioteca pyTelegramBotAPI
from telebot.types import Message

from data.bus_schedule import BUS_FULL_PHOTO
from telegram.telegram_msg import *

# Logging configuration
logging.basicConfig(level=logging.INFO)

# Make connection with bot's API
API_TOKEN = "7141300367:AAHBHEelfnAig53EVxqq0oabZrRz15CjIJ8"
bot = telebot.TeleBot(API_TOKEN, parse_mode="MarkdownV2")


# --------------------- #
#  Auxiliary functions
# --------------------- #

def send_message(message: Message, text: str, reply_markup_=None):
    try:
        bot.send_message(message.chat.id, text, reply_markup=reply_markup_)
    except Exception as e:
        logging.error(f"Error sending message: {e}")


def send_photo(message: Message, photo, reply_markup_=None):
    try:
        bot.send_photo(message.chat.id, photo, reply_markup=reply_markup_)
    except Exception as e:
        logging.error(f"Error sending photo: {e}")


def edit_message(chat_id, message_id,  text_: str, reply_markup_=None):
    bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text_,
        reply_markup=reply_markup_
    )

# --------------------- #
#        Commands
# --------------------- #


# /start
@bot.message_handler(commands=["start"])
def start_menu(message: Message) -> None:
    """
        Essa função envia uma mensagem de boas vindas no chat, com a sugestão
        do comando /help.
    """
    try:
        send_message(message, start_message.short_text.format(first_name=message.chat.first_name))
        send_message(message, start_message.text, start_message.inline_markup)
    except Exception as e:
        logging.error(f"Error in start_menu command: {e}")


# /home
@bot.message_handler(commands=["home"])
def home(message: Message) -> None:
    """
    Essa função envia uma mensagem no chat com 3 comandos principais para
    ajudar o usuário.
    """
    try:
        send_message(message, home_message.short_text, False)
        send_message(message, home_message.text, home_message.inline_markup)
    except Exception as e:
        logging.error(f"Error in home command: {e}")


# /tudo
@bot.message_handler(commands=["tudo"])
def todos_comandos(message: Message) -> None:
    """
        Envia uma mensagem com todos os comandos disponíveis.
    """
    try:
        send_message(message, ALL_COMMANDS_TEXT, start_message.inline_markup)
    except Exception as e:
        logging.error(f"Error in todos_comandos command: {e}")


# --------------------- #
#         Ônibus
# --------------------- #

# /onibus
@bot.message_handler(commands=["onibus"])
def onibus(message: Message) -> None:
    """
        Essa função envia uma mensagem no chat listando todos os comandos
        relacionados com os ônibus da moradia.
    """
    try:
        send_message(message, onibus_message.short_text)
        send_message(message, onibus_message.text, onibus_message.inline_markup)
    except Exception as e:
        logging.error(f"Error in onibus command: {e}")


# /oProx
@bot.message_handler(commands=["oProx"])
def oProx(message: Message) -> None:
    """
        Envia uma tabela de IDA e VOLTA no chat com os N números de ônibus
        fornecidos. Default: 3
    """
    try:
        _, num_buses = message.text.split()
        num_buses = int(num_buses)
    except ValueError:
        num_buses = 3

    try:
        next_buses_text = "Horários\n" + create_next_buses_msg(n_buses=num_buses)
        next_buses_text = format_msg(next_buses_text, "```")
        send_message(
            message,
            escape_msg(f"Okay! Aqui estão os horários dos próximos {num_buses} ônibus da moradia:")
        )
        send_message(message, next_buses_text, start_message.reply_markup)
    except Exception as e:
        logging.error(f"Error in oProx command: {e}")


# /oFoto
@bot.message_handler(commands=["oFoto"])
def oFoto(message: Message) -> None:
    """Envia uma foto no chat da tabela de horários dos ônibus da moradia."""
    try:
        send_message(
            message,
            "Aqui está a foto oficial de todos os horários dos ônibus da moradia:"
        )
        send_photo(message, BUS_FULL_PHOTO, start_message.reply_markup)
    except Exception as e:
        logging.error(f"Error in oFoto command: {e}")


# /oTodos
@bot.message_handler(commands=["oTodos"])
def oTodos(message: Message) -> None:
    """Envia uma tabela de ida e volta no chat do dia atual.
    """
    try:
        MAX_BUSES = 72
        all_buses_text = "Horários\n" + create_next_buses_msg(time="00:00", n_buses=MAX_BUSES)
        all_buses_text = format_msg(all_buses_text, "```")
        send_message(message, escape_msg("Okay! Aqui estão os horários de todos os ônibus do dia de hoje da moradia:"))
        send_message(message, all_buses_text, start_message.reply_markup)
    except Exception as e:
        logging.error(f"Error in oTodos command: {e}")


# --------------------- #
#        Bandejão
# --------------------- #

# /bandejao
@bot.message_handler(commands=["bandejao"])
def bandejao(message: Message) -> None:
    """Essa função envia uma mensagem no chat listando todos os comandos
    relacionados ao bandejao.
    """
    try:
        send_message(message, bandejao_message.short_text)
        send_message(message, bandejao_message.text, bandejao_message.inline_markup)
    except Exception as e:
        logging.error(f"Error in bandejao command: {e}")



@bot.message_handler(commands=["bCardapio"])
def bCardapio(message: Message, menu_number_: int = None) -> None:
    """Envia o menu solicitado. 0 == todos, 1 == tradicional, 2 == vegano.
    Default: 0
    """
    if not menu_number_:
        try:
            _, food_menu_number = message.text.split()
            food_menu_number = int(food_menu_number)
        except ValueError:
            food_menu_number = 0
    else:
        food_menu_number = menu_number_

    try:
        food_menu_text = escape_msg(create_menu_msg(menu_number=food_menu_number))
        send_message(message, escape_msg("Okay! Aqui está o menu solicitado de hoje:"))
        send_message(message, food_menu_text, start_message.reply_markup)
    except Exception as e:
        logging.error(f"Error in bCardapio command: {e}")


# --------------------- #
#        Callback
# --------------------- #

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call) -> None:
    try:
        chat_id = call.message.chat.id
        message_id = call.message.message_id

        # Geral

        if call.data == "cb_home":
            edit_message(chat_id, message_id, home_message.text, home_message.inline_markup)

        # Ônibus

        elif call.data == "cb_onibus":
            edit_message(chat_id, message_id, onibus_message.text, onibus_message.inline_markup)

        elif call.data == "cb_oProx":
            bot.answer_callback_query(call.id)
            oProx(call.message)

        elif call.data == "cb_oFoto":
            bot.answer_callback_query(call.id)
            oFoto(call.message)

        elif call.data == "cb_oTodos":
            bot.answer_callback_query(call.id)
            oTodos(call.message)

        # Bandejão

        elif call.data == "cb_bandejao":
            edit_message(chat_id, message_id, bandejao_message.text, bandejao_message.inline_markup)

        elif call.data == "cb_bCardapio0":
            bot.answer_callback_query(call.id)
            bCardapio(call.message)

        elif call.data == "cb_bCardapio1":
            bot.answer_callback_query(call.id)
            bCardapio(call.message, 1)

        elif call.data == "cb_bCardapio2":
            bot.answer_callback_query(call.id)
            bCardapio(call.message, 2)

        # Outros

        elif call.data == "cb_tudo":
            bot.answer_callback_query(call.id)
            todos_comandos(call.message)

    except telebot.apihelper.ApiException as api_error:
        if "query is too old" in str(api_error):
            logging.error("Error in callback query: The query is too old and the response timeout expired.")
        elif "query ID is invalid" in str(api_error):
            logging.error("Error in callback query: The query ID is invalid.")
        else:
            logging.error(f"Error in callback query: {api_error}")
    except Exception as e:
        logging.error(f"Unexpected error in callback query: {e}")


def verify(message: Message) -> bool:
    """Essa função retorna True para a chegada de toda e qualquer mensagem.
    """
    return True


@bot.message_handler(func=verify)
def handle_unknown_message(message: Message) -> None:
    """Essa função deve ser a última de todas, porque ela é ativada para
    QUALQUER mensagem. Ela é responsável por pegar todas as mensagens que não
    caíram nas funções anteriores.
    """
    try:
        bot.reply_to(message, unknown_message.short_text)
        send_message(message, unknown_message.text, unknown_message.inline_markup)
    except Exception as e:
        logging.error(f"Error in handle_unknown_message command: {e}")

if __name__ == "__main__":
    bot.polling()
