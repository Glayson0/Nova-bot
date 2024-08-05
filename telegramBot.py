"""Este arquivo é para a construção do bot para o Telegram"""

import telebot # Biblioteca pyTelegramBotAPI para acessar a API do bot do Telegram
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime
from restaurantsInfo import *
from timeUtils import *
from bus import *

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

### Comandos intermediários: apenas auxiliam o usuário a chegarem às funcionalidades do bot

## Geral

# Comando /start
@bot.message_handler(commands=["start"]) # Atribuição do comando /start à função
def start(mensagem):

    """
    Essa função
    - envia uma mensagem de introdução ao bot no chat, indicando o usuário a utilizar o comando /help.
    """

    # Texto da mensagem do bot
    startText = f"""
Eu me chamo Nova e sou um bot criado por alunos da Unicamp\!

Meu objetivo é fornecer informações dos ônibus da moradia e dos restaurantes da Unicamp de forma rápida e fácil\.

Clique no botão abaixo ou digite /help para conhecer alguns dos comandos que você pode utilizar\.
"""
    
    # Botões
    startButton = ReplyKeyboardMarkup(resize_keyboard=True)  # Criação

    startButton.add(KeyboardButton('/help'))

    # Envio de mensagem
    bot.send_message(mensagem.chat.id, f'👋 Olá, {mensagem.chat.first_name}\! Como vai?')
    bot.send_message(mensagem.chat.id, startText, reply_markup=startButton)

# Comando /help
@bot.message_handler(commands=["help"])  # Atribuição do comando /help à função
def help(mensagem):

    """
    Essa função
    - envia uma mensagem no chat com 3 comandos principais para ajudar o usuário.
    """

    # Texto da mensagem do bot
    helpText = """
\- /onibus: Ver comandos para os ônibus da moradia

\- /bandejao: Ver os comandos para o bandejao

\- /tudo: Listar todos os comandos
"""  

    # Botões
    helpButtons = ReplyKeyboardMarkup(resize_keyboard=True) # Criação

    helpButtons.add(KeyboardButton('/onibus'))
    helpButtons.add(KeyboardButton('/bandejao'))
    helpButtons.add(KeyboardButton('/tudo'))

    # Envio de mensagem
    bot.reply_to(mensagem, 'Entendido\! Aqui está uma lista com os comandos principais:')
    bot.send_message(mensagem.chat.id, helpText, reply_markup=helpButtons)

# Comando /onibus
@bot.message_handler(commands=["onibus"]) # Atribuição do comando /ônibus à função
def onibus(mensagem):

    """
    Essa função
    - envia uma mensagem no chat listando todos os comandos relacionados com os ônibus da moradia.
    """

    # Texto da mensagem do bot
    onibusText = """
\- /oProx: Ver os próximos 2 ônibus de ida e de volta

\- /oTodos: Ver foto com todos os horários de ônibus

\- /oTodosIda: Ver todos os horários de ônibus de IDA do dia \(Moradia \-\> Unicamp\)

\- /oTodosVolta: Ver todos os horários de ônibus de VOLTA dia \(Unicamp \-\> Moradia\)
"""
    # Botões
    onibusButtons = ReplyKeyboardMarkup(resize_keyboard=True) # Criação

    onibusButtons.add(KeyboardButton('/oProx'))
    onibusButtons.add(KeyboardButton('/oTodos'))
    onibusButtons.add(KeyboardButton('/oTodosIda'))
    onibusButtons.add(KeyboardButton('/oTodosVolta'))

    # Envio de mensagem
    bot.reply_to(mensagem, 'Okay\! Aqui estão os comandos para os ônibus da moradia:')
    bot.send_message(mensagem.chat.id, onibusText, reply_markup=onibusButtons)

