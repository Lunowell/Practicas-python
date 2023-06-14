import PySimpleGUI as sg
import os.path
from PySimpleGUI.PySimpleGUI import FolderBrowse, Listbox
import io
from PIL import Image
import csv
import datetime
import imghdr
import json

sg.theme('LightGrey4')

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

"""La siguiente funcion se hace con el fin de guardar una nueva foto que no tenia descripcion y eitquetas previamente cargadas  """
def guardar_nueva_linea(nombre_foto,descripcion,etiquetas,alias):
    try: 
        fecha = datetime.date.today().strftime("%d/%m/%Y")
        with open ('imagenes.csv','a',newline='') as archivo:
            imagen = Image.open(nombre_foto)
            writer = csv.writer(archivo)
            writer.writerow([nombre_foto,descripcion,imagen.size,os.stat(nombre_foto).st_size,imghdr.what(nombre_foto),etiquetas,fecha,alias])
            sg.Popup('¡Nueva foto guardada con éxito!')
    except:
        sg.popup('Por favor seleccione la imagen.')

"""La siguiente funcion se hace con el fin de guardar o editar los datos de las imagenes en un csv  """
def guardar_datos(nombre_foto,descripcion,etiquetas,alias):
    try:
        with open('imagenes.csv', 'r+') as archivo:
            lector = csv.reader(archivo)
            contenido_csv = list(lector)
            imagen = Image.open(nombre_foto)
        #Una vez abierto el archivo procedemos a buscar la foto
        exito =False
        for i, sublista in enumerate(contenido_csv):
            if nombre_foto in sublista:
                #editamos la fila si se encontro la foto
                fecha = datetime.date.today().strftime("%d/%m/%Y") #actualizamos antes la variable temporal
                contenido_csv[i]=[nombre_foto,descripcion,imagen.size,os.stat(nombre_foto).st_size,imghdr.what(nombre_foto),etiquetas,fecha,alias]
                modificar_csv(alias,'Actualizacion')
                sg.Popup('Imagen actualizada!')
                exito = True
                break
        #Si la foto no se encontro entonces debemos guardar los datos en una nueva linea
        if not exito: 
            guardar_nueva_linea(nombre_foto, descripcion, etiquetas,alias)
            modificar_csv(alias,'Creo')
    except:
        sg.Popup('Ups! Ha ocurrido un error!')

"""La siguiente funcion se hace con el fin de verificar si la foto seleccionada ya tiene etiquetas, descripcion y metadatos almacenados, y devolverlos """
def buscar_foto(nombre_foto):
    datos_imagen = None
    try:
        with open('imagenes.csv', 'r') as archivo:
            lector = csv.reader(archivo)
            contenido_csv = list(lector)
        #Una vez abierto el archivo procedemos a buscar la foto
        for i, sublista in enumerate(contenido_csv):
            if nombre_foto in sublista:
                datos_imagen = sublista #Informacion de la imagen que buscamos
                break
    except FileNotFoundError:
        sg.Popup('No se encontro el archivo de imagenes')
    return datos_imagen

#Se crea esta función para poder abrir las fotos en formatos diferentes al png convirtiendolos en bytes.
def abrir_foto(ruta_foto):
    """
    Se abre la foto desde la ruta (que debe ser pasada por parametro) solo para lectura en formato binario, de esa manera obteniendo los bytes respectivos de la imagen y 
    utilizando el PIL se lee y se la reacomoda en un tamaño de 200x200, guardandandola y enviando a traves del return los bytes de la imagen.
"""
    with open(ruta_foto, 'rb') as file:
        img_bytes = file.read()
        image = Image.open(io.BytesIO(img_bytes))
        image.thumbnail((300, 300))
        bio = io.BytesIO()
        image.save(bio, format='PNG')
    return bio.getvalue()

"""La siguiente funcion se hace con el fin de agregar en el archivo csv la informacion si el usuario agregó etiquetas 
o descripcion a una nueva foto o a una modificada.  """
def modificar_csv (alias,accion): 
    hora = datetime.datetime.now().time()
    fecha = datetime.date.today().strftime("%d/%m/%Y")
    with open ('perfiles.csv','a',newline='') as archivo:
        writer = csv.writer(archivo)
        datos = [fecha,hora,alias,accion]
        writer.writerow(datos) 


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
    
