import telebot # Biblioteca pyTelegramBotAPI para acessar a API do bot do Telegram
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime
from localidadesBandejao import *
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
    startMessage = f"""
Eu me chamo Nova e sou um bot criado por alunos da Unicamp\!

Meu objetivo é fornecer informações dos ônibus da moradia e dos restaurantes da Unicamp de forma rápida e fácil\.

Clique no botão abaixo ou digite /help para conhecer alguns dos comandos que você pode utilizar\.
"""
    
    # Botões
    startButton = ReplyKeyboardMarkup(resize_keyboard=True)  # Criação

    startButton.add(KeyboardButton('/help'))

    # Envio de mensagem
    bot.send_message(mensagem.chat.id, f'👋 Olá, {mensagem.chat.first_name}\! Como vai?')
    bot.send_message(mensagem.chat.id, startMessage, reply_markup=startButton)

# Comando /help
@bot.message_handler(commands=["help"])  # Atribuição do comando /help à função
def help(mensagem):

    """
    Essa função
    - envia uma mensagem no chat com 3 comandos principais para ajudar o usuário.
    """

    # Texto da mensagem do bot
    menuDescription = """
\- /onibus: Ver comandos para os ônibus da moradia

\- /bandejao: Ver os comandos para o bandejao

\- /tudo: Listar todos os comandos
"""  

    # Botões
    menuButtons = ReplyKeyboardMarkup(resize_keyboard=True) # Criação

    menuButtons.add(KeyboardButton('/onibus'))
    menuButtons.add(KeyboardButton('/bandejao'))
    menuButtons.add(KeyboardButton('/tudo'))

    # Envio de mensagem
    bot.reply_to(mensagem, 'Entendido\! Aqui está uma lista com os comandos principais:')
    bot.send_message(mensagem.chat.id, menuDescription, reply_markup=menuButtons)

# Comando /onibus
@bot.message_handler(commands=["onibus"]) # Atribuição do comando /ônibus à função
def onibus(mensagem):

    """
    Essa função
    - envia uma mensagem no chat listando todos os comandos relacionados com os ônibus da moradia.
    """

    # Texto da mensagem do bot
    onibusDescription = """
\- /oProx: Ver os próximos 2 ônibus de ida e de volta

\- /oTodos: Ver foto com todos os horários de ônibus

\- /oTodosIda: Ver todos os horários de ônibus de IDA do dia \(Moradia \-\> Unicamp\)

\- /oTodosVolta: Ver todos os horários de ônibus de VOLTA dia \(Unicamp \-\> Moradia\)
"""
    # Botões
    busButtons = ReplyKeyboardMarkup(resize_keyboard=True) # Criação

    busButtons.add(KeyboardButton('/oProx'))
    busButtons.add(KeyboardButton('/oTodos'))
    busButtons.add(KeyboardButton('/oTodosIda'))
    busButtons.add(KeyboardButton('/oTodosVolta'))

    # Envio de mensagem
    bot.reply_to(mensagem, 'Okay\! Aqui estão os comandos para os ônibus da moradia:')
    bot.send_message(mensagem.chat.id, onibusDescription, reply_markup=busButtons)

# Comando /bandejão
@bot.message_handler(commands=["bandejao"]) # Atribuição do comando /bandejao à função
def bandejao(mensagem):

    """
    Essa função
    - envia uma mensagem no chat listando todos os comandos relacionados com os restaurantes da Unicamp.
    """

    # Texdo da mensagem do bot
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

    # Botões
    bandejaoButtons = ReplyKeyboardMarkup(resize_keyboard=True) # Criação
    bandejaoButtons.add(KeyboardButton('/bHoras'), KeyboardButton('/bCardapio'), KeyboardButton('/bJaPode'))
    bandejaoButtons.add(KeyboardButton('/ru'), KeyboardButton('/rs'), KeyboardButton('/ra'))

    # Envio de mensagem
    bot.reply_to(mensagem, 'Certo\! Aqui estão os comandos para o bandejão:')
    bot.send_message(mensagem.chat.id, bandejaoDescription, reply_markup=bandejaoButtons)

# Comando /bCardapio
@bot.message_handler(commands=["bCardapio"]) # Atribuição do comando /bCardapio à função
def bCardapio(mensagem):

    """
    Essa função envia uma mensagem no chat com as opções de cardápio (Tradicional e Vegano) para o usuário escolher.
    """
    
    # Texto da mensagem do bot
    dietMenuDescription = """
\- /bTradicional: Cardápio tradicional

\- /bVegano: Cardápio vegano
"""

    # Botões
    dietButtons = ReplyKeyboardMarkup(resize_keyboard=True) # Criação
    dietButtons.add(KeyboardButton('/bTradicional'))
    dietButtons.add(KeyboardButton('/bVegano'))

    # Envio de mensagem
    bot.reply_to(mensagem, 'Ta bom\! Qual cardápio deseja ver?')
    bot.send_message(mensagem.chat.id, dietMenuDescription, reply_markup=dietButtons)




### Comandos de funcionalidades: as funcionalidades de fato do bot

## Ônibus

# Comando /oTodos
@bot.message_handler(commands=["oTodos"]) # Atribuição do comando /oTodos à função
def oTodos(mensagem):

    """
    Essa função envia uma foto no chat da tabela de horários dos ônibus da moradia
    """

    tabelaHorariosOnibus = 'https://i.pinimg.com/736x/8f/72/57/8f7257a0d878b4ce78543183ace8acf1.jpg' # URL da foto em um perfil do Pinterest

    # Envio de mensagem
    bot.send_message(mensagem.chat.id, 'Aqui está a foto com todos os horários dos ônibus da moradia:')
    bot.send_photo(mensagem.chat.id, tabelaHorariosOnibus)

