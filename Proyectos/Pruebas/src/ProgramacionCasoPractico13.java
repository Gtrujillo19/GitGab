import java.util.Scanner;

public class ProgramacionCasoPractico13 {

	public static void main(String[] args) {

		// Variables

		int numero;

		// Scanner
		Scanner scanner = new Scanner(System.in);
		System.out.println("Introduce un número positivo:");
		numero = scanner.nextInt();

		// Comprobar si es positivo

		while (numero < 0) {
			System.out.println("El número introducido es negativo. Inténtalo de nuevo.");
			System.out.print("Introduce un número positivo: ");
			numero = scanner.nextInt();
		}

		for (int i = numero; i <= 20; i++) {
			System.out.println(i);
		}
	}
}
