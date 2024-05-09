import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime
from localidadesBandejao import *
from timeUtils import *
from bus import *

# Inicialização do bot
## add access link to the bot here: [https://t.me/unicampus_bot]
CHAVE_API = "7141300367:AAHBHEelfnAig53EVxqq0oabZrRz15CjIJ8"
bot = telebot.TeleBot(CHAVE_API, parse_mode='MarkdownV2')

@bot.message_handler(commands=["start"])
def start(message):

    startMessage = f"""
Eu me chamo Nova e sou um bot criado por alunos da Unicamp\!

Meu objetivo é fornecer informações dos ônibus da moradia e dos restaurantes da Unicamp de forma rápida e fácil\.

Clique no botão abaixo ou digite /help para conhecer alguns dos comandos que você pode utilizar\.
"""

    startButton = ReplyKeyboardMarkup(resize_keyboard=True)
    startButton.add(KeyboardButton('/help'))

    bot.send_message(message.chat.id, f'👋 Olá, {message.chat.first_name}\! Como vai?')
    bot.send_message(message.chat.id, startMessage, reply_markup=startButton)

# Help section
@bot.message_handler(commands=["help"])
def help(message):

    menuDescription = """
\- /onibus: Ver comandos para os ônibus da moradia

\- /bandejao: Ver os comandos para o bandejao

\- /tudo: Listar todos os comandos
"""  

    menuButtons = ReplyKeyboardMarkup(resize_keyboard=True)
    menuButtons.add(KeyboardButton('/onibus'))
    menuButtons.add(KeyboardButton('/bandejao'))
    menuButtons.add(KeyboardButton('/tudo'))

    bot.reply_to(message, 'Entendido\! Aqui está uma lista com os comandos principais:')


    bot.send_message(message.chat.id, menuDescription, reply_markup=menuButtons)

# Onibus
@bot.message_handler(commands=["onibus"])
def onibus(message):
    onibusDescription = """
\- /oProx: Ver os próximos 2 ônibus de ida e de volta

\- /oTodos: Ver foto com todos os horários de ônibus

\- /oTodosIda: Ver todos os horários de ônibus de IDA do dia \(Moradia \-\> Unicamp\)

\- /oTodosVolta: Ver todos os horários de ônibus de VOLTA dia \(Unicamp \-\> Moradia\)
"""
    busButtons = ReplyKeyboardMarkup(resize_keyboard=True)

    busButtons.add(KeyboardButton('/oProx'))
    busButtons.add(KeyboardButton('/oTodos'))
    busButtons.add(KeyboardButton('/oTodosIda'))
    busButtons.add(KeyboardButton('/oTodosVolta'))

    bot.reply_to(message, 'Okay\! Aqui estão os comandos para os ônibus da moradia:')
    bot.send_message(message.chat.id, onibusDescription, reply_markup=busButtons)

# Bandejao
@bot.message_handler(commands=["bandejao"])
def bandejao(message):
    bandejaoDescription = """
Geral
\- /bHoras: Ver os horários dos três restaurantes

\- /bCardapio: Ver o cardápio de almoço e jantar

\- /bJaPode: Ver refeições em andamento

Restaurantes
\- /ru: Ver informações do RU

\- /rs: Ver informações do RS

\- /ra: Ver informações do RA
"""

    bandejaoButtons = ReplyKeyboardMarkup(resize_keyboard=True)
    bandejaoButtons.add(KeyboardButton('/bHoras'), KeyboardButton('/bCardapio'), KeyboardButton('/bJaPode'))
    bandejaoButtons.add(KeyboardButton('/ru'), KeyboardButton('/rs'), KeyboardButton('/ra'))

    bot.reply_to(message, 'Certo\! Aqui estão os comandos para o bandejão:')
    bot.send_message(message.chat.id, bandejaoDescription, reply_markup=bandejaoButtons)

