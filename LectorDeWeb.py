import xml.etree.ElementTree as ET
from lxml import etree
import requests


class LectorDeWeb():
    def __init__(self, url="https://www.movistarplus.es/programacion-tv", timeout=3) -> None:
        self.response = requests.get(url)

    def __str__(self):
        return self.response.text

if __name__ == "__main__":
    datosxml='<programme><title></title></programme>'
    lector = LectorDeWeb()
    # print(type(lector.response.text))
    # print(lector)
    # print (type(lector.response.content))
    # prueba = ET.fromstring(datosxml)
    # print(type(prueba))
    parser = etree.HTMLParser()
    tree = etree.parse(lector.response.text, parser)
    result = etree.tostring(tree.getroot(), pretty_print=True, method="html")
    # print(type(result))
    