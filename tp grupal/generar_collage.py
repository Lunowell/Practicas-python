import PySimpleGUI as sg
import os
import io
import json
#import Configuracion as configuracion
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import etiquetas as etiqueta
import textwrap

sg.theme ('LightGrey4')

#Se crea esta función para poder abrir las fotos en formatos diferentes al png convirtiendolos en bytes.
def abrir_foto_collage(ruta_foto):
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
def buscar_ruta_imagenes_por_alias(alias): 
    try:
        with open('directorios.json') as file:
            data = json.load(file)
            for item in data:
                if item.get('Alias') == alias:
                    return item.get('R_Imagenes')
    except (FileNotFoundError):
        sg.popup('El archivo al que se quiere acceder no existe')
    except (json.JSONDecodeError):
        sg.popup('Ocurrió un error al decodificar el archivo que contiene las rutas de imagenes. Fijese de haber llenado todos los campos previamente en la pestaña de conffiguración')
    except Exception as e:
        print(f"Se produjo un error inesperado: {str(e)}")
    return None
def listar_imagenes(alias):
    ruta_imagenes = buscar_ruta_imagenes_por_alias(alias)
    if ruta_imagenes:
        try:
            imagenes = [filename for filename in os.listdir(ruta_imagenes) if filename.endswith(('.jpg', '.png'))]
            return imagenes
        except FileNotFoundError:
            sg.popup(f"No se encontró el directorio de imágenes para el alias '{alias}'.")
        except Exception as e:
            sg.popup(f"Se produjo un error al listar las imágenes: {str(e)}")
    else:
        sg.popup(f"No se encontró ninguna ruta de imágenes para el alias '{alias}'.")

    return []
          
def layout_collage(foto,alias):
    imagenes = listar_imagenes(alias)
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
        #[arc["name"] for arc in imagenes], #¡¡¡¡ARREGLAR PORQUE NAME HACE REFERENCIA AL JSON DE COORDENADAS, NO HAY UN NAME EN LAS FOTOS ETIQUETADAS!!!!
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
        )]
    ]
    columna_derecha =[
        [sg.Text(
        'Previsualización', 
        size=(30, 1), 
        font=('Times New Roman', 15), 
        text_color='Black', 
        justification=('right'))],
        [sg.Image(
        data=abrir_foto_collage(foto), 
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
    
def window_generar_collage (alias,foto,textbox):
    imagenes = listar_imagenes(alias)
    window = sg.Window('',layout_collage(foto,alias), element_justification='c', size=(1366,768), resizable=True )
    while True:
        event,values = window.read()

        if event == ("-VOLVER-") or event == sg.WIN_CLOSED:
            break
        
        """if event == "-ARCHIVOS-":
            #Seleccionamos un archivo de la lista y lo mostramos.
            try:
                #Buscamos la información de la foto en el archivo de templates.
                for arc in imagenes:
                    if (arc['name'] == values["-ARCHIVOS-"][0]):
                        datos = arc
                #Mostramos en panalla el meme seleccionado.
                collage_seleccionado = abrir_foto_collage(os.path.join(os.getcwd(),"Fotos",datos["image"]))
                window["-IMAGE-"].update(data=collage_seleccionado)
            except:
                pass
        """
        if event == "-ARCHIVOS-":
            try:
                imagen_seleccionada = values["-ARCHIVOS-"][0]
                ruta_imagen = os.path.join(buscar_ruta_imagenes_por_alias(alias), imagen_seleccionada)
                imagen = abrir_foto_collage(ruta_imagen)
                data=abrir_foto_collage(foto)
                window["-IMAGE-"].update(data=imagen)
            except:
                pass

        if event == "-AGREGAR-":
            try:
                imagen_seleccionada = values["-ARCHIVOS-"][0]
                ruta_imagen = os.path.join(buscar_ruta_imagenes_por_alias(alias), imagen_seleccionada)
                imagen = abrir_foto_collage(ruta_imagen)
                # Obtener las coordenadas desde la variable textbox
                coordenadas = textbox
                # Agregar la imagen en las coordenadas especificadas
                imagen_base = Image.open(foto)
                imagen_base.paste(imagen, (coordenadas['top_left_x'], coordenadas['top_left_y']))
                imagen_resultante_data = io.BytesIO()
                imagen_base.save(imagen_resultante_data, format='PNG')
                window["-IMAGE-"].update(data=imagen_resultante_data.getvalue())
            except:
                pass
        if event == "-ETIQUETAR-":
            window.Hide()
            etiqueta.eti(alias)
            window.UnHide()
        if event == ('-GUARDAR-') or event == sg.WIN_CLOSED: 
            break
    window.close()
