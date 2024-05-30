from datetime import datetime, timedelta

## General time conversion
def getWeekDay(date: datetime):
    
    """
    Essa função
    - obtém o dia atual em string em inglês a partir do objeto mensagem
    - converte os dias em inglês para português brasileiro e retorna o dia
    """

    currentWeekDay = date.strftime('%A') # Inglês

    # Conversão para pt-br
    if currentWeekDay == "Monday":
        currentWeekDay = "Segunda"

    elif currentWeekDay == "Tuesday":
        currentWeekDay = "Terça"

    elif currentWeekDay == "Wednesday":
        currentWeekDay = "Quarta"

    elif currentWeekDay == "Thursday":
        currentWeekDay = "Quinta"

    elif currentWeekDay == "Friday":
        currentWeekDay = "Sexta"

    elif currentWeekDay == "Saturday":
        currentWeekDay = "Sábado"

    elif currentWeekDay == "Sunday":
        currentWeekDay = "Domingo"
    
    return currentWeekDay

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