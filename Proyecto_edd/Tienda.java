import java.util.ArrayList;
import java.util.List;

public class Tienda {
    private int idTienda;
    private String nombre;
    private String ubicacion;
    private String telefono;
    private List<Producto> productos;

    public Tienda(int idTienda, String nombre, String ubicacion, String telefono) {
        this.idTienda = idTienda;
        this.nombre = nombre;
        this.ubicacion = ubicacion;
        this.telefono = telefono;
        this.productos = new ArrayList<>();
    }

    // Métodos getters
    public int getIdTienda() {
        return idTienda;
    }

    public String getNombre() {
        return nombre;
    }

    public String getUbicacion() {
        return ubicacion;
    }

    public String getTelefono() {
        return telefono;
    }

    public List<Producto> getProductos() {
        return productos;
    }

    // Método para agregar productos
    public void agregarProducto(Producto producto) {
        productos.add(producto);
    }

    // Método para buscar un producto por nombre
    public Producto buscarProductoPorNombre(String nombreProducto) {
        for (Producto producto : productos) {
            if (producto.getNombre().equalsIgnoreCase(nombreProducto)) {
                return producto;
            }
        }
        return null;
    }

    // Método toString para imprimir detalles de la tienda
    @Override
    public String toString() {
        return "Tienda{" +
                "idTienda=" + idTienda +
                ", nombre='" + nombre + '\'' +
                ", ubicacion='" + ubicacion + '\'' +
                ", telefono='" + telefono + '\'' +
                ", productos=" + productos +
                '}';
    }
}
