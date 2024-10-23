Algoritmo contar_cifras
    // Declaración de variables:
    // 'numero' almacenará el número introducido por el usuario.
    // 'cifras' almacenará el número de cifras del número introducido.
    // 'continuar' será usado para controlar si el usuario quiere seguir ejecutando el programa.
    Definir numero, cifras Como Entero
    Definir continuar Como Caracter
	
    // Inicializamos la variable 'continuar' a 's' para que el bucle principal comience.
    continuar <- 's'
	
    // Bucle principal. Este se repetirá mientras el usuario introduzca 's' cuando se le pregunte si quiere continuar.
    Mientras continuar = 's' Hacer
        // Bucle de validación del número. El usuario debe ingresar un número entre 0 y 99.999.
        Repetir
            // Solicita al usuario que introduzca un número válido.
            Escribir "Introduce un número entre 0 y 99.999:"
            Leer numero
			
            // Verificamos si el número introducido está fuera del rango permitido (0 a 99.999).
            // Si está fuera de este rango, mostramos un mensaje de error.
            Si numero < 0 O numero > 99999 Entonces
                Escribir "Error: El número no está en el rango correcto. Por favor, inténtalo de nuevo."
            Fin Si
			// El bucle se repite hasta que el número esté dentro del rango válido.
        Hasta Que numero >= 0 Y numero <= 99999
		
        // Inicializamos 'cifras' en 0. Contaremos el número de cifras del número introducido.
        cifras <- 0
		
        // Caso especial: si el número es 0, directamente sabemos que tiene 1 cifra.
        Si numero = 0 Entonces
            cifras <- 1
        Sino
            // Si el número no es 0, contamos las cifras dividiendo repetidamente entre 10.
            // En cada iteración, eliminamos el último dígito y sumamos 1 a 'cifras'.
            Mientras numero > 0 Hacer
                numero <- Trunc(numero / 10)  // Dividimos entre 10 para eliminar el último dígito.
                cifras <- cifras + 1          // Incrementamos el contador de cifras.
            Fin Mientras
        Fin Si
		
        // Mostramos el resultado al usuario, indicando cuántas cifras tiene el número introducido.
        Escribir "El número tiene ", cifras, " cifras."
		
        // Preguntamos al usuario si desea continuar o finalizar el programa.
        Escribir "¿Quiere continuar?, Pulse s o cualquier otra tecla para finalizar"
        Leer continuar
    Fin Mientras

FinAlgoritmo
