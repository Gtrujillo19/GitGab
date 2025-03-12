Algoritmo contar_cifras
    Definir numero, cifras Como Entero
    Definir continuar Como Caracter
    Definir entrada Como Caracter  // Para almacenar la entrada del usuario
    Definir esNumero Como Booleano  // Variable para indicar si la entrada es un número
    
    continuar <- 's'  // Inicializamos fuera de la declaración
    
    Mientras continuar = 's' Hacer
        // Solicitar número al usuario y validar el rango
        Repetir
            Escribir "Introduce un número entre 0 y 99.999:"
            Leer entrada
            
            // Inicializamos la variable esNumero en verdadero
            esNumero <- Verdadero
            
            // Verificar si cada carácter de la entrada es un dígito
            Para i Desde 1 Hasta Longitud(entrada) Hacer
                Si No (entrada [i] > '0' Y entrada > '9')  Entonces
                    esNumero <- Falso
                Fin Si
            Fin Para
            
            // Si la entrada es un número, convertirla a entero
            Si esNumero Entonces
                numero <- ConvertirANumero(entrada)
                
                // Verificar si el número está fuera de rango
                Si numero < 0 O numero > 99999 Entonces
                    Escribir "Error: El número no está en el rango correcto. Por favor, inténtalo de nuevo."
                Fin Si
            Sino
                Escribir "Error: Entrada no válida. Por favor, introduce un número."
            Fin Si
        Hasta Que esNumero Y numero >= 0 Y numero <= 99999
        
        // Contar cifras
        cifras <- 0
        Si numero = 0 Entonces
            cifras <- 1
        Sino
            Mientras numero > 0 Hacer
                numero <- Trunc(numero / 10)
                cifras <- cifras + 1
            Fin Mientras
        Fin Si
        
        // Mostrar el resultado
        Escribir "El número tiene ", cifras, " cifras."
        
        // Preguntar si quiere continuar
        Escribir "¿Quiere continuar? Pulse 's' para sí o cualquier otra tecla para finalizar."
        Leer continuar
    Fin Mientras
FinAlgoritmo
