import json
import os

# esta clase tendrá la responsabilidad de linkar los canales m3u con los de la web movistar
# y almacenar el dictEPG en un archivo json
class EmparejadorCanales():
    #diccionario con codigos unicode para eliminar acentos áéíóúüñ -ÁÉÍÓÚ/àèìòùÀÈÌÒÙ\'çïÏ => aeiouun__aeiou_aeiouaeiou_cii
    TABLA = {
        225: 97, 233: 101, 237: 105, 243: 111, 250: 117, 252: 117,
        241: 110, 32: 95, 45:95,  193: 97, 201: 101, 205: 105,
        211: 111, 218: 117, 47: 95, 224: 97, 232: 101, 236: 105,
        242: 111, 249: 117, 192: 97, 200: 101, 204: 105, 210: 111,
        217: 117, 39: 95, 231: 99, 239: 105, 207: 105
    }

    def __init__(self, dictCanalesM3u, dictCanalesWeb):
        self.dictM3u = dictCanalesM3u
        self.dictWeb = dictCanalesWeb
        

    def analizaUnCanal(self, canales:list):
        if os.path.isfile('emparejamientoEPG.json'):
            # el archivo existe, lo abro
            with open('emparejamientoEPG.json','r',encoding='utf-8') as file:
                contenido = file.read()
                # si no está vacío lo guardo como python dict
                if contenido:
                    dictEmparejamientoEPG = json.loads(contenido)
                # si está vacío inicializo el diccionario python
                else:
                    dictEmparejamientoEPG = {}
        else:
            dictEmparejamientoEPG = {}

        print(dictEmparejamientoEPG, type(dictEmparejamientoEPG))
        for canal in canales:
            i=0
            j=0
            for k, v in self.dictM3u.items():
                if canal.casefold().translate(EmparejadorCanales.TABLA) in v.casefold().translate(EmparejadorCanales.TABLA) and k not in dictEmparejamientoEPG:
                    print(f"En diccionario 1 {canal} -> {k}:{v}")
                    k1Temp = k
                    i+=1
            for k, v in self.dictWeb.items():
                if canal.casefold().translate(EmparejadorCanales.TABLA) in v.casefold().translate(EmparejadorCanales.TABLA) and i!=0:# and k not in dictEmparejamientoEPG.values():
                    print(f"En diccionario 2 {canal} -> {k}:{v}")
                    k2Temp = k
                    j+=1
            if i == 1 and j == 1:
                dictEmparejamientoEPG.update({k1Temp:k2Temp})
                with open('emparejamientoEPG.json','w',encoding='utf-8') as file:
                    file.write(json.dumps(dictEmparejamientoEPG, indent=4))