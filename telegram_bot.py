"""Este arquivo é para a construção do bot para o Telegram"""

from datetime import datetime

import telebot  # Biblioteca pyTelegramBotAPI para acessar a API do bot do Telegram
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from bus import *
from bus_schedule import BUS_FULL_PHOTO
from restaurants_info import *
from texts import *
from time_utils import *

# Fazer conexão com a API do bot do Telegram
CHAVE_API = "7141300367:AAHBHEelfnAig53EVxqq0oabZrRz15CjIJ8"
bot = telebot.TeleBot(CHAVE_API, parse_mode='MarkdownV2')

"""
NOTAS:
- O parâmetro "messagem" é um objeto mensagem enviada pelo usuário;
- Todas as funções podem ser chamadas a qualquer momento no chat pelos seus respectivos comandos;
- Há uma hierarquia vertical para a chamada das funções que têm o message_handler. Ou seja, por exemplo: se houver mais de uma função 
com o mesmo trigger, apenas aquela que está mais acima será ativada.

"""






##
##  Comandos
##

# Comando /start
@bot.message_handler(commands=["start"])
def start(mensagem):

    # Botões
    startButton = InlineKeyboardMarkup(row_width=1)
    startButton.add(InlineKeyboardButton('/help', callback_data="cb_help"))

    # Envio de mensagem
    bot.send_message(mensagem.chat.id, f'👋 Olá, {mensagem.chat.first_name}\! Como vai?')
    bot.send_message(mensagem.chat.id, start_text, reply_markup=startButton)

# Comando /help
@bot.message_handler(commands=["help"])
def help(mensagem):
    """Essa função
    - envia uma mensagem no chat com 3 comandos principais para ajudar o usuário.
    """

    # Botões
    helpButtons = InlineKeyboardMarkup(row_width=1)
    helpButtons.add(
        InlineKeyboardButton('Comandos ônibus', callback_data='cb_onibus'), 
        InlineKeyboardButton('Comandos bandejao', callback_data='cb_bandejao'),
        InlineKeyboardButton('Todos os comandos', callback_data='cb_tudo'),
    )

    # Envio de mensagem
    bot.send_message(mensagem.chat.id, r'Entendido\! Aqui está uma lista com os comandos principais:')
    bot.send_message(mensagem.chat.id, help_text, reply_markup=helpButtons)

# Comando /onibus
@bot.message_handler(commands=["onibus"]) # Atribuição do comando /ônibus à função
def onibus(mensagem):
    """Essa função
    - envia uma mensagem no chat listando todos os comandos relacionados com os ônibus da moradia.
    """

    # Botões
    onibusButtons = InlineKeyboardMarkup(row_width=2)
    onibusButtons.add(
        InlineKeyboardButton('Próximo ônibus', callback_data="cb_oProx"),
        InlineKeyboardButton('Todos os ônibus de IDA', callback_data="cb_oTodosIda"),
        InlineKeyboardButton('Todos os ônibus de VOLTA', callback_data="cb_oTodosVolta")
    )

    # Envio de mensagem
    bot.reply_to(mensagem, r'Okay\! Aqui estão os comandos para os ônibus da moradia:')
    bot.send_message(mensagem.chat.id, onibus_text, reply_markup=onibusButtons)


##
##  Ônibus
##


# Comando /oTodos
@bot.message_handler(commands=["oTodos"])
def oTodos(mensagem):
    """Envia uma foto no chat da tabela de horários dos ônibus da moradia."""

    bot.send_message(mensagem.chat.id, 'Aqui está a foto com todos os horários dos ônibus da moradia:')
    bot.send_photo(mensagem.chat.id, BUS_FULL_PHOTO)

# Comando /oProx
@bot.message_handler(commands=["oProx"]) # Atribuição do comando /oProx à função
def oProx(mensagem):
    
    next_buses_text = "Horários\n" + create_next_buses_msg()
    next_buses_text = format_msg(next_buses_text, "```")

    # Envio da mensagem no chat
    bot.reply_to(mensagem, r"Claro\! Aqui estão os horários dos próximos ônibus da moradia:")
    bot.send_message(mensagem.chat.id, next_buses_text)

## Resposta à mensagens desconhecidas ao bot 

def verify(mensagem):
    """
    Essa função retorna True para a chegada de toda e qualquer mensagem.
    """
    return True

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "cb_help":
        bot.answer_callback_query(help(call.message))

    elif call.data == "cb_onibus":
        bot.answer_callback_query(onibus(call.message))


@bot.message_handler(func=verify) # Essa função é ativada sempre que receber True da função verify()
def unknownCommand(mensagem):
    """
    Essa função deve ser a última de todas, porque ela é ativada para QUALQUER mensagem.
    Ela é responsável por pegar todas as mensagens que não caíram nas funções anteriores.
    """

    # Botões
    helpButton = ReplyKeyboardMarkup(resize_keyboard=True) # Criação
    helpButton.add(KeyboardButton('/help'))

    # Envio de mensagem
    bot.reply_to(mensagem, r'Hmmm, eu não conheço esse comando\.') 
    bot.send_message(mensagem.chat.id, r'Digite /help ou clique no botão abaixo para ver os comandos disponíveis\.', reply_markup=helpButton)

bot.polling()