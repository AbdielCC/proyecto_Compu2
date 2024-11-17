public class Main {
    public static void main(String[] args) {
        // Crear árbol AVL
        ArbolAVL arbol = new ArbolAVL();

        // Crear tiendas
        Tienda tienda1 = new Tienda(1, "Tienda A", "Ubicación A", "123456789");
        Tienda tienda2 = new Tienda(2, "Tienda B", "Ubicación B", "987654321");
        Tienda tienda3 = new Tienda(3, "Tienda C", "Ubicación C", "456789123");

        // Insertar tiendas en el árbol
        arbol.insertar(tienda1);
        arbol.insertar(tienda2);
        arbol.insertar(tienda3);

        // Agregar productos a las tiendas
        tienda1.agregarProducto(new Producto(1, "Producto A1", "Descripción A1", 10.0f, 100, "ruta/a1"));
        tienda1.agregarProducto(new Producto(2, "Producto A2", "Descripción A2", 20.0f, 50, "ruta/a2"));

        tienda2.agregarProducto(new Producto(3, "Producto B1", "Descripción B1", 15.0f, 200, "ruta/b1"));
        tienda2.agregarProducto(new Producto(4, "Producto B2", "Descripción B2", 30.0f, 80, "ruta/b2"));

        tienda3.agregarProducto(new Producto(5, "Producto C1", "Descripción C1", 25.0f, 60, "ruta/c1"));

        // Mostrar información de las tiendas
        System.out.println("Tienda 1: " + tienda1);
        System.out.println("Tienda 2: " + tienda2);
        System.out.println("Tienda 3: " + tienda3);

        // Buscar la tienda más cercana utilizando la API de geolocalización
        GeolocalizacionAPI api = new GeolocalizacionAPI("Ubicación A"); // Supongamos que el usuario está en "Ubicación A"
        Tienda tiendaCercana = api.obtenerTiendaCercana(arbol);

        // Mostrar la tienda más cercana
        if (tiendaCercana != null) {
            System.out.println("La tienda más cercana es: " + tiendaCercana.getNombre());
        } else {
            System.out.println("No se encontraron tiendas cercanas.");
        }

        // Buscar un producto por nombre en una tienda específica
        String nombreProducto = "Producto A1";
        Producto productoBuscado = tienda1.buscarProductoPorNombre(nombreProducto);

        if (productoBuscado != null) {
            System.out.println("Producto encontrado: " + productoBuscado);
        } else {
            System.out.println("El producto '" + nombreProducto + "' no está disponible en la tienda " + tienda1.getNombre());
        }
    }
}