# Comando /bandejão
@bot.message_handler(commands=["bandejao"]) # Atribuição do comando /bandejao à função
def bandejao(mensagem):

    """
    Essa função
    - envia uma mensagem no chat listando todos os comandos relacionados com os restaurantes da Unicamp.
    """

    # Texdo da mensagem do bot
    bandejaoText = """
Geral
\- /bHoras: Ver os horários dos três restaurantes

\- /bCardapio: Ver o cardápio de almoço e jantar

\- /bJaPode: Ver refeições em andamento

Restaurantes
\- /ru: Ver informações do RU

\- /rs: Ver informações do RS

\- /ra: Ver informações do RA
"""

    # Botões
    bandejaoButtons = ReplyKeyboardMarkup(resize_keyboard=True) # Criação
    bandejaoButtons.add(KeyboardButton('/bHoras'), KeyboardButton('/bCardapio'), KeyboardButton('/bJaPode'))
    bandejaoButtons.add(KeyboardButton('/ru'), KeyboardButton('/rs'), KeyboardButton('/ra'))

    # Envio de mensagem
    bot.reply_to(mensagem, 'Certo\! Aqui estão os comandos para o bandejão:')
    bot.send_message(mensagem.chat.id, bandejaoText, reply_markup=bandejaoButtons)

# Comando /bCardapio
@bot.message_handler(commands=["bCardapio"]) # Atribuição do comando /bCardapio à função
def bCardapio(mensagem):

    """
    Essa função envia uma mensagem no chat com as opções de cardápio (Tradicional e Vegano) para o usuário escolher.
    """
    
    # Texto da mensagem do bot
    cardapioText = """
\- /bTradicional: Cardápio tradicional

\- /bVegano: Cardápio vegano
"""

    # Botões
    cardapioButtons = ReplyKeyboardMarkup(resize_keyboard=True) # Criação
    cardapioButtons.add(KeyboardButton('/bTradicional'))
    cardapioButtons.add(KeyboardButton('/bVegano'))

    # Envio de mensagem
    bot.reply_to(mensagem, 'Ta bom\! Qual cardápio deseja ver?')
    bot.send_message(mensagem.chat.id, cardapioText, reply_markup=cardapioButtons)




### Comandos de funcionalidades: as funcionalidades de fato do bot

## Ônibus

# Comando /oTodos
@bot.message_handler(commands=["oTodos"])
def oTodos(mensagem):
    """Envia uma foto no chat da tabela de horários dos ônibus da moradia."""

    bot.send_message(mensagem.chat.id, 'Aqui está a foto com todos os horários dos ônibus da moradia:')
    bot.send_photo(mensagem.chat.id, BUS_FULL_SCHEDULE_PHOTO)

