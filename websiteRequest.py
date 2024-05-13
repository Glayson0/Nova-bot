from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
import base64
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


class Camera:
    def __init__(self) -> None:
        pass

ru_camera = Camera()
ra_camera = Camera()
rs_camera = Camera()


def webScrapingCamera(restaurante, data):

    URL = f"https://www.prefeitura.unicamp.br/apps/cardapio/index.php?d={data.date()}"

    ## Selenium 

    # Configura as opções do navegador para headless
    options = Options()
    options.add_argument("--headless")

    driver = webdriver.Firefox(options=options) # Inicia o navegador

    driver.get(URL) # Navega para a página web

    driver.implicitly_wait(1)

    ## BeautifulSoup4

    if restaurante.nome == 'ru':

        botao = driver.find_element('xpath', '//*[@id="thumbnail_ru_a"]')

        botao.click()
        driver.implicitly_wait(1)

        content = driver.page_source
        soup = BeautifulSoup(content, 'html.parser')
        driver.quit() # Fecha o navegador

        try:
            image_url = soup.find(id="img_camera_ru_a")["src"]
        except:
            webScrapingCamera(restaurante, data)

        _, encoded_image = image_url.split(",", 1)
        image_data = base64.b64decode(encoded_image)

        # Carrega a imagem a partir dos dados decodificados
        ru_camera.imagem = Image.open(BytesIO(image_data))

        # Converte a imagem para o formato PNG (ou JPEG, se preferir)
        # Aqui estamos convertendo para PNG
        output_buffer = BytesIO()
        ru_camera.imagem.save(output_buffer, format="PNG")
        output_buffer.seek(0)

        ru_camera.pessoas = soup.find(id="cam_data2_ru_a").text

        return ru_camera

    elif restaurante.nome == 'ra':

        botao = driver.find_element('xpath', '//*[@id="thumbnail_ra"]')
        botao.click()
        driver.implicitly_wait(1)

        content = driver.page_source
        soup = BeautifulSoup(content, 'html.parser')
        driver.quit() # Fecha o navegador

        try:
            image_url = soup.find(id="img_camera_ra")["src"]
        except:
            webScrapingCamera(restaurante, data)

        _, encoded_image = image_url.split(",", 1)
        image_data = base64.b64decode(encoded_image)

        # Carrega a imagem a partir dos dados decodificados
        ra_camera.imagem = Image.open(BytesIO(image_data))

        # Converte a imagem para o formato PNG (ou JPEG, se preferir)
        # Aqui estamos convertendo para PNG
        output_buffer = BytesIO()
        ra_camera.imagem.save(output_buffer, format="PNG")
        output_buffer.seek(0)
        
        ra_camera.pessoas = soup.find(id="cam_data2_ra").text

        return ra_camera

    else:

        botao = driver.find_element('xpath', '//*[@id="thumbnail_rs"]')
        botao.click()
        driver.implicitly_wait(1)

        content = driver.page_source
        soup = BeautifulSoup(content, 'html.parser')
        driver.quit() # Fecha o navegador

        try:
            image_url = soup.find(id="img_camera_rs")["src"]
        except:
            webScrapingCamera(restaurante, data)

        _, encoded_image = image_url.split(",", 1)
        image_data = base64.b64decode(encoded_image)

        # Carrega a imagem a partir dos dados decodificados
        rs_camera.imagem = Image.open(BytesIO(image_data))

        # Converte a imagem para o formato PNG (ou JPEG, se preferir)
        # Aqui estamos convertendo para PNG
        output_buffer = BytesIO()
        rs_camera.imagem.save(output_buffer, format="PNG")
        output_buffer.seek(0)
        
        rs_camera.pessoas = soup.find(id="cam_data2_rs").text

        return rs_camera