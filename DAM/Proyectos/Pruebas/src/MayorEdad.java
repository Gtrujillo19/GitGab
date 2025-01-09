import java.util.Scanner;  // Corregido: Scanner con mayúscula

public class MayorEdad {

    public static void main(String[] args) {
        /* Declaración Variables */
        int edad;
        boolean mayorEdad;
        Scanner sc = new Scanner(System.in);  // Correcto uso de Scanner
        
        /* Introducción variables */
        System.out.println("Introduce la edad");
        
        edad = sc.nextInt();
        
        /* Condicionales */
        if (edad >= 18) { 
            System.out.println("Es mayor de edad");
            mayorEdad = true;
        } else {
            System.out.println("No es mayor de edad");
            mayorEdad = false;
        }

        /* Cierre Scanner */
        sc.close();
    }
}
