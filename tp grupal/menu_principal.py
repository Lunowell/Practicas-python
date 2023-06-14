import PySimpleGUI as sg
import os
import io
from PIL import Image
import editar_perfil as perfil_editar
import Configuracion as configuracion
import seleccionar_template as generar_meme
import seleccionar_template_collage as collage
import etiquetas as etiquetar


sg.theme ('LightGrey4')

#Se crea esta función para poder abrir las fotos en formatos diferentes al png convirtiendolos en bytes.
def abrir_foto(ruta_foto):
    """
    Se abre la foto desde la ruta (que debe ser pasada por parametro) solo para lectura en formato binario, de esa manera obteniendo los bytes respectivos de la imagen y 
    utilizando el PIL se lee y se la reacomoda en un tamaño de 200x200, guardandandola y enviando a traves del return los bytes de la imagen.
"""
    try:
        with open(ruta_foto, 'rb') as file:
            img_bytes = file.read()
            image = Image.open(io.BytesIO(img_bytes))
            image.thumbnail((200, 200))
            bio = io.BytesIO()
            image.save(bio, format='PNG')
        return bio.getvalue()
    except FileNotFoundError:
        sg.popup ("Error: No se encontró la imagen en la ruta especificada")
    except Exception as e:
        sg.popup ("Error desconocido: ",str(e))
    return None 

def layout_menu(perfil):
    print(perfil)
    # Rutas de las fotos predeterminadas para el uso de la interfaz
    ruta_fotos1 = os.path.join(os.getcwd(),"Fotos","signo.png")
    ruta_fotos2 = os.path.join(os.getcwd(),"Fotos","config.png")
    # Declaracion de los botones de configuracion y ayuda, se declaran de esta manera para poder acomodarlos correctamente en la pantalla
    boton_ayuda=[[sg.Button(key ='configuracion', button_color=('LightGrey', 'grey'),image_data=abrir_foto(ruta_fotos2),border_width=0,image_size=(100,100), image_subsample=2),
                 sg.Button(key ='ayuda', button_color=('LightGrey', 'grey'), image_data=abrir_foto(ruta_fotos1),border_width=0,image_size=(100,100),image_subsample=2)]]
    # Se declara la manera en la que aparece el perfil seleccionado en el menu principal, este es importado desde el inicio y aparece la foto y el alias del usuario
    boton_imagen=[[sg.Button(image_data=abrir_foto(perfil['Foto']), image_size=(100,100),image_subsample=2,key='editar_perfil')],
        [sg.Text((f"-{perfil['Alias']}-"),justification='center', size=(10, 1), font=('Helvetica', 12), border_width=2, text_color='black')]]
    # Se utiliza para acomodar los botones previamente declarado es una misma linea y con sus respectivas justificaciones
    barra_principal = [[sg.Column(boton_imagen, element_justification='left', expand_x=True),
                        sg.Column(boton_ayuda, element_justification='rigth', expand_x=True)]]
    
    # Declaracion del Layout, se utiliza la "barra_principal" previamente declarada y se ubican debajo de esta los botones para llamar a las distintas interfaces
    layout = [[barra_principal],
        [sg.Button("Etiquetar Imagenes", size=(40, 4), button_color=('Black', 'mediumpurple'), font=('Helvetica', 17), border_width=2, key='etiquetar')], 
        [sg.Button("Generar Meme", size=(40, 4), button_color=('Black', 'LightBlue'), font=('Helvetica', 17), border_width=2,key='generar_meme')],
        [sg.Button("Generar Collage", size=(40, 4), button_color=('Black', 'skyblue'), font=('Helvetica', 17), border_width=2,key='generar_collage')],
        [sg.Button("Salir", size=(40, 4), button_color=('Black', 'steelblue'), font=('Helvetica', 17), border_width=2)]
    ]
    return layout
# Se define una funcion para poder llamar al menu principal desde el inicio
def window_menu (perfil):
    

    # Se define el tamaño de la pantalla y se utiliza la funcion resizable para que la pantalla sea redimensionable por el usuario
    window = sg.Window('',layout_menu(perfil), element_justification='c', size=(1366,768), resizable=True ) 
    while True:
        event, values = window.read()
        if ((event == sg.WIN_CLOSED) or (event == "Salir")):
            break
        """
        Se llama a la interfaz configuracion y se le pasa el nombre de la funcion que vamos a utilizar, en este caso "conf". 
        Y tambien se pasa por parametro el perfil actual para poder guardar la informacion de este cuando utilize las funcionalidades de "configuracion".
    """
        if event == "configuracion": 
            window.hide()
            print(perfil["Alias"])
            configuracion.conf(perfil["Alias"])
            window.UnHide()
        """
        Cuando se selecciona el boton "ayuda" se hace el popup de una imagen en la cual se explican las funcionalidades que tiene el menu
    """
        if event == "ayuda":
            foto_ayuda = os.path.join(os.getcwd(),"Fotos","ayuda.png")
            sg.popup(image=foto_ayuda)
        """
        Los siguientes if son las llamadas a las demás iterfaces, utilizando las funciones declaradas en los respectivos archivos
    """
        if event == 'editar_perfil':
            perfil = perfil_editar.editar_perfil(perfil)
            #La siguiente linea se utiliza para que aparezcan los cambios realizados cuando se ejecutó editar perfil en el menu princiapl
            window['editar_perfil'].update(image_data=abrir_foto(perfil['Foto']), image_size=(100,100),image_subsample=2)
        if event == 'generar_meme':
            generar_meme.window_seleccionar_template()
        if event == 'generar_collage':
            collage.window_seleccionar_template(perfil)
        if event == 'etiquetar':
            etiquetar.eti(perfil['Alias'])
    window.close()
    return perfil