public class Nodo {
    Tienda tienda;
    Nodo izquierda;
    Nodo derecha;
    int altura;

    // Constructor
    public Nodo(Tienda tienda) {
        this.tienda = tienda;
        this.izquierda = null;
        this.derecha = null;
        this.altura = 1;
    }
}
