import PySimpleGUI as sg
import os, io
import crear_perfil as perfil
import menu_principal as menu
from PIL import Image
import json
import csv
sg.ChangeLookAndFeel('LightGrey4')

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




#Inicializamos los botones con los primeros elementos de la lista y/o elementos vacios. SE USA AL MOMENTO DEL INICIO. SE CREO POR EL CASO EN QUE EL TAMAÑO DE LA LISTA SEA MENOR O IGUAL A 4
def mostrar_botones(datos_json):
    """
    Se cargan los botones con su respectiva foto y en caso de que haya menos de 4 botones para mostrar se invisibilizan las posiciones para la cual no hay cargados.
    """

    # Se inicializan los botones en vacío.
    botones = [0, 0, 0, 0]
    i=0

    #Recorre 4 posiciones verificando si la lista es menor que el puntero (osea si existe un botón cargado para esa posicion). Si es así carga la foto, sino hace invisible el botón.
    for j in range(4):
        if len(datos_json) > i:
            botones[j] = sg.Button(
                image_data=abrir_foto(datos_json[i]['Foto']),
                image_size=(150, 150),
                border_width=0,
                key=f'boton{j}',
            )
            i += 1
        else:
            botones[j] = sg.Button(
                image_size=(150, 150),
                border_width=0,
                key=f'boton{j}',
                visible=False,
            )

    return botones


#Esta función es similar a mostrar_botones pero la diferencia que tiene es que en este se actualizan los botones creados en mostrar_botones.
def actualizar_botones(i, datos_json, window):
    """
    Esta función actualiza con los proximos 4 datos cargados los botones. Se pasa el "i" como parametro para poder ir avanzando en la lista de datos.
    """
    
    window['num_pagina'].update(f'Pagina n° {(i // 4) + 1}')
    for j in range(4):
        if i < len(datos_json):
            window[f'boton{j}'].update(
                image_data=abrir_foto(datos_json[i]['Foto']),
                image_size=(150, 150),
                visible=True
            )
            i+=1
        else:
            window[f'boton{j}'].update(visible=False)
    return i


def layout_inicio(datos_json):
    """
    Esta función retorna el layout del inicio con todos sus botones.
    """

    #Se crea boton_cerrar para utilizarlo como columna y asi posicionarlo en el costado derecho.
    boton_cerrar = [[sg.Button(
        'Cerrar',
        size=(20, 2),
        button_color=('black', 'skyblue'), 
        font=('Comis Sans MS', 12)
        )]]

    #Se verifica que la lista_imagenes sea menor a 4. Si esto es verdadero se crea el texto con la pagina correcta y con el boton "Ver más" desactivado. En el caso de que sea mayor a 4 se habilita el boton "Ver más" y se crea el texto con la pagina correcta. 
    if (len(datos_json) > 4):
        boton_ver_mas = [[sg.Button(
            "Ver más",
            size=(20, 2), 
            button_color=('black', 'skyblue'), 
            font=('Helvetica', 12),
            key='ver_mas',
            disabled=False),
                sg.Button(
            "Agregar perfil",
            size=(20, 2), 
            button_color=('black', 'skyblue'), 
            font=('Helvetica', 12),
            key='agregar_perfil')]]
    else:
        boton_ver_mas = [[sg.Button(
            "Ver más",
            size=(20, 2), 
            button_color=('black', 'skyblue'), 
            font=('Helvetica', 12),
            key='ver_mas',
            disabled=True),
                sg.Button(
            "Agregar perfil",
            size=(20, 2), 
            button_color=('black', 'skyblue'), 
            font=('Helvetica', 12),
            key='agregar_perfil')]]
    
    botones = mostrar_botones(datos_json)

    layout = [[sg.Text(
        'UNLP-Image', 
        size=(50, 2), 
        font=('Times New Roman', 75), 
        text_color='Black', 
        justification=("c"))],
            [sg.Text(
        f'Pagina n° 1', 
        key='num_pagina', 
        text_color='Black',
        font=('Times New Roman', 15))],
            [botones],
            [boton_ver_mas],
            [sg.Text('')], 
            [sg.Column(boton_cerrar, element_justification='rigth', expand_x=True)]]
    
    return layout

def crear_csv_logs(nombre):
    """
    Esta función crea el archivo con el nombre se pasa por parametro, en el caso de que ya se haya creado se informa en pantalla.
    """
    if not (os.path.exists(nombre)):
        with open(nombre,'w', newline='') as archivo_csv:
            writer = csv.writer(archivo_csv)
            writer.writerow(['Fecha','Hora','Nick','Operacion'])
    else:
        sg.popup

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


def window_inicio():
    """
    Función que retorna la ventana del inicio.
    """

    i=4

    crear_csv_logs('perfiles.csv')
    datos_json = cargar_lista_json('perfiles.json')

    window = sg.Window('Inicio', layout_inicio(datos_json), element_justification='c', size=(1366,768),resizable=True )

    while True:
        event,values = window.read()

        if event == ('Cerrar') or event == sg.WIN_CLOSED:
            break
        if event ==("agregar_perfil"):
            window.hide()
            perfil_cargado = perfil.agregar_perfil()
            #verifica si se uso el agregar perfil, porque puede entrar a crear perfil y no crear ningun perfil
            if (perfil_cargado != None):
                if (len(datos_json)==0):
                    datos_json.append(menu.window_menu(perfil_cargado)) #si se agrega un perfil va al menú
                elif(datos_json[-1] != perfil_cargado):
                    datos_json.append(menu.window_menu(perfil_cargado)) #si se agrega un perfil va al menú
            break

        if event == ("ver_mas"):
            if len(datos_json) > i:
                i = actualizar_botones(i, datos_json, window)
            else:
                i = actualizar_botones(0, datos_json, window)

        
        #Se itera en cada 1 de los 4 botones verificando cual fue presionado (si así lo hizo) y una vez que se sabe cual botón se presionó se calcula el resto de i (iterador) divido 4 (tamaño total del arreglo de botones mostrados en pantalla) y con el resultado de esto podemos saber si estan completos todos los lugares en pantalla. Si hay algún lugar vacío se resta por el resto y sino por 4.
        for posicion in range(4):
            if event == f'boton{posicion}':
                inicio = i % 4
                if (inicio == 0):
                    inicio = i - 4
                else:
                    inicio = i - inicio

                window.hide()

                #La posición esta dada por la suma de inicio y posicion. Inicio es el calculo con el resto de 4 y posición es en que posición se presionó el botón.
                datos_json[inicio+posicion] = menu.window_menu(datos_json[inicio+posicion])
                window.close()
            

    window.close()
