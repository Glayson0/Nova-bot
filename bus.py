from timeUtils import *

## Horários do ônibus
"""
Listas com horários de ônibus em string dos dias úteis e não-úteis.
"""

# Dia útil
diaUtil_horariosIda = ['06:30', '06:45', '06:50', '07:00', '07:10', '07:15', '07:20', '07:25', '07:35', '07:40', '07:45', '08:00', '08:10', '08:20',
    '08:30', '08:40', '08:50', '09:00', '09:10', '09:20', '09:30', '09:40', '09:45', '10:05', '10:15', '10:30','10:45', '11:00',
    '11:20', '11:30', '11:45', '12:00', '12:15', '12:20', '12:35', '12:45', '13:00', '13:05', '13:20', '13:30', '13:45', '14:00',
    '14:15', '14:30', '14:45', '15:00', '15:15', '15:30', '15:45', '16:00', '16:15', '16:30', '16:45', '17:00', '17:30', '17:45',
    '18:00', '18:10','18:20', '18:25', '18:30', '18:40', '18:55', '19:00', '19:15', '19:25', '19:35', '19:50', '19:55', '20:10',
    '20:30', '20:45']

diaUtil_horariosVolta = ['09:00', '09:30', '09:50', '10:00', '10:15', '10:40', '11:05', '11:15', '11:30', '11:45', '11:55', '12:00',
                  '12:20', '12:30', '12:45', '12:50', '13:00', '13:15', '13:30', '13:45', '14:00', '14:15', '14:30', '14:45',
                  '15:00', '15:15', '15:30', '15:45', '16:00', '16:15', '16:30', '16:45', '17:15', '17:40', '17:30', '17:45',
                  '17:50', '18:00', '18:15', '18:20', '18:30', '18:40', '18:50', '19:05', '19:10', '19:25', '19:35', '19:45',
                  '20:05', '20:20', '20:40', '20:50', '21:00', '21:25', '21:35', '21:55', '22:00', '22:10', '22:20', '22:30',
                  '22:35', '22:45', '23:05', '23:15', '23:25', '23:35', '23:45']

# Dia inútil
diaNaoUtil_horariosIda = ['07:10', '07:20', '07:30', '07:40', '07:50', '08:00', '08:10', '08:20', '11:00', '11:10', '11:20', '11:30', 
                      '11:40', '11:50', '12:00', '12:10', '12:20', '12:30', '12:40', '12:50', '13:00', '13:10', '13:20', 
                      '13:30', '13:40', '13:50', '17:30', '17:40', '17:50', '18:00', '18:10', '18:20', '18:30', '18:40', '18:50']

diaNaoUtil_horariosVolta = ['07:20', '07:30', '07:40', '07:50', '08:00', '08:10', '08:20', '08:30', '11:10', '11:20', '11:30', '11:40', 
                        '11:50', '12:00', '12:10', '12:20', '12:30', '12:40', '12:50', '13:00', '13:10', '13:20', '13:30', 
                        '13:40', '13:50', '14:00', '17:40', '17:50', '18:00', '18:10', '18:20', '18:30', '18:40', '18:50', '19:00']

## Funções relacionadas aos ônibus da moradia

