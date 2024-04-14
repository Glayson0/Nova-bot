import telebot
from datetime import datetime

# Horários do ônibus em inteiro HHMM
dia_util_IDA = [630, 645, 650, 700, 710, 715, 720, 725, 735, 740, 745, 800, 810, 820, 830, 840,
                850, 900, 910, 920, 930, 940, 945, 1005, 1015, 1030, 1045, 1100, 1120, 1130,
                1145, 1200, 1215, 1220, 1235, 1245, 1300, 1305, 1320, 1330, 1345, 1400, 1415, 1430,
                1445, 1500, 1515, 1530, 1545, 1600, 1615, 1630, 1645, 1700, 1730, 1745, 1800, 1810, 
                1820, 1825, 1830, 1840, 1855, 1900, 1915, 1925, 1935, 1950, 1955, 2010, 2030, 2045]

dia_util_VOLTA = [900, 930, 950, 1000, 1015, 1040, 1105, 1115, 1130, 1145, 1155, 1200,
                  1220, 1230, 1245, 1250, 1300, 1315, 1330, 1345, 1400, 1415, 1430, 1445,
                  1500, 1515, 1530, 1545, 1600, 1615, 1630, 1645, 1715, 1740, 1730, 1745,
                  1750, 1800, 1815, 1820, 1830, 1840, 1850, 1905, 1910, 1925, 1935, 1945,
                  2005, 2020, 2040, 2050, 2100, 2125, 2135, 2155, 2200, 2210, 2220, 2230,
                  2235, 2245, 2305, 2315, 2325, 2335, 2345]

findis_feriado_IDA = [710, 720, 730, 740, 750, 800, 810, 820, 1100, 1110, 1120, 1130, 
                      1140, 1150, 1200, 1210, 1220, 1230, 1240, 1250, 1300, 1310, 1320, 
                      1330, 1340, 1350, 1730, 1740, 1750, 1800, 1810, 1820, 1830, 1840, 1850]

findis_feriado_VOLTA = [720, 730, 740, 750, 800, 810, 820, 830, 1110, 1120, 1130, 1140, 
                        1150, 1200, 1210, 1220, 1230, 1240, 1250, 1300, 1310, 1320, 1330, 
                        1340, 1350, 1400, 1740, 1750, 1800, 1810, 1820, 1830, 1840, 1850, 1900]

# Inicialização do bot
CHAVE_API = "7141300367:AAHBHEelfnAig53EVxqq0oabZrRz15CjIJ8"
bot = telebot.TeleBot(CHAVE_API)

