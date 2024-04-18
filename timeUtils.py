from datetime import datetime, timedelta

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
    if len(time_str) == 3:
        time_str = '0' + time_str

    if time_str[-2:] >= '60':
        hours = int(time_str[:2])
        minutes = int(time_str[-2:])
        hours += minutes // 60
        minutes %= 60
        time_str = f"{hours:02d}{minutes:02d}"
        
    formatted_time = datetime.strptime(time_str, '%H%M').strftime('%H:%M')
    return formatted_time

def getTimeDifference(h1, h2):
    if h1 > h2:
        h1 = datetime.strptime(str(h1), '%H%M')
        h2 = datetime.strptime(str(h2), '%H%M')

        h2 += timedelta(days=1)

        until_h2 = h2 - h1
        return until_h2
    if h1 == h2:
        return '00:00'
    if h1 < h2:
        return timedelta(hours=h2 // 100, minutes=h2 % 100) - timedelta(hours=h1 // 100, minutes=h1 % 100)
    
def convertToInt(string):
    if string[0] == 0:
        del string[0]
        print(string)
    string.replace(':','')