"""
Nome do arquivo: main.py
Autor: Glayson Oliveira
Descrição: Este é o arquivo principal do bot. É aqui que são definidas as funções que serão chamadas pelo
usuário por meio das mensagens pelo Telegram, que são checadas continuamente.
"""

# Importações de bibliotecas
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime

from bandejao import *
from timeUtils import *
from onibus import *
from websiteRequest import *
from menus import *


# Fazer conexão com a API do bot do Telegram
CHAVE_API = "7141300367:AAHBHEelfnAig53EVxqq0oabZrRz15CjIJ8"
bot = telebot.TeleBot(CHAVE_API, parse_mode='MarkdownV2')

### Comandos intermediários: apenas auxiliam o usuário a chegarem às funcionalidades do bot

## Geral

# Comando /start
@bot.message_handler(commands=["start"]) # Atribuição do comando /start à função
def start(mensagem):
    """
    Envia uma mensagem de introdução no chat. Geralmente utilizada apenas na primeira
    interação do usuário com o bot.

    :param mensagem: A mensagem enviada pelo usuário.
    """

    # Texto da mensagem do bot
    startText = f"""
Eu me chamo Nova e sou um bot criado por alunos da Unicamp\!

Meu objetivo é fornecer informações dos ônibus da moradia e dos restaurantes da Unicamp de forma rápida e fácil\.

Clique no botão que apareceu no lugar do seu teclado ou digite /home para ver o menu principal\.
"""
    
    # Botões
    startButton = ReplyKeyboardMarkup(resize_keyboard=True)  # Criação

    startButton.add(KeyboardButton('/home'))

    # Envio de mensagem
    bot.send_message(mensagem.chat.id, f'👋 Olá, {mensagem.chat.first_name}\! Como vai?')
    bot.send_message(mensagem.chat.id, startText, reply_markup=startButton)

@bot.message_handler(commands=["home"]) # Atribuição do comando /start à função
def menuPrincipal(mensagem):
    """
    Envia uma mensagem no chat: um menu com botões inline para acessar as os menus das funcionalidades do bot.

    :param mensagem: A mensagem enviada pelo usuário.
    """

    bot.send_message(mensagem.chat.id, menuHome.text, reply_markup=menuHome.buttons)

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

    # Envio de mensagem
    bot.reply_to(mensagem, 'Okay\! Aqui estão os comandos para os ônibus da moradia:')
    bot.send_message(mensagem.chat.id, menuOnibus.text, reply_markup=menuOnibus.buttons)

# Comando /bandejão
@bot.message_handler(commands=["bandejao"]) # Atribuição do comando /bandejao à função
def bandejao(mensagem):

    """
    Essa função
    - envia uma mensagem no chat listando todos os comandos relacionados com os restaurantes da Unicamp.
    """

    # Envio de mensagem
    bot.reply_to(mensagem, 'Certo\! Aqui estão os comandos para o bandejão:')
    bot.send_message(mensagem.chat.id, menuRestaurantes.text, reply_markup=menuRestaurantes.buttons)

# Comando /bCardapio
@bot.message_handler(commands=["bCardapio"]) # Atribuição do comando /bCardapio à função
def bCardapio(mensagem, isCallback=False):

    """
    Essa função envia uma mensagem no chat com as opções de cardápio (Tradicional e Vegano) para o usuário escolher.
    """

    # Envio de mensagem
    if isCallback:
        bot.send_message(mensagem.chat.id, menuCardapios.text, reply_markup=menuCardapios.buttons)
    else:
        bot.reply_to(mensagem, 'Ta bom\! Qual cardápio deseja ver?')
        bot.send_message(mensagem.chat.id, menuCardapios.text, reply_markup=menuCardapios.buttons)

### Comandos de funcionalidades: as funcionalidades de fato do bot

## Ônibus

