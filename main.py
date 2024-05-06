import telebot
from datetime import datetime
from localidadesBandejao import *
from timeUtils import *

# Inicialização do bot
## add access link to the bot here: [https://t.me/unicampus_bot]
CHAVE_API = "7141300367:AAHBHEelfnAig53EVxqq0oabZrRz15CjIJ8"
bot = telebot.TeleBot(CHAVE_API, parse_mode='MARKDOWN')

########## Resposta à opção "/onibus"
@bot.message_handler(commands=["onibus"]) # funciona quando recebe o comando "onibus"
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
        output_ProxOnibusIda = 'acabaram os ônibus de hoje!'

    if existeOnibusVolta == True:
        if diffHorariosVolta.hour > 0:
            output_ProxOnibusVolta = f'{horarioOnibusVolta} ({diffHorariosVolta.hour} hr e {diffHorariosVolta.minute} min)'
        else:
            output_ProxOnibusVolta = f'{horarioOnibusVolta} ({diffHorariosVolta.minute} min(s))'
    else:
        output_ProxOnibusVolta = 'acabaram os ônibus de hoje!'

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

def verificar(mensagem): # Checa a mensagem do usuário e retorna True (vale para qualquer mensagem)
    return True

# Função que manda o Menu independentemente da mensagem do usuário
@bot.message_handler(func=verificar)
def responder(mensagem):
#     menu = """
#     Qual função gostaria de acessar? (Clique no item):
#  🚌 · /onibus - Ver horário do próximo ônibus
#  🍽️ · /bandejao - Ver horário da próxima refeição
#     Responder qualquer coisa não funcionará. Clique em uma das opções.
#     """
    menu = """
(MENU TEMPORÁRIO)
Lista com todos os comandos:

    ÔNIBUS
        - /onibus
        - /oTodos
        - /oProx

    BANDEJÃO
        - /bandejao
        - /bHoras
        - /bCardapio
        - /bJapode
        - /ru
        - /rs
        - /ra
"""

    bot.reply_to(mensagem, f'👋 Olá, {mensagem.chat.first_name}! Como vai?')
    bot.send_message(mensagem.chat.id, menu)

bot.polling() # Vai checar a mensagem recebida pelo bot