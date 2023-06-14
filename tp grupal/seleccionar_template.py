import PySimpleGUI as sg
import os
import io
import json
import Configuracion as configuracion
#import generar_meme_copy as generar_meme
import generar_meme as generar_meme
from PIL import Image
sg.theme ('LightGrey4')


#Se crea esta función para poder abrir las fotos en formatos diferentes al png convirtiendolos en bytes.
def abrir_foto_meme(ruta_foto):
    """
    Se abre la foto desde la ruta (que debe ser pasada por parametro) solo para lectura en formato binario, de esa manera obteniendo los bytes respectivos de la imagen y 
    utilizando el PIL se lee y se la reacomoda en un tamaño de 200x200, guardandandola y enviando a traves del return los bytes de la imagen.
"""
    with open(ruta_foto, 'rb') as file:
        img_bytes = file.read()
        image = Image.open(io.BytesIO(img_bytes))
        image.thumbnail((400, 400))
        bio = io.BytesIO()
        image.save(bio, format='PNG')
    return bio.getvalue()


def cargar_lista_json(nombre):
    """
    Esta función retorna la lista de datos. Puede devolverla vacia en caso de que el archivo no exista o en el caso de que sea vacío.
    """
    #Se verifica si el archivo existe, si es asi se lo abre en modo lectura. En el case de que el archivo no exista se lo abre en modo escritura y se crea la lista de imagenes vacia.
    if os.path.exists(nombre):
        with open(nombre,'r') as archivo:
            #Se verifica si el archivo esta vacio, si es asi se crea la lista de imagenes vacia. Si el archivo no esta vacio se carga lista_imagenes con los datos.
            if (os.stat(nombre).st_size == 0):
                datos_json=[]
            else:
                datos = json.load(archivo)
                datos_json = list(map(lambda elem : elem,datos))
    else:
        with open(nombre,'w') as archivo:
            datos_json=[]

    return datos_json

def layout_seleccionar_template(templates):
    boton_volver = [[sg.Button(
        "< Volver", 
        size=(20, 2), 
        button_color=('black', 'skyblue'), 
        font=('Helvetica', 12),
        key='-VOLVER-')]]
    boton_guardar = [[sg.Button(
        'Generar', 
        size=(20, 2), 
        button_color=('black', 'skyblue'), 
        font=('Helvetica', 12),
        key='-GENERAR-')]]
    columna= [sg.Column(
        boton_volver, 
        element_justification='left', 
        expand_x=True),
            sg.Column(
        boton_guardar, 
        element_justification='rigth', 
        expand_x=True)]

    layout = [[sg.Text(
        'Generar Meme', 
        size=(20, 1), 
        font=('Times New Roman', 75), 
        text_color='Black', 
        justification=("c"))],
        [sg.Text(
        'Seleccionar template: ', 
        size=(30, 1), 
        font=('Times New Roman', 15), 
        text_color='Black', 
        justification=('left')),
        sg.Text(
        'Previsualización', 
        size=(30, 1), 
        font=('Times New Roman', 15), 
        text_color='Black', 
        justification=('right'))],
            [sg.Listbox(
        [arc["name"] for arc in templates], 
        enable_events=True, 
        size=(40, 20),
        key="-ARCHIVOS-",
        background_color='skyblue',
        text_color='black',
        sbar_arrow_color='black', 
        sbar_background_color='skyblue', 
        highlight_background_color='steelblue',
        highlight_text_color='white'),
            sg.Image(
        data=abrir_foto_meme(os.path.join(os.getcwd(),"Fotos","Fondo_Meme.png")),
        key='-IMAGE-')],
            [columna]]
    
    return layout


def window_seleccionar_template():

    #Cargamos los templates en una variable.
    templates = cargar_lista_json("template.json")

    window = sg.Window('',layout_seleccionar_template(templates), element_justification='c', size=(1366,768), resizable=True )

    while True:
        event,values = window.read()

        if event == ("-VOLVER-") or event == sg.WIN_CLOSED:
            break
        
        if event == "-ARCHIVOS-":
            #Seleccionamos un archivo de la lista y lo mostramos.
            try:
                #Buscamos la información de la foto en el archivo de templates.
                for arc in templates:
                    if (arc['name'] == values["-ARCHIVOS-"][0]):
                        datos = arc
                #Mostramos en panalla el meme seleccionado.
                meme_seleccionado = abrir_foto_meme(os.path.join(os.getcwd(),"Fotos",datos["image"]))
                window["-IMAGE-"].update(data=meme_seleccionado)
            except:
                pass
        if event == "-GENERAR-":
            if (values["-ARCHIVOS-"] != []):
                window.Hide()
                #Buscamos la información de la foto en el archivo de templates.
                for arc in templates:
                    if (arc['name'] == values["-ARCHIVOS-"][0]):
                        datos = arc
                meme_seleccionado = os.path.join(os.getcwd(),"Fotos",datos["image"])
                textbox = (datos["text_boxes"])
                generar_meme.window_generar_meme(meme_seleccionado,textbox)
                window.UnHide()
    window.close()