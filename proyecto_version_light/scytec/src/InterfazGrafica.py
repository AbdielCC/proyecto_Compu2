import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from PIL import Image, ImageTk
from ArbolAVL import ArbolAVL
import requests

class InterfazGrafica:
    def __init__(self, root, base_datos, api_maps):
        self.root = root
        self.base_datos = base_datos
        self.api_maps = api_maps

        # Instancia del árbol AVL
        self.arbol_avl = ArbolAVL()

        self.root.title("Sistema de Inventario y Mapa")
        self.root.geometry("1200x800")

        # Título dinámico de la tabla
        self.table_title = tk.Label(self.root, text="Esquema: Todos los Productos", font=("Arial", 14), pady=10)
        self.table_title.pack()

        # Tabla de productos
        self.tree = ttk.Treeview(self.root, columns=("ID", "Nombre", "Precio", "Stock"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Precio", text="Precio")
        self.tree.heading("Stock", text="Stock")
        self.tree.pack(fill=tk.BOTH, expand=True, pady=10)

        # Botones principales
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=10)

        buscar_button = tk.Button(self.button_frame, text="Buscar Tiendas Cercanas", command=self.buscar_tiendas_cercanas)
        buscar_button.grid(row=0, column=0, padx=10)

        ajustes_button = tk.Button(self.button_frame, text="Ajustes", command=self.abrir_ajustes)
        ajustes_button.grid(row=0, column=1, padx=10)

        modificar_button = tk.Button(self.button_frame, text="Modificar Búsqueda", command=self.modificar_busqueda)
        modificar_button.grid(row=0, column=2, padx=10)

        refresh_button = tk.Button(self.button_frame, text="Refresh", command=self.refrescar_tabla)
        refresh_button.grid(row=0, column=3, padx=10)

        salir_button = tk.Button(self.button_frame, text="Salir", command=self.root.quit)
        salir_button.grid(row=0, column=4, padx=10)

        # Contenedor del mapa
        self.map_frame = tk.Frame(self.root)
        self.map_frame.pack(pady=10)

        self.map_label = tk.Label(self.map_frame, text="Mapa de Tiendas")
        self.map_label.pack()

        self.map_image_label = tk.Label(self.map_frame)
        self.map_image_label.pack()

        # Cargar productos y mapa
        self.mostrar_productos()
        self.mostrar_mapa()

    def mostrar_productos(self, criterio=None):
        # Limpiar tabla
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Limpiar el árbol AVL
        self.arbol_avl = ArbolAVL()

        # Obtener productos y ordenarlos en el árbol AVL
        productos = self.base_datos.obtener_productos()
        if criterio == "nombre":
            self.table_title.config(text="Esquema: Ordenado por Nombre")
            for producto in productos:
                self.arbol_avl.insertar((producto["nombre"], producto))
        elif criterio == "precio":
            self.table_title.config(text="Esquema: Ordenado por Precio")
            for producto in productos:
                self.arbol_avl.insertar((producto["precio"], producto))
        elif criterio == "stock":
            self.table_title.config(text="Esquema: Ordenado por Stock")
            for producto in productos:
                self.arbol_avl.insertar((producto["stock"], producto))
        else:
            self.table_title.config(text="Esquema: Todos los Productos")
            for producto in productos:
                self.arbol_avl.insertar((producto["id_producto"], producto))

        # Obtener los datos ordenados del árbol AVL
        productos_ordenados = self.arbol_avl.en_orden()
        for _, producto in productos_ordenados:
            self.tree.insert("", "end", values=(producto["id_producto"], producto["nombre"], producto["precio"], producto["stock"]))

    def mostrar_mapa(self):
        ubicaciones = [
            {"nombre": "Tienda A", "lat": 19.432608, "lng": -99.133209},
            {"nombre": "Tienda B", "lat": 20.659699, "lng": -103.349609},
        ]
        centro = {"lat": 19.432608, "lng": -99.133209}
        url = self.api_maps.obtener_mapa(ubicaciones, centro)

        response = requests.get(url)
        with open("mapa.png", "wb") as f:
            f.write(response.content)

        img = Image.open("mapa.png")
        img = img.resize((800, 600), Image.LANCZOS)
        self.map_image = ImageTk.PhotoImage(img)

        self.map_image_label.config(image=self.map_image)

    def buscar_tiendas_cercanas(self):
        usuario_lat, usuario_lng = 19.432608, -99.133209
        tiendas = [
            {"nombre": "Tienda A", "lat": 19.432608, "lng": -99.133209},
            {"nombre": "Tienda B", "lat": 20.659699, "lng": -103.349609},
        ]

        tiendas_ordenadas = sorted(
            tiendas,
            key=lambda tienda: ((tienda["lat"] - usuario_lat) ** 2 + (tienda["lng"] - usuario_lng) ** 2) ** 0.5
        )

        mensaje = "Tiendas más cercanas:\n\n"
        for tienda in tiendas_ordenadas:
            distancia = ((tienda["lat"] - usuario_lat) ** 2 + (tienda["lng"] - usuario_lng) ** 2) ** 0.5
            mensaje += f"{tienda['nombre']}: {distancia:.2f} unidades\n"

        messagebox.showinfo("Tiendas Cercanas", mensaje)

    def abrir_ajustes(self):
        opcion = simpledialog.askstring("Ajustes", "¿Qué deseas hacer? (Agregar/Actualizar/Eliminar):").lower()

        if opcion == "agregar":
            tipo = simpledialog.askstring("Agregar", "¿Deseas agregar 'tienda' o 'producto'?:").lower()
            if tipo == "tienda":
                self.agregar_tienda()
            elif tipo == "producto":
                self.agregar_producto()
            else:
                messagebox.showerror("Error", "Tipo no válido.")
        elif opcion == "actualizar":
            tipo = simpledialog.askstring("Actualizar", "¿Deseas actualizar 'tienda' o 'producto'?:").lower()
            if tipo == "tienda":
                self.actualizar_tienda()
            elif tipo == "producto":
                self.actualizar_producto()
            else:
                messagebox.showerror("Error", "Tipo no válido.")
        elif opcion == "eliminar":
            tipo = simpledialog.askstring("Eliminar", "¿Deseas eliminar 'tienda' o 'producto'?:").lower()
            if tipo == "tienda":
                self.eliminar_tienda()
            elif tipo == "producto":
                self.eliminar_producto()
            else:
                messagebox.showerror("Error", "Tipo no válido.")
        else:
            messagebox.showerror("Error", "Opción no válida.")

    def agregar_tienda(self):
        nombre = simpledialog.askstring("Nueva Tienda", "Nombre de la tienda:")
        ubicacion = simpledialog.askstring("Nueva Tienda", "Ubicación de la tienda:")
        telefono = simpledialog.askstring("Nueva Tienda", "Teléfono de la tienda:")

        if nombre and ubicacion and telefono:
            self.base_datos.agregar_tienda(nombre, ubicacion, telefono)
            messagebox.showinfo("Éxito", f"Tienda '{nombre}' agregada con éxito.")
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")

    def agregar_tienda(self):
        """
        Solicita los datos para agregar una nueva tienda.
        """
        nombre = simpledialog.askstring("Nueva Tienda", "Nombre de la tienda:")
        ubicacion = simpledialog.askstring("Nueva Tienda", "Ubicación de la tienda:")
        telefono = simpledialog.askstring("Nueva Tienda", "Teléfono de la tienda:")
        latitud = simpledialog.askfloat("Nueva Tienda", "Latitud de la tienda:")
        longitud = simpledialog.askfloat("Nueva Tienda", "Longitud de la tienda:")

        if nombre and ubicacion and telefono and latitud and longitud:
            self.base_datos.agregar_tienda(nombre, ubicacion, telefono, latitud, longitud)
            messagebox.showinfo("Éxito", f"Tienda '{nombre}' agregada con éxito.")
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")


    def agregar_producto(self):
        nombre = simpledialog.askstring("Nuevo Producto", "Nombre del producto:")
        descripcion = simpledialog.askstring("Nuevo Producto", "Descripción del producto:")
        precio = simpledialog.askfloat("Nuevo Producto", "Precio del producto:")
        stock = simpledialog.askinteger("Nuevo Producto", "Cantidad en stock:")
        id_tienda = simpledialog.askinteger("Nuevo Producto", "ID de la tienda asociada:")

        if nombre and descripcion and precio and stock and id_tienda:
            self.base_datos.agregar_producto(nombre, descripcion, precio, stock, "ruta/foto.jpg", id_tienda)
            messagebox.showinfo("Éxito", f"Producto '{nombre}' agregado con éxito.")
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")

    def eliminar_producto(self):
        id_producto = simpledialog.askinteger("Eliminar Producto", "ID del producto a eliminar:")
        if id_producto:
            self.base_datos.eliminar_producto(id_producto)
            messagebox.showinfo("Éxito", f"Producto con ID {id_producto} eliminado.")
        else:
            messagebox.showerror("Error", "El ID es obligatorio.")

    def modificar_busqueda(self):
        criterio = simpledialog.askstring(
            "Modificar Búsqueda",
            "Escribe el criterio de búsqueda: 'nombre', 'precio' o 'stock'."
        )
        if criterio in ["nombre", "precio", "stock"]:
            self.mostrar_productos(criterio=criterio)
            messagebox.showinfo("Éxito", f"Búsqueda actualizada por {criterio}.")
        else:
            messagebox.showerror("Error", "Criterio no válido.")
    def refrescar_tabla(self):
        """
        Recarga la tabla de productos con los datos más recientes.
        """
        self.mostrar_productos()  # Llama al método para mostrar productos
        messagebox.showinfo("Refresh", "La tabla ha sido actualizada.")
