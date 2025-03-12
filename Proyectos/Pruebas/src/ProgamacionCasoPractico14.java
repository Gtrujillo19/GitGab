import java.util.Scanner;

public class ProgamacionCasoPractico14 {

	public static void main(String[] args) {

		// Declaracion variables

		double peso;
		double altura;
		Scanner teclado = new Scanner(System.in);

		// Pedir peso

		System.out.println("Introduzca su peso en Kilos:\n");
		peso = teclado.nextDouble();

		while (peso < 30 || peso > 300) {
			System.out.println("Peso no válido, introduzca el peso de nuevo:");
			peso = teclado.nextDouble();
		}

		// Pedir altura (con coma)

		System.out.println("Introduzca su altura en Metros:\n");
		altura = teclado.nextDouble();

		while (altura < 1.30 || altura > 2.0) {
			System.out.println("Altura no válida, introduzca altura de nuevo:\n");
			altura = teclado.nextDouble();
		}

		// Imprimir imc

		System.out.println("DATOS CORRECTOS, CALCULANDO IMC!\n");

		// Calculo imc

		double imc;
		imc = peso / (altura * altura);
		System.out.printf("Su indice de masa corporal es: %.2f%n\n", imc);

		// Imprimir categoria segun imc

		if (imc < 18.5) {
			System.out.println("Bajo peso");
		}

		if (imc >= 18.5 && imc <= 24.9) {
			System.out.println("Peso Normal");
		}

		if (imc >= 25 && imc <= 29.9) {
			System.out.println("Sobrepeso");
		}
		if (imc >= 30) {
			System.out.println("Obesidad");
		}

		// Cerrar scanner

		teclado.close();
	}

}