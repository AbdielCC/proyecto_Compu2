class Inventario:
    def __init__(self, base_datos):
        """
        Constructor para inicializar el inventario.
        :param base_datos: Instancia de la clase BaseDeDatos para interactuar con la base de datos.
        """
        self.base_datos = base_datos

    def agregar_producto(self, nombre, descripcion, precio, stock, ruta_foto, id_tienda):
        """
        Agrega un producto al inventario.
        :param nombre: Nombre del producto.
        :param descripcion: Descripción del producto.
        :param precio: Precio del producto.
        :param stock: Cantidad disponible del producto.
        :param ruta_foto: Ruta de la foto del producto.
        :param id_tienda: ID de la tienda asociada al producto.
        """
        self.base_datos.agregar_producto(nombre, descripcion, precio, stock, ruta_foto, id_tienda)

    def actualizar_stock(self, id_producto, nuevo_stock):
        """
        Actualiza el stock de un producto específico.
        :param id_producto: ID del producto a actualizar.
        :param nuevo_stock: Nueva cantidad de stock.
        """
        try:
            self.base_datos.cursor.execute(
                "UPDATE productos SET stock = %s WHERE id_producto = %s;",
                (nuevo_stock, id_producto)
            )
            self.base_datos.conn.commit()
            print(f"Stock del producto {id_producto} actualizado a {nuevo_stock}.")
        except Exception as e:
            print(f"Error al actualizar el stock: {e}")
            self.base_datos.conn.rollback()

    def obtener_productos(self):
        """
        Obtiene la lista completa de productos en el inventario.
        :return: Lista de productos.
        """
        return self.base_datos.obtener_productos()

    def obtener_tiendas(self):
        """
        Obtiene la lista completa de tiendas.
        :return: Lista de tiendas.
        """
        return self.base_datos.obtener_tiendas()

    def buscar_producto(self, id_producto):
        """
        Busca un producto por su ID en el inventario.
        :param id_producto: ID del producto.
        :return: Información del producto o None si no se encuentra.
        """
        return self.base_datos.consultar_producto(id_producto)

    def eliminar_producto(self, id_producto):
        """
        Elimina un producto del inventario por su ID.
        :param id_producto: ID del producto a eliminar.
        """
        try:
            self.base_datos.cursor.execute(
                "DELETE FROM productos WHERE id_producto = %s;",
                (id_producto,)
            )
            self.base_datos.conn.commit()
            print(f"Producto {id_producto} eliminado del inventario.")
        except Exception as e:
            print(f"Error al eliminar el producto: {e}")
            self.base_datos.conn.rollback()
