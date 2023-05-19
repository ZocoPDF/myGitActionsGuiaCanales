import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC



# La misión de esta clase es leer la web https://movistarplus.es/programacion-tv y extraer los datos de los programas
# para cada canal

class LectorDeWeb():
    def __init__(self, url="https://www.movistarplus.es/programacion-tv", timeout=3) -> None:
        self.url=url
        # self.response = requests.get(url)
        # self.bsoup = BeautifulSoup(self.response.content, 'html.parser')
        # self.parrilla = self.bsoup.find(name='body')#,attrs={'id':'parrilla'})
        # # print(self.parrilla.prettify())
        self.soup = None
        self.listCanales = []
        self.programacion = {} # {canal:{programa_n:{'titulo':'aaa', 'hora inicio':'aaa', 'categoria':'aaa' } } } => 3 niveles de dict

    def explorarPagina(self):
        # abrir una instacia de chrome
        driver = webdriver.Chrome()

        # navegar a una url
        driver.get(self.url)

        # esperar hasta que la página haya cargado el elemento div con xpath ....
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="parrilla"]/div[2]')))

        # almacenar contenido en variable html y cierro chrome
        html = driver.page_source
        driver.quit()

        # creación de instancia BeautifulSoup, le paso la pagina almacenada en html junto con el parser parsrer.html
        self.soup = BeautifulSoup(html, 'html.parser')

        # mi div clave es el de id='parrilla' => lo almaceno en una variable
        divParrilla = self.soup.find(name='div', attrs={'id':'parrilla'})

        # a partir del div id='parrilla' obtengo lista beautifulsoup de los divs con 'class'='container_fila' que contiene
        listadoDivsEnParrilla = divParrilla.find_all(name='div', attrs={'class':'container_fila'})
        # print(listadoDivsEnParrilla)
        # print(len(listadoDivsEnParrilla))
        for divCanal in listadoDivsEnParrilla:
            if divCanal.has_attr('data-cod'):
                self.listCanales.append(divCanal['data-cod'])
                self.extraerDatosCanal(divCanal) # paso al método el div del canal con 'data-cod'='canal'
        print(self.listCanales)
        print(self.programacion)

    def extraerDatosCanal(self, divChannel):
        # el nombre del canal
        canal = divChannel['data-cod']
        print(f"hasta aquí llega: {canal}")

        # para el  div de canal divChannel obtengo el div 'class'='fila' 
        divFila = divChannel.find(name='div')#, attr={'class':'fila'})

        # obtengo todos los divs hijos directos del div fila
        listaProgramas = divFila.find_all("div", recursive=False)

        # obtengo para cada programa, su título <a>, fecha de inicio <span> y categoria <div class='info-programa'
        dict = {}
        for programa in listaProgramas:
            titulo = programa.find(name='a').text
            horaInicio = programa.find(name='span').text
            categoria = programa.find(name='div', attr={'class':'info-programa'}).text

            dict.update({
                'programa_0'+listaProgramas.index('programa'):{
                    'titulo':titulo,
                    'horaInicio':horaInicio,
                    'categoria':categoria
            }})
        self.programacion.update({canal:dict})

        


        
    
    # obtener horas inicio y hora final en formato "YYYYMMDDHHMMSS + Zona Horaria" a partir
    # de la hora como str y de date
    def getHoras(self):
        pass
            

if __name__ == "__main__":
    lector = LectorDeWeb()
    lector.explorarPagina()
    