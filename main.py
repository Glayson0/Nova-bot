import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime
from localidadesBandejao import *
from timeUtils import *

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
\- /oTodos: Ver foto com todos os horários de ônibus

\- /oTodosIda: Ver todos os horários de ônibus de IDA do dia \(Moradia \-\> Unicamp\)

\- /oTodosVolta: Ver todos os horários de ônibus de VOLTA dia \(Unicamp \-\> Moradia\)

\- /oProx: Ver os próximos 2 ônibus de ida e de volta
"""
    busButtons = ReplyKeyboardMarkup(resize_keyboard=True)

    busButtons.add(KeyboardButton('/oTodos'))
    busButtons.add(KeyboardButton('/oTodosIda'))
    busButtons.add(KeyboardButton('/oTodosVolta'))
    busButtons.add(KeyboardButton('/oTodosProx'))

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

@bot.message_handler(commands=["onibusProx"]) # funciona quando recebe o comando "onibus"
def onibus(mensagem):

    existeOnibusIda = existeOnibusVolta = True

    horaAtual = datetime.fromtimestamp(mensagem.date)
    diaAtual = getCurrentDay(mensagem)

    # DIA ÚTIL
    if diaAtual in 'Segunda Terça Quarta Quinta Sexta':

        # Condição para quando não tiver mais ônibus no dia
        if horaAtual > fStrToTime(diaUtil_horariosIda[-1]):
            existeOnibusIda = False

        if horaAtual > fStrToTime(diaUtil_horariosVolta[-1]):
            existeOnibusVolta = False

        # Encontrar próximos ônibus
        for horarioOnibusIda in diaUtil_horariosIda:
            if horaAtual <= fStrToTime(horarioOnibusIda):
                break
        for horarioOnibusVolta in diaUtil_horariosVolta:
            if horaAtual <= fStrToTime(horarioOnibusVolta):
                break
    
    # FIM DE SEMANA
    else:
        # Condição para quando não tiver mais ônibus de IDA no dia
        if horaAtual > fStrToTime(diaInutil_horariosIda[-1]):
            existeOnibusIda = False
        else:
            # Encontrar próximos ônibus
            for horarioOnibusIda in diaInutil_horariosIda:
                if horaAtual <= fStrToTime(horarioOnibusIda):
                    break

        # Condição para quando não tiver mais ônibus de VOLTA no dia
        if horaAtual > fStrToTime(diaInutil_horariosVolta[-1]):
            existeOnibusVolta = False
        else:
            for horarioOnibusVolta in diaInutil_horariosVolta:
                    if horaAtual <= fStrToTime(horarioOnibusVolta):
                        break

    # Calculando a diferença de tempo
    if existeOnibusIda == True:
        diffHorariosIda = getTimeDifference2(horarioOnibusIda, horaAtual)
    if existeOnibusVolta == True:
        diffHorariosVolta = getTimeDifference2(horarioOnibusVolta, horaAtual)

    # Output
    if existeOnibusIda == True:
        if diffHorariosIda.hour > 0:
            output_ProxOnibusIda = f'{horarioOnibusIda} ({diffHorariosIda.hour} hr e {diffHorariosIda.minute} min)'
        else:
            output_ProxOnibusIda = f'{horarioOnibusIda} ({diffHorariosIda.minute} min(s))'
    else:
        output_ProxOnibusIda = 'acabaram os ônibus de hoje\!'

    if existeOnibusVolta == True:
        if diffHorariosVolta.hour > 0:
            output_ProxOnibusVolta = f'{horarioOnibusVolta} ({diffHorariosVolta.hour} hr e {diffHorariosVolta.minute} min)'
        else:
            output_ProxOnibusVolta = f'{horarioOnibusVolta} ({diffHorariosVolta.minute} min(s))'
    else:
        output_ProxOnibusVolta = 'acabaram os ônibus de hoje\!'

    # Envio da mensagem no chat
    bot.send_message(mensagem.chat.id,
    f"""🚌🚌🚌 HORÁRIO ÔNIBUS 🚌🚌🚌

Dia atual: {diaAtual}
Horário atual: {fTimeToStr(horaAtual)}
    
Próximo ônibus IDA: {output_ProxOnibusIda}
Próximo ônibus VOLTA: {output_ProxOnibusVolta}"""
    )

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