# Comando /oTodos
@bot.message_handler(commands=["oTodos"]) # Atribuição do comando /oTodos à função
def oTodos(mensagem):

    """
    Essa função envia uma foto no chat da tabela de horários dos ônibus da moradia
    """

    horariosOnibusFoto = 'https://i.pinimg.com/736x/8f/72/57/8f7257a0d878b4ce78543183ace8acf1.jpg' # URL da foto em um perfil do Pinterest

    # Envio de mensagem
    bot.send_message(mensagem.chat.id, 'Aqui está a foto com todos os horários dos ônibus da moradia:')
    bot.send_photo(mensagem.chat.id, horariosOnibusFoto)

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
    horarioOnibus_ida1, horarioOnibus_volta1 = nextBus(horaAtual, diaAtual)

    horarioOnibus_ida2, horarioOnibus_volta2 = nextBusFromBus(horarioOnibus_ida1, horarioOnibus_volta1, diaAtual)


    ## Diferença de tempo
        # Ida
    if horarioOnibus_ida1 != None:
        diffHorarios_ida1 = getTimeDifference(horarioOnibus_ida1, horaAtual)
    else:
        diffHorarios_ida1 = None

    if horarioOnibus_ida2 != None:
        diffHorarios_ida2 = getTimeDifference(horarioOnibus_ida2, horaAtual)
    else:
        diffHorarios_ida2 = None

        # Volta
    if horarioOnibus_volta1 != None:
        diffHorarios_volta1 = getTimeDifference(horarioOnibus_volta1, horaAtual)
    else:
        diffHorarios_volta1 = None

    if horarioOnibus_volta2 != None:
        diffHorarios_volta2 = getTimeDifference(horarioOnibus_volta2, horaAtual)
    else:
        diffHorarios_volta2 = None

    ## Texto de tempo faltante para cada ônibus
        # Ida
    tempoProxOnibus_ida1 = formatingDiffTime(horarioOnibus_ida1, diffHorarios_ida1)
    tempoProxOnibus_ida2 = formatingDiffTime(horarioOnibus_ida2, diffHorarios_ida2)
        # Volta
    tempoProxOnibus_volta1 = formatingDiffTime(horarioOnibus_volta1, diffHorarios_volta1)
    tempoProxOnibus_volta2 = formatingDiffTime(horarioOnibus_volta2, diffHorarios_volta2)

    ##  Texto do horário de cada ônibus
        # Ida
    if horarioOnibus_ida1 == None:
        outputProxOnibus_ida1 = f"""Acabaram os ônibus por hoje"""
    else:
        outputProxOnibus_ida1 = f"""{horarioOnibus_ida1} \({tempoProxOnibus_ida1}\)"""

    if horarioOnibus_ida2 == None:
        outputProxOnibus_ida2 = f"""Acabaram os ônibus por hoje"""
    else:
        outputProxOnibus_ida2 = f"""{horarioOnibus_ida2} \({tempoProxOnibus_ida2}\)"""
        # Volta
    if horarioOnibus_volta1 == None:
        outputProxOnibus_volta1 = f"""Acabaram os ônibus por hoje"""
    else:
        outputProxOnibus_volta1 = f"""{horarioOnibus_volta1} \({tempoProxOnibus_volta1}\)"""

    if horarioOnibus_volta2 == None:
        outputProxOnibus_volta2 = f"""Acabaram os ônibus por hoje"""
    else:
        outputProxOnibus_volta2 = f"""{horarioOnibus_volta2} \({tempoProxOnibus_volta2}\)"""

    # Texto da mensagem do bot
    proxOnibus_text = f"""
Ida \(Moradia \-\> Unicamp\):
01\) {outputProxOnibus_ida1}
02\) {outputProxOnibus_ida2}

Volta \(Unicamp \-\> Moradia\):
01\) {outputProxOnibus_volta1}
02\) {outputProxOnibus_volta2}
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
    proxOnibus = nextBus(horaAtual, diaAtual, 0)

    ### Lista com todos os horários de Ida

    pos = 0

    ## Texto da mensagem do bot
    oTodosIdaText = ""

    # Dia útil
    if diaAtual in 'Segunda Terça Quarta Quinta Sexta':

        for horario in diaUtil_horariosIda:

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

        for horario in diaNaoUtil_horariosIda:

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

## Bandejao

# Comando /bTradicional
@bot.message_handler(commands=["bTradicional"]) # Atribuição do comando /bandejao à função
def bTradicional(mensagem, isCallback=False):

    """
    Essa função:
    - Envia uma mensagem no chat com o almoço e janta
    """

    if not isCallback:
        # Obtenção do tempo atual a partir da mensagem
        tempoAtual = datetime.fromtimestamp(mensagem.date)
        diaAtual = getCurrentDay(mensagem)
    else:
        tempoAtual = datetime.now()
        diaAtual = getCurrentDay(mensagem, False)

    if diaAtual == "Domingo":
        almocoTradicional = webScrapingCardapio(tempoAtual, diaAtual)[0]
    
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
        almocoTradicional = webScrapingCardapio(tempoAtual, diaAtual)[0]
        jantarTradicional = webScrapingCardapio(tempoAtual, diaAtual)[1]

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

    # Envio da mensagem no chat
    bot.send_message(mensagem.chat.id, cardapioTradicionalText)

# Comando /bVegano
@bot.message_handler(commands=["bVegano"]) # Atribuição do comando /bandejao à função
def bVegano(mensagem, isCallback=False):

    """
    Essa função:
    - Envia uma mensagem no chat com o almoço e janta
    """

    # Obtenção do tempo atual a partir da mensagem
    tempoAtual = datetime.fromtimestamp(mensagem.date)

    diaAtual = getCurrentDay(mensagem)

    if diaAtual == "Domingo":
        almocoVegano = webScrapingCardapio(tempoAtual, diaAtual)[0]
    
    # Texto da mensagem do bot
        cardapioVeganoText = f"""
    Cardápio *Vegano* 💚

