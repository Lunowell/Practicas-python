import PySimpleGUI as sg
import os
import io
import json
import Configuracion as configuracion
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import textwrap
sg.theme ('LightGrey4')

#Se crea esta función para poder abrir las fotos en formatos diferentes al png convirtiendolos en bytes.
def abrir_foto_meme(ruta_foto):
    """
    Se abre la foto desde la ruta (que debe ser pasada por parametro) solo para lectura en formato binario, de esa manera obteniendo los bytes respectivos de la imagen y 
    utilizando el PIL se lee y se la reacomoda en un tamaño de 400x400, guardandandola y enviando a traves del return los bytes de la imagen.
"""
    with open(ruta_foto, 'rb') as file:
        img_bytes = file.read()
        image = Image.open(io.BytesIO(img_bytes))
        image.thumbnail((400, 400))
        bio = io.BytesIO()
        image.save(bio, format='PNG')
    return bio.getvalue()

# Función para agregar texto a una imagen
def obtener_imagen_con_texto(foto, texto, fuente, posicion, textbox):

    imagen = Image.open(foto)

    draw = ImageDraw.Draw(imagen) 

    #Inicializamos la letra
    font_size = 20
    font = ImageFont.truetype(fuente, font_size)

    #Inicializamos el lugar donde se posiciona el recuadro. 
    pos_x = textbox[posicion]["top_left_x"]
    pos_y = textbox[posicion]["top_left_y"]
    coordenadas= (pos_x, pos_y)

    lineas = textwrap.wrap(texto, width=int(imagen.width / font_size))

    # Dibujar cada línea de texto
    for linea in lineas:
        coordenadas= (pos_x, pos_y)
        draw.text(coordenadas, linea, font=font, fill='black')
        pos_y += font_size #Generamos el salto de linea.

    #Transformamos la imagen en bytes y la mostramos en pantalla.
    bio = io.BytesIO()
    imagen.save(bio, format="PNG")
    
    return bio.getvalue()


def layout_meme(foto):
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

    columna= [sg.Column(
            boton_volver, 
            element_justification='left', 
            expand_x=True),
            sg.Column(
            boton_guardar, 
            element_justification='rigth', 
            expand_x=True)]


    # Obtener la lista de nombres de tipografías disponibles eliminando el ".ttf" y poniendo la primer letra en mayuscula.
    directorio = os.listdir(os.path.join(os.getcwd(),"Tipografias"))
    tipografias = [fichero.split(".")[0].title() for fichero in directorio]

    columna_izquierda = [
        [sg.Text('Seleccionar una tipografía',
                 size=(20, 1), 
                 font=('Times New Roman', 25), 
                 text_color='Black', 
                 justification=("c"))],
         [sg.Combo(tipografias,
                    key='-TIPOGRAFIA-', 
                    size=(48,1),
                    default_value="Arial",
                    enable_events=True,
                    readonly=True,
                    background_color='skyblue',
                    font=('Helvetica', 10),
                    button_arrow_color=('black'),
                    button_background_color='skyblue')],
        [sg.Text("Texto 1",
                 size=(20, 1), 
                 font=('Times New Roman', 25), 
                 text_color='Black', 
                 justification=("c"))],        
         [sg.In(size=(50, 1), 
                enable_events=True, 
                key="-TEXTO1-",
                background_color='skyblue',
                text_color='black')],
         [sg.Text("Texto 2",
                 size=(20, 1), 
                 font=('Times New Roman', 25), 
                 text_color='Black', 
                 justification=("c"))],        
         [sg.In(size=(50, 1), 
                enable_events=True, 
                key="-TEXTO2-",
                background_color='skyblue',
                text_color='black')]
         ]

    columna_derecha= [[sg.Text('Previsualización', 
        size=(30, 1), 
        font=('Times New Roman', 15), 
        text_color='Black', 
        justification=('c'))],
        [sg.Image(
        data= abrir_foto_meme(foto),
        key='-IMAGE-', 
        size=(400,400),
        subsample=0)]]

    layout = [
        [sg.Text('Generar Meme', 
        size=(20, 1), 
        font=('Times New Roman', 75), 
        text_color='Black', 
        justification=("c"))],
        [sg.Column(columna_izquierda, justification='c'),
        sg.Column(columna_derecha, justification='c')],
            [columna]]
    
    return layout 

def window_generar_meme(foto, textbox):

    window = sg.Window('',layout_meme(foto), element_justification='c', size=(1366,768), resizable=True)

    while True:
        event,values = window.read()

        if event == ('-VOLVER-') or event == sg.WIN_CLOSED:
            break
        if event == ('-GUARDAR-') or event == sg.WIN_CLOSED: 
            break
        
        
        fuente = os.path.join(os.getcwd(),"Tipografias",f"{values['-TIPOGRAFIA-']}.ttf")
        if event == ('-TEXTO1-'):
            window["-IMAGE-"].update(size=(400,400),subsample=2 ,data=obtener_imagen_con_texto(foto, values['-TEXTO1-'], fuente, 0, textbox))
        elif event == ('-TEXTO2-'):
            window["-IMAGE-"].update(size=(400,400),subsample=2 ,data=obtener_imagen_con_texto(foto, values['-TEXTO2-'], fuente, 1, textbox))
    window.close()