"""
Esse arquivo contém todas as funções relacionadas aos restaurantes da Unicamp.
"""
from restaurants_info import *


def printLocalidades(dia_atual, h_atual, h_atual_time):

    """
    Essa função retorna o texto da mensagem do bot com os três restaurantes, seus horários dde abertura e fechamento
    e o tempo restante para a próxima refeição em cada um.
    """
        
    ##Segunda a Sexta
    if (dia_atual in 'Segunda Terça Quarta Quinta Sexta'):
        if h_atual < 830:
            proximaRefeicao = 'o Café da Manhã'
            localidades = cafe_localidades
            left = calc_time_diff(h_atual, 730)
        elif h_atual < 1400:
            proximaRefeicao = 'o Almoço'
            localidades = almoco_localidades
        elif h_atual < 1945:
            proximaRefeicao = 'o Jantar'
            localidades = jantarLocalidades
        elif h_atual > 1945:
            proximaRefeicao = 'o Café da Manhã'
            localidades = cafeLocalidades
            left = calc_time_diff(h_atual, 730)

    ##Sabado
    elif dia_atual in 'Sábado':
        if h_atual < 1030:
            proximaRefeicao = 'o Almoço'
            localidades = almocoLocalidades['RS']
            left = datetime.strptime(localidades['RS'][0], '%H:%M') - h_atual_time
        elif h_atual < 1730:
            proximaRefeicao = 'o Jantar'
            localidades = jantarLocalidades['RS']
            left = datetime.strptime(localidades['RS'][0], '%H:%M') - h_atual_time
        elif h_atual > 1945:
            proximaRefeicao = 'o Almoço'
            localidades = almocoLocalidades['RS']
            left = calc_time_diff(h_atual, 730)
    
    ##Domingo
    elif (dia_atual in 'Domingo'):
        if h_atual < 1030:
            proximaRefeicao = 'o Almoço'
            localidades = almocoLocalidades['RS']
            left = datetime.strptime(localidades['RS'][0], '%H:%M') - h_atual_time
        else:
            proximaRefeicao = 'o Café da Manhã'
            localidades = cafeLocalidades
            left = calc_time_diff(h_atual, 730)
        
    ##Present Results
    if localidades == cafeLocalidades:
        return f"""
\- RU ({localidades['RU'][0]} \- {localidades['RU'][1]}):
· faltam {left} horas para {proximaRefeicao}
          """
    elif dia_atual in 'Sábado Domingo':
        return f"""
\- RS ({localidades['RS'][0]} \- {localidades['RS'][1]}):
· faltam {datetime.strptime(localidades['RS'][0], '%H:%M') - h_atual_time} horas para {proximaRefeicao}
          """
    else:
        return f"""
\- RU ({localidades['RU'][0]} \- {localidades['RU'][1]}):
· faltam {calc_time_diff(convertToInt(localidades['RU'][0]), h_atual)} horas para {proximaRefeicao}
\- RA ((({localidades['RA'][0]} \- {localidades['RA'][1]}):
· faltam {calc_time_diff(convertToInt(localidades['RA'][0]), h_atual)} horas para {proximaRefeicao}
\- RS ((({localidades['RS'][0]} \- {localidades['RS'][1]}):
· faltam {calc_time_diff(convertToInt(localidades['RS'][0]), h_atual)} horas para {proximaRefeicao}
          """