\-\> *Almoço*
    *Proteína*: {almocoVegano.proteina}
    *Base*: {almocoVegano.base}
    *Complemento*: {almocoVegano.complemento}
    *Salada*: {almocoVegano.salada}
    *Fruta*: {almocoVegano.fruta}
    *Suco*: {almocoVegano.suco}
    
\-\> *Jantar*
    Não tem jantar aos domingos\!
"""

    else:
        almocoVegano = webScrapingCardapio(tempoAtual, diaAtual)[0]
        jantarVegano = webScrapingCardapio(tempoAtual, diaAtual)[1]

        # Texto da mensagem do bot
        cardapioVeganoText = f"""
    Cardápio *Vegano* 💚

\-\> *Almoço*
    *Proteína*: {almocoVegano.proteina}
    *Base*: {almocoVegano.base}
    *Complemento*: {almocoVegano.complemento}
    *Salada*: {almocoVegano.salada}
    *Fruta*: {almocoVegano.fruta}
    *Suco*: {almocoVegano.suco}

\-\> *Jantar*
    *Proteína*: {jantarVegano.proteina}
    *Base*: {jantarVegano.base}
    *Complemento*: {jantarVegano.complemento}
    *Salada*: {jantarVegano.salada}
    *Fruta*: {jantarVegano.fruta}
    *Suco*: {jantarVegano.suco}
    """

    # Envio da mensagem no chat
    bot.send_message(mensagem.chat.id, cardapioVeganoText)

# Comando /ru
@bot.message_handler(commands=["ru"]) # Atribuição do comando /bandejao à função
def bRS(mensagem, isCallback=False):
    
    # Obtenção do tempo atual a partir da mensagem
    horaAtual = datetime.fromtimestamp(mensagem.date)
    diaAtual = getCurrentDay(mensagem)

    ru = rest()[0]
    status(horaAtual, diaAtual, ru)

    ru = camRestaurante(horaAtual, ru)

    horarioOnibus_ida, _ = nextBus(horaAtual, diaAtual)

    if horarioOnibus_ida == None:
        horarioOnibus_ida = f'Acabaram os ônibus por hoje'
    

    textoRU = f"""
