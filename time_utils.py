"""Esse arquivo contém todas as funções relacionadas à manipulação de tempo.
"""
# Use locale to set the default locale
# that converts literals to portuguese

def is_business_day (day: int) -> bool:
    """Receives days as int, Monday = 0, Tuesday = 1, ..., Sunday = 6
       and Returns True if it is a business day, False otherwise
    """
    return day < 5

# BUG Esse modulo não tem muita utilidade,
# tudo o que ele faz é ter uma função que ja ta implementado no datetime