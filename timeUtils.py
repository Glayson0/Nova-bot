from datetime import datetime, timedelta

# Horários do ônibus em inteiro HHMM
onibus_util_IDA = ['06:30', '06:45', '06:50', '07:00', '07:10', '07:15', '07:20', '07:25', '07:35', '07:40', '07:45', '08:00', '08:10', '08:20',
    '08:30', '08:40', '08:50', '09:00', '09:10', '09:20', '09:30', '09:40', '09:45', '10:05', '10:15', '10:30','10:45', '11:00',
    '11:20', '11:30', '11:45', '12:00', '12:15', '12:20', '12:35', '12:45', '13:00', '13:05', '13:20', '13:30', '13:45', '14:00',
    '14:15', '14:30', '14:45', '15:00', '15:15', '15:30', '15:45', '16:00', '16:15', '16:30', '16:45', '17:00', '17:30', '17:45',
    '18:00', '18:10','18:20', '18:25', '18:30', '18:40', '18:55', '19:00', '19:15', '19:25', '19:35', '19:50', '19:55', '20:10',
    '20:30', '20:45']

onibus_util_VOLTA = ['09:00', '09:30', '09:50', '10:00', '10:15', '10:40', '11:05', '11:15', '11:30', '11:45', '11:55', '12:00',
                  '12:20', '12:30', '12:45', '12:50', '13:00', '13:15', '13:30', '13:45', '14:00', '14:15', '14:30', '14:45',
                  '15:00', '15:15', '15:30', '15:45', '16:00', '16:15', '16:30', '16:45', '17:15', '17:40', '17:30', '17:45',
                  '17:50', '18:00', '18:15', '18:20', '18:30', '18:40', '18:50', '19:05', '19:10', '19:25', '19:35', '19:45',
                  '20:05', '20:20', '20:40', '20:50', '21:00', '21:25', '21:35', '21:55', '22:00', '22:10', '22:20', '22:30',
                  '22:35', '22:45', '23:05', '23:15', '23:25', '23:35', '23:45']

onibus_findis_IDA = ['07:10', '07:20', '07:30', '07:40', '07:50', '08:00', '08:10', '08:20', '11:00', '11:10', '11:20', '11:30', 
                      '11:40', '11:50', '12:00', '12:10', '12:20', '12:30', '12:40', '12:50', '13:00', '13:10', '13:20', 
                      '13:30', '13:40', '13:50', '17:30', '17:40', '17:50', '18:00', '18:10', '18:20', '18:30', '18:40', '18:50']

onibus_findis_VOLTA = ['07:20', '07:30', '07:40', '07:50', '08:00', '08:10', '08:20', '08:30', '11:10', '11:20', '11:30', '11:40', 
                        '11:50', '12:00', '12:10', '12:20', '12:30', '12:40', '12:50', '13:00', '13:10', '13:20', '13:30', 
                        '13:40', '13:50', '14:00', '17:40', '17:50', '18:00', '18:10', '18:20', '18:30', '18:40', '18:50', '19:00']

## General time conversion
def getCurrentDay(mensagem):

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
    
    return dia_atual

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
        h2 += timedelta(days=1)
        until_h2 = h2 - h1
        return until_h2
    if h1 == h2:
        return '00:00'
    if h1 < h2:
        return timedelta(hours=h2 // 100, minutes=h2 % 100) - timedelta(hours=h1 // 100, minutes=h1 % 100)
    
def convertToInt(time):
    time = str(time)
    if time[0] == 0:
        del time[0]
    return int(time.replace(':',''))

def convertToString(datetime):
    return datetime.strftime('%H:%M')

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