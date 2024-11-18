class Producto:
    def __init__(self, id_producto: int, nombre: str, descripcion: str, precio: float, stock: int, ruta_foto: str, id_tienda: int):
        """
        Constructor para inicializar un producto.
        :param id_producto: Identificador único del producto.
        :param nombre: Nombre del producto.
        :param descripcion: Descripción del producto.
        :param precio: Precio del producto.
        :param stock: Cantidad disponible del producto.
        :param ruta_foto: Ruta de la foto del producto.
        :param id_tienda: Identificador de la tienda asociada.
        """
        self.id_producto = id_producto
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock
        self.ruta_foto = ruta_foto
        self.id_tienda = id_tienda

    def __str__(self):
        """
        Representación en cadena del producto.
        """
        return (f"Producto(ID: {self.id_producto}, Nombre: {self.nombre}, "
                f"Descripción: {self.descripcion}, Precio: ${self.precio:.2f}, "
                f"Stock: {self.stock}, Foto: {self.ruta_foto}, Tienda: {self.id_tienda})")

    def actualizar_stock(self, nuevo_stock: int):
        """
        Actualiza el stock del producto.
        :param nuevo_stock: Nueva cantidad de stock.
        """
        self.stock = nuevo_stock
        print(f"El stock del producto '{self.nombre}' se ha actualizado a {nuevo_stock}.")

    def aplicar_descuento(self, porcentaje: float):
        """
        Aplica un descuento al precio del producto.
        :param porcentaje: Porcentaje de descuento a aplicar.
        """
        descuento = self.precio * (porcentaje / 100)
        self.precio -= descuento
        print(f"Se aplicó un descuento del {porcentaje}%. Nuevo precio: ${self.precio:.2f}")
