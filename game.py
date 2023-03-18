from random import choice, randrange
from datetime import datetime
operators = ["+", "-", "*","/"]
times = 5
init_time = datetime.now()
print(f"¡Veremos cuanto tardas en responder estas {times} operaciones!")
count = 0
for i in range(0, times):
  number_1 = randrange(10)
  operator = choice(operators)
  if operator == "/":    #Lo hago de esta manera por si number_2 es 0 y la cuenta no se puede efectuar.
    number_2 = randrange(10)
    if number_2 == "0":
        while number_2 == "0":
            number_2 = randrange(10)
  if operator != "/":
    number_2 = randrange(10)
  print(f"{i+1}- ¿Cuánto es {number_1} {operator} {number_2}?")
  result = float(input("resultado: "))
  if operator == "+":
    if number_1 + number_2 == result:
      print ("¡correcto!")
      count = count + 1
    else:
      print ("Incorrecto")
  elif operator == "-":
    if number_1 - number_2 == result :
      print ("¡correcto!")
      count = count + 1
    else:
      print ("Incorrecto")
  elif operator == "*":
    if number_1 * number_2 == result:
      print ("¡correcto!")
      count = count + 1
    else:
      print ("Incorrecto")
  else:
    if number_1 / number_2 == result:
      print ("¡correcto!")
      count = count + 1
    else:
      print ("Incorrecto")
end_time = datetime.now()
total_time = end_time - init_time
print(f"\n Tardaste {total_time.seconds} segundos.")
incorrecta = times - count
print (f"El total de respuestas correctas fue {count}, y tuviste {incorrecta} respuestas incorrectas")

