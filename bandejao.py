import requests
from datetime import datetime
from timeUtils import *
from webScraping import *

# Restaurantes
class Restaurante:
    """
    Essa classe é para a criação dos objetos restaurante
    """

    def __init__(self, cafe, almoco, janta, abreNoDomingo):
        self.horariosCafe = cafe
        self.horariosAlmoco = almoco
        self.horariosJantar = janta
        self.abreDomingo = abreNoDomingo

ru = Restaurante(['07:30','08:30'], ['10:30','14:00'], ['17:30','19:45'], False)
ra = Restaurante(None, ['11:15','14:00'], ['17:30','19:00'], False)
rs = Restaurante(None, ['11:00','14:00'], ['17:30','19:00'], True)

ru.nome = 'ru'
rs.nome = 'rs'
ra.nome = 'ra'

class Alimentos:
    """
    Essa classe é para a atribuição de alimentos de uma refeição.
    """

    def __init__(self, alimentos: list):

        self.proteina = alimentos[0]
        self.base = alimentos[1]
        self.complemento = alimentos[2]
        self.salada = alimentos[3]
        self.fruta = alimentos[4]
        self.suco = alimentos[5]
class Refeicao:
        """
        Essa classe é para a criação de uma refeição com atributos: proteína, base, complemento, salada, fruta e suco.
        """

        def __init__(self, pathAlmoco: str, pathJantar: str):

            ##
            ##  Almoço
            ##

            almoco = Alimentos(getAlimentos(pathAlmoco))

            # Cardápio Almoço Tradicional
            self.proteina = cardapio[0]
            self.base = cardapio[1]
            self.complemento = cardapio[2]
            self.salada = cardapio[3]
            self.fruta = cardapio[4]
            self.suco = cardapio[5]

# Web scraping do cardápio diretamente do site da prefeiura unicamp

# Funções

def rest():
    return ru, ra, rs

def getAlimentos(path: str) -> list:
    """
    Essa função pega os alimentos do path fornecido e retorna uma lista de strings com os alimentos
    na seguinte ordem: [Proteina, Base, Complemento, Salada, Fruta, Suco]
    """

    alimentos = path.find(class_="menu-item-description").text.splitlines()

    #   Arrumando os items da lista self.resto
    dump = []
    alimentos = []
    alimentos.pop(0)

    for item in alimentos:
        dump += item.splitlines()
    elementos = dump[1].strip().split('                    ')
    dump.pop(-1)
    dump.pop(-1)

    # Adicionando items do cardápio
    alimentos.append(path.find(class_="menu-item-name").text.capitalize()) # Proteína
    alimentos.append(dump[0].strip().capitalize()) # Base
    for item in elementos: # Complemento, salada, fruta, suco
        alimentos.append(item.capitalize())
    alimentos[-1] = alimentos[-1][:-13]

    return alimentos

def getCardapio(date: datetime, cardapio: str) -> tuple:
    """
    Essa função faz o web scraping do site da prefeitura e determina o path para cada refeição.
    E possível ver o cardápio de outros dias da semana, e para isso é preciso colocar a URL
    correspondente.
    
    Args:
    - date: a data do cardápio.
    - cardapio: qual cardápio deseja extrair
        - 'Tradicional'
        - 'Vegano"
    """

    # Extraindo código HTML da página da prefeitura Unicamp
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0"}

    URL = f"https://www.prefeitura.unicamp.br/apps/cardapio/index.php?d={date}"

    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.text, 'html.parser')   

    # Paths das refeições
    refeicoes = soup.find_all(class_="col-xs-12")

    try:

        if cardapio == 'Tradicional':

            almocoTradicional_path = refeicoes[0]
            jantarTradicional_path = refeicoes[2]

            refeicaoTradicional = Refeicao(almocoTradicional_path, jantarTradicional_path)
        
        elif cardapio == 'Vegano':

            almocoVegano_path = refeicoes[1]
            jantarVegano_path = refeicoes[3]

        almocoVegano = Refeicao(almocoVegano_path)
        jantarTradicional = Refeicao(jantarTradicional_path)
        jantarVegano = Refeicao(jantarVegano_path)

        return almocoTradicional, almocoVegano, jantarTradicional, jantarVegano
    except:
        almocoTradicional_path = refeicoes[0]
        almocoVegano_path = refeicoes[1]

        almocoTradicional = Refeicao(almocoTradicional_path)
        almocoVegano = Refeicao(almocoVegano_path)

    return almocoTradicional, almocoVegano

