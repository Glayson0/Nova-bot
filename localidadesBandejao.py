from datetime import datetime
from timeUtils import *

cafeLocalidades = {
    'RU': ['07:30','08:30']
}

almocoLocalidades = {
    'RU': ['10:30','14:00'],
    'RA': ['11:15','14:00'],
    'RS': ['11:00','14:00']
}

jantarLocalidades = {
    'RU': ['17:30','19:45'],
    'RA': ['17:30','19:00'],
    'RS': ['17:30','19:00']
}

def printLocalidades(dia_atual, h_atual, h_atual_time):
        
    ##Segunda a Sexta
    if (dia_atual in 'Segunda Terça Quarta Quinta Sexta'):
        if h_atual < 830:
            prox_refeicao = 'o Café da Manhã'
            localidades = cafeLocalidades
            left = getTimeDifference(h_atual, 730)
        elif h_atual < 1400:
            prox_refeicao = 'o Almoço'
            localidades = almocoLocalidades
        elif h_atual < 1945:
            prox_refeicao = 'o Jantar'
            localidades = jantarLocalidades
        elif h_atual > 1945:
            prox_refeicao = 'o Café da Manhã'
            localidades = cafeLocalidades
            left = getTimeDifference(h_atual, 730)

    ##Sabado
    elif dia_atual in 'Sábado':
        if h_atual < 1030:
            prox_refeicao = 'o Almoço'
            localidades = almocoLocalidades['RS']
            left = datetime.strptime(localidades['RS'][0], '%H:%M') - h_atual_time
        elif h_atual < 1730:
            prox_refeicao = 'o Jantar'
            localidades = jantarLocalidades['RS']
            left = datetime.strptime(localidades['RS'][0], '%H:%M') - h_atual_time
        elif h_atual > 1945:
            prox_refeicao = 'o Almoço'
            localidades = almocoLocalidades['RS']
            left = getTimeDifference(h_atual, 730)
    
    ##Domingo
    elif (dia_atual in 'Domingo'):
        if h_atual < 1030:
            prox_refeicao = 'o Almoço'
            localidades = almocoLocalidades['RS']
            left = datetime.strptime(localidades['RS'][0], '%H:%M') - h_atual_time
        else:
            prox_refeicao = 'o Café da Manhã'
            localidades = cafeLocalidades
            left = getTimeDifference(h_atual, 730)
        
    ##Present Results
    if localidades == cafeLocalidades:
        return f"""
- RU ({localidades['RU'][0]} - {localidades['RU'][1]}):
· faltam {left} horas para {prox_refeicao}
        """
    elif dia_atual in 'Sábado Domingo':
        return f"""
- RS ({localidades['RS'][0]} - {localidades['RS'][1]}):
· faltam {datetime.strptime(localidades['RS'][0], '%H:%M') - h_atual_time} horas para {prox_refeicao}
        """
    else:
        return f"""
- RU ({localidades['RU'][0]} - {localidades['RU'][1]}):
· faltam {getTimeDifference(convertToInt(localidades['RU'][0]), h_atual)} horas para {prox_refeicao}
- RA ({localidades['RA'][0]} - {localidades['RA'][1]}):
· faltam {getTimeDifference(convertToInt(localidades['RA'][0]), h_atual)} horas para {prox_refeicao}
- RS ({localidades['RS'][0]} - {localidades['RS'][1]}):
· faltam {getTimeDifference(convertToInt(localidades['RS'][0]), h_atual)} horas para {prox_refeicao}
        """
