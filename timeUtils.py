from datetime import datetime, timedelta

## General time conversion
def getCurrentDay(mensagem):

    # Dia atual
    diaAtual = datetime.fromtimestamp(mensagem.date).strftime('%A') # Em inglês

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
    time = str(time)
    if time[0] == 0:
        del time[0]
    return int(time.replace(':',''))

def convertToString(datetime):
    return datetime.strftime('%H:%M')

def format_time(time_str):
    ## Not working that well.
    ## I don't recommend using this function

    if int(time_str[2:]) >= 60:
        hours = int(time_str[:2])
        minutes = int(time_str[2:])
    
    if len(time_str) == 3:
        time_str = f"0{hours}:{minutes}"
    else:
        time_str = f"{hours}:{minutes}"
        
    formatted_time = datetime.strptime(time_str, '%H%M').strftime('%H:%M')
    return formatted_time

def getTimeDifference(h1, h2):
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

def fTimeToStr(h):
    return datetime.strftime(h, '%H:%M')

def fStrToTime(h):
    agora = datetime.now()
    h = datetime.strptime(h, '%H:%M')
    return datetime(agora.year, agora.month, agora.day, h.hour, h.minute)

def getTimeDifference2(h1, h2):
    if type(h1) == str:
        h1 = fStrToTime(h1)
    if type(h2) == str:
        h2 = fStrToTime(h2)

    return h1 - timedelta(hours=h2.hour, minutes=h2.minute)