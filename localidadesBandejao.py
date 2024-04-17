from datetime import datetime

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
            time_until = datetime.strptime(localidades['RU'][0], '%H:%M') - h_atual_time
        elif h_atual < 1400:
            prox_refeicao = 'o Almoço'
            localidades = almocoLocalidades
        elif h_atual < 1945:
            prox_refeicao = 'o Jantar'
            localidades = jantarLocalidades
        elif h_atual > 1945:
            prox_refeicao = 'o Café da Manhã'
            localidades = cafeLocalidades

    ##Sabado
    elif dia_atual in 'Sábado':
        if h_atual < 1030:
            prox_refeicao = 'o Almoço'
            localidades = almocoLocalidades['RS']
        elif h_atual < 1730:
            prox_refeicao = 'o Jantar'
            localidades = jantarLocalidades['RS']
        elif h_atual > 1945:
            prox_refeicao = 'o Almoço'
            localidades = almocoLocalidades['RS']

    
    ##Domingo
    elif (dia_atual in 'Domingo') and (h_atual < 1030):
        if h_atual < 1030:
            prox_refeicao = 'o Almoço'
            localidades = almocoLocalidades['RS']
        else:
            prox_refeicao = 'o Café da Manhã'
            localidades = cafeLocalidades
        
    ##Present Results
    if dia_atual in 'Sábado Domingo':
        return f"""
- RS ({localidades['RS'][0]} - {localidades['RS'][1]}):
· faltam {datetime.strptime(localidades['RS'][0], '%H:%M') - h_atual_time} horas para {prox_refeicao}
        """
    elif localidades == cafeLocalidades:
        if h_atual > 830:
            ## logic for calculating time until next meal
        else:
            left = datetime.strptime(localidades['RU'][0], '%H:%M') - h_atual_time
        return f"""
- RU ({localidades['RU'][0]} - {localidades['RU'][1]}):
· faltam {left} horas para {prox_refeicao}
    
        """
    else:
        return f"""
- RU ({localidades['RU'][0]} - {localidades['RU'][1]}):
· faltam {datetime.strptime(localidades['RU'][0], '%H:%M') - h_atual_time} horas para {prox_refeicao}
- RA ({localidades['RA'][0]} - {localidades['RA'][1]}):
· faltam {datetime.strptime(localidades['RA'][0], '%H:%M') - h_atual_time} horas para {prox_refeicao}
- RS ({localidades['RS'][0]} - {localidades['RS'][1]}):
· faltam {datetime.strptime(localidades['RS'][0], '%H:%M') - h_atual_time} horas para {prox_refeicao}
        """