# Comando /oProx
@bot.message_handler(commands=["oProx"]) # Atribuição do comando /oProx à função
def oProx(mensagem):
    """
    Essa função:
    - Pega o horário dos próximos 2 ônibus de ida e volta cada com a função nextBus();
    - Calcula a diferença de tempo entre o horário atual e o próximo ônibus encontrado;
    - Envia uma mensagem com os horários dos próximos 2 ônibus de ida e volta cada e o tempo faltante.
    """

    departureBusSchedule, returnBusSchedule = getDayBusSchedule(CURRENT_WEEKDAY)

    # Obtenção dos próximo 2 horários dos ônibus
    nextDepartureBusTime1 = nextBusFromNow(departureBusSchedule)
    nextDepartureBusTime2 = nextBusFromNow(departureBusSchedule, nextDepartureBusTime1)

    nextReturnBusTime1 = nextBusFromNow(returnBusSchedule)
    nextReturnBusTime2 = nextBusFromNow(returnBusSchedule, nextReturnBusTime1)

    # Tempo restante para os horários - IDA
    if hasAvailableBus(CURRENT_DATETIME, departureBusSchedule):
        timeForNextDepartureBus1 = calculateTimeDifference(nextDepartureBusTime1, CURRENT_DATETIME)
        if hasAvailableBus(nextDepartureBusTime1, departureBusSchedule):
            timeForNextDepartureBus2 = calculateTimeDifference(nextDepartureBusTime2, CURRENT_DATETIME)
        else:
            timeForNextDepartureBus2 = None
    else:
        timeForNextDepartureBus1 = None
        timeForNextDepartureBus2 = None

    # Tempo restante para os horários - VOLTA
    if hasAvailableBus(CURRENT_DATETIME, returnBusSchedule):
        timeForNextReturnBus1 = calculateTimeDifference(nextReturnBusTime1, CURRENT_DATETIME)
        if hasAvailableBus(nextReturnBusTime1, returnBusSchedule):
            timeForNextReturnBus2 = calculateTimeDifference(nextReturnBusTime1, CURRENT_DATETIME)
        else:
            timeForNextReturnBus2 = None
    else:
        timeForNextReturnBus1 = None
        timeForNextReturnBus2 = None

    times = [
        [datetimeToStr(nextDepartureBusTime1), timeForNextDepartureBus1], 
        [datetimeToStr(nextDepartureBusTime2), timeForNextDepartureBus2], 
        [datetimeToStr(nextReturnBusTime1), timeForNextReturnBus1], 
        [datetimeToStr(nextReturnBusTime2), timeForNextReturnBus2]
    ]

    timesOutput = []
    for time in times:
        if time[0] == None:
            time = "Acabaram os ônibus por hoje\!"
        else:
            time = f"{time[0]} \({time[1]}\)"
        timesOutput.append(time)

    print(timesOutput)

    # Texto da mensagem do bot
    proxOnibus_text = f"""
Ida \(Moradia \-\> Unicamp\):
01\) {timesOutput[0]}
02\) {timesOutput[1]}

Volta \(Unicamp \-\> Moradia\):
01\) {timesOutput[2]}
02\) {timesOutput[3]}
"""
    # Envio da mensagem no chat
    bot.reply_to(mensagem, "Claro\! Aqui estão os horários dos próximos ônibus da moradia:")
    bot.send_message(mensagem.chat.id, proxOnibus_text)

# oTodosIda
@bot.message_handler(commands=["oTodosIda"]) # Atribuição do comando /oTodosIda à função
def oTodosIda(message):

    """
    Essa função envia uma mensagem no chat com uma lista de 3 colunas com
        - os horários de ônibus de Ida que já passaram tachados
        - o horário do próximo ônibus de Ida em negrito
        - os horários de ônibus de Ida que ainda não passaram
    """
    
    # Obtenção do tempo atual a partir da mensagem
    horaAtual = datetime.fromtimestamp(message.date)
    diaAtual = getCurrentDay(message)

    # Obtenção do horário do próximo ônibus
    proxOnibus = nextBusFromNow(horaAtual, diaAtual, 0)

    ### Lista com todos os horários de Ida

    pos = 0

    ## Texto da mensagem do bot
    oTodosIdaText = ""

    # Dia útil
    if diaAtual in 'Segunda Terça Quarta Quinta Sexta':

        for horario in weekdayBusDepartureSchedule:

            # Ônibus que já passaram
            if strToTime(horario) < strToTime(proxOnibus): 
                pos += 1
                if pos % 3 == 0:
                    oTodosIdaText += f'~{horario}~\n'
                else:
                    oTodosIdaText += f'~{horario}~  \|  '
            
            # Próximo ônibus
            elif strToTime(horario) == strToTime(proxOnibus):
                pos += 1
                if pos % 3 == 0:
                    oTodosIdaText += f'*{proxOnibus}*\n'
                else:
                    oTodosIdaText += f'*{proxOnibus}*  \|  '
            
            # Ônibus que ainda não passaram
            else:
                pos += 1
                if pos % 3 == 0:
                    oTodosIdaText += f'{horario}\n'
                else:
                    oTodosIdaText += f'{horario}  \|  '
    
    # Dia não-útil
    else:

        for horario in nonWorkingDayBusDepartureSchedule:

            # Ônibus que já passaram
            if strToTime(horario) < strToTime(proxOnibus): 
                pos += 1
                if pos % 3 == 0:
                    oTodosIdaText += f'~{horario}~\n'
                else:
                    oTodosIdaText += f'~{horario}~  \|  '
            
            # Próximo ônibus
            elif strToTime(horario) == strToTime(proxOnibus):
                pos += 1
                if pos % 3 == 0:
                    oTodosIdaText += f'*{proxOnibus}*\n'
                else:
                    oTodosIdaText += f'*{proxOnibus}*  \|  '
            
            # Ônibus que ainda não passaram
            else:
                pos += 1
                if pos % 3 == 0:
                    oTodosIdaText += f'{horario}\n'
                else:
                    oTodosIdaText += f'{horario}  \|  '

    # Envio de mensagem
    bot.reply_to(message, 'Ta bom\! Aqui está a lista dos ônibus de Ida de hoje\!')
    bot.send_message(message.chat.id, oTodosIdaText)

