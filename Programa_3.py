# Memoria estatica en Python
import numpy as np

class MemoriaEstatica:

    print("")
    print("########## MEMORIA ESTATICA ##########")

    #Crear array "estatico" de tamaño fijo (como en Java: int calificaciones[] = new int[5])
    calificaciones = np.zeros(5, dtype=np.int32)

    #Capturar 5 calificaciones
    for i in range(5):
        calificaciones[i] = int(input(f"Ingrese la calificación {i+1}: "))

    print ("Calificaciones: ")
    for i in range(5):
        print (f"calificaciones [{i}] = {calificaciones[i]}")


# Memoria dinamica en python

class MemoriaDinamica:

    print("")
    print("########## MEMORIA DINAMICA ##########")

    frutas = []

    frutas.append("Mango")
    frutas.append("Manzana")
    frutas.append("Banana")
    frutas.append("Uvas")
    print (frutas)
    frutas.remove("Mango")
    frutas.remove("Manzana")
    frutas.append("Sandia")
    print(frutas)






