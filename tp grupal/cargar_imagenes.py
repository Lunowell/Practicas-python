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
def layout (alias):
    ruta_repositorio=cargar_ruta_repositorio(alias)
    boton_volver = [[sg.Button("< Volver", size=(20, 2), button_color=('black', 'skyblue'), font=('Helvetica', 12),key='volver')]]
    boton_guardar = [[sg.Button('Guardar', size=(20, 2), button_color=('black', 'skyblue'), font=('Helvetica', 12), key='guardar')]]
    columna= [sg.Column(boton_volver, element_justification='left', expand_x=True),
            sg.Column(boton_guardar, element_justification='rigth', expand_x=True)]
    columna_izquierda = [[sg.In(ruta_repositorio, size=(50, 1), enable_events=True, key="-CARPETA-",background_color='skyblue',text_color='black'),
    sg.Listbox(values=[], enable_events=True, size=(40, 20),key="-ARCHIVOS-",background_color='skyblue',text_color='black',sbar_arrow_color='black', sbar_background_color='skyblue', highlight_background_color='steelblue',highlight_text_color='white')]]
    #"""Hacer un boton que llame a etiquetar para que etiquete imagenes y despues las muestre en la listbox"""]
    layout = [
    [columna]
    ]
    return layout


"""Se le pasa "num" para saber la cantidad de fotos que hay que seleccionar y el alias para saber los direcctorios
a tomar de ese usuario"""
def cargar_imagenes (alias,nombre): 
    with open('coordenadas.json') as archivo_json:
        data = json.load(archivo_json)
    imagenes_seleccionadas = 0 #es un contador que se actualiza a medida que se seleccionan las fotos, se compara con num para saber hasta cuantas fotos hay que cargar
    for item in data:
        if item['image'] == nombre:
            # Acceder a la lista "text_boxes" dentro del JSON
            text_boxes = data[0]['text_boxes']
            # Obtener la cantidad de posiciones en la lista "text_boxes"
            num = len(text_boxes)
            break
    while imagenes_seleccionadas<(num+1):#le sumo uno a num porque arranca desde 0
        
        imagenes_seleccionadas += 1
    window = sg.Window("Cargar Imagenes", layout, element_justification= 'c', size=(1366,768), resizable=True)

    """que seleccione una foto (HAY QUE VER DONDE GUARDAR LAS IMAGENES SELECCIONADAS, O SE VAN AGREGANDO EN EL COLLAGE A MEDIDA QUE SE SELECCIONAN (el 
    problema aca es que va a haber que hacer una distincion por el collage que se selecciono) )
    """
