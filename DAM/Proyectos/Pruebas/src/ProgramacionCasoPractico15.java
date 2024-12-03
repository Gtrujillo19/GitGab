
public class ProgramacionCasoPractico15 {

	public static void main(String[] args) {
		
        int contadorMultiplos2 = 0;  // Contador de múltiplos de 2
        int contadorMultiplos3 = 0;  // Contador de múltiplos de 3

        for (int i = 0; i <= 100; i++) {

            if (i % 2 == 0) {  // Si el número es múltiplo de 2
                System.out.println(i);
                contadorMultiplos2++;  // Aumentar el contador de múltiplos de 2
            }
            
            if (i % 3 == 0) {  // Si el número es múltiplo de 3
                System.out.println(i);
                contadorMultiplos3++;  // Aumentar el contador de múltiplos de 3
            }
        }
        System.out.printf("Hay %d múltiplos de 2 y %d múltiplos de 3.\n", contadorMultiplos2, contadorMultiplos3);
	}
}
