import PySimpleGUI as sg
import os
import json
import csv
import datetime

#Color de fondo
sg.theme('LightGrey')
def conf(alias):
    #Se setea la hora y la fecha en que se ingresa a configuracion
    hora = datetime.datetime.now().time()
    fecha = datetime.date.today().strftime("%d/%m/%Y")

    #Verifica si el archivo directorio existe, sino lo crea.
    if os.path.exists('directorios.json'):
        with open('directorios.json','r') as archivo:
            #Se verifica si el archivo esta vacio, si es asi se crea la lista de imagenes vacia. Si el archivo no esta vacio se carga lista_imagenes con los datos.
            if (os.stat('directorios.json').st_size == 0):
                contenido_archivo=[]
            else:
                contenido_archivo = json.load(archivo)
                contenido_archivo = list(map(lambda elem : elem,contenido_archivo))
    else:
        with open('directorios.json','w') as archivo:
            contenido_archivo=[]

    #Inicializo las tres variables y en el caso de que esten en el archivo se cargan.
    repositorio =  ""
    collages =  ""
    memes = ""
    for dato in contenido_archivo:
        if ([dato["Alias"]][0] == alias): #Se compara el alias en la posicion 0 ya que dato["alias"] es una lista con el alias pasado por parametro
            repositorio = dato["R_Imagenes"]
            collages = dato["R_Collage"]
            memes = dato["R_Memes"]
            

    #Layout para acomodar el boton ed guardar
    boton_volver = [[sg.Button("< Volver", size=(20, 2), button_color=('black', 'skyblue'), font=('Helvetica', 12),key='volver')]]
    boton_guardar = [[sg.Button('Guardar', size=(20, 2), button_color=('black', 'skyblue'), font=('Helvetica', 12))]]
    columna= [sg.Column(boton_volver, element_justification='left', expand_x=True),
              sg.Column(boton_guardar, element_justification='rigth', expand_x=True)]

    
    

    #layout principal
    layout = [
        [sg.Text("Configuración", size=(50, 1), font=('Times New Roman', 75), text_color='Black', justification=("c"))],
        [sg.Text('',font=('Times New Roman', 30))],
        [sg.Text("Repositorio de Imagenes", key="-MOSTRAR TEXTO-", size=(20, 1), font=('Times New Roman', 25), text_color='Black', justification=("c"))],
        [sg.In(repositorio, key="-Repositorio-", background_color='skyblue', text_color='Black', border_width=1, enable_events=True, readonly=True), 
         sg.FolderBrowse('Seleccionar', button_color=('black', 'skyblue'), size=(10,1))],
        [sg.Text('')],
        [sg.Text("Directorio de collages", key="-MOSTRAR TEXTO-",  size=(20, 1), font=('Times New Roman', 25), text_color='Black', justification=("c"))],
        [sg.In(collages,key="-Collages-", background_color='skyblue', text_color='Black', border_width=1, enable_events=True, readonly=True), 
         sg.FolderBrowse('Seleccionar', button_color=('black', 'skyblue'), size=(10,1))],
        [sg.Text('')],
        [sg.Text("Directorio de memes", key="-MOSTRAR TEXTO-",  size=(20, 1), font=('Times New Roman', 25), text_color='Black', justification=("c"))],
        [sg.Input(memes, key="-Memes-", background_color='skyblue', text_color='Black', border_width=1, enable_events=True, readonly=True), 
         sg.FolderBrowse('Seleccionar', button_color=('black', 'skyblue'), size=(10,1))],
        [sg.Text('')],
        [(columna)]
    ]

    #ventana
    window = sg.Window('Configuración', layout, element_justification='c', size=(1366,768), resizable=True)

    #eventos
    while True:
        event, values = window.read()
        if (event == sg.WIN_CLOSED):
            break
        if (event == 'volver'):
            #Nos movemos al menu principal
            break
        if (event == 'Guardar'):
            #Aca cargamos las rutas que se seleccionan con el browse
            if values['-Repositorio-']!='': 
                repositorio= values['-Repositorio-']
            if values['-Memes-']!='':
                memes= values['-Memes-']
            if values['-Collages-']!='':
                collages= values['-Collages-']

            #Verificamos que ninguno de los 3 campos no este vacio, ya sea por una carga actual o que recien lo estemos inicializando.
            if ((repositorio != '') and (memes != '') and (collages != '')):
                esta = False #La variable "esta" funciona para saber si tiene que sobreescribir o crear. 
                datos_modificados = ({"Alias":alias,"R_Imagenes": repositorio,"R_Collage": collages,"R_Memes":memes}) #Creamos el diccionario con los datos
                with open('directorios.json','w') as archivo:
                    for elem in contenido_archivo:
                        if elem["Alias"] == alias:
                            elem.update(datos_modificados)
                            esta = True
                    if not(esta):
                        contenido_archivo.append({"Alias":alias,"R_Imagenes": repositorio,"R_Collage": collages,"R_Memes":memes})
                    json.dump(contenido_archivo,archivo,indent=2)
                
                #Se carga en el archivo csv la modificación.
                with open ('perfiles.csv','a',newline='') as archivo:
                    writer = csv.writer(archivo)
                    writer.writerow([fecha,hora,alias,"Hizo cambios en la configuracion"]) 
                sg.Popup('¡Rutas cargadas con éxito!')
                break
            else:
                sg.popup('Por favor complete todos los campos.')
    window.close()