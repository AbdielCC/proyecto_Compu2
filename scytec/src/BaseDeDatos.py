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
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id_usuario SERIAL PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    ubicacion VARCHAR(255),
                    edad INT
                );
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS tiendas (
                    id_tienda SERIAL PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    ubicacion VARCHAR(255) NOT NULL,
                    telefono VARCHAR(15)
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
                    id_usuario INT REFERENCES usuarios(id_usuario),
                    id_producto INT REFERENCES productos(id_producto),
                    id_tienda INT REFERENCES tiendas(id_tienda),
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

    def agregar_tienda(self, nombre: str, ubicacion: str, telefono: str):
        try:
            self.cursor.execute(
                """
                INSERT INTO tiendas (nombre, ubicacion, telefono)
                VALUES (%s, %s, %s)
                RETURNING id_tienda;
                """,
                (nombre, ubicacion, telefono)
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
