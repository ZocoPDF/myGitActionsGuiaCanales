import xml.etree.ElementTree as ET

import requests


class LectorDeWeb():
    def __init__(self, url="https://www.movistarplus.es/programacion-tv", timeout=3) -> None:
        self.response = requests.get(url)

    def __str__(self):
        return self.response.text

if __name__ == "__main__":
    datosxml='<programme><title></title></programme>'
    # lector = LectorDeWeb()
    # print(type(lector.response.text))
    # print(lector)
    # print (type(lector.response.content))
    prueba = ET.fromstring(datosxml)
    print(type(prueba))