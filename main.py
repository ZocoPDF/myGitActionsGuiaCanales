from buscadorArchivo import BuscadorDeCanalesEnArchivo
import buscadorWeb

buscador = BuscadorDeCanalesEnArchivo('/Users/Gestor/Documents/mio/paulo/vscode_mis_proyectos/python/project_07_guia_tv/copia.m3u')
diccionarioCanales = buscador.dicCanalesTv
for key, value in diccionarioCanales.items():
    print(key + ' : ' + value)