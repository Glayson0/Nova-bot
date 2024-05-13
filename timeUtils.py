from datetime import datetime, timedelta

## General time conversion
def getCurrentDay(mensagem, m=True):
    
    """
    Essa função
    - obtém o dia atual em string em inglês a partir do objeto mensagem
    - converte os dias em inglês para português brasileiro e retorna o dia
    """

    # Obtém o dia atual
    if m:
        diaAtual = datetime.fromtimestamp(mensagem.date).strftime('%A') # Inglês
    else:
        diaAtual = datetime.now()
        diaAtual = diaAtual.strftime('%A') # Inglês

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

def getTimeDifference(h1, h2):

    """
    Essa função calcula a diferença de tempo entre dois horários do tipo datetime.
    h1 precisa ser sempre menor que o h2.
    """

    if type(h1) == str:
        h1 = strToTime(h1)
    if type(h2) == str:
        h2 = strToTime(h2)

    return h1 - timedelta(hours=h2.hour, minutes=h2.minute)

def formatingDiffTime(horaAtual, diffTime):
    """
    Essa função formata o tempo faltante para o próximo ônibus
    Parâmentros:
    - horaAtual: horário da mensagem;
    - diffTime: a diferença de tempo entre o horário da mensagem e o horário do ônibus.
    """
    
    if horaAtual != None:
        if diffTime.hour > 0:
            return f'{diffTime.hour} hr e {diffTime.minute} min'
        else:
            return f'{diffTime.minute} min'