#funcion general de la interfaz
def eti(alias):

    #variables editables
    etiquetas = [] 
    descripcion = ''
    ruta_repositorio=cargar_ruta_repositorio(alias)
    #creamos el archivo csv en caso de que no exista
    if not (os.path.exists('imagenes.csv')):
        with open('imagenes.csv','w', newline='') as archivo_csv:
            writer = csv.writer(archivo_csv)
            writer.writerow(['Ubicación','Descripción','Resolución','Tamaño','Tipo','Etiquetas','Fecha','Ultimo Perfil'])

    columna_izquierda = [
        [sg.Text("Directorio de imágenes",size=(20, 1), font=('Times New Roman', 25), text_color='Black', justification=("c"))],
         [sg.In(ruta_repositorio, size=(50, 1), enable_events=True, key="-CARPETA-",background_color='skyblue',text_color='black'),
         sg.FolderBrowse('Buscar',button_color='skyblue')],
        [sg.Text("Etiquetar imagen",size=(20, 1), font=('Times New Roman', 25), text_color='Black', justification=("c"))],
         [sg.In(size=(50, 1), enable_events=True, key="-ETIQUETAR TEXT-",background_color='skyblue',text_color='black'),
         sg.Button('Etiquetar', key="-ETIQUETAR-",button_color='skyblue')],
        [sg.Text("Agregar descripcion",size=(20, 1), font=('Times New Roman', 25), text_color='Black', justification=("c"))],
         [sg.In(size=(50, 1), enable_events=True, key="-DESCRIBIR TEXT-",background_color='skyblue',text_color='black'),
         sg.Button('Modificar', key="-DESCRIBIR-",button_color='skyblue')],
        [sg.Text("Eliminar etiqueta",size=(20, 1), font=('Times New Roman', 25), text_color='Black', justification=("c"))],
         [sg.In(size=(50, 1), enable_events=True, key="-ELIMINAR TEXT-",background_color='skyblue',text_color='black'),
         sg.Button('Eliminar', key="-ELIMINAR-",button_color='skyblue')]
    ]

    #fondo para la zona de la imagen previo a cargar una imagen de la carpeta
    ruta_foto = os.path.join(os.getcwd(),"Fotos","Fondo_Meme.png")

    columna_derecha = [
        [sg.Text(size=(100,1), key="-DESCRIPCION-")],
        [sg.Image(data=abrir_foto(ruta_foto),key="-IMAGEN-")],
        [sg.Text(size=(200,2), key='-METADATOS-')],
        [sg.Text(size=(200,2), key="-ETIQUETAS-")],
        [sg.Text('')]
    ]

    boton_volver = [[sg.Button("< Volver", size=(20, 2), button_color=('black', 'skyblue'), font=('Helvetica', 12),key='volver')]]
    boton_guardar = [[sg.Button('Guardar', size=(20, 2), button_color=('black', 'skyblue'), font=('Helvetica', 12), key='guardar')]]

    columna= [sg.Column(boton_volver, element_justification='left', expand_x=True),
            sg.Column(boton_guardar, element_justification='rigth', expand_x=True)]
    
    layout = [
        [sg.Text("Etiquetar imagenes", font=('Times New Roman', 50), text_color='Black', justification=("c"),size=(20, 1))], 
        [sg.Column(columna_izquierda, justification='right'),
        sg.Text('', size=(10,20)),
        sg.Listbox(values=[], enable_events=True, size=(40, 20),key="-ARCHIVOS-",background_color='skyblue',text_color='black',sbar_arrow_color='black', sbar_background_color='skyblue', highlight_background_color='steelblue',highlight_text_color='white'),
        sg.Text('', size=(10,20)),   
        sg.Column(columna_derecha,justification='left')],
        [columna]
    ]

    window = sg.Window("Etiquetas", layout, element_justification= 'c', size=(1366,768), resizable=True)

    while True:
        event, values = window.read(timeout=0)
        if event == "volver" or event == sg.WIN_CLOSED:
            break
        if event == sg.TIMEOUT_EVENT:
            if (ruta_repositorio != ''):
                desplegar_lista(ruta_repositorio,window)    
        if event == "-CARPETA-":
            ruta_carpeta = values["-CARPETA-"]
            desplegar_lista(ruta_carpeta,window)
        elif event == "-ARCHIVOS-":
            #si seleccionamos un archivo de la lista
            try:
                nombre_foto = os.path.join(values["-CARPETA-"], values["-ARCHIVOS-"][0]) #traemos la foto seleccionada
                window["-IMAGEN-"].update(data=abrir_foto(nombre_foto))
                imagen = Image.open(nombre_foto)
                #extraemos los metadatos de la foto cargada en la variable imagen
                window["-METADATOS-"].update("| " + "x".join(map(str, imagen.size))  + " | " + str(os.stat(nombre_foto).st_size) + " | " + imghdr.what(nombre_foto) + " | ")
                #en caso de que la foto seleccionada ya tuviese datos cargados previamente los traemos y visualizamos
                if buscar_foto(nombre_foto) != None:
                    datos_imagen = buscar_foto(nombre_foto)
                    window["-DESCRIPCION-"].update(datos_imagen[1])
                    etiquetas=datos_imagen[5]
                    window["-ETIQUETAS-"].update(etiquetas)
                    etiquetas=[etiquetas] #Como traje un string del csv lo vuelvo a convertir a lista
                else:
                    #resetemos las variables principales, listas para su posterior carga
                    etiquetas = []
                    descripcion = ''
                    window["-DESCRIPCION-"].update(descripcion)
                    window["-ETIQUETAS-"].update(" ".join(map(str, etiquetas)))
            except:
                pass
        if event=='-DESCRIBIR-':
            descripcion = values['-DESCRIBIR TEXT-']
            window["-DESCRIPCION-"].update(descripcion)
        if event=='-ETIQUETAR-':
            #guardamos una etiqueta y la agreamos a la lista de etiquetas
            etiqueta = "#" + values['-ETIQUETAR TEXT-']
            etiquetas.append(etiqueta)
            window["-ETIQUETAS-"].update(" ".join(map(str, etiquetas)))
            window["-ETIQUETAR TEXT-"].update("")
        if event=='-ELIMINAR-':
            etiqueta = "#" + values['-ELIMINAR TEXT-']
            try:
                etiquetas.remove(etiqueta)
                window["-ETIQUETAS-"].update(" ".join(map(str, etiquetas)))
                window["-ETIQUETAR TEXT-"].update("")
            except(ValueError):
                sg.popup('No existe la etiqueta')
        if event =='guardar':
            if not values ["-CARPETA-"]:
                sg.popup('Por favor complete todos los campos.')
            else:
                etiquetas = " ".join(map(str, etiquetas)) #convertimos la lista de etiquetas a una cadena para almacenarla en el csv
                guardar_datos(nombre_foto,descripcion,etiquetas,alias)
    window.close()