def status(horaAtual, diaAtual, restaurante):

    """
    Essa função determina:
    - status do restaurante: Aberto ou Fechado
    - qual é ou qual será a refeição do momento
    - quanto tempo falta para começar/acabar a refeição
    """
    
    if diaAtual == 'Domingo' and restaurante.abreDomingo:
        # Café da manha
        if restaurante.horariosCafe != None:

            if horaAtual < strToTime(restaurante.horariosCafe[1]):

                if horaAtual < strToTime(restaurante.horariosCafe[0]):
                    restaurante.status = 'Fechado'
                    restaurante.refeicao = '*Próxima refeição:* Café da Manhã'
                    restaurante.timeLeft = getTimeDifference(horaAtual, restaurante.horariosCafe[0])
                    restaurante.tempo = f'{formatingDiffTime(restaurante.horariosCafe[1], restaurante.timeLeft)} para começar'

                else:
                    restaurante.status = 'Aberto'
                    restaurante.refeicao = '*Refeição atual:* Café da Manhã'
                    restaurante.timeLeft = getTimeDifference(restaurante.horariosCafe[1], horaAtual)
                    restaurante.tempo = f'{formatingDiffTime(restaurante.horariosCafe[1], restaurante.timeLeft)} para terminar'


        # Almoço
        if horaAtual < strToTime(restaurante.horariosAlmoco[1]):

            if horaAtual < strToTime(restaurante.horariosAlmoco[0]):
                restaurante.status = 'Fechado'
                restaurante.refeicao = '*Próxima refeição:* Almoço'
                restaurante.timeLeft = getTimeDifference(horaAtual, restaurante.horariosAlmoco[0])
                restaurante.tempo = f'{formatingDiffTime(restaurante.horariosAlmoco[0], restaurante.timeLeft)} para começar'

            else:
                restaurante.status = 'Aberto'
                restaurante.refeicao = '*Refeição atual:* Almoço'
                restaurante.timeLeft = getTimeDifference(restaurante.horariosAlmoco[1], horaAtual)
                restaurante.tempo = f'{formatingDiffTime(restaurante.horariosAlmoco[1], restaurante.timeLeft)} para terminar'

        # Sem refeições
        else:
            restaurante.status = 'Fechado'
            restaurante.refeicao = 'Acabaram as refeições de hoje'
            restaurante.timeLeft = 'Só amanhã agora :\/'
            restaurante.tempo = 'Só amanhã agora :\/'
    else:
        restaurante.status = 'Fechado'
        restaurante.refeicao = 'Não abre aos domingos'
        restaurante.timeLeft = 'Não abre aos domingos'
        restaurante.tempo = 'Agora é só segunda\-feira'
    
    if diaAtual in 'Segunda Terça Quarta Quinta Sexta Sábado':
        # Café da manha
        if restaurante.horariosCafe != None:

            if horaAtual < strToTime(restaurante.horariosCafe[1]):

                if horaAtual < strToTime(restaurante.horariosCafe[0]):
                    restaurante.status = 'Fechado'
                    restaurante.refeicao = '*Próxima refeição:* Café da Manhã'
                    restaurante.timeLeft = getTimeDifference(horaAtual, restaurante.horariosCafe[0])
                    restaurante.tempo = f'{formatingDiffTime(restaurante.horariosCafe[1], restaurante.timeLeft)} para começar'

                else:
                    restaurante.status = 'Aberto'
                    restaurante.refeicao = '*Refeição atual:* Café da Manhã'
                    restaurante.timeLeft = getTimeDifference(restaurante.horariosCafe[1], horaAtual)
                    restaurante.tempo = f'{formatingDiffTime(restaurante.horariosCafe[1], restaurante.timeLeft)} para terminar'


        # Almoço
        if horaAtual < strToTime(restaurante.horariosAlmoco[1]):

            if horaAtual < strToTime(restaurante.horariosAlmoco[0]):
                restaurante.status = 'Fechado'
                restaurante.refeicao = '*Próxima refeição:* Almoço'
                restaurante.timeLeft = getTimeDifference(horaAtual, restaurante.horariosAlmoco[0])
                restaurante.tempo = f'{formatingDiffTime(restaurante.horariosAlmoco[0], restaurante.timeLeft)} para começar'

            else:
                restaurante.status = 'Aberto'
                restaurante.refeicao = '*Refeição atual:* Almoço'
                restaurante.timeLeft = getTimeDifference(restaurante.horariosAlmoco[1], horaAtual)
                restaurante.tempo = f'{formatingDiffTime(restaurante.horariosAlmoco[1], restaurante.timeLeft)} para terminar'


        # Jantar
        elif horaAtual < strToTime(restaurante.horariosJantar[1]):

            if horaAtual < strToTime(restaurante.horariosJantar[0]):
                restaurante.status = 'Fechado'
                restaurante.refeicao = '*Próxima refeição:* Jantar'
                restaurante.timeLeft = getTimeDifference(horaAtual, restaurante.horariosJantar[0])
                restaurante.tempo = f'{formatingDiffTime(restaurante.horariosJantar[0], restaurante.timeLeft)} para começar'

            else:
                restaurante.status = 'Aberto'
                restaurante.refeicao = '*Refeição atual:* Jantar'
                restaurante.timeLeft = getTimeDifference(restaurante.horariosJantar[1], horaAtual)
                restaurante.tempo = f'{formatingDiffTime(restaurante.horariosJantar[1], restaurante.timeLeft)} para terminar'

        # Sem refeições
        else:
            restaurante.status = 'Fechado'
            restaurante.refeicao = 'Acabaram as refeições de hoje'
            restaurante.timeLeft = 'Só amanhã agora :\/'
            restaurante.tempo = 'Só amanhã agora :\/'

def camRestaurante(diaAtual, restaurante):

    """
    Essa função retorna a imagem e os dados da camera do restaurante escolhido
    
    Parâmetros:
    - restaurante: ru, ra, rs
    """

    restaurante.camera = webScrapingCamera(restaurante, diaAtual)

    return restaurante
