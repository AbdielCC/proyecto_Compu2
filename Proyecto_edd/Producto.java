public class Producto {
    private int idProducto;
    private String nombre;
    private String descripcion;
    private float precio;
    private int stock;
    private String rutaFoto;

    // Constructor
    public Producto(int idProducto, String nombre, String descripcion, float precio, int stock, String rutaFoto) {
        this.idProducto = idProducto;
        this.nombre = nombre;
        this.descripcion = descripcion;
        this.precio = precio >= 0 ? precio : 0;
        this.stock = stock >= 0 ? stock : 0;
        this.rutaFoto = rutaFoto;
    }

    // Getters
    public int getIdProducto() {
        return idProducto;
    }

    public String getNombre() {
        return nombre;
    }

    public String getDescripcion() {
        return descripcion;
    }

    public float getPrecio() {
        return precio;
    }

    public int getStock() {
        return stock;
    }

    public String getRutaFoto() {
        return rutaFoto;
    }

    // Setters
    public void setNombre(String nombre) {
        this.nombre = nombre;
    }

    public void setDescripcion(String descripcion) {
        this.descripcion = descripcion;
    }

    public void setPrecio(float precio) {
        if (precio < 0) {
            throw new IllegalArgumentException("El precio no puede ser negativo.");
        }
        this.precio = precio;
    }

    public void setStock(int stock) {
        if (stock < 0) {
            throw new IllegalArgumentException("El stock no puede ser negativo.");
        }
        this.stock = stock;
    }

    public void setRutaFoto(String rutaFoto) {
        this.rutaFoto = rutaFoto;
    }

    // Método para actualizar el stock del producto
    public boolean actualizarStock(int cantidad) {
        if (stock + cantidad < 0) {
            System.out.println("No hay suficiente stock disponible para realizar esta operación.");
            return false;
        }
        stock += cantidad;
        return true;
    }

    // Representación en cadena del producto
    @Override
    public String toString() {
        return "Producto{" +
               "idProducto=" + idProducto +
               ", nombre='" + nombre + '\'' +
               ", descripcion='" + descripcion + '\'' +
               ", precio=" + precio +
               ", stock=" + stock +
               ", rutaFoto='" + rutaFoto + '\'' +
               '}';
    }
}
