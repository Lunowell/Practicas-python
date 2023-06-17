import PySimpleGUI as sg
from PIL import Image 



sg.theme ('LightGrey4')




def window_generar_collage(alias,plantilla,textbox):
    window = sg.Window('',layout_generar_collage(), element_justification='c', size=(1366,768), resizable=True )
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        coordenadas=[]
        cantidad_textboxes = len(textbox)
        i=0
        
        if plantilla == "Plantilla_1.png":
            # Obtener la cantidad de imágenes y las rutas de las imágenes
            cantidad_imagenes, rutas_imagenes = obtener_imagenes(plantilla_seleccionada)
            # Coordenadas de las imágenes en la plantilla
            for i in range(cantidad_textboxes):
                coordenadas.append((textbox[i]["top_left_x"], textbox[i]["top_left_y"]))
            #variables que se pasan para poder hacer el resize de la imagen
            x = 650
            y = 260
        elif plantilla == "Plantilla_2.png":
            cantidad_imagenes, rutas_imagenes = obtener_imagenes(plantilla_seleccionada)
            for i in range(cantidad_textboxes):
                coordenadas.append((textbox[i]["top_left_x"], textbox[i]["top_left_y"]))
            x = 300
            y = 350
        elif plantilla == "Plantilla_3.png":
            cantidad_imagenes, rutas_imagenes = obtener_imagenes(plantilla_seleccionada)
            for i in range(cantidad_textboxes):
                coordenadas.append((textbox[i]["top_left_x"], textbox[i]["top_left_y"]))
            x = 610
            y = 400
        elif plantilla == "Plantilla_4.png":
            cantidad_imagenes, rutas_imagenes = obtener_imagenes(plantilla_seleccionada)
            for i in range(cantidad_textboxes):
                coordenadas.append((textbox[i]["top_left_x"],textbox[i]["top_left_y"]))
            x = 320
            y = 250
        plantilla = pegar_imagenes(plantilla,cantidad_textboxes, coordenadas, x, y) 

    window.close()   