Restaurante Universitário \(RU\)

    *Status:* {ru.status}
    {ru.refeicao}
    *Tempo:* {ru.tempo}

    Se estiver se planejando\.\.\.
    *Próximo ônibus:* {horarioOnibus_ida}
"""

    bot.send_photo(mensagem.chat.id, ru.camera.imagem, caption=textoRU)

# Comando /ra
@bot.message_handler(commands=["ra"]) # Atribuição do comando /bandejao à função
def bRA(mensagem, isCallback=False):
    
    # Obtenção do tempo atual a partir da mensagem
    horaAtual = datetime.fromtimestamp(mensagem.date)
    diaAtual = getCurrentDay(mensagem)

    ra = rest()[1]
    status(horaAtual, diaAtual, ra)

    ra = camRestaurante(horaAtual, ra)

    horarioOnibus_ida, _ = nextBus(horaAtual, diaAtual)

    if horarioOnibus_ida == None:
        horarioOnibus_ida = f'Acabaram os ônibus por hoje'

    textoRA = f"""
Restaurante Administrativo \(RA\)

    *Status:* {ra.status}
    {ra.refeicao}
    *Tempo:* {ra.tempo}

    Se estiver se planejando\.\.\.
    *Próximo ônibus:* {horarioOnibus_ida}
"""

    bot.send_photo(mensagem.chat.id, ra.camera.imagem, caption=textoRA)

# Comando /rs
@bot.message_handler(commands=["rs"]) # Atribuição do comando /bandejao à função
def bRU(mensagem, isCallback=False):
    
    # Obtenção do tempo atual a partir da mensagem
    horaAtual = datetime.fromtimestamp(mensagem.date)
    diaAtual = getCurrentDay(mensagem)

    rs = rest()[2]
    status(horaAtual, diaAtual, rs)

    rs = camRestaurante(horaAtual, rs)

    horarioOnibus_ida, _ = nextBus(horaAtual, diaAtual)

    if horarioOnibus_ida == None:
        horarioOnibus_ida = f'Acabaram os ônibus por hoje'

    textoRS = f"""
Restaurante Saturnino \(RS\)

    *Status:* {rs.status}
    {rs.refeicao}
    *Tempo:* {rs.tempo}

    Se estiver se planejando\.\.\.
    *Próximo ônibus:* {horarioOnibus_ida}
"""

    bot.send_photo(mensagem.chat.id, rs.camera.imagem, caption=textoRS)

# Manipulador de callback para processar a seleção do usuário
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    """
    Recebe todos os retornos dos botões do tipo inline do bot.
    """

    # botão Menu ônibus
    if call.data == 'menuOnibus':

        bot.edit_message_text(menuOnibus.text, call.message.chat.id, call.message.message_id, reply_markup=menuOnibus.buttons)

    # botão Menu restaurantes
    elif call.data == 'menuRestaurantes':
        
        bot.edit_message_text(menuRestaurantes.text, call.message.chat.id, call.message.message_id, reply_markup=menuRestaurantes.buttons)

    # botao Menu principal (home)
    elif call.data == 'home':

        bot.edit_message_text(menuHome.text, call.message.chat.id, call.message.message_id, reply_markup=menuHome.buttons)

    # botao Menu principal (home)
    elif call.data == 'bCardapios':

        bCardapio(call.message, True)

    # botao Menu principal (home)
    elif call.data == 'bTradicional':

        bTradicional(call.message, True)

    elif call.data == 'bVegano':

        bVegano(call.message, True)
    
    elif call.data == 'ru':

        bRU(call.message, True)

    elif call.data == 'ra':

        bRA(call.message, True)

    elif call.data == 'rs':

        bRS(call.message, True)

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
    helpButton.add(KeyboardButton('/home'))

    # Envio de mensagem
    bot.reply_to(mensagem, 'Hmmm, eu não conheço esse comando\.') 
    bot.send_message(mensagem.chat.id, 'Digite /home ou clique no botão abaixo para ver os comandos disponíveis\.', reply_markup=helpButton)

bot.polling()