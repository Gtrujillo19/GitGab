package DAM.Programación.UD3.CPUD3.CPPROG1UD3;

// Clase Empleado
public class Empleado {
    private String nombre;
    private String apellidos;
    private int edad;
    private double salario;

    // Constructor sin parámetros
    public Empleado() {}

    // Constructor con parámetros
    public Empleado(String nombre, String apellidos, int edad, double salario) {
        this.nombre = nombre;
        this.apellidos = apellidos;
        this.edad = edad;
        this.salario = salario;
    }

    // Getters y Setters
    public String getNombre() {
        return nombre;
    }

    public void setNombre(String nombre) {
        this.nombre = nombre;
    }

    public String getApellidos() {
        return apellidos;
    }

    public void setApellidos(String apellidos) {
        this.apellidos = apellidos;
    }

    public int getEdad() {
        return edad;
    }

    public void setEdad(int edad) {
        this.edad = edad;
    }

    public double getSalario() {
        return salario;
    }

    public void setSalario(double salario) {
        this.salario = salario;
    }
}

// Clase Administrativo
public class Administrativo extends Empleado {
    private String departamento;

    // Constructor sin parámetros
    public Administrativo() {}

    // Constructor con parámetros
    public Administrativo(String nombre, String apellidos, int edad, double salario, String departamento) {
        super(nombre, apellidos, edad, salario);
        this.departamento = departamento;
    }

    // Getters y Setters
    public String getDepartamento() {
        return departamento;
    }

    public void setDepartamento(String departamento) {
        this.departamento = departamento;
    }
}

// Clase Contable
public class Contable extends Empleado {
    private String tipoContabilidad;

    // Constructor sin parámetros
    public Contable() {}

    // Constructor con parámetros
    public Contable(String nombre, String apellidos, int edad, double salario, String tipoContabilidad) {
        super(nombre, apellidos, edad, salario);
        this.tipoContabilidad = tipoContabilidad;
    }

    // Getters y Setters
    public String getTipoContabilidad() {
        return tipoContabilidad;
    }

    public void setTipoContabilidad(String tipoContabilidad) {
        this.tipoContabilidad = tipoContabilidad;
    }
}

// Clase Informático
public class Informatico extends Empleado {
    private String lenguajePrincipal;

    // Constructor sin parámetros
    public Informatico() {}

    // Constructor con parámetros
    public Informatico(String nombre, String apellidos, int edad, double salario, String lenguajePrincipal) {
        super(nombre, apellidos, edad, salario);
        this.lenguajePrincipal = lenguajePrincipal;
    }

    // Getters y Setters
    public String getLenguajePrincipal() {
        return lenguajePrincipal;
    }

    public void setLenguajePrincipal(String lenguajePrincipal) {
        this.lenguajePrincipal = lenguajePrincipal;
    }
}
{

}
