from datetime import datetime, timedelta

## General time conversion
def getCurrentDay(mensagem):
    
    """
    Essa função
    - obtém o dia atual em string em inglês a partir do objeto mensagem
    - converte os dias em inglês para português brasileiro e retorna o dia
    """

    # Obtém o dia atual
    diaAtual = datetime.fromtimestamp(mensagem.date).strftime('%A') # Inglês

    # Conversão para pt-br
    if diaAtual == "Monday":
        diaAtual = "Segunda"

    elif diaAtual == "Tuesday":
        diaAtual = "Terça"

    elif diaAtual == "Wednesday":
        diaAtual = "Quarta"

    elif diaAtual == "Thursday":
        diaAtual = "Quinta"

    elif diaAtual == "Friday":
        diaAtual = "Sexta"

    elif diaAtual == "Saturday":
        diaAtual = "Sábado"

    elif diaAtual == "Sunday":
        diaAtual = "Domingo"
    
    return diaAtual

def convertToInt(time):

    """
    Essa função
    - converte uma variável do tipo string para o tipo inteiro
    """

    time = str(time)
    if time[0] == 0:
        del time[0]
    return int(time.replace(':',''))

def getTimeDifference(h1, h2):

    """
    Essa função
    - calcula a diferença entre dois horários do tipo int
    - retorna a diferença formatada em "HH horas e mm minutos"
    """

    if h1 > h2:
        h2 = datetime.strptime(str(h2), '%H%M')
        h1 = datetime.strptime(str(h1), '%H%M')
        h2 += timedelta(days=1)
        until_h2 = h2 - h1
        until_h2 = datetime.strftime(until_h2)
        leftTime = convertToInt(until_h2)
        return f'{leftTime[:2]} horas e {leftTime[4:]} minutos'
    if h1 == h2:
        return '00:00'
    if h1 < h2:
        return timedelta(hours=h2 // 100, minutes=h2 % 100) - timedelta(hours=h1 // 100, minutes=h1 % 100)


#### New functions

def timeToStr(h):

    """
    Essa função converte variáveis do tipo datetime para str no formato '%H:%M'
    """

    return datetime.strftime(h, '%H:%M')

def strToTime(h):

    """
    Essa função converte horários do tipo str no formato '%H:%M' para datetime no formato 'ano-mês-dia hora:minuto'
    """

    currentTime = datetime.now()
    h = datetime.strptime(h, '%H:%M')
    return datetime(currentTime.year, currentTime.month, currentTime.day, h.hour, h.minute)

def getTimeDifference2(h1, h2):

    """
    Essa função calcula a diferença de tempo entre dois horários do tipo datetime
    """

    if type(h1) == str:
        h1 = strToTime(h1)
    if type(h2) == str:
        h2 = strToTime(h2)

    return h1 - timedelta(hours=h2.hour, minutes=h2.minute)