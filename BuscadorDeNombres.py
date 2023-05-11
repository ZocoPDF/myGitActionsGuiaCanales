import os, re

#La idea de esta clase es que busque los nombres de los canales en el archivo .m3u, que
#tiene codificación utf-8.(si quito encoding='utf-8' no abre bien el fichero) para después asociarlos
#a los canales del movistarplus.es/programacion-tv. para tivimate el capo necesario es tvg-id
class BuscadorDeCanales():

    def __init__(self, pathToFile: str):
        self.pathToFile = pathToFile
        self.file = None
        self.dicCanalesTv = {}
        self.leerArchivo()

    def leerArchivo(self, patron: str = '(?<=tvg-id=").*?(?=")'):
        try:
            self.file = open(self.pathToFile,"rt", encoding="utf-8")
            print("Archivo leído")
        except FileNotFoundError:
            print("hubo un problema al abrir el archivo")
        # with open(self.pathToFile, 'rt', encoding="utf-8") as file:
        #     self.file = file
        # file.close()
    
    # def leerLinea(self, linea: int):
    #     if self.file != None:
    #         for i in range(linea + 1):
    #             if (i == linea):
    #                 miLinea = self.file.readline()
    #             self.file.readline()
    #         self.file.close()
    #         return miLinea
    #     else:
    #         print("No hay archivo leído, leelo primero")
    #     print(miLinea)
    #     print(type(miLinea))
    #     self.file.close()
    #     return None
    
    # Recorre el archivo, en principio m3u, y crea diccionario con los campos tvg-id:tvg-name.
    # En las lineas en las que encuentra tvg-name="|ES|
    def creaDiccionarioCanales(self, patronKey: str ='(?<=tvg-id=").*?(?=")', patronValue: str ='(?<=tvg-name="\|ES\|\s).*?(?=")'):
        # self.leerArchivo()
        if self.file != None:
            print("creando diccionario de canales...")
            for linea in self.file:
               if (linea.find('tvg-name="|ES|') != -1):
                #    print(linea)
                   key = re.search(patronKey, linea)
                   value = re.search(patronValue, linea)
                #    if(key == None or len(key.group()) == 0):key=value.group()
                #    else:key=key.group()
                #    if(value==None):value=key.group()
                #    else:value=value.group()
                #    print(key, value, type(key), type(value))
                   self.dicCanalesTv[key.group()]= value.group()
            self.file.close()
            print(f"hay {len(self.dicCanalesTv)} canales")
            # return self.dicCanalesTv
        else:
            print("No hay archivo leído, leelo primero")

        # return None
        #leer primera línea

        #busca el patrón de interés en la línea

            #si existe añade al diccionario el par "a":"b"
    #crea una copia del archivo completando los campos tvg-id="" vacios con el campo tvg-name
    def completarIdsCanales(self, patronName: str ='(?<=tvg-name="\|ES\|\s).*?(?=")'):
        if self.file == None: self.leerArchivo()
        for linea in self.file:
            if 'tvg-id=""' in linea:
                pass# linea.replace('tvg-id=""', )


        

                


if __name__ == '__main__':
    buscador = BuscadorDeCanales('/Users/Gestor/Documents/mio/paulo/vscode_mis_proyectos/python/project_07_guia_tv/copia.m3u')
    buscador.creaDiccionarioCanales()
    # buscador.leerArchivo()
    # linea = buscador.leerLinea(2)
    # print(linea)
    # search = re.search('(?<=tvg-id=").*?(?=")', linea)
    # print(type(search))
    # print(search.start(), search.end())
    # print(search.group())
    # print(re.Match.__dict__)
    # print(buscador.creaDiccionarioCanales())
    print(buscador.dicCanalesTv)

    