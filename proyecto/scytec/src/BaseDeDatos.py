import psycopg2

class BaseDeDatos:
    def __init__(self, host: str, database: str, user: str, password: str):
        try:
            self.conn = psycopg2.connect(
                host=host,
                database=database,
                user=user,
                password=password
            )
            self.cursor = self.conn.cursor()
            print("Conexión a la base de datos establecida correctamente.")
        except Exception as e:
            print(f"Error al conectar a la base de datos: {e}")
            raise

    def crear_tablas(self):
        """
        Crea las tablas necesarias en la base de datos.
        """
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS tiendas (
                    id_tienda SERIAL PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    ubicacion VARCHAR(255) NOT NULL,
                    telefono VARCHAR(15),
                    ubicacion_lat NUMERIC,
                    ubicacion_lng NUMERIC
                );
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS productos (
                    id_producto SERIAL PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    descripcion TEXT,
                    precio NUMERIC NOT NULL,
                    stock INT NOT NULL,
                    ruta_foto VARCHAR(255),
                    id_tienda INT REFERENCES tiendas(id_tienda)
                );
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS compras (
                    id_compra SERIAL PRIMARY KEY,
                    id_producto INT REFERENCES productos(id_producto),
                    cantidad INT NOT NULL,
                    total NUMERIC NOT NULL,
                    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            self.conn.commit()
            print("Tablas creadas correctamente.")
        except Exception as e:
            print(f"Error al crear las tablas: {e}")
            self.conn.rollback()


    def agregar_tienda(self, nombre, ubicacion, telefono, latitud, longitud):
        """
        Agrega una nueva tienda con sus coordenadas.
        """
        try:
            self.cursor.execute(
                """
                INSERT INTO tiendas (nombre, ubicacion, telefono, ubicacion_lat, ubicacion_lng)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id_tienda;
                """,
                (nombre, ubicacion, telefono, latitud, longitud)
            )
            self.conn.commit()
            id_tienda = self.cursor.fetchone()[0]
            print(f"Tienda agregada correctamente con ID: {id_tienda}")
        except Exception as e:
            print(f"Error al agregar la tienda: {e}")
            self.conn.rollback()


    def agregar_producto(self, nombre: str, descripcion: str, precio: float, stock: int, ruta_foto: str, id_tienda: int):
        try:
            self.cursor.execute(
                """
                INSERT INTO productos (nombre, descripcion, precio, stock, ruta_foto, id_tienda)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id_producto;
                """,
                (nombre, descripcion, precio, stock, ruta_foto, id_tienda)
            )
            self.conn.commit()
            id_producto = self.cursor.fetchone()[0]
            print(f"Producto agregado correctamente con ID: {id_producto}")
        except Exception as e:
            print(f"Error al agregar el producto: {e}")
            self.conn.rollback()

    def registrar_usuario(self, nombre: str, ubicacion: str, edad: int):
        try:
            self.cursor.execute(
                """
                INSERT INTO usuarios (nombre, ubicacion, edad)
                VALUES (%s, %s, %s)
                RETURNING id_usuario;
                """,
                (nombre, ubicacion, edad)
            )
            self.conn.commit()
            id_usuario = self.cursor.fetchone()[0]
            print(f"Usuario registrado con ID: {id_usuario}")
            return id_usuario
        except Exception as e:
            print(f"Error al registrar usuario: {e}")
            self.conn.rollback()
            return None

    def registrar_compra(self, id_usuario: int, id_producto: int, id_tienda: int, cantidad: int):
        try:
            self.cursor.execute(
                "SELECT precio, stock FROM productos WHERE id_producto = %s;",
                (id_producto,)
            )
            producto = self.cursor.fetchone()
            if producto and producto[1] >= cantidad:
                precio, stock = producto
                total = precio * cantidad
                nuevo_stock = stock - cantidad

                self.cursor.execute(
                    """
                    INSERT INTO compras (id_usuario, id_producto, id_tienda, cantidad, total)
                    VALUES (%s, %s, %s, %s, %s);
                    """,
                    (id_usuario, id_producto, id_tienda, cantidad, total)
                )
                self.cursor.execute(
                    "UPDATE productos SET stock = %s WHERE id_producto = %s;",
                    (nuevo_stock, id_producto)
                )
                self.conn.commit()
                print(f"Compra registrada: Usuario {id_usuario}, Producto {id_producto}, Tienda {id_tienda}, Cantidad {cantidad}, Total {total}.")
            else:
                print("Stock insuficiente o producto no encontrado.")
        except Exception as e:
            print(f"Error al registrar la compra: {e}")
            self.conn.rollback()

    def obtener_productos(self):
        try:
            self.cursor.execute("SELECT * FROM productos;")
            productos = self.cursor.fetchall()
            return [
                {
                    "id_producto": producto[0],
                    "nombre": producto[1],
                    "descripcion": producto[2],
                    "precio": float(producto[3]),
                    "stock": producto[4],
                    "ruta_foto": producto[5],
                    "id_tienda": producto[6]
                }
                for producto in productos
            ]
        except Exception as e:
            print(f"Error al obtener productos: {e}")
            return []

    def cerrar_conexion(self):
        self.cursor.close()
        self.conn.close()
        print("Conexión a la base de datos cerrada.")
    
    def eliminar_tienda(self, id_tienda):
        """
        Elimina una tienda de la base de datos por su ID.
        """
        try:
            # Verificar si la tienda tiene productos asociados
            self.cursor.execute(
                "SELECT COUNT(*) FROM productos WHERE id_tienda = %s", (id_tienda,)
            )
            productos_asociados = self.cursor.fetchone()[0]

            if productos_asociados > 0:
                print(f"No se puede eliminar la tienda con ID {id_tienda} porque tiene productos asociados.")
                return

            # Eliminar la tienda
            self.cursor.execute("DELETE FROM tiendas WHERE id_tienda = %s", (id_tienda,))
            self.conn.commit()
            print(f"Tienda con ID {id_tienda} eliminada correctamente.")
        except Exception as e:
            print(f"Error al eliminar la tienda: {e}")
            self.conn.rollback()
    
    def eliminar_producto(self, id_producto):
        """
        Elimina un producto de la base de datos por su ID.
        """
        try:
            # Verificar si el producto existe
            self.cursor.execute("SELECT COUNT(*) FROM productos WHERE id_producto = %s", (id_producto,))
            existe_producto = self.cursor.fetchone()[0]

            if existe_producto == 0:
                print(f"El producto con ID {id_producto} no existe.")
                return

            # Eliminar el producto
            self.cursor.execute("DELETE FROM productos WHERE id_producto = %s", (id_producto,))
            self.conn.commit()
            print(f"Producto con ID {id_producto} eliminado correctamente.")
        except Exception as e:
            print(f"Error al eliminar el producto: {e}")
            self.conn.rollback()
    
    def obtener_tiendas(self):
        """
        Obtiene todas las tiendas de la base de datos.
        """
        try:
            self.cursor.execute("SELECT * FROM tiendas;")
            tiendas = self.cursor.fetchall()
            return [
                {
                    "id_tienda": tienda[0],
                    "nombre": tienda[1],
                    "ubicacion": tienda[2],
                    "telefono": tienda[3],
                    "ubicacion_lat": float(tienda[4]),
                    "ubicacion_lng": float(tienda[5])
                }
                for tienda in tiendas
            ]
        except Exception as e:
            print(f"Error al obtener tiendas: {e}")
            return []
        