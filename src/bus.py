"""
Esse arquivo contém todas as funções relacionadas aos ônibus da Unicamp.
"""
from src.timeUtils import *
from data.busSchedule import *

## Funções relacionadas aos ônibus da moradia

def nextBus(horaAtual, diaAtual, percurso=2):
    """
    Essa função descobre o horário dos próximos dois ônibus de ida e de volta cada. Ela
    - compara a hora atual da mensagem com os horários de ônibus da lista do dia correto, percorrendo a lista
    e verificando qual horário já passou e qual está por vir com as comparações com variáveis do tipo datetime.
    
    Parâmetros:
    - horaAtual: horário atual da mensagem
    - diaAtual: dia atual da mensagem
    - percurso:
        - [1] Retorna apenas horário de Ida 
        - [2] Retorna apenas horário de Volta
        - [3] Retorna ambos horarios
    """

    ### Busca do horário do próximo ônibus
    
    ## Dia útil
    
    # Ida
    if diaAtual in 'Segunda Terça Quarta Quinta Sexta':

        if horaAtual < strToTime(diaUtil_horariosVolta[-1]): # Checagem se ainda há ônibus no dia
            
            for horarioOnibusIda in diaUtil_horariosVolta:

                if horaAtual <= strToTime(horarioOnibusIda):
                    break

        else:
            horarioOnibusIda = None

    # Volta
        if horaAtual < strToTime(diaUtil_horariosVolta[-1]):  # Checagem se ainda há ônibus no dia

            # Encontrar próximos ônibus
            for horarioOnibusVolta in diaUtil_horariosVolta:

                if horaAtual <= strToTime(horarioOnibusVolta):
                    break
        else:
            horarioOnibusVolta = None
        
    ## Dia inútil

    # Ida
    else:

        if horaAtual < strToTime(diaNaoUtil_horariosIda[-1]): # Checagem se ainda há ônibus no dia


            for horarioOnibusIda in diaNaoUtil_horariosIda:

                if horaAtual <= strToTime(horarioOnibusIda):
                    horarioOnibusIda1 = horarioOnibusIda
                    if horarioOnibusIda1 != diaNaoUtil_horariosIda[-1]:
                        horarioOnibusIda2 = diaNaoUtil_horariosIda[diaNaoUtil_horariosIda.index(horarioOnibusIda1) + 1] # Õnibus próximo ao próximo
                    else:
                        horarioOnibusIda2 = None
                    break
        else:
            horarioOnibusIda = None

        if horaAtual < strToTime(diaNaoUtil_horariosVolta[-1]):  # Checagem se ainda há ônibus no dia

            # Encontrar próximos ônibus
            for horarioOnibusVolta in diaNaoUtil_horariosVolta:

                if horaAtual <= strToTime(horarioOnibusVolta):
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

        if horarioOnibusIda != diaUtil_horariosVolta[-1]:
            horarioOnibusIda2 = diaUtil_horariosVolta[diaUtil_horariosVolta.index(horarioOnibusIda) + 1]
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
    