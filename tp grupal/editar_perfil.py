import PySimpleGUI as sg
import os
import io
import json
from PIL import Image
import datetime
import csv


def abrir_foto(ruta_foto):
    foto_default = os.path.join(os.getcwd(),"Fotos","usuario.png")
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
    return  foto_default

def imagen(perfil):
    try:
        with open(perfil, 'rb') as file:
            img_bytes = file.read()
            image = Image.open(io.BytesIO(img_bytes))
            image.thumbnail((150, 150))
            bio = io.BytesIO()
            image.save(bio, format='PNG')
            perfil = bio.getvalue()
        return perfil
    except FileNotFoundError:
        sg.popup ("Error: No se encontró la imagen en la ruta especificada")
    except Exception as e:
        sg.popup ("Error desconocido: ",str(e))
    return None


def editar_perfil(perfil):
    """
    Se ejecuta una ventana donde se muestra el alias del perfil, inmutable, y sus respectivos datos cargados anteriormente,
    estos datos se pueden cambiar con nuevos datos, editando la informacion de ese perfil, en el archivo perfiles.json se 
    reemplazara la informacion de ese usuario con la informacion nueva cargada, y en el archivo csv se informara en caso de 
    que el usuario haya cambiado su foto
    """

    cambio_foto = False
    datos_modificados = perfil
    foto = perfil['Foto']
    with open('perfiles.json') as archivo:
        contenido_archivo = json.load(archivo)

    boton_volver = [[sg.Button("< Volver", size=(20, 2), button_color=('black', 'skyblue'), font=('Helvetica', 12),key='volver')]]
    boton_guardar = [[sg.Button('Guardar', size=(20, 2), button_color=('black', 'skyblue'), font=('Helvetica', 12))]]
    columna= [sg.Column(boton_volver, element_justification='left', expand_x=True),
              sg.Column(boton_guardar, element_justification='rigth', expand_x=True)]
    
    #layout
    layout = [[sg.Text('Editar perfil', size=(20, 1), font=('Times New Roman', 75), text_color='Black', justification=("c"))],
          [sg.Text('Nick o alias', size=(20, 1), font=('Times New Roman', 25), text_color='Black', justification=("c"))],
          [sg.Text(f'-{perfil["Alias"]}-',size=(20, 1), font=('Helvetica', 15), text_color='Black', justification=("c"))],
          [sg.Text('Nombre',size=(20, 1), font=('Times New Roman', 25), text_color='Black', justification=("c"))],
          [sg.InputText(perfil["Nombre"],background_color='skyblue', size=(50,1), font=('Helvetica', 10))],
          [sg.Text('Edad',size=(20, 1), font=('Times New Roman', 25), text_color='Black', justification=("c"))],
          [sg.Input(perfil["Edad"],background_color='skyblue', size=(50,1), font=('Helvetica', 10))],
          [sg.Text('Genero autopercibido',size=(20, 1), font=('Times New Roman', 25), text_color='Black', justification=("c"))],
          [sg.Combo(['Masculino','Femenino','Otro'],default_value=perfil["Genero"],key='Genero',size=(50,1),readonly=True,background_color='skyblue',font=('Helvetica', 10),button_arrow_color=('black'))], #combo es una lista desplegable
          [sg.Image(imagen(perfil['Foto']),key='-AVATAR_IMAGE-',size=(150,150))],
          [sg.Button("Seleccionar avatar",key='-AVATAR-',button_color=('black', 'skyblue'), font=('Helvetica', 12))],
          [columna]]


    #creacion ventana
    window = sg.Window("Editar perfil",layout,size=(1366,768), element_justification='c', resizable=True )
    #ejecucion ventana
    while True:
        event,values = window.read()
        #cerrado
        if event == sg.WINDOW_CLOSED or event == "volver":
            break
        
        #eleccion de imagen
        if event == '-AVATAR-':
            ruta_imagen = sg.popup_get_file('Seleccionar avatar', no_window=True, file_types=(('Imagenes', '*.png *.jpg *.jpeg *.gif *.bmp *.tiff'),))
            if ruta_imagen:
                try:
                    with open(ruta_imagen, 'rb') as file:
                        img_bytes = file.read()
                        image = Image.open(io.BytesIO(img_bytes))
                        image.thumbnail((150, 150))
                        bio = io.BytesIO()
                        image.save(bio, format='PNG')
                        window['-AVATAR_IMAGE-'].update(data=bio.getvalue())
                        cambio_foto = True #asi no da error 
                except Exception as e:
                    sg.popup_error(f'Error al cargar la imagen: {e}')

        #guardado
        if event == 'Guardar':
            
            nombre = values[0]
            #verificacion edad sea un entero
            while True:
                try:
                    edad = int(values[1])
                    break
                except ValueError:
                    sg.popup('Por favor ingrese un número entero válido para la edad.')
                    event, values = window.read()#se declara de vuelta para que lea el nuevo valor de edad ingresado
                    continue

            #como guardar el genero
            if values['Genero'] == 'Otro':
                genero = sg.popup_get_text("Complete manualmente su genero")
                while genero is None or genero.strip() == '':
                    # Se ejecuta si el usuario presiona Cancelar o no ingresa ningún valor.
                    sg.popup('Debe ingresar un valor para su género')
                    genero = sg.popup_get_text("Complete manualmente su genero")
            else:
                genero = values['Genero']
            
            #verificacion para saber si hay que modificar la variable foto
            if cambio_foto:
                foto = ruta_imagen
                
                hora = datetime.datetime.now().time()
                fecha = datetime.date.today().strftime("%d/%m/%Y")
                with open ('perfiles.csv','a',newline='') as archivo:
                    writer = csv.writer(archivo)
                    datos = [fecha,hora,perfil['Alias'],"Cambió de foto"]
                    writer.writerow(datos) 
                
            #nuevos datos
            datos_modificados = {"Nombre":nombre,"Edad":edad,"Alias":perfil["Alias"],"Genero":genero,"Foto":foto}

            #sobreescritura del JSON con nuevos datos si hubo, sino esta igual
            with open('perfiles.json','w') as archivo:
                for elem in contenido_archivo:
                    if elem["Alias"] == perfil["Alias"]:
                        elem.update(datos_modificados)
                json.dump(contenido_archivo,archivo,indent=2)

            sg.Popup("Perfil editado con exito")
            break
    window.close()
    return datos_modificados
