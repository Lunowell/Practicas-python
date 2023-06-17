import PySimpleGUI as sg
from PIL import Image
from PIL import ImageOps

# Diccionario de plantillas y el número de imágenes requeridas
plantillas = {
    "Plantilla_1.png": 3,
    "Plantilla_2.png": 4,
    "Plantilla_3.png": 2,
    "Plantilla_4.png": 6
}

# Obtener las opciones de plantilla
opciones_plantillas = list(plantillas.keys())

def obtener_imagenes(plantilla_seleccionada):
    # Obtener el número de imágenes requeridas para la plantilla 
    cantidad_imagenes = plantillas[plantilla_seleccionada]
    # Lista de rutas de las imágenes a superponer
    rutas_imagenes = [
        "ruta_de_la_imagen1.png",
        "ruta_de_la_imagen2.png",
        "ruta_de_la_imagen3.png",
        "ruta_de_la_imagen4.png",
        "ruta_de_la_imagen5.png",
        "ruta_de_la_imagen6.png"
    ]
    # Lista de rutas de las imágenes a superponer
    cantidad_imagenes = min(len(rutas_imagenes), cantidad_imagenes)
    return cantidad_imagenes, rutas_imagenes

def pegar_imagenes(cantidad_imagenes, rutas_imagenes, coordenadas, x, y):
    plantilla = Image.open(plantilla_seleccionada)
    # Iterar sobre las imágenes y superponerlas en la plantilla
    for i in range(cantidad_imagenes):
        imagen = Image.open(rutas_imagenes[i])
        posicion = coordenadas[i]
        imagen = imagen.resize((x, y))
        plantilla.paste(imagen, posicion)
    return plantilla

# Crear el diseño de la ventana
layout = [
    [sg.Text("Selecciona una plantilla:")],
    [sg.Listbox(values=opciones_plantillas, size=(30, len(opciones_plantillas)), key="-PLANTILLA-")],
    [sg.Button("Aceptar")]
]

# Crear la ventana
window = sg.Window("Seleccionar plantilla", layout)

# Mostrar la ventana y esperar eventos
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event == "Aceptar":
        # Obtener la plantilla seleccionada
        plantilla_seleccionada = values["-PLANTILLA-"][0]
        
        # Verificar si la plantilla seleccionada existe en el diccionario
        if plantilla_seleccionada in plantillas:
            coordenadas = []
            x = 0
            y = 0
            if plantilla_seleccionada == "Plantilla_1.png":
                # Obtener la cantidad de imágenes y las rutas de las imágenes
                cantidad_imagenes, rutas_imagenes = obtener_imagenes(plantilla_seleccionada)
                # Coordenadas de las imágenes en la plantilla
                coordenadas = [(48, 48), (48, 305), (48, 590)]
                x = 650
                y = 260
            elif plantilla_seleccionada == "Plantilla_2.png":
                # Obtener la cantidad de imágenes y las rutas de las imágenes
                cantidad_imagenes, rutas_imagenes = obtener_imagenes(plantilla_seleccionada)
                # Coordenadas de las imágenes en la plantilla
                coordenadas = [(55, 55), (380, 48), (48, 450), (380, 450)]
                x = 300
                y = 350
            elif plantilla_seleccionada == "Plantilla_3.png":
                # Obtener la cantidad de imágenes y las rutas de las imágenes
                cantidad_imagenes, rutas_imagenes = obtener_imagenes(plantilla_seleccionada)
                # Coordenadas de las imágenes en la plantilla
                coordenadas = [(53, 41), (53, 455)]
                x = 610
                y = 400
            elif plantilla_seleccionada == "Plantilla_4.png":
                # Obtener la cantidad de imágenes y las rutas de las imágenes
                cantidad_imagenes, rutas_imagenes = obtener_imagenes(plantilla_seleccionada)
                # Coordenadas de las imágenes en la plantilla
                coordenadas = [(41, 41), (360, 38),(40, 310), (361, 310),(40, 581), (361, 579)]
                x = 320
                y = 250
            plantilla = pegar_imagenes(cantidad_imagenes, rutas_imagenes, coordenadas, x, y)

            # Guardar el collage resultante
            ruta_del_collage = "ruta_del_collage.png"
            plantilla.save(ruta_del_collage)

            # Mostrar la imagen del collage en una ventana
            layout = [[sg.Image(filename=ruta_del_collage)]]
            collage_window = sg.Window("Collage", layout)
            collage_window.read()

            # Cerrar la ventana del collage
            collage_window.close()
        else:
            print("La plantilla seleccionada no existe en el diccionario de plantillas.")

# Cerrar la ventana principal
window.close()
