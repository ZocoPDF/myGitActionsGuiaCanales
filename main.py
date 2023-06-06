from oculto_a_github.buscadorArchivo import BuscadorDeCanalesEnArchivo
from emparejador import *
from buscadorWeb import *
from escritorXml import *

buscadorArchivo = BuscadorDeCanalesEnArchivo('/Users/Gestor/Documents/mio/paulo/vscode_mis_proyectos/python/project_07_guia_tv/copia.m3u')
diccionarioCanalesArchivo = buscadorArchivo.dicCanalesTv

buscadorWeb = LectorDeWeb()
buscadorWeb.explorarPagina()
diccionarioCanalesWeb = buscadorWeb.dictCanales
diccionarioProgramacionWeb = buscadorWeb.programacion

diccionarioEmparejado = None
with open('emparejamientoEPG.json') as file:
    diccionarioEmparejado = json.loads(file.read())

# print(f"\n{diccionarioProgramacionWeb}\n{diccionarioEmparejado}\n{diccionarioCanalesWeb}\n")

# emparejador = EmparejadorCanales(diccionarioCanalesArchivo, diccionarioCanalesWeb)
# emparejador.analizaUnCanal(['#0','0#','vamos'])

escritor = EscritorXml(diccionarioProgramacionWeb,diccionarioEmparejado, diccionarioCanalesWeb)
escritor.construirXml()


