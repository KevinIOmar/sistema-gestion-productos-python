import dataset

db = dataset.connect("sqlite:///inventario.db")
tabla = db["productos"]

# FUNCIONES DE VALIDACIÓN
def validar_texto(mensaje):
    """Solicita un texto y verifica que no esté vacío."""
    while True:
        entrada = input(mensaje).strip()
        if entrada != "":
            return entrada
        print(">> Error: El campo no puede quedar vacío. Ingrese un dato válido.")


def validar_precio(mensaje):
    """Solicita el precio y valida que sea un número decimal mayor a 0."""
    while True:
        entrada = input(mensaje).strip()
        try:
            valor = float(entrada)
            if valor > 0:
                return valor
            else:
                print(">> Error: El precio debe ser mayor a 0.")
        except ValueError:
            print(">> Error: Debe ingresar un valor numérico válido (ej: 1500 o 350.50).")


def validar_cantidad(mensaje):
    """Solicita el stock y valida que sea un entero mayor o igual a 0."""
    while True:
        entrada = input(mensaje).strip()
        try:
            valor = int(entrada)
            if valor >= 0:
                return valor
            else:
                print(">> Error: La cantidad no puede ser negativa.")
        except ValueError:
            print(">> Error: Ingrese un número entero válido (ej: 0, 5, 20).")


# FUNCIONES DEL SISTEMA
def agregar_producto():
    print("\n--- AGREGAR PRODUCTO ---")
    nombre = validar_texto("Ingrese el nombre del producto: ").title()
    categoria = validar_texto("Ingrese la categoría: ").title()
    precio = validar_precio("Ingrese el precio: $")
    cantidad = validar_cantidad("Ingrese la cantidad (stock): ")

    tabla.insert({
        "nombre": nombre,
        "categoria": categoria,
        "precio": precio,
        "cantidad": cantidad
    })
    print(f"\n¡Éxito! Producto '{nombre}' guardado en la base de datos.")


def listar_productos():
    print("\n--- LISTA DE PRODUCTOS ---")
    registros = list(tabla.all())

    if len(registros) == 0:
        print("No hay productos cargados en el sistema.")
        return False

    for prod in registros:
        print(
            f"ID: {prod['id']} | Nombre: {prod['nombre']} | "
            f"Categoría: {prod['categoria']} | Precio: ${prod['precio']:.2f} | "
            f"Stock: {prod['cantidad']}"
        )
    return True


def buscar_producto_unico():
    print("\n--- BÚSQUEDA EXACTA ---")
    if len(list(tabla.all())) == 0:
        print("No hay productos en el sistema para buscar.")
        return

    nombre_buscar = validar_texto("Nombre exacto del producto a buscar: ").title()
    existe = tabla.find_one(nombre=nombre_buscar)

    if existe:
        print("\nProducto encontrado:")
        print(
            f"ID: {existe['id']} | Nombre: {existe['nombre']} | "
            f"Categoría: {existe['categoria']} | Precio: ${existe['precio']:.2f} | "
            f"Stock: {existe['cantidad']}"
        )
    else:
        print(f"\n*** NO se encontró '{nombre_buscar}' ***")


def busqueda_multiple():
    print("\n--- BÚSQUEDA MÚLTIPLE ---")
    registros = list(tabla.all())

    if len(registros) == 0:
        print("No hay productos en el sistema para buscar.")
        return

    termino = validar_texto("Ingrese el nombre (o parte) a buscar: ").lower()
    encontrados = [prod for prod in registros if termino in prod["nombre"].lower()]

    if len(encontrados) > 0:
        print(f"\nSe encontraron {len(encontrados)} coincidencia(s):")
        for prod in encontrados:
            print(
                f"ID: {prod['id']} | Nombre: {prod['nombre']} | "
                f"Categoría: {prod['categoria']} | Precio: ${prod['precio']:.2f} | "
                f"Stock: {prod['cantidad']}"
            )
    else:
        print(f"\nNo se encontraron productos que coincidan con '{termino}'.")


def borrar_por_id():
    print("\n--- BORRAR POR ID ---")
    if not listar_productos():
        return

    while True:
        entrada = input("\nIngrese el ID a borrar (o 0 para cancelar): ").strip()
        try:
            id_objetivo = int(entrada)
            if id_objetivo == 0:
                print("Operación cancelada.")
                return

            producto = tabla.find_one(id=id_objetivo)
            if producto is not None:
                tabla.delete(id=id_objetivo)
                print(f"\n¡El producto '{producto['nombre']}' (ID {id_objetivo}) fue borrado con éxito!")
                return
            else:
                print(f">> Error: No existe ningún producto con el ID {id_objetivo}.")
        except ValueError:
            print(">> Error: Debe ingresar un número entero válido.")


def borrar_por_nombre():
    print("\n--- BORRAR POR NOMBRE ---")
    if not listar_productos():
        return

    nombre_borrar = validar_texto("\nIngrese el nombre exacto del producto a borrar: ").title()
    coincidencias = list(tabla.find(nombre=nombre_borrar))

    if len(coincidencias) == 0:
        print(f">> Error: No se encontró ningún producto llamado '{nombre_borrar}'.")
        return

    confirmar = input(
        f"Se encontraron {len(coincidencias)} registro(s) con el nombre '{nombre_borrar}'. "
        "¿Confirma que desea borrarlo(s)? (S/N): "
    ).strip().upper()

    if confirmar == "S":
        tabla.delete(nombre=nombre_borrar)
        print(f"\n¡'{nombre_borrar}' borrado con éxito!")
    else:
        print("Operación cancelada.")


# MENÚ PRINCIPAL CON MATCH
def menu_principal():
    while True:
        print("\n========================================")
        print("  SISTEMA DE GESTIÓN DE PRODUCTOS")
        print("========================================")
        print("A - Agregar producto")
        print("L - Listar productos")
        print("B - Buscar")
        print("G - Búsqueda múltiple")
        print("*** Borrar ***")
        print("I - Borrar por ID")
        print("N - Borrar por nombre")
        print("----------------------------------------")
        print("S - Salir")
        print("========================================")

        opcion = input("Seleccione una opción: ").strip().upper()

        match opcion:
            case "A":
                agregar_producto()
            case "L":
                listar_productos()
            case "B":
                buscar_producto_unico()
            case "G":
                busqueda_multiple()
            case "I":
                borrar_por_id()
            case "N":
                borrar_por_nombre()
            case "S":
                print("\n¡Gracias por usar el sistema! Saliendo...")
                break
            case _:
                print(">> Opción inválida. Por favor, elija una de las letras del menú.")


menu_principal()