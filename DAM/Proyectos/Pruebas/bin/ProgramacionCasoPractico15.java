

public class ProgramacionCasoPractico15 {

    public static void main(String[] args) {
        int contador = 0; // Variable para contar los múltiplos

        // Bucle que recorre los números entre 1 y 100
        for (int i = 1; i <= 100; i++) {
            // Verifica si el número es múltiplo de 2 o de 3
            if (i % 2 == 0 || i % 3 == 0) {
                System.out.println(i); // Muestra el número
                contador++; // Incrementa el contador
            }
        }

        // Muestra la cantidad total de múltiplos encontrados
        System.out.println("Total de números múltiplos de 2 o 3 entre 1 y 100: " + contador);
    }


}
