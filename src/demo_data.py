from src.inventory import agregar_producto
from src.sales import registrar_venta


def cargar_demo():

    productos_demo = [
        ("Coca Cola 350ml", 25, 1200),
        ("Pepsi 350ml", 18, 1100),
        ("Agua Mineral", 40, 900),
        ("Papas Fritas", 12, 1500),
        ("Galletas Oreo", 20, 1800),
        ("Arroz 1kg", 15, 1400),
        ("Azúcar 1kg", 10, 1300),
        ("Fideos Espagueti", 22, 1000),
        ("Aceite 1L", 8, 4500),
        ("Leche Entera", 16, 1600),
        ("Pan de Molde", 14, 2200),
        ("Café Instantáneo", 11, 3500),
        ("Té 100 bolsas", 9, 2800),
        ("Chocolate", 7, 2000),
        ("Atún en lata", 13, 1700),
        ("Mayonesa", 6, 2500),
        ("Ketchup", 5, 1900),
        ("Detergente", 4, 5200),
        ("Jabón Líquido", 17, 4800),
        ("Papel Higiénico", 30, 6500),
    ]

    for nombre, stock, precio in productos_demo:
        agregar_producto(nombre, stock, precio)

    ventas_demo = [
        ("Coca Cola 350ml", 3, 1200),
        ("Papas Fritas", 2, 1500),
        ("Leche Entera", 4, 1600),
        ("Aceite 1L", 1, 4500),
        ("Chocolate", 5, 2000),
    ]

    for producto, cantidad, precio in ventas_demo:
        registrar_venta(producto, cantidad, precio)

    return True