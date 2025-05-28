import sqlite3
from colorama import Fore, init

init()


# Crear tabla, y si existe que no se cree otra.
def crear_tabla_productos():
    try:
        with sqlite3.connect("Inventario.db") as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS productos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    descripcion TEXT,
                    categoria TEXT NOT NULL,
                    cantidad INTEGER NOT NULL,
                    precio REAL NOT NULL
                )
            """
            )
            print(Fore.GREEN + "Tabla 'productos' creada o ya existe.")
    except Exception as e:
        print(Fore.RED + f"Error al crear la tabla: {e}")


def mostrar_menu():
    print(Fore.CYAN + "-" * 30)
    print(Fore.CYAN + "Menú principal")
    print("-" * 30)
    print(
        """
        1. Agregar producto
        2. Mostrar producto
        3. Actualizar Cantidad de Producto
        4. Eliminar Producto
        5. Buscar producto
        6. Reporte bajo stock
        7. Salir
    """
    )
    while True:
        try:
            opcion = int(input("Ingrese opción deseada (1-7): "))
            if 1 <= opcion <= 7:
                return opcion
            else:
                print(Fore.RED + "Por favor, seleccione una opción válida del 1 al 7.")
        except ValueError:
            print(Fore.RED + "Error: Por favor ingrese un número válido.")


def obtener_producto_por_nombre(nombre):
    with sqlite3.connect("Inventario.db") as conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM productos WHERE nombre = ?", (nombre,))
        return cursor.fetchall()


def agregar_producto():
    while True:
        nombre = input(
            "Ingrese el nombre del producto (Presione 'n' para salir): "
        ).capitalize()
        if nombre.lower() == "n":
            break

        descripcion = input("Ingrese una breve descripción: ").capitalize()
        categoria = input("Ingrese la categoría del producto: ").capitalize()

        cantidad = validar_entrada_numero("Ingrese la cantidad: ", int)
        precio = validar_entrada_numero("Ingrese el precio: ", float)

        with sqlite3.connect("Inventario.db") as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                """
                INSERT INTO productos (nombre, descripcion, categoria, cantidad, precio) 
                VALUES (?, ?, ?, ?, ?)
            """,
                (nombre, descripcion, categoria, cantidad, precio),
            )

        print(Fore.GREEN + f"Producto '{nombre}' agregado correctamente.")


def mostrar_productos():
    with sqlite3.connect("Inventario.db") as conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM productos ORDER BY id ASC;")
        resultados = cursor.fetchall()

    if resultados:
        for producto in resultados:
            print(
                Fore.LIGHTWHITE_EX
                + f"ID: {producto[0]} | Nombre: {producto[1]} | Cantidad: {producto[4]} | Precio: {producto[5]}"
            )
    else:
        print(Fore.RED + "No hay productos registrados en el inventario.")


def actualizar_producto():
    nombre = input("Ingrese el nombre del producto que desea actualizar: ").capitalize()
    resultados = obtener_producto_por_nombre(nombre)

    if resultados:
        nuevo_stock = validar_entrada_numero("Ingrese la nueva cantidad: ", int)
        with sqlite3.connect("Inventario.db") as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                "UPDATE productos SET cantidad = ? WHERE nombre = ?",
                (nuevo_stock, nombre),
            )
        print(Fore.GREEN + f"El stock del producto '{nombre}' ha sido actualizado.")
    else:
        print(Fore.RED + f"No se encontró el producto '{nombre}'.")


def eliminar_producto():
    nombre = input("Ingrese el nombre del producto que desea eliminar: ").capitalize()
    resultados = obtener_producto_por_nombre(nombre)

    if resultados:
        with sqlite3.connect("Inventario.db") as conexion:
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM productos WHERE nombre = ?", (nombre,))
        print(Fore.RED + f"Producto '{nombre}' eliminado.")
    else:
        print(Fore.RED + f"No se encontró el producto '{nombre}'.")


def buscar_producto():
    nombre = input("Ingrese el nombre del producto que desea buscar: ").capitalize()
    resultados = obtener_producto_por_nombre(nombre)

    if resultados:
        for producto in resultados:
            print(
                Fore.LIGHTWHITE_EX
                + f"ID: {producto[0]} | Nombre: {producto[1]} | Cantidad: {producto[4]} | Precio: {producto[5]}"
            )
    else:
        print(Fore.RED + f"No se encontró el producto '{nombre}'.")


def bajo_stock():
    umbral = validar_entrada_numero("Ingrese el umbral de stock mínimo: ", int)
    with sqlite3.connect("Inventario.db") as conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM productos WHERE cantidad < ?", (umbral,))
        productos = cursor.fetchall()

    if productos:
        print("\nProductos con bajo stock:")
        for producto in productos:
            print(
                Fore.LIGHTWHITE_EX
                + f"ID: {producto[0]} | Nombre: {producto[1]} | Cantidad: {producto[4]}"
            )
    else:
        print(Fore.RED + f"No hay productos con stock inferior a {umbral}.")


def validar_entrada_numero(mensaje, tipo):
    while True:
        try:
            entrada = tipo(input(mensaje))
            if entrada > 0:
                return entrada
            else:
                print(Fore.RED + "El valor debe ser mayor a cero.")
        except ValueError:
            print(Fore.RED + "Por favor ingrese un valor válido.")


def main():
    crear_tabla_productos()
    while True:
        opcion = mostrar_menu()
        if opcion == 1:
            agregar_producto()
        elif opcion == 2:
            mostrar_productos()
        elif opcion == 3:
            actualizar_producto()
        elif opcion == 4:
            eliminar_producto()
        elif opcion == 5:
            buscar_producto()
        elif opcion == 6:
            bajo_stock()
        elif opcion == 7:
            print(Fore.GREEN + "Saliendo del sistema de inventario.")
            break
        else:
            print(Fore.RED + "Opción no válida, intente nuevamente.")


if __name__ == "__main__":
    main()