# Comando /oProx
@bot.message_handler(commands=["oProx"]) # Atribuição do comando /oProx à função
def oProx(mensagem):
    """
    Essa função:
    - Pega o horário dos próximos 2 ônibus de ida e volta cada com a função nextBus();
    - Calcula a diferença de tempo entre o horário atual e o próximo ônibus encontrado;
    - Envia uma mensagem com os horários dos próximos 2 ônibus de ida e volta cada e o tempo faltante.
    """

    # Obtenção do tempo atual a partir da mensagem
    horaAtual = datetime.fromtimestamp(mensagem.date)
    diaAtual = getCurrentDay(mensagem)

    # Obtenção dos horários dos ônibus
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

    ## Texto de tempo faltante para cada ônibus
        # Ida
    tempo_ProxOnibusIda1 = formatingBusDiffTime(horarioOnibusIda1, diffHorariosIda1)
    tempo_ProxOnibusIda2 = formatingBusDiffTime(horarioOnibusIda2, diffHorariosIda2)
        # Volta
    tempo_ProxOnibusVolta1 = formatingBusDiffTime(horarioOnibusVolta1, diffHorariosVolta1)
    tempo_ProxOnibusVolta2 = formatingBusDiffTime(horarioOnibusVolta2, diffHorariosVolta2)

    ##  Texto do horário de cada ônibus
        # Ida
    if horarioOnibusIda1 == None:
        output_ProxOnibusIda1 = f"""Acabaram os ônibus por hoje"""
    else:
        output_ProxOnibusIda1 = f"""{horarioOnibusIda1} \({tempo_ProxOnibusIda1}\)"""

    if horarioOnibusIda2 == None:
        output_ProxOnibusIda2 = f"""Acabaram os ônibus por hoje"""
    else:
        output_ProxOnibusIda2 = f"""{horarioOnibusIda2} \({tempo_ProxOnibusIda2}\)"""
        # Volta
    if horarioOnibusVolta1 == None:
        output_ProxOnibusVolta1 = f"""Acabaram os ônibus por hoje"""
    else:
        output_ProxOnibusVolta1 = f"""{horarioOnibusVolta1} \({tempo_ProxOnibusVolta1}\)"""

    if horarioOnibusVolta2 == None:
        output_ProxOnibusVolta2 = f"""Acabaram os ônibus por hoje"""
    else:
        output_ProxOnibusVolta2 = f"""{horarioOnibusVolta2} \({tempo_ProxOnibusVolta2}\)"""

    # Texto da mensagem do bot
    proxOnibus = f"""
Ida \(Moradia \-\> Unicamp\):
01\) {output_ProxOnibusIda1}
02\) {output_ProxOnibusIda2}

Volta \(Unicamp \-\> Moradia\):
01\) {output_ProxOnibusVolta1}
02\) {output_ProxOnibusVolta2}
"""
    # Envio da mensagem no chat
    bot.reply_to(mensagem, "Claro\! Aqui estão os horários dos próximos ônibus da moradia:")
    bot.send_message(mensagem.chat.id, proxOnibus)

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
    proxOnibus = nextBus(horaAtual, diaAtual, 0)

    ### Lista com todos os horários de Ida

    pos = 0

    ## Texto da mensagem do bot
    horariosIda = ""

    # Dia útil
    if diaAtual in 'Segunda Terça Quarta Quinta Sexta':

        for horario in diaUtil_horariosIda:

            # Ônibus que já passaram
            if strToTime(horario) < strToTime(proxOnibus): 
                pos += 1
                if pos % 3 == 0:
                    horariosIda += f'~{horario}~\n'
                else:
                    horariosIda += f'~{horario}~  \|  '
            
            # Próximo ônibus
            elif strToTime(horario) == strToTime(proxOnibus):
                pos += 1
                if pos % 3 == 0:
                    horariosIda += f'*{proxOnibus}*\n'
                else:
                    horariosIda += f'*{proxOnibus}*  \|  '
            
            # Ônibus que ainda não passaram
            else:
                pos += 1
                if pos % 3 == 0:
                    horariosIda += f'{horario}\n'
                else:
                    horariosIda += f'{horario}  \|  '
    
    # Dia não-útil
    else:

        for horario in diaNaoUtil_horariosIda:

            # Ônibus que já passaram
            if strToTime(horario) < strToTime(proxOnibus): 
                pos += 1
                if pos % 3 == 0:
                    horariosIda += f'~{horario}~\n'
                else:
                    horariosIda += f'~{horario}~  \|  '
            
            # Próximo ônibus
            elif strToTime(horario) == strToTime(proxOnibus):
                pos += 1
                if pos % 3 == 0:
                    horariosIda += f'*{proxOnibus}*\n'
                else:
                    horariosIda += f'*{proxOnibus}*  \|  '
            
            # Ônibus que ainda não passaram
            else:
                pos += 1
                if pos % 3 == 0:
                    horariosIda += f'{horario}\n'
                else:
                    horariosIda += f'{horario}  \|  '

    # Envio de mensagem
    bot.reply_to(message, 'Ta bom\! Aqui está a lista dos ônibus de Ida de hoje\!')
    bot.send_message(message.chat.id, horariosIda)

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
    proxOnibus = nextBus(horaAtual, diaAtual, 0)

    ### Lista com todos os horários de Ida

    pos = 0

    ## Texto da mensagem do bot
    horariosVolta = ""

    # Dia útil
    if diaAtual in 'Segunda Terça Quarta Quinta Sexta':

        for horario in diaUtil_horariosVolta:

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

        for horario in diaNaoUtil_horariosIda:

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