# Cardapio
@bot.message_handler(commands=["bCardapio"])
def bCardapio(message):
    dietMenuDescription = """
\- /bTradicional: Cardápio tradicional

\- /bVegano: Cardápio vegano
"""

    dietButtons = ReplyKeyboardMarkup(resize_keyboard=True)
    dietButtons.add(KeyboardButton('/bTradicional'))
    dietButtons.add(KeyboardButton('/bVegano'))

    bot.reply_to(message, 'Ta bom\! Qual cardápio deseja ver?')
    bot.send_message(message.chat.id, dietMenuDescription, reply_markup=dietButtons)





#### Funcionalidades



## Ônibus

# oTodos
@bot.message_handler(commands=["oTodos"])
def oTodos(mensagem):
    bot.send_message(mensagem.chat.id, 'Aqui está a foto com todos os horários dos ônibus da moradia:')
    bot.send_photo(mensagem.chat.id, 'https://i.pinimg.com/736x/8f/72/57/8f7257a0d878b4ce78543183ace8acf1.jpg')

# oProx
@bot.message_handler(commands=["oProx"])
def oProx(message):

    horaAtual = datetime.fromtimestamp(message.date)
    diaAtual = getCurrentDay(message)

    horarioOnibusIda1, horarioOnibusVolta1 = nextBus(horaAtual, diaAtual)

    horarioOnibusIda2, horarioOnibusVolta2 = nextBusFromBus(horarioOnibusIda1, horarioOnibusVolta1, diaAtual)


    ## Diferença de tempo

    # Ida
    if horarioOnibusIda1 != None:
        diffHorariosIda1 = getTimeDifference2(horarioOnibusIda1, horaAtual)
    else:
        diffHorariosIda1 = None

    if horarioOnibusIda2 != None:
        diffHorariosIda2 = getTimeDifference2(horarioOnibusIda2, horaAtual)
    else:
        diffHorariosIda2 = None
    
    # Volta
    if horarioOnibusVolta1 != None:
        diffHorariosVolta1 = getTimeDifference2(horarioOnibusVolta1, horaAtual)
    else:
        diffHorariosVolta1 = None

    if horarioOnibusVolta2 != None:
        diffHorariosVolta2 = getTimeDifference2(horarioOnibusVolta2, horaAtual)
    else:
        diffHorariosVolta2 = None

    ## Output
    # Ida
    tempo_ProxOnibusIda1 = formatingBusDiffTime(horarioOnibusIda1, diffHorariosIda1)
    tempo_ProxOnibusIda2 = formatingBusDiffTime(horarioOnibusIda2, diffHorariosIda2)
    
    # Volta
    tempo_ProxOnibusVolta1 = formatingBusDiffTime(horarioOnibusVolta1, diffHorariosVolta1)
    tempo_ProxOnibusVolta2 = formatingBusDiffTime(horarioOnibusVolta2, diffHorariosVolta2)

    # Mensagem onibus Ida
    if horarioOnibusIda1 == None:
        output_ProxOnibusIda1 = f"""Acabaram os ônibus por hoje"""
    else:
        output_ProxOnibusIda1 = f"""{horarioOnibusIda1} \({tempo_ProxOnibusIda1}\)"""

    if horarioOnibusIda2 == None:
        output_ProxOnibusIda2 = f"""Acabaram os ônibus por hoje"""
    else:
        output_ProxOnibusIda2 = f"""{horarioOnibusIda2} \({tempo_ProxOnibusIda2}\)"""
        
    # Mensagem onibus Volta
    if horarioOnibusVolta1 == None:
        output_ProxOnibusVolta1 = f"""Acabaram os ônibus por hoje"""
    else:
        output_ProxOnibusVolta1 = f"""{horarioOnibusVolta1} \({tempo_ProxOnibusVolta1}\)"""

    if horarioOnibusVolta2 == None:
        output_ProxOnibusVolta2 = f"""Acabaram os ônibus por hoje"""
    else:
        output_ProxOnibusVolta2 = f"""{horarioOnibusVolta2} \({tempo_ProxOnibusVolta2}\)"""

    proxOnibus = f"""
Ida \(Moradia \-\> Unicamp\):
01\) {output_ProxOnibusIda1}
02\) {output_ProxOnibusIda2}

Volta \(Unicamp \-\> Moradia\):
01\) {output_ProxOnibusVolta1}
02\) {output_ProxOnibusVolta2}
"""
    # Envio da mensagem no chat
    bot.reply_to(message, "Claro\! Aqui estão os horários dos próximos ônibus da moradia:")
    bot.send_message(message.chat.id, proxOnibus)

