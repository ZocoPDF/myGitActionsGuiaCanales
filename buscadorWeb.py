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
        self.soup = None
        self.dictCanales = {}   # diccionario {'codigo canal movistar':'titulo canal movistar'}
        self.programacion = {}  # {canal:{programa_n:{'titulo':'aaa', 'hora inicio':'aaa', 'horaFin':'aaa' 'categoria':'aaa' } } }
                                # => 3 niveles de dict

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
        # para los canales el elemento clave es ul id='lista_canales'
        divParrilla = self.soup.find(name='div', attrs={'id':'parrilla'})
        ulCanales = self.soup.find(name='ul', attrs={'id':'lista_canales'})
        self.anotarCanales(ulCanales)

        # a partir del div id='parrilla' obtengo lista beautifulsoup de los divs con 'class'='container_fila' que contiene
        listadoDivsEnParrilla = divParrilla.find_all(name='div', attrs={'class':'container_fila'})#, limit=5)
        for divCanal in listadoDivsEnParrilla:
            if divCanal.has_attr('data-cod'):
                self.extraerDatosCanal(divCanal) # paso al método el div del canal con 'data-cod'='canal'

    # con este método se llena el diccionario de la programación
    def extraerDatosCanal(self, divChannel):
        if divChannel == None:
            raise Exception("divChannel vacío, tal vez la web no se haya explorado")
        # el nombre del canal
        canal = divChannel['data-cod']
        # print(f"hasta aquí llega: {canal}")

        # para el  div de canal divChannel obtengo el div 'class'='fila' 
        divFila = divChannel.find(name='div', attrs={'class':'fila'})
        

        # obtengo todos los divs hijos directos del div fila
        listaProgramas = divFila.find_all(name='div', recursive=False)
        # print(len(listaProgramas))

        # obtengo para cada programa, su título <a>, fecha de inicio <span> y categoria <div class='info-programa'
        dict = {}
        for programa in listaProgramas:
            if programa.find('div') == None: continue
            titulo = programa.find(name='a').text
            horaInicio = programa.find(name='span').text
            horaFin = programa['style'][7:][:-3]
            categoria = (programa.find(name='div', attrs={'class':'info-programa'})).find(string=True, recursive=False).strip()
            # print(f"{titulo} : {horaInicio} : {categoria}")

            dict.update({
                canal+'_p0'+str(listaProgramas.index(programa)):{
                    'titulo':titulo,
                    'horaInicio':horaInicio,
                    'horaFin':horaFin,
                    'categoria':categoria
            }})
        self.programacion.update({canal:dict})

    # con este método llenamos el diccionario de canales dictCanales
    def anotarCanales(self, ulCanales):
        if ulCanales == None:
            raise Exception("divChannel vacío, tal vez la web no se haya explorado")
        
        listaCanales = ulCanales.find_all(name='li', recursive=False)
        for li in listaCanales:
            self.dictCanales[li['data-cod']]=li.find(name='img')['title']
            

if __name__ == "__main__":
    lector = LectorDeWeb()
    lector.explorarPagina()
    # print(lector.listCanales)
    print(f"MV1 programas:\n{lector.programacion['MV1']}")
    print(lector.dictCanales)
    