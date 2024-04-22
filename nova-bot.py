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

    ha_onibus_IDA = ha_onibus_VOLTA = True
    
    # Horario atual (inteiro e formatado)

    h_atual = int(datetime.fromtimestamp(mensagem.date).strftime('%H%M'))
    h_atual_f = datetime.fromtimestamp(mensagem.date).strftime('%H:%M')

    dia_atual = getCurrentDay(mensagem)

    #### Pegar lista de horários correspondente ao dia_atual

    # DIA ÚTIL
    if dia_atual in 'Segunda Terça Quarta Quinta Sexta':

        # Condição para quando não tiver mais ônibus no dia
        if h_atual > onibus_util_IDA[-1]:
            ha_onibus_IDA = False

        if h_atual > onibus_util_VOLTA[-1]:
            ha_onibus_VOLTA = False

        # Encontrar próximos ônibus
        for h_onibus_IDA in onibus_util_IDA:
            if h_atual <= h_onibus_IDA:
                prox_onibus_IDA = str(h_onibus_IDA)
                break
        for h_onibus_VOLTA in onibus_util_VOLTA:
            if h_atual <= h_onibus_VOLTA:
                prox_onibus_VOLTA = str(h_onibus_VOLTA)
                break
    
    # FIM DE SEMANA
    else:

        # Condição para quando não tiver mais ônibus de IDA no dia
        if h_atual > onibus_findis_IDA[-1]:
            ha_onibus_IDA = False
        else:
            # Encontrar próximos ônibus
            for h_onibus_IDA in onibus_findis_IDA:
                if h_atual <= h_onibus_IDA:
                    prox_onibus_IDA = str(h_onibus_IDA)
                    break

        # Condição para quando não tiver mais ônibus de VOLTA no dia
        if h_atual > onibus_findis_VOLTA[-1]:
            ha_onibus_VOLTA = False
        else:
            for h_onibus_VOLTA in onibus_findis_VOLTA:
                    prox_onibus_VOLTA = str(h_onibus_VOLTA)
                    break
        
    ###  Formatação do horário inteiro para str HH:MM
    # IDA
    if ha_onibus_IDA == True:
        prox_onibus_IDA_list = list(prox_onibus_IDA)
        if len(prox_onibus_IDA_list) == 3:
            prox_onibus_IDA_list.insert(0, '0'); prox_onibus_IDA_list.insert(2, ':')
        else:
            prox_onibus_IDA_list.insert(2, ':')
        prox_onibus_IDA_f = ''.join(prox_onibus_IDA_list)
    # VOLTA
    if ha_onibus_VOLTA == True:
        prox_onibus_VOLTA_list = list(prox_onibus_VOLTA)
        if len(prox_onibus_VOLTA_list) == 3:
            prox_onibus_VOLTA_list.insert(0, '0'); prox_onibus_VOLTA_list.insert(2, ':')
        else:
            prox_onibus_VOLTA_list.insert(2, ':')
        prox_onibus_VOLTA_f = ''.join(prox_onibus_VOLTA_list)

    ### Tempo em minutos até o próximo ônibus
    # Definindo dois horários
    h_atual_time = datetime.strptime(h_atual_f, '%H:%M')
    if ha_onibus_IDA == True:
        prox_onibus_IDA_time = datetime.strptime(prox_onibus_IDA_f, '%H:%M') # Ida
    if ha_onibus_VOLTA == True:
        prox_onibus_VOLTA_time = datetime.strptime(prox_onibus_VOLTA_f, '%H:%M') # Volta

    # Calculando a diferença de tempo
    if ha_onibus_IDA == True:
        intervalo_tempo_onibus_IDA = (prox_onibus_IDA_time - h_atual_time).seconds // 60 # Ida
    if ha_onibus_VOLTA == True:
        intervalo_tempo_onibus_VOLTA = (prox_onibus_VOLTA_time - h_atual_time).seconds // 60 # Volta

    if ha_onibus_IDA == True:
        output_prox_IDA = f'{prox_onibus_IDA_f} ({intervalo_tempo_onibus_IDA} min)'
    else:
        output_prox_IDA = 'acabaram os ônibus de hoje!'

    if ha_onibus_VOLTA == True:
        output_prox_VOLTA = f'{prox_onibus_VOLTA_f} ({intervalo_tempo_onibus_VOLTA} min)'
    else:
        output_prox_VOLTA = 'acabaram os ônibus de hoje!'

    # Envio da mensagem no chat
    bot.send_message(mensagem.chat.id,
    f"""🚌🚌🚌 HORÁRIO ÔNIBUS 🚌🚌🚌

    Dia atual: {dia_atual}
    Horário atual: {h_atual_f}
    
    Próximo ônibus IDA: {output_prox_IDA}
    Próximo ônibus VOLTA: {output_prox_VOLTA}"""
    )

########### Resposta à opção "/bandejao"
@bot.message_handler(commands=["bandejao"]) # funciona quando recebe o comando "bandejao"
def bandejao(mensagem):

    # Horario atual (inteiro e formatado)
    h_atual = int(datetime.fromtimestamp(mensagem.date).strftime('%H%M'))
    h_atual_f = datetime.fromtimestamp(mensagem.date).strftime('%H:%M')

    dia_atual = getCurrentDay(mensagem)

    h_atual_time = datetime.strptime(h_atual_f, '%H:%M')

    # Envio da mensagem no chat
    bot.send_message(mensagem.chat.id,
f"""🍽️🥛🍎 HORÁRIOS DE REFEIÇÃO 🍽️🥛🍎

Dia atual: {dia_atual}
Horário atual: {h_atual_f}
{printLocalidades(dia_atual, h_atual, h_atual_time)}    
""")

def verificar(mensagem): # Checa a mensagem do usuário e retorna True (vale para qualquer mensagem)
    return True

# Função que manda o Menu independentemente da mensagem do usuário
@bot.message_handler(func=verificar)
def responder(mensagem):
    menu = """
    Qual função gostaria de acessar? (Clique no item):
 🚌 · /onibus - Ver horário do próximo ônibus
 🍽️ · /bandejao - Ver horário da próxima refeição
    Responder qualquer coisa não funcionará. Clique em uma das opções.
    """

    bot.reply_to(mensagem, f'👋 Olá, {mensagem.chat.first_name}! Como vai?')
    bot.send_message(mensagem.chat.id, menu)

bot.polling() # Vai checar a mensagem recebida pelo bot