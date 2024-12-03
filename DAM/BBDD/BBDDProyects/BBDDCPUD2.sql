CREATE DATABASE CasoPractico2;
USE Normalizacion;
CREATE TABLE Estudiantes_Original (
    DNI VARCHAR(9),
    Apellidos VARCHAR(50),
    Nombre VARCHAR(50),
    Asignatura VARCHAR(255)
);
CREATE TABLE Facturas_Original (
    Sucursal INT,
    Numero_Factura INT,
    Codigo_Articulo INT,
    Nombre_Articulo VARCHAR(50),
    Cantidad INT,
    Precio DECIMAL(10,2),
    Subtotal DECIMAL(10,2)
);
INSERT INTO Estudiantes_Original VALUES 
('67454561B', 'Martínez García', 'Antonio', 'Bases de Datos, Programación, Cartografía'),
('78974635K', 'Sánchez López', 'María', 'Bases de datos, Geomática'),
('45436725H', 'Suárez Domínguez', 'Ana', 'Geomorfología, Topografía, Bases de datos');





