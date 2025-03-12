Algoritmo contar_cifras
    // Declaraci�n de variables:
    // 'numero' almacenar� el n�mero introducido por el usuario.
    // 'cifras' almacenar� el n�mero de cifras del n�mero introducido.
    // 'continuar' ser� usado para controlar si el usuario quiere seguir ejecutando el programa.
    Definir numero, cifras Como Entero
    Definir continuar Como Caracter
	
    // Inicializamos la variable 'continuar' a 's' para que el bucle principal comience.
    continuar <- 's'
	
    // Bucle principal. Este se repetir� mientras el usuario introduzca 's' cuando se le pregunte si quiere continuar.
    Mientras continuar = 's' Hacer
        // Bucle de validaci�n del n�mero. El usuario debe ingresar un n�mero entre 0 y 99.999.
        Repetir
            // Solicita al usuario que introduzca un n�mero v�lido.
            Escribir "Introduce un n�mero entre 0 y 99.999:"
            Leer numero
			
            // Verificamos si el n�mero introducido est� fuera del rango permitido (0 a 99.999).
            // Si est� fuera de este rango, mostramos un mensaje de error.
            Si numero < 0 O numero > 99999 Entonces
                Escribir "Error: El n�mero no est� en el rango correcto. Por favor, int�ntalo de nuevo."
            Fin Si
			// El bucle se repite hasta que el n�mero est� dentro del rango v�lido.
        Hasta Que numero >= 0 Y numero <= 99999
		
        // Inicializamos 'cifras' en 0. Contaremos el n�mero de cifras del n�mero introducido.
        cifras <- 0
		
        // Caso especial: si el n�mero es 0, directamente sabemos que tiene 1 cifra.
        Si numero = 0 Entonces
            cifras <- 1
        Sino
            // Si el n�mero no es 0, contamos las cifras dividiendo repetidamente entre 10.
            // En cada iteraci�n, eliminamos el �ltimo d�gito y sumamos 1 a 'cifras'.
            Mientras numero > 0 Hacer
                numero <- Trunc(numero / 10)  // Dividimos entre 10 para eliminar el �ltimo d�gito.
                cifras <- cifras + 1          // Incrementamos el contador de cifras.
            Fin Mientras
        Fin Si
		
        // Mostramos el resultado al usuario, indicando cu�ntas cifras tiene el n�mero introducido.
        Escribir "El n�mero tiene ", cifras, " cifras."
		
        // Preguntamos al usuario si desea continuar o finalizar el programa.
        Escribir "�Quiere continuar?, Pulse s o cualquier otra tecla para finalizar"
        Leer continuar
    Fin Mientras

FinAlgoritmo
