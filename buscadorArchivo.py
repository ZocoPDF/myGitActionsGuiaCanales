import os, re

# La idea de esta clase es que busque los nombres de los canales en el archivo .m3u, que
# tiene codificación utf-8.(si quito encoding='utf-8' no abre bien el fichero) para después asociarlos, a través de
# otra clase, a los canales del movistarplus.es/programacion-tv. Los nombres de los canales se buscan en el campo tvg-id
# para que el  tivimate los vea, no le vale otro campo.
class BuscadorDeCanalesEnArchivo():

    def __init__(self, pathToFile: str):
        self.pathToFile = pathToFile
        self.dicCanalesTv = {}
        self.leerArchivo()

    def leerArchivo(self, patron: str = '(?<=tvg-id=").*?(?=")'):
        try:
            fichero = open(self.pathToFile,"rt", encoding="utf-8")
            print("Archivo leído")
            self.__creaDiccionarioCanales__(fichero)
        except FileNotFoundError:
            print("hubo un problema al abrir el archivo")
        else:
            fichero.close()


    # Recorre el archivo, de texto m3u por ejemplo, y crea diccionario con los campos tvg-id:tvg-name.
    # En las lineas en las que encuentra tvg-name="|ES|. si tvg-id"|ES| existe tb limpia |ES|
    def __creaDiccionarioCanales__(self, fichero, patronKey: str ='(?<=tvg-id=").*?(?=")', patronValue: str ='(?<=tvg-name=").*?(?=")'):
        # if self.file != None:
        print("creando diccionario de canales...")
        for linea in fichero:
            if (linea.find('group-title="ESPANA') != -1):

                key = re.search(patronKey, linea) 
                value = re.search(patronValue, linea)
                if key is not None and value is not None:
                    if key.group() == "": key = value
                    self.dicCanalesTv[key.group()]= value.group()
                else:
                    raise Exception("tvg-id o tvg-name no están presentes, uno de ellos ha devuelto None")
        
        self.__limpiarDiccionario__()
        print(f"Diccionario creado, hay {len(self.dicCanalesTv)} canales")

    #eliminamos |ES| de keys y values
    def __limpiarDiccionario__(self):
        listaKeysParaCambiar=[]

        for key, value in self.dicCanalesTv.items():
            if value.find('|ES|') != -1:
                self.dicCanalesTv[key] = value[5:]

        for key, value in self.dicCanalesTv.items():
            if key.find('|ES|') != -1:
                listaKeysParaCambiar.append(key)
        
        for key in listaKeysParaCambiar:
            self.dicCanalesTv[key[5:]] = self.dicCanalesTv.pop(key)
        print("diccionario revisado")
        # print(self.dicCanalesTv)
        


    #crea una copia del archivo completando los campos tvg-id="" vacios con el campo tvg-name si existe, esto para cada línea.
    def completarIdsCanales(self, patronName: str ='(?<=tvg-name=").*?(?=")'):
        with open(self.pathToFile, 'rt', encoding="utf-8") as fichero:
            with open("/Users/Gestor/Documents/mio/paulo/vscode_mis_proyectos/python/project_07_guia_tv/corregido.m3u","w", encoding="utf-8") as fichero_corregido:
                for linea in fichero:
                    # si en la línea hay campo tvg-id vacío, y hay  tvg-name no vacío
                    if 'tvg-id=""' in linea and 'tvg-name="' in linea and 'tvg-name=""' not in linea:
                        print(linea)
                        #completo campo tvg-id vacío con el campo tvg-name no vacío
                        nombre = re.search(patronName, linea)
                        if nombre is not None:
                            linea = linea.replace('tvg-id=""', 'tvg-id="'+ nombre.group()+'"')
                            print(linea)
                        else:
                            raise Exception("el campo tvg-name no está presente, ha devuelto None")
                    fichero_corregido.write(linea)

# uso:
if __name__ == '__main__':
    buscador = BuscadorDeCanalesEnArchivo('/Users/Gestor/Documents/mio/paulo/vscode_mis_proyectos/python/project_07_guia_tv/copia.m3u')
    # buscador.completarIdsCanales()
    # for key, value in buscador.dicCanalesTv.items():
    #     print(key +':'+ value)

    