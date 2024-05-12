import requests
from datetime import datetime
from timeUtils import *
from websiteRequest import *



# Restaurantes
class Restaurantes:

    """
    Essa classe é para a criação dos objetos restaurante
    """

    def __init__(self, cafe, almoco, janta, domingo):
        self.horariosCafe = cafe
        self.horariosAlmoco = almoco
        self.horariosJantar = janta
        self.abreDomingo = domingo

ru = Restaurantes(['07:30','08:30'], ['10:30','14:00'], ['17:30','19:45'], False)
ra = Restaurantes(None, ['11:15','14:00'], ['17:30','19:00'], False)
rs = Restaurantes(None, ['11:00','14:00'], ['17:30','19:00'], True)

ru.nome = 'ru'
rs.nome = 'rs'
ra.nome = 'ra'

# Web scraping do cardápio diretamente do site da prefeiura unicamp

# Funções

def rest():
    return ru, ra, rs

def webScrapingCardapio(data, diaSemana):
    """
    Essa função faz o web scraping do site da prefeitura e determina o path para cada refeição.
    E possível ver o cardápio de outros dias da semana, e para isso é preciso colocar a URL
    correspondente. 
    """

    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0"}

    URL = f"https://www.prefeitura.unicamp.br/apps/cardapio/index.php?d={data.date()}"

    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.text, 'html.parser')   

    # Paths
    refeicoes = soup.find_all(class_="col-xs-12")

    class Refeicao:

        """
        Essa classe é de cada refeição (Almoço e Janta) contendo a proteína, base, complemento, salada, fruta e suco.
        """

        def __init__(self, path):

            self.path = path
            self.description = self.path.find(class_="menu-item-description").text.splitlines()

            # Arrumando os items da lista self.resto
            dump = []
            cardapio = []
            self.description.pop(0)
            for item in self.description:
                dump += item.splitlines()
            elementos = dump[1].strip().split('                    ')
            dump.pop(-1)
            dump.pop(-1)

            # Adicionando items do cardápio
            cardapio.append(self.path.find(class_="menu-item-name").text.capitalize()) # Proteína
            cardapio.append(dump[0].strip().capitalize()) # Base
            for item in elementos: # Complemento, salada, fruta, suco
                cardapio.append(item.capitalize())
            cardapio[-1] = cardapio[-1][:-13]

            # Observações
            self.observacoes = []
            for i in dump[2:]:
                i = i.strip().capitalize()
                self.observacoes.append(i)

            # Cardápio
            self.proteina = cardapio[0]
            self.base = cardapio[1]
            self.complemento = cardapio[2]
            self.salada = cardapio[3]
            self.fruta = cardapio[4]
            self.suco = cardapio[5]

    if diaSemana == "Domingo":
        almocoTradicional_path = refeicoes[0]
        almocoVegano_path = refeicoes[1]

        almocoTradicional = Refeicao(almocoTradicional_path)
        almocoVegano = Refeicao(almocoVegano_path)

        return almocoTradicional, almocoVegano
    
    else:
        almocoTradicional_path = refeicoes[0]
        almocoVegano_path = refeicoes[1]
        jantarTradicional_path = refeicoes[2]
        jantarVegano_path = refeicoes[3]

        almocoTradicional = Refeicao(almocoTradicional_path)
        almocoVegano = Refeicao(almocoVegano_path)
        jantarTradicional = Refeicao(jantarTradicional_path)
        jantarVegano = Refeicao(jantarVegano_path)

        return almocoTradicional, almocoVegano, jantarTradicional, jantarVegano

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
