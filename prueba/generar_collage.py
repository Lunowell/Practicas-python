import PySimpleGUI as sg
from PIL import Image 
import json
import utilidades.abrir_fotos as abrir_foto
import os
from utilidades.constantes import ROOT_PATH
import csv

sg.theme ('LightGrey4')
def buscar_csv (alias_buscar):   
    nombres_imagenes = []
    with open('perfiles.csv', newline='') as archivo_csv:
        lector_csv = csv.reader(archivo_csv)
        for fila in lector_csv:
            nombre_imagen = fila[3] # Obtener el nombre de la imagen 
            alias = fila[1]  # Obtener el alias 
            
            if alias == alias_buscar:
                nombres_imagenes.append(nombre_imagen)
    return nombres_imagenes
def obtener(alias):
    nombres_imagenes = buscar_csv(alias)

    if nombres_imagenes:
        with open('directorios.json') as file:
            data = json.load(file)
            for item in data:
                if item['Alias'] == alias:
                    ruta_imagenes = item['R_Imagenes']
                    break

        imagenes = []
        for nombre_imagen in nombres_imagenes:
            ruta_imagen = os.path.join(ruta_imagenes, nombre_imagen)
            imagenes.append(ruta_imagen)
        return imagenes

    return []

def pegar_imagenes(plantilla,cantidad_textboxes, imagenes, coordenadas, x, y):
    plantilla_seleccionada = Image.open(plantilla)
    for i in range(cantidad_textboxes):
        imagen = Image.open(imagenes[i])
        posicion = coordenadas[i]
        imagen = imagen.resize((x, y))
        plantilla_seleccionada.paste(imagen, posicion)
    return plantilla_seleccionada
def layout_generar_collage(alias,plantilla):
    imagenes= obtener(alias)
    boton_volver = [[sg.Button("< Volver", 
                size=(20, 2), 
                button_color=('black', 'skyblue'), 
                font=('Helvetica', 12),
                key='-VOLVER-')]]
    boton_guardar = [[sg.Button('Guardar', 
            size=(20, 2), 
            button_color=('black', 'skyblue'), 
            font=('Helvetica', 12),
            key='-GUARDAR-')]]
    boton_etiqueta = [[sg.Button(
            'Ir a etiquetar', 
            size=(20, 2), 
            button_color=('black', 'skyblue'), 
            font=('Helvetica', 12),
            key='-ETIQUETAR-')]]
    columna= [sg.Column(
        boton_volver, 
        element_justification='left', 
        expand_x=True),
        sg.Column(
        boton_etiqueta, 
        element_justification='left', 
        expand_x=True),
            sg.Column(
        boton_guardar, 
        element_justification='rigth', 
        expand_x=True)]
    columna_izquierda = [[sg.Text(
        'Seleccionar imagenes: ', 
        size=(30, 1), 
        font=('Times New Roman', 15), 
        text_color='Black', 
        justification=('left'))],
        [sg.Listbox(
        values=imagenes,
        enable_events=True, 
        size=(40, 20),
        key="-ARCHIVOS-",
        background_color='skyblue',
        text_color='black',
        sbar_arrow_color='black', 
        sbar_background_color='skyblue', 
        highlight_background_color='steelblue',
        highlight_text_color='white')],
        [sg.Button(
            'Agregar imagen',
            size=(20, 2),
            button_color=('black', 'skyblue'),
            font=('Helvetica', 12),
            key='-AGREGAR-'
        )],
        [sg.Text(
        'Agregar titulo: ', 
        size=(30, 1), 
        font=('Times New Roman', 15), 
        text_color='Black', 
        justification=('left'))],
        [sg.In(size=(50, 1), 
        enable_events=True, 
        key="-TEXTO-",
        background_color='skyblue',
        text_color='black'),
        sg.Button('Enter', 
        key="-ENTER-",
        button_color='skyblue')]
    ]
    columna_derecha =[
        [sg.Text(
        'Previsualización', 
        size=(30, 1), 
        font=('Times New Roman', 15), 
        text_color='Black', 
        justification=('right'))],
        [sg.Image(
        data=abrir_foto.abrir(os.path.join(ROOT_PATH,"fotos",plantilla),(400,400)), 
        key='-IMAGE-',
        size=(400,400),
        subsample=0)]
    ]
    layout =[ 
        [sg.Text(
        'Generar Collage', 
        size=(20, 1), 
        font=('Times New Roman', 75), 
        text_color='Black', 
        justification=("c"))],
        [sg.Column(columna_izquierda,justification='c'),
        sg.Column(columna_derecha,justification='c')],  
        [columna]]
    
    return layout



def window_generar_collage(alias,plantilla,textbox):
    window = sg.Window('',layout_generar_collage(alias,plantilla), element_justification='c', size=(1366,768), resizable=True )
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        imagenes=[]
        coordenadas=[]
        cantidad_textboxes = len(textbox)
        i=0
        
        if plantilla == "Plantilla_1.png":
            # Obtener la cantidad de imágenes y las rutas de las imágenes
            imagenes = obtener(alias)
            # Coordenadas de las imágenes en la plantilla
            for i in range(cantidad_textboxes):
                coordenadas.append((textbox[i]["top_left_x"], textbox[i]["top_left_y"]))
            #variables que se pasan para poder hacer el resize de la imagen
            x = 650
            y = 260
        elif plantilla == "Plantilla_2.png":
            imagenes = obtener(alias)
            for i in range(cantidad_textboxes):
                coordenadas.append((textbox[i]["top_left_x"], textbox[i]["top_left_y"]))
            x = 300
            y = 350
        elif plantilla == "Plantilla_3.png":
            imagenes = obtener(alias)
            for i in range(cantidad_textboxes):
                coordenadas.append((textbox[i]["top_left_x"], textbox[i]["top_left_y"]))
            x = 610
            y = 400
        elif plantilla == "Plantilla_4.png":
            imagenes = obtener(alias)
            for i in range(cantidad_textboxes):
                coordenadas.append((textbox[i]["top_left_x"],textbox[i]["top_left_y"]))
            x = 320
            y = 250
        plantilla = pegar_imagenes(plantilla,cantidad_textboxes, imagenes, coordenadas, x, y) 

    window.close()   