# oTodosVolta
@bot.message_handler(commands=["oTodosVolta"]) # Atribuição do comando /oTodosVolta à função
def oTodosVolta(message):

    """
    Essa função envia uma mensagem no chat com uma lista de 3 colunas com
        - os horários de ônibus de Volta que já passaram tachados
        - o horário do próximo ônibus de Volta em negrito
        - os horários de ônibus de Volta que ainda não passaram
    """
    
    # Obtenção do tempo atual a partir da mensagem
    horaAtual = datetime.fromtimestamp(message.date)
    diaAtual = getCurrentDay(message)

    # Obtenção do horário do próximo ônibus
    proxOnibus = nextBusFromNow(horaAtual, diaAtual, 0)

    ### Lista com todos os horários de Ida

    pos = 0

    ## Texto da mensagem do bot
    horariosVolta = ""

    # Dia útil
    if diaAtual in 'Segunda Terça Quarta Quinta Sexta':

        for horario in weekdayBusReturnSchedule:

            # Ônibus que já passaram
            if strToTime(horario) < strToTime(proxOnibus): 
                pos += 1
                if pos % 3 == 0:
                    horariosVolta += f'~{horario}~\n'
                else:
                    horariosVolta += f'~{horario}~  \|  '
            
            # Próximo ônibus
            elif strToTime(horario) == strToTime(proxOnibus):
                pos += 1
                if pos % 3 == 0:
                    horariosVolta += f'*{proxOnibus}*\n'
                else:
                    horariosVolta += f'*{proxOnibus}*  \|  '
            
            # Ônibus que ainda não passaram
            else:
                pos += 1
                if pos % 3 == 0:
                    horariosVolta += f'{horario}\n'
                else:
                    horariosVolta += f'{horario}  \|  '
    
    # Dia não-útil
    else:

        for horario in nonWorkingDayBusDepartureSchedule:

            # Ônibus que já passaram
            if strToTime(horario) < strToTime(proxOnibus): 
                pos += 1
                if pos % 3 == 0:
                    horariosVolta += f'~{horario}~\n'
                else:
                    horariosVolta += f'~{horario}~  \|  '
            
            # Próximo ônibus
            elif strToTime(horario) == strToTime(proxOnibus):
                pos += 1
                if pos % 3 == 0:
                    horariosVolta += f'*{proxOnibus}*\n'
                else:
                    horariosVolta += f'*{proxOnibus}*  \|  '
            
            # Ônibus que ainda não passaram
            else:
                pos += 1
                if pos % 3 == 0:
                    horariosVolta += f'{horario}\n'
                else:
                    horariosVolta += f'{horario}  \|  '

    # Envio de mensagem
    bot.reply_to(message, 'Ta bom\! Aqui está a lista dos ônibus de Ida de hoje\!')
    bot.send_message(message.chat.id, horariosVolta)

# Comando /bandejao
@bot.message_handler(commands=["bHoras"]) # Atribuição do comando /bandejao à função
def bandejao(mensagem):

    """
    Essa função:
    - Envia uma mensagem no chat com o 
    """

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

## Resposta à mensagens desconhecidas ao bot 

def verify(mensagem):
    """
    Essa função retorna True para a chegada de toda e qualquer mensagem.
    """
    return True

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
    bot.reply_to(mensagem, 'Hmmm, eu não conheço esse comando\.') 
    bot.send_message(mensagem.chat.id, 'Digite /help ou clique no botão abaixo para ver os comandos disponíveis\.', reply_markup=helpButton)

bot.polling()