
import java.util.Scanner;

public class Prg2Proyct2 {

	public static void main(String[] args) {
		
	/* Declaración Variables */
	
	  int  edad;
	  boolean mayorEdad;
	  Scanner sc = new Scanner (System.in);
	  
	/* Introcucción variables */
	
	System.out.println("Introduce la edad");
	
	edad = sc.nextInt();
	
	/* Condicionales */
	
    if (edad>=18)  { 
    	System.out.print("Es mayor de edad");
    	mayorEdad = true;
    }
  	 
    else  {
    	System.out.println("No es mayor de edad");
    	mayorEdad = false;
    }
    /* Cierre Scanner */
 
    sc.close();
	}

}
 