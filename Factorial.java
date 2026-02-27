public class Factorial {

    public int factorial (int n){
        if (n < 0) {
            throw new IllegalArgumentException("n debe ser >= 0");
        }

        int fact = 1;

        for (int i = 1; i <= n; i++) {
            fact = i * fact;
        }

        return fact;
    }

    // Versión recursiva
    public int factorialRecursive(int n) {
        if (n < 0) {
            throw new IllegalArgumentException("n debe ser >= 0");
        }

        if (n == 0) {
            return 1; // caso base
        }

        return n * factorialRecursive(n - 1); // llamada recursiva
    }

    // Método main de ejemplo
    public static void main(String[] args) {
        Factorial f = new Factorial();
        int n = 5;
        System.out.println("Iterativo " + n + "! = " + f.factorial(n));
        System.out.println("Recursivo " + n + "! = " + f.factorialRecursive(n));
    }
}