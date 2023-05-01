import requests
import xml.etree.ElementTree as ET

class LectorDeWeb():
    def __init__(self, url="https://www.movistarplus.es/programacion-tv", timeout=1) -> None:
        self.response = requests.get(url)
    
    def __str__(self):
        return self.response.text

if __name__ == "__main__":
    lector = LectorDeWeb()
    print (lector.response.headers)

