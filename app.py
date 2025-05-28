# Lista para almacenar los productos

productos = []


def agregar_producto():

    while True:
        # Verificar si el usuario quiere salir
        elemento = input(
            "Por favor, ingrese el nombre del producto (Presione 'n' para salir) : "
        ).lower()
        if elemento == "n":
            print("\nSaliendo de la función de agregar producto.\n")
            break

        # Validación de cantidad
        while True:
            try:
                cant = float(input("Por favor, ingrese la cantidad: "))
                if cant <= 0:
                    print("La cantidad debe ser mayor que cero.")
                else:
                    break
            except ValueError:
                print("Error: Por favor ingrese un número válido.")

        # Agregar el producto al inventario
        producto = {"Nombre": elemento, "stock": cant}
        productos.append(producto)
        print(f"\nProducto '{elemento}' agregado al inventario con cantidad {cant}.\n")

    return productos  # Retorna la lista de productos en lugar del último producto


def ver_lista():
    if not productos:
        print("\nNo hay productos en la lista")
        return
    else:
        print("\nLista de productos: \n")
        for i, producto in enumerate(productos):
            print(
                f"Producto {i+1}: {producto['Nombre']} - cantidad {producto['stock']}\n"
            )


# Función principal para el sistema de inventario (NO ELIMINAR)
def main():
    # AQUÍ PUEDES COMENZAR A DESARROLLAR LA SOLUCIÓN
    print("Bienvenido al menu interactivo de inventario")

    while True:
        print("\n1- Agregar producto al inventario")
        print("2- Mostrar productos del inventario")
        print("3- Salir")

        opcion = input("\nPor favor, ingrese una opción: ").upper()

        if opcion == "1":
            agregar_producto()

        elif opcion == "2":
            ver_lista()

        elif opcion == "3":
            print("\nHa salida del menu iteractivo\n")
            break
        else:
            print(
                "\nHa ingresado un opción incorrecta, selecciones entre las opciones indicadas."
            )

    print("Detalles del producto:")
    for producto in productos:
        print(f"Nombre: {producto['Nombre']}, Cantidad: {producto['stock']}")

    # Ejecución de la función main() - (NO ELIMINAR)


if __name__ == "__main__":
    main()
