import java.util.Scanner;

public class ProgramaciónCasoPractico11 {

    public static void main(String[] args) {

        // DECLARACION VARIABLES
        int primerNumeroPedir;
        int segundoNumeroPedir;
        int tercerNumeroPedir;
        int cajaAuxiliar;

        // Scanner
        Scanner scanner = new Scanner(System.in);

        // PEDIR NUMEROS AL USUARIO
        System.out.println("Introduzca número 1:");
        primerNumeroPedir = scanner.nextInt();

        System.out.println("Introduzca número 2:");
        segundoNumeroPedir = scanner.nextInt();

        System.out.println("Introduzca número 3:");
        tercerNumeroPedir = scanner.nextInt();

        // Ascendente o descendente
        System.out.println("Escoja ordenación: introduzca 'a' para ascendente o 'd' para descendente.");
        String orden = scanner.next();

        // Metodo de ordenación con for
        if (orden.equals("a")) {
            System.out.println("Ha elegido orden ascendente.");

            // Ordenar ascendentemente usando un bucle for
            for (int i = 0; i < 2; i++) {
                if (primerNumeroPedir > segundoNumeroPedir) {
                    cajaAuxiliar = primerNumeroPedir;
                    primerNumeroPedir = segundoNumeroPedir;
                    segundoNumeroPedir = cajaAuxiliar;
                }
                if (segundoNumeroPedir > tercerNumeroPedir) {
                    cajaAuxiliar = segundoNumeroPedir;
                    segundoNumeroPedir = tercerNumeroPedir;
                    tercerNumeroPedir = cajaAuxiliar;
                }
            }

            System.out.println("Orden ascendente: " + primerNumeroPedir + ", " + segundoNumeroPedir + ", " + tercerNumeroPedir);

        } else if (orden.equals("d")) {
            System.out.println("Ha elegido orden descendente.");

            // Ordenar descendentemente usando un bucle for
            for (int i = 0; i < 2; i++) {
                if (primerNumeroPedir < segundoNumeroPedir) {
                    cajaAuxiliar = primerNumeroPedir;
                    primerNumeroPedir = segundoNumeroPedir;
                    segundoNumeroPedir = cajaAuxiliar;
                }
                if (segundoNumeroPedir < tercerNumeroPedir) {
                    cajaAuxiliar = segundoNumeroPedir;
                    segundoNumeroPedir = tercerNumeroPedir;
                    tercerNumeroPedir = cajaAuxiliar;
                }
            }

            System.out.println("Orden descendente: " + primerNumeroPedir + ", " + segundoNumeroPedir + ", " + tercerNumeroPedir);

        } else {
            System.out.println("Opción no válida. Intente de nuevo.");
        }

        scanner.close();
    }

}
