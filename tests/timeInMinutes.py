from datetime import datetime
from time import sleep

def str_to_min(time:str) -> int:
    """Converte um horário no formato HH:MM em minutos."""
    horas = int(time[1]) if time[0] == 0 else int(time[:2])
    minutos = int(time[4]) if time[3] == 0 else int(time[3:])
    return 60*horas + minutos

def min_to_str(time:int) -> str:
    """Converte minutos em um horário no formato HH:MM."""
    horas = time // 60
    horas = f'0{str(horas)}' if len(str(horas)) == 1 else str(horas)

    minutos = time % 60
    minutos = f'0{str(minutos)}' if len(str(minutos)) == 1 else str(minutos)
    return f'{time//60}:{time%60}'

def create_hours_dict(nowInMinutes:int) -> dict[int:int]:
    """
    Cria um dicionario com cada chave sendo os próximos 11 minutos em minutos e os valores
    um horário fixo de 10 minutos a partir da chamada.
    """
    d_horarios = {}
    for i in range(11):
        d_horarios[nowInMinutes + i] = nowInMinutes + 10

    return d_horarios

def main():
    NOW = datetime.now()
    NOW_IN_MINUTES = 60*NOW.hour + NOW.minute
    d_horarios = create_hours_dict(NOW_IN_MINUTES)

    while True:
        NOW = datetime.now()
        NOW_IN_MINUTES = 60*NOW.hour + NOW.minute

        print('- Hora atual:', min_to_str(NOW_IN_MINUTES), 'ou', f'{NOW_IN_MINUTES} min', end=' ')
        print('| Próximo ônibus:', min_to_str(d_horarios[NOW_IN_MINUTES]), 'ou', f'{d_horarios[NOW_IN_MINUTES]} min')
        sleep(1)

main()