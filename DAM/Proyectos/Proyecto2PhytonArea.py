# Programa para calcular el área de:
print ("1.Réctángulo")
print ("2.Círculo")
print ("3.Triángulo")


#Solicitar al usuario que elija una opción

opcion = int(input("Elige una opción"))
             

# Función para calcular el área de:


# Rectángulo
if opcion == 1:

# Cálculo del área de un rectángulo
    base = float(input("Introduce la base del rectángulo: "))
    altura = float(input("Introduce la altura del rectángulo: "))
    area = base * altura
    print(f"El área del rectángulo es: {area}")


# Círculo 
elif opcion == 2:

# Cálculo del área de un círculo
    radio = float(input("Introduce el radio del círculo: "))
    area = 3.1416 * radio ** 2  # Fórmula del área de un círculo: π * r^2
    print(f"El área del círculo es: {area}")

# Triángulo
elif opcion == 3:

#Cálculo del área del triángulo

base =float(input("Itroduce la base del triángulo"))
altura = float(input("Introduce la altura del triángulo"))
area = (base,altura)/2
print (f"El área del triángulo es: {area}")

# Opción no válida:
else :print("ERROR, Elija una opción entre 1,2,3")


# Solicitar al usuario que ingrese los valores
base = float(input("Ingrese la base del rectángulo: "))
altura = float(input("Ingrese la altura del rectángulo: "))



# Mostrar el resultado
print(f"El área del rectángulo e# Calcular el área
area = calcular_area(base, altura)s: {area}")


