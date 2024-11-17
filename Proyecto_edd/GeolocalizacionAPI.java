public class GeolocalizacionAPI {
    private String ubicacionUsuario;

    // Constructor
    public GeolocalizacionAPI(String ubicacionUsuario) {
        this.ubicacionUsuario = ubicacionUsuario;
    }

    // Getter
    public String getUbicacionUsuario() {
        return ubicacionUsuario;
    }

    // Setter
    public void setUbicacionUsuario(String ubicacionUsuario) {
        this.ubicacionUsuario = ubicacionUsuario;
    }

    // Método para obtener la tienda más cercana
    public Tienda obtenerTiendaCercana(ArbolAVL arbol) {
        if (arbol == null) {
            System.out.println("El árbol AVL no está inicializado.");
            return null;
        }
        return arbol.buscarCercano(ubicacionUsuario);
    }
}
