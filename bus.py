"""
Esse arquivo contém todas as funções relacionadas aos ônibus da Unicamp.
"""
import datetime as dt

from busSchedule import *
from time_utils import *


# Funções auxiliares
def next_bus_from_now() -> tuple[str, str]:
    """Retorna o horário em datetime do próximo ônibus a partir do horário em que a função foi chamada."""
    day_type = is_business_day(dt.datetime.now().weekday())
    day_type = "business_day" if day_type else "weekend"

    return BUS_SCHEDULER[day_type]

# Funções principais
def createNextBusMessage() -> str:
    # TODO
    # Pode implementar o resto com a nova lógica :p

    # String formatada
    next2busText = f"""
🚌 HORÁRIOS DOS PRÓXIMOS ÔNIBUS

⌚ Horário atual: {dt_to_str(CURRENT_DATETIME)}

➡️ IDA \(Moradia \-\> Unicamp\):
    01\) \) \) \) \) \) \) \) \) \) \) \) \) \) \) \) ) \) ) ) \) ) ) \) ) ) \) ) ) \) ) ) \) ) ) \) ) ) \) ) ) \) ) ) \) ) ) \) ) ) \) ) ) \) ) ) \) ) ) \) ) ) \) ) ) \) ) ) \) ) ) \) ) ) \) ) ) \) ) ) \) ) ) \) {timesOutput[0]}
    02\) {timesOutput[1]}

⬅️ VOLTA \(Unicamp \-\> Moradia\):
    01\) {timesOutput[2]}
    02\) {timesOutput[3]}
"""
    return next2busText

def createAvailableBusListMessage(busSchedule:list) -> str:
    """Cria uma string com todos os horários do dia de ônibus, riscando os horários que já passaram e destacando o próximo."""
    # BUG
    # Retornar toda a lista de onibus que ja foram não vale a pena
    # É muita informação e provavelmente o usuario não quer
    # Mas pode reeimplementar isso se quiser usando a nova lógica