# Resposta à opção "/onibus"
@bot.message_handler(commands=["onibus"]) # funciona quando recebe o comando "onibus"
def onibus(mensagem):
    # Horario atual (inteiro e formatado)
    h_atual = int(datetime.fromtimestamp(mensagem.date).strftime('%H%M'))
    h_atual_f = datetime.fromtimestamp(mensagem.date).strftime('%H:%M')

    # Dia atual
    dia_atual = datetime.fromtimestamp(mensagem.date).strftime('%A') # Em inglês
    # Conversão para pt-br
    if dia_atual == "Monday":
        dia_atual = "Segunda"

    elif dia_atual == "Tuesday":
        dia_atual = "Terça"

    elif dia_atual == "Wednesday":
        dia_atual = "Quarta"

    elif dia_atual == "Thursday":
        dia_atual = "Quinta"

    elif dia_atual == "Friday":
        dia_atual = "Sexta"

    elif dia_atual == "Saturday":
        dia_atual = "Sábado"

    elif dia_atual == "Sunday":
        dia_atual = "Domingo"

    # Pegar lista de horários correspondente ao dia_atual
    if dia_atual in 'Segunda Terça Quarta Quinta Sexta':
        for h_onibus_IDA in dia_util_IDA: # Laço para encontrar o horário do próximo ônibus IDA
            if h_atual <= h_onibus_IDA:
                prox_onibus_IDA = str(h_onibus_IDA)
                break
        for h_onibus_VOLTA in dia_util_VOLTA: # Laço para encontrar o horário do próximo ônibus VOLTA
            if h_atual <= h_onibus_VOLTA:
                prox_onibus_VOLTA = str(h_onibus_VOLTA)
                break
    else:
        for h_onibus_IDA in findis_feriado_IDA: # Laço para encontrar o horário do próximo ônibus IDA
            if h_atual <= h_onibus_IDA:
                prox_onibus_IDA = str(h_onibus_IDA)
                break
        for h_onibus_VOLTA in findis_feriado_VOLTA: # Laço para encontrar o horário do próximo ônibus VOLTA
            if h_atual <= h_onibus_VOLTA:
                prox_onibus_VOLTA = str(h_onibus_VOLTA)
                break
        
    # Formatação do horário inteiro para str HH:MM
        # IDA
    prox_onibus_IDA_list = list(prox_onibus_IDA)
    if len(prox_onibus_IDA_list) == 3:
        prox_onibus_IDA_list.insert(0, '0'); prox_onibus_IDA_list.insert(2, ':')
    else:
        prox_onibus_IDA_list.insert(2, ':')
    prox_onibus_IDA_f = ''.join(prox_onibus_IDA_list)
        # VOLTA
    prox_onibus_VOLTA_list = list(prox_onibus_VOLTA)
    if len(prox_onibus_VOLTA_list) == 3:
        prox_onibus_VOLTA_list.insert(0, '0'); prox_onibus_VOLTA_list.insert(2, ':')
    else:
        prox_onibus_VOLTA_list.insert(2, ':')
    prox_onibus_VOLTA_f = ''.join(prox_onibus_VOLTA_list)

    # Tempo em minutos até o próximo ônibus
    # Definindo dois horários
    h_atual_time = datetime.strptime(h_atual_f, '%H:%M')
    prox_onibus_IDA_time = datetime.strptime(prox_onibus_IDA_f, '%H:%M')
    prox_onibus_VOLTA_time = datetime.strptime(prox_onibus_VOLTA_f, '%H:%M')

    # Calculando a diferença de tempo
    intervalo_tempo_onibus_IDA = (prox_onibus_IDA_time - h_atual_time).seconds // 60
    intervalo_tempo_onibus_VOLTA = (prox_onibus_VOLTA_time - h_atual_time).seconds // 60

    # Envio da mensagem no chat
    bot.send_message(mensagem.chat.id,
f"""###### HORÁRIO ÔNIBUS ######

Dia atual: {dia_atual}
Horário atual: {h_atual_f}
Próximo ônibus IDA: {prox_onibus_IDA_f} ({intervalo_tempo_onibus_IDA} min)
Próximo ônibus VOLTA: {prox_onibus_VOLTA_f} ({intervalo_tempo_onibus_VOLTA} min)""")

# Resposta à opção "/bandejao"
@bot.message_handler(commands=["bandejao"]) # funciona quando recebe o comando "bandejao"
def bandejao(mensagem):
      bot.reply_to(mensagem, "Já tá querendo ao mossar, é?")
      pass

def verificar(mensagem): # Checa a mensagem do usuário e retorna True (vale para qualquer mensagem)
    return True

# Função que manda o Menu independentemente da mensagem do usuário
@bot.message_handler(func=verificar)
def responder(mensagem):
    menu = """
    Qual função gostaria de acessar? (Clique no item):
    · /onibus - Ver horário do próximo ônibus
    · /bandejao - Ver horário da próxima refeição
    Responder qualquer coisa não funcionará. Clique em uma das opções.
    """

    bot.reply_to(mensagem, f'Olá, {mensagem.chat.first_name}! Como vai?')
    bot.send_message(mensagem.chat.id, menu)

bot.polling() # Vai checar a mensagem recebida pelo bot
