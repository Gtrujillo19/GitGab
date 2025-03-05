Algoritmo contar_cifras
    Definir numero, cifras Como Entero
    Definir continuar Como Caracter
    
    continuar <- 's'  // Inicializamos fuera de la declaraci�n
    
    Mientras continuar = 's' Hacer
        // Solicitar n�mero al usuario y validar el rango
        Repetir
            Escribir "Introduce un n�mero entre 0 y 99.999:"
            Leer numero
            
            // Verificar si el n�mero est� fuera de rango
            Si numero < 0 O numero > 99999 Entonces
                Escribir "Error: El n�mero no est� en el rango correcto. Por favor, int�ntalo de nuevo."
            Fin Si
        Hasta Que numero >= 0 Y numero <= 99999
        
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
        Escribir "El n�mero tiene ", cifras, " cifras."
        
        // Preguntar si quiere continuar
        Escribir  "�Quiere continuar?, Pulse s o cualquier otra tecla para finalizar"
        Leer continuar
    Fin Mientras
FinAlgoritmo
