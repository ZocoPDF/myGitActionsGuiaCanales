import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

# clase que crea guia_01.xml a partir del 2 diccionarios, uno con los datos de programación y otro con
class EscritorXml():
    def __init__(self, dictProgramacion, dictCanalesEmparejados, dictCanalesMovistar ):
        self.programacion = dictProgramacion        # -> diccionario de BuscadorWeb {canal:{programa_n:{'titulo':'texto', 'hora inicio':'hh:mm', 'horaFin':'pixels' 'categoria':'texto' } } } => 3 niveles de dict
        self.canales = dictCanalesEmparejados       # -> diccionario de Emparejador {'cod canal m3u':'cod canal web movistar'}
        self.titulosCanales = dictCanalesMovistar   # -> diccionario de BuscadorWeb {'codigo canal movistar':'titulo canal movistar'}
    
    def construirXml(self):

        root = ET.Element("tv") #,attrib={'version':'2.0','encoding':'UTF-8', 'xmlns':'https://www.xmltv.org/xmltv'})
        
        # agregamos los elementos <channel>
        for canal in self.canales:
            channel = ET.SubElement(root, "channel", attrib={'id':canal})
            displayName = ET.SubElement(channel, "display-name")
            displayName.text = self.titulosCanales[self.canales[canal]]

        # agregamos los elementos <programme>
        for canal in self.programacion:
            for programa in self.programacion[canal]:
                programme = ET.SubElement(root, "programme", attrib={
                    'start':self.convertirFechas(self.programacion[canal][programa]['horaInicio']),
                    'stop':self.convertirPixelsEnFechas(self.programacion[canal][programa]['horaInicio'],
                                                        self.programacion[canal][programa]['horaFin']),
                    'channel':canal
                    })
                titulo = ET.SubElement(programme, "title")
                titulo.text = self.programacion[canal][programa]['titulo']
        
        # crea objeto ElementTree con el elemento raiz
        tree = ET.ElementTree(root)

        # Configura el formato de indentación y espaciado
        indentation = "  "  # Espacio de indentación (por ejemplo, 2 espacios)
        newline = "\n"     # Salto de línea

        # Genera el archivo XML con formato legible
        tree_str = ET.tostring(root, encoding="utf-8").decode("utf-8")
        tree_str = tree_str.replace("><", ">" + newline + "<")  # Agrega saltos de línea entre elementos
        # tree_str = tree_str.replace(">", ">" + indentation)    # Agrega indentación antes de cada elemento de cierre
        # tree_str = indentation + tree_str[len(indentation):]   # Ajusta la indentación del elemento raíz
        
        # Agrega el encoding al elemento <?xml ?>
        xml_declaration = '<?xml version="1.0" encoding="UTF-8"?>' + newline + tree_str
        
        # guardamos en un archivo
        with open("guia_01.xml", "w", encoding='UTF-8') as file:
            file.write(xml_declaration)

    # 'hh:mm' -> "YYYYMMDDHHMMSS + Zona Horaria"
    def convertirFechas(self, hora:str):
        hoyFecha = datetime.now().date()
        fechaHora = datetime.combine(hoyFecha, datetime.strptime(hora, "%H:%M").time(), tzinfo=timezone(timedelta(minutes=2)))
        return fechaHora.strftime("%Y%m%d%H%M%S %z")

    # obtener hora fin en formato hh:mm a partir de la hora de inicio y duración en pixels, 20/100 min/pixel
    def convertirPixelsEnFechas(self, hora:str, pixels:str):
        minutos = int(pixels)*20/100
        hoyFecha = datetime.now().date()
        fechaHora = datetime.combine(hoyFecha, datetime.strptime(hora, "%H:%M").time(), tzinfo=timezone(timedelta(minutes=2)))
        fechaHoraFin = fechaHora + timedelta(minutes=minutos)
        return fechaHoraFin.strftime("%Y%m%d%H%M%S %z")