# oTodosIda
@bot.message_handler(commands=["oTodosIda"])
def oTodosIda(message):
    
    horaAtual = datetime.fromtimestamp(message.date)
    diaAtual = getCurrentDay(message)

    proxOnibus = nextBus(horaAtual, diaAtual, 0)

    # Lista com todos os horários de Ida

    pos = 0

    horariosIda = ""

    if diaAtual in 'Segunda Terça Quarta Quinta Sexta':

        for horario in diaUtil_horariosIda:

            if fStrToTime(horario) < fStrToTime(proxOnibus):
                pos += 1
                horariosIda += f'{pos}\) ~{horario}~\n'
            
            elif fStrToTime(horario) == fStrToTime(proxOnibus):
                pos += 1
                horariosIda += f'{pos}\) *{proxOnibus}*\n'
            
            else:
                pos += 1
                horariosIda += f'{pos}\) {horario}\n'
    
    else:

        for horario in diaInutil_horariosIda:

            if fStrToTime(horario) < fStrToTime(proxOnibus):
                pos += 1
                horariosIda += f'~{pos}\) {horario}~\n'
            
            elif fStrToTime(horario) == fStrToTime(proxOnibus):
                pos += 1
                horariosIda += f'{pos}\) *{proxOnibus}*\n'
            
            else:
                pos += 1
                horariosIda += f'{pos}\) {horario}\n'

    bot.reply_to(message, 'Ta bom\! Aqui está a lista dos ônibus de Ida de hoje\!')
    bot.send_message(message.chat.id, horariosIda)

########### Resposta à opção "/bandejao"
@bot.message_handler(commands=["bandejao"]) # funciona quando recebe o comando "bandejao"
def bandejao(mensagem):

    # Horario atual (inteiro e formatado)
    horaAtual = int(datetime.fromtimestamp(mensagem.date).strftime('%H%M'))
    horaAtual_formated = datetime.fromtimestamp(mensagem.date).strftime('%H:%M')

    diaAtual = getCurrentDay(mensagem)

    horaAtual_time = datetime.strptime(horaAtual_formated, '%H:%M')

    # Envio da mensagem no chat
    bot.send_message(mensagem.chat.id,
f"""🍽️🥛🍎 HORÁRIOS DE REFEIÇÃO 🍽️🥛🍎

Dia atual: {diaAtual}
Horário atual: {horaAtual_formated}
{printLocalidades(diaAtual, horaAtual, horaAtual_time)}    
""")


def verify(mensagem): # Checa a chegada de uma mensagem qualquer
    return True

"""
Essa função deve ser a última de todas, porque ela é ativada para QUALQUER mensagem enviada que não tenha caído das funções acima.
"""

# Caso o usuário envie um comando desconhecido
@bot.message_handler(func=verify)
def unknownCommand(message):

    helpButton = ReplyKeyboardMarkup(resize_keyboard=True)
    helpButton.add(KeyboardButton('/help'))

    bot.reply_to(message, 'Hmmm, eu não conheço esse comando\.') 
    bot.send_message(message.chat.id, 'Digite /help ou clique no botão abaixo para ver os comandos disponíveis\.', reply_markup=helpButton)

bot.polling() # Vai checar a mensagem recebida pelo bot