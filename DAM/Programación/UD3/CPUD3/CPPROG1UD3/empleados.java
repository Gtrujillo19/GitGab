package DAM.Programación.UD3.CPUD3.CPPROG1UD3;

// Clase principal
public class empleados {
    public static void main(String[] args) {
        // Usando el constructor con parámetros
        Administrativo admin1 = new Administrativo("Juan", 30, "Recursos Humanos");
        Contable contable1 = new Contable("Ana", 28, "Presupuesto");
        Informatico informatico1 = new Informatico("Carlos", 35, "Ciberseguridad");

        // Usando el constructor sin parámetros y setter
        Administrativo admin2 = new Administrativo();
        admin2.setNombre("Laura");
        admin2.setEdad(32);
        admin2.setDepartamento("Ventas");

        Contable contable2 = new Contable();
        contable2.setNombre("Luis");
        contable2.setEdad(40);
        contable2.setAreaFinanciera("Auditoría");

        Informatico informatico2 = new Informatico();
        informatico2.setNombre("María");
        informatico2.setEdad(29);
        informatico2.setEspecialidad("Desarrollo Web");

        // Mostrar los datos de los objetos
        System.out.println("Administrativo 1 (con parámetros):");
        System.out.println("Nombre: " + admin1.getNombre());
        System.out.println("Edad: " + admin1.getEdad());
        System.out.println("Departamento: " + admin1.getDepartamento());

        System.out.println("\nContable 1 (con parámetros):");
        System.out.println("Nombre: " + contable1.getNombre());
        System.out.println("Edad: " + contable1.getEdad());
        System.out.println("Área Financiera: " + contable1.getAreaFinanciera());

        System.out.println("\nInformático 1 (con parámetros):");
        System.out.println("Nombre: " + informatico1.getNombre());
        System.out.println("Edad: " + informatico1.getEdad());
        System.out.println("Especialidad: " + informatico1.getEspecialidad());

        System.out.println("\nAdministrativo 2 (sin parámetros):");
        System.out.println("Nombre: " + admin2.getNombre());
        System.out.println("Edad: " + admin2.getEdad());
        System.out.println("Departamento: " + admin2.getDepartamento());

        System.out.println("\nContable 2 (sin parámetros):");
        System.out.println("Nombre: " + contable2.getNombre());
        System.out.println("Edad: " + contable2.getEdad());
        System.out.println("Área Financiera: " + contable2.getAreaFinanciera());

        System.out.println("\nInformático 2 (sin parámetros):");
        System.out.println("Nombre: " + informatico2.getNombre());
        System.out.println("Edad: " + informatico2.getEdad());
        System.out.println("Especialidad: " + informatico2.getEspecialidad());
    }
}

// Clase base: Empleado
class Empleado {
    private String nombre;
    private int edad;

    // Constructor con parámetros
    public Empleado(String nombre, int edad) {
        this.nombre = nombre;
        this.edad = edad;
    }

    // Constructor sin parámetros
    public Empleado() {
        this.nombre = "Desconocido";
        this.edad = 0;
    }

    public String getNombre() {
        return nombre;
    }

    public void setNombre(String nombre) {
        this.nombre = nombre;
    }

    public int getEdad() {
        return edad;
    }

    public void setEdad(int edad) {
        this.edad = edad;
    }
}

// Clase derivada: Administrativo
class Administrativo extends Empleado {
    private String departamento;

    // Constructor con parámetros
    public Administrativo(String nombre, int edad, String departamento) {
        super(nombre, edad);
        this.departamento = departamento;
    }

    // Constructor sin parámetros
    public Administrativo() {
        super(); // Llamada al constructor de la clase base
        this.departamento = "No asignado";
    }

    public String getDepartamento() {
        return departamento;
    }

    public void setDepartamento(String departamento) {
        this.departamento = departamento;
    }
}

// Clase derivada: Contable
class Contable extends Empleado {
    private String areaFinanciera;

    // Constructor con parámetros
    public Contable(String nombre, int edad, String areaFinanciera) {
        super(nombre, edad);
        this.areaFinanciera = areaFinanciera;
    }

    // Constructor sin parámetros
    public Contable() {
        super(); // Llamada al constructor de la clase base
        this.areaFinanciera = "No asignado";
    }

    public String getAreaFinanciera() {
        return areaFinanciera;
    }

    public void setAreaFinanciera(String areaFinanciera) {
        this.areaFinanciera = areaFinanciera;
    }
}

// Clase derivada: Informático
class Informatico extends Empleado {
    private String especialidad;

    // Constructor con parámetros
    public Informatico(String nombre, int edad, String especialidad) {
        super(nombre, edad);
        this.especialidad = especialidad;
    }

    // Constructor sin parámetros
    public Informatico() {
        super(); // Llamada al constructor de la clase base
        this.especialidad = "No asignado";
    }

    public String getEspecialidad() {
        return especialidad;
    }

    public void setEspecialidad(String especialidad) {
        this.especialidad = especialidad;
    }
}
