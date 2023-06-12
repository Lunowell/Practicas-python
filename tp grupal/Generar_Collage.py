import PySimpleGUI as sg
import os
import io
from PIL import Image
import cargar_imagenes as load_imagenes

#Color de fondo
sg.theme('LightGrey4')
"""
Se abre la foto desde la ruta (que debe ser pasada por parametro) solo para lectura en formato binario, de esa manera obteniendo los bytes respectivos de la imagen y 
utilizando el PIL se lee y se la reacomoda en un tamaño de 200x200, guardandandola y enviando a traves del return los bytes de la imagen.
"""
def abrir_foto(ruta_foto):
    with open(ruta_foto, 'rb') as file:
        img_bytes = file.read()
        image = Image.open(io.BytesIO(img_bytes))
        image.thumbnail((200, 200))
        bio = io.BytesIO()
        image.save(bio, format='PNG')
    return bio.getvalue()
def layout ():
    # Rutas de las fotos predeterminadas para el uso de la interfaz, son utilizadas en los botones y en el popup de la imagen para mostrar las plantillas de collage
    ruta_fotos1 = os.path.join(os.getcwd(),"Fotos","amorpopup.png")
    ruta_fotos2 = os.path.join(os.getcwd(),"Fotos","naturalezapopup.png")
    ruta_fotos3 = os.path.join(os.getcwd(),"Fotos","cienciapopup.png")
    ruta_fotos4 = os.path.join(os.getcwd(),"Fotos","genericopopup.png")
    ruta_fotos5 = os.path.join(os.getcwd(),"Fotos","familiapopup.png")
    ruta_fotos6 = os.path.join(os.getcwd(),"Fotos","aydpopup.png")
    
    
    # Declaracion de la primera columna, la cual contiene 3 botenes y dichos botones contiene cada uno una imagen diferente, la cual es la posible plantilla a utilizar por el usuario.
    columna1 = sg.Column ([[sg.Button(key ='amor', button_color=('LightGrey', 'grey'),image_data=abrir_foto(ruta_fotos1),border_width=0,image_size=(150,200), image_subsample=1), 
            sg.Button(key ='naturaleza', button_color=('LightGrey', 'grey'), image_data=abrir_foto(ruta_fotos2),border_width=0,image_size=(150,200),image_subsample=1),
            sg.Button(key ='ciencia', button_color=('LightGrey', 'grey'), image_data=abrir_foto(ruta_fotos3),border_width=0,image_size=(150,200),image_subsample=1)]], 
            element_justification='c')
    # Declaración de la segunda columna, tiene el mismo funcionamiento que la colimna1
    columna3 = sg.Column([[sg.Button(key ='familia', button_color=('LightGrey', 'grey'), image_data=abrir_foto(ruta_fotos5),border_width=0,image_size=(150,200),image_subsample=1), 
            sg.Button(key ='ayd', button_color=('LightGrey', 'grey'), image_data=abrir_foto(ruta_fotos6),border_width=0,image_size=(150,200),image_subsample=1),
            sg.Button(key ='generico', button_color=('LightGrey', 'grey'), image_data=abrir_foto(ruta_fotos4),border_width=0,image_size=(150,200),image_subsample=1)]],
            element_justification='c')
    # Declaracion del boton salir, para poder volver al menu principal
    columna4= sg.Column([[ sg.Button("< Volver",  size=(20, 2), button_color=('black', 'skyblue'), font=('Helvetica', 12), key='volver')]],
            element_justification='c')
    """
    Layout para acomodar las columnas generadas anteriormente. La columna 1 se encuetra a la derecha de la pagina mientras que la columna 2 a la izquierda, 
    el boton "< volver" se encuentra centrado en la pantalla debajo de los botones de seleccion 
    """
    layout = [[sg.Text("Generar collage", font=('Times New Roman', 50), text_color='Black', justification=("c"),size=(20, 1))],
              [sg.Text('')], # Se utilizan para que haya una separación entre el titulo y las columnas
              [sg.Text('')],
              [columna1],

              [columna3],
              [sg.Text('')],# Se utilizan para que haya una separación entre las columnas y el boton "< volver"
              [sg.Text('')],
              [columna4]]
    return layout
# Se define una funcion llamada coll para poder llamar a la interfaz desde el menú principal
def coll(alias):

    
    
    # Se define el tamaño de la pantalla y se utiliza la funcion resizable para que la pantalla sea redimensionable por el usuario
    window = sg.Window('',layout, element_justification='c', size=(1366,768), resizable=True) 

    while True:
        event, values = window.read()
        if ((event == sg.WIN_CLOSED) or (event == "volver")):
            break
        #Los siguientes if son para poder abrir en grande la plantilla seleccionada por el usuario. Se utiliza la funcion popup para poder abrir dicha imagen
        if event == "amor": 
            load_imagenes.cargar_imagenes(alias,"amorpopup.png")
        if event == "naturaleza": 
            load_imagenes.cargar_imagenes(alias,"naturalezapopup.png")
        if event == "ciencia":
            load_imagenes.cargar_imagenes(alias,"cienciapopup.png")
        if event == "generico":
            load_imagenes.cargar_imagenes(alias,"genericopopup.png")
        if event == "familia":
            load_imagenes.cargar_imagenes(alias,"familiapopup.png")
        if event == "ayd":
            load_imagenes.cargar_imagenes(alias,"aydpopup.png")
            
    window.close()
