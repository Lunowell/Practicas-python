nombres = ''' 'Agustin', 'Alan', 'Andrés', 'Ariadna', 'Bautista', 'CAROLINA', 'CESAR',
'David','Diego', 'Dolores', 'DYLAN', 'ELIANA', 'Emanuel', 'Fabián', 'Facundo',
'Francsica', 'FEDERICO', 'Fernanda', 'GONZALO', 'Gregorio', 'Ignacio', 'Jonathan',
'Joaquina', 'Jorge','JOSE', 'Javier', 'Joaquín' , 'Julian', 'Julieta', 'Luciana',
'LAUTARO', 'Leonel', 'Luisa', 'Luis', 'Marcos', 'María', 'MATEO', 'Matias',
'Nicolás', 'Nancy', 'Noelia', 'Pablo', 'Priscila', 'Sabrina', 'Tomás', 'Ulises',
'Yanina' '''
notas_1 = [81, 60, 72, 24, 15, 91, 12, 70, 29, 42, 16, 3, 35, 67, 10, 57, 11, 69,
12, 77, 13, 86, 48, 65, 51, 41, 87, 43, 10, 87, 91, 15, 44,
85, 73, 37, 42, 95, 18, 7, 74, 60, 9, 65, 93, 63, 74]
notas_2 = [30, 95, 28, 84, 84, 43, 66, 51, 4, 11, 58, 10, 13, 34, 96, 71, 86, 37,
64, 13, 8, 87, 14, 14, 49, 27, 55, 69, 77, 59, 57, 40, 96, 24, 30, 73,
95, 19, 47, 15, 31, 39, 15, 74, 33, 57, 10]

# Función para generar una estructura con todas las notas relacionando el nombre del estudiante con las notas
def generar_estructura_notas(nombres, notas_1, notas_2):
    nombres = nombres.replace(" ", "").replace("\n", "")  
    nombres = nombres[1:-1].split(",")  
    nombres = list(map(lambda x: x.title(), nombres))  
    notas_por_estudiante = list(map(lambda x, y: [x, y], notas_1, notas_2))
    notas_promedio = list(map(lambda x: sum(x)/len(x), notas_por_estudiante))
    notas_totales = sum(notas_promedio)
    notas_por_estudiante = dict(zip(nombres, notas_por_estudiante))
    return notas_por_estudiante


# Función para calcular el promedio de notas de cada estudiante
def promedio_notas_estudiantes(notas_por_estudiante):
    promedios = {}
    for nombre, notas in notas_por_estudiante.items():
        promedios[nombre] = sum(notas) / len(notas)
    return promedios


# Función para calcular el promedio general del curso
def promedio_general_curso(notas_por_estudiante):
    notas_totales = []
    for notas in notas_por_estudiante.values():
        notas_totales.extend(notas)
    return sum(notas_totales) / len(notas_totales)

def estudiante_mejor_promedio(notas_por_estudiante):
    promedios = {estudiante: sum(notas_por_estudiante[estudiante])/len(notas_por_estudiante[estudiante]) for estudiante in notas_por_estudiante}
    estudiante_mejor_promedio = max(promedios, key=promedios.get)
    return estudiante_mejor_promedio.title(), promedios[estudiante_mejor_promedio]

def estudiante_nota_mas_baja(notas_por_estudiante):
    nota_minima = min(notas_por_estudiante.values())
    estudiante, nota = next((est, nota) for est, nota in notas_por_estudiante.items() if nota == nota_minima)
    return estudiante.title()

notas_por_estudiante = generar_estructura_notas(nombres, notas_1, notas_2)
promedios_por_estudiante = promedio_notas_estudiantes(notas_por_estudiante)
promedio_general = promedio_general_curso(notas_por_estudiante)
estudiante, promedio = estudiante_mejor_promedio(notas_por_estudiante)
estudiante_nota_mas_baja = estudiante_nota_mas_baja(notas_por_estudiante)


print("Notas por estudiante:")
print("")
for key, value in notas_por_estudiante.items():
    print(key, ":", value)
print("")
print('-' * 40)
print("")
print("\nPromedio de notas por estudiante:")
print("")
for key, value in promedios_por_estudiante.items():
    print(key, ":", value)
print("")
print('-' * 40)
print("")
print("\nPromedio general del curso:", promedio_general)
print("")
print('-' * 40)
print("")
print(f"El estudiante con el promedio más alto es {estudiante} con un promedio de {promedio:.2f}")
print("")
print('-' * 40)
print("")
print("\nEstudiante con la nota más baja:", estudiante_nota_mas_baja)
print("")