def nextBus(horaAtual, diaAtual, percurso=2):
    """
    Essa função descobre o horário dos próximos dois ônibus de ida e de volta cada. Ela
    - compara a hora atual da mensagem com os horários de ônibus da lista do dia correto, percorrendo a lista
    e verificando qual horário já passou e qual está por vir com as comparações com variáveis do tipo datetime.
    """

    # Determina que há ônibus disponíveis
    existeOnibusIda = True
    existeOnibusVolta = True

    ### Busca do horário do próximo ônibus
    
    ## Dia útil
    
    # Ida
    if diaAtual in 'Segunda Terça Quarta Quinta Sexta':

        if horaAtual < fStrToTime(diaUtil_horariosIda[-1]): # Checagem se ainda há ônibus no dia
            
            for horarioOnibusIda in diaUtil_horariosIda:

                if horaAtual <= fStrToTime(horarioOnibusIda):
                    break

        else:
            horarioOnibusIda = None

    # Volta
        if horaAtual < fStrToTime(diaUtil_horariosVolta[-1]):  # Checagem se ainda há ônibus no dia

            # Encontrar próximos ônibus
            for horarioOnibusVolta in diaUtil_horariosVolta:

                if horaAtual <= fStrToTime(horarioOnibusVolta):
                    break
        else:
            horarioOnibusVolta = None
        
    ## Dia inútil

    # Ida
    else:

        if horaAtual < fStrToTime(diaNaoUtil_horariosIda[-1]): # Checagem se ainda há ônibus no dia


            for horarioOnibusIda in diaNaoUtil_horariosIda:

                if horaAtual <= fStrToTime(horarioOnibusIda):
                    horarioOnibusIda1 = horarioOnibusIda
                    if horarioOnibusIda1 != diaNaoUtil_horariosIda[-1]:
                        horarioOnibusIda2 = diaNaoUtil_horariosIda[diaNaoUtil_horariosIda.index(horarioOnibusIda1) + 1] # Õnibus próximo ao próximo
                    else:
                        horarioOnibusIda2 = None
                    break
        else:
            horarioOnibusIda = None

        if horaAtual < fStrToTime(diaNaoUtil_horariosVolta[-1]):  # Checagem se ainda há ônibus no dia

            # Encontrar próximos ônibus
            for horarioOnibusVolta in diaNaoUtil_horariosVolta:

                if horaAtual <= fStrToTime(horarioOnibusVolta):
                    horarioOnibusVolta1 = horarioOnibusVolta
                    if horarioOnibusVolta1 != diaNaoUtil_horariosVolta[-1]:
                        horarioOnibusVolta2 = diaNaoUtil_horariosVolta[diaNaoUtil_horariosVolta.index(horarioOnibusVolta1) + 1] # Õnibus próximo ao próximo
                    else:
                        horarioOnibusVolta2 = None
                    break
        else:
            horarioOnibusVolta = None
    
    if percurso == 0:
        return horarioOnibusIda
    elif percurso == 1:
        return horarioOnibusVolta
    else:
        return horarioOnibusIda, horarioOnibusVolta

def formatingBusDiffTime(horaAtual, diffTime):
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

def nextBusFromBus(horarioOnibusIda, horarioOnibusVolta, diaAtual):

    # DIA ÚTIL
    if diaAtual in 'Segunda Terça Quarta Quinta Sexta':

        if horarioOnibusIda != diaUtil_horariosIda[-1]:
            horarioOnibusIda2 = diaUtil_horariosIda[diaUtil_horariosIda.index(horarioOnibusIda) + 1]
        else:
            horarioOnibusIda2 = None
    
        if horarioOnibusVolta != diaUtil_horariosVolta[-1]:
            horarioOnibusVolta2 = diaUtil_horariosVolta[diaUtil_horariosVolta.index(horarioOnibusVolta) + 1]
        else:
            horarioOnibusVolta2 = None

# Dia Não útil
    else:

        if horarioOnibusIda != diaNaoUtil_horariosIda[-1]:
            horarioOnibusIda2 = diaNaoUtil_horariosIda[diaNaoUtil_horariosIda.index(horarioOnibusIda) + 1]
        else:
            horarioOnibusIda2 = None
    
        if horarioOnibusVolta != diaNaoUtil_horariosVolta[-1]:
            horarioOnibusVolta2 = diaNaoUtil_horariosVolta[diaNaoUtil_horariosVolta.index(horarioOnibusVolta) + 1]
        else:
            horarioOnibusVolta2 = None

    return horarioOnibusIda2, horarioOnibusVolta2
    