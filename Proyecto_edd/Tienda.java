
import java.util.ArrayList;
import java.util.List;

public class Tienda {
    private int idTienda;
    private String nombre;
    private String ubicacion;
    private String telefono;
    private List<Producto> productos;

    // Constructor
    public Tienda(int idTienda, String nombre, String ubicacion, String telefono) {
        this.idTienda = idTienda;
        this.nombre = nombre;
        this.ubicacion = ubicacion;
        this.telefono = telefono;
        this.productos = new ArrayList<>();
    }

    // Getters
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

    public List<Producto> obtenerProductosDisponibles() {
        return new ArrayList<>(productos); // Devuelve una copia de la lista
    }

    // Métodos para gestionar productos
    public Producto buscarProductoPorNombre(String nombreProducto) {
        for (Producto producto : productos) {
            if (producto.getNombre().equalsIgnoreCase(nombreProducto)) {
                return producto;
            }
        }
        return null;
    }

    public void agregarProducto(Producto producto) {
        if (producto != null) {
            productos.add(producto);
        } else {
            System.out.println("El producto no puede ser nulo.");
        }
    }

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
