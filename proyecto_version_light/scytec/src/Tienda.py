class Tienda:
    def __init__(self, id_tienda: int, nombre: str, ubicacion: str, telefono: str):
        self.id_tienda = id_tienda
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.telefono = telefono

    def obtener_productos_disponibles(self):
        print(f"Obteniendo productos disponibles en la tienda '{self.nombre}'...")
        productos = [
            {"id": 1, "nombre": "Producto A", "precio": 100.0, "stock": 10},
            {"id": 2, "nombre": "Producto B", "precio": 200.0, "stock": 5},
            {"id": 3, "nombre": "Producto C", "precio": 300.0, "stock": 2},
        ]
        return productos

    def buscar_tienda_cercana(self, ubicacion_usuario: str):
        print(f"Buscando si '{self.nombre}' es cercana al usuario en '{ubicacion_usuario}'...")
        return f"Tienda '{self.nombre}' es cercana al usuario."


if __name__ == "__main__":
    tienda = Tienda(1, "Tienda A", "Ciudad de México", "555-1234")

    productos = tienda.obtener_productos_disponibles()
    print("Productos disponibles:")
    for producto in productos:
        print(f"- {producto['nombre']} (Precio: {producto['precio']}, Stock: {producto['stock']})")

    resultado = tienda.buscar_tienda_cercana("Ciudad de México")
    print(resultado)
