import java.util.Scanner;
 
public class Pract_Prog21{
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.print("Introduce un número entero: ");
        int num = sc.nextInt();
       
        System.out.print("Introduce un valor booleano: ");
        boolean b = sc.nextBoolean();
       
        System.out.print("Introduce un valor con decimales(tipo dato con precisión simple): ");
        float f = sc.nextFloat();
       
        System.out.print("Introduce un valor con decimales(tipo dato con precisión doble): ");
        double d = sc.nextDouble();
       
        sc.nextLine();
       
        System.out.print("Introduce una cadena de texto: ");
        String str = sc.nextLine();
       
        System.out.println("El número introducido es: " + num);
        System.out.println("El valor booleano introducido es: " + b);
        System.out.println("El valor con decimales de precisión simple es: " + f);
        System.out.println("El valor con decimales de precisión doble es: " + d);
        System.out.println("La cadena de texto introducida es: "
+ str);
        sc.close();
    }
}