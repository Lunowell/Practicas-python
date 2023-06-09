import PySimpleGUI as sg
import os
import io
import json
import csv

""" Esta funcion verifica si las rutas fueron cargadas previamente en la configuracion """            
def cargar_ruta_repositorio(alias):
    #Verifica si el archivo directorio existe, sino lo informa 
    r=''
    if os.path.exists('directorios.json'):
        with open('directorios.json','r') as archivo:
            #Se verifica si el archivo esta vacio, si es asi lo notifica.
            if (os.stat('directorios.json').st_size == 0):
                sg.popup('No se cargo ninguna ruta')
            else:
                #cargar rutas cargadas en configuracion
                contenido_archivo = json.load(archivo)
                rutas = list(filter(lambda a: a['Alias']==alias, contenido_archivo))
                r=rutas[0]['R_Imagenes']
    return r
def layout (alias):
    ruta_repositorio=cargar_ruta_repositorio(alias)
    columna_izquierda = [
    [sg.In(ruta_repositorio, size=(50, 1), enable_events=True, key="-CARPETA-",background_color='skyblue',text_color='black'),
     sg.FolderBrowse('Buscar',button_color='skyblue')]
    ]
    return layout
"""La siguiente funcion se hace con el fin listar las imagenes en la listbox"""
def desplegar_lista(ruta_carpeta,window):
    try:
        lista_archivos = os.listdir(ruta_carpeta)
    except:
        lista_archivos =[]
    #desplegamos la lista de archivos que podemos abrir que se encuentren en la carpeta seleccionada    
    nombres_archivos = [
        arc #archivo de la carpeta
        for arc in lista_archivos
        if os.path.isfile(os.path.join(ruta_carpeta, arc))
        and arc.lower().endswith((".png",".gif"))
        ]
    window["-ARCHIVOS-"].update(nombres_archivos)
"""Se le pasa "num" para saber la cantidad de fotos que hay que seleccionar"""
def cargar_imagenes (num,alias): 
    imagenes_seleccionadas = 0 #es un contador que se actualiza a medida que se seleccionan las fotos, se compara con num para saber hasta cuantas fotos hay que cargar
    if (imagenes seleccionadas<num):
        """que seleccione una foto (HAY QUE VER DONDE GUARDAR LAS IMAGENES SELECCIONADAS, O SE VAN AGREGANDO EN EL COLLAGE A MEDIDA QUE SE SELECCIONAN (el 
        problema aca es que va a haber que hacer una distincion por el collage que se selecciono) )"""
#PASAR: ALIAS 
    """ HAY QUE PASAR POR PARAMETRO LA CANTIDAD DE IMAGENES QUE SE PUEDEN SELECCIONAR """