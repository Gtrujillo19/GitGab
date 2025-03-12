
import java.util.Scanner;

public class gNumber {
    public static void main(String[] args) {

        Scanner scanner = new Scanner(System.in);

        // Date Needed//
        int altNumb = (int) (Math.random() * 100) + 1;
        int userNumb = 0;
        int attempts = 0;

        // Start Mesagge//
        System.out.println("Guess the number between 1 and 100");

        // Bucle//

        while (userNumb != altNumb) {
            userNumb = scanner.nextInt();
            attempts++;

            if (userNumb > altNumb) {
                System.out.println("Wrong Number , try again.");
                System.out.println("Lower!");
            } else if (userNumb < altNumb) {
                System.out.println("Wrong Number , try again.");
                System.out.println("Higher!");
            }

        }

        // Mensaje de éxito
        System.out.println("Correct! You guessed the number in " + attempts + " attempts.");

        // Cerrar Scanner
        scanner.close();

    }
}