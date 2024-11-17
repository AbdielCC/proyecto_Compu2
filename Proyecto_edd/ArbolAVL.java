public class ArbolAVL {
    private Nodo raiz;

    // Método para insertar una tienda en el árbol
    public void insertar(Tienda tienda) {
        if (tienda == null) {
            System.out.println("No se puede insertar una tienda nula.");
            return;
        }
        raiz = insertar(raiz, tienda);
    }

    private Nodo insertar(Nodo nodo, Tienda tienda) {
        if (nodo == null) {
            return new Nodo(tienda);
        }

        if (tienda.getIdTienda() < nodo.tienda.getIdTienda()) {
            nodo.izquierda = insertar(nodo.izquierda, tienda);
        } else if (tienda.getIdTienda() > nodo.tienda.getIdTienda()) {
            nodo.derecha = insertar(nodo.derecha, tienda);
        } else {
            // No se permiten claves duplicadas
            return nodo;
        }

        // Actualizar altura del nodo
        nodo.altura = 1 + Math.max(altura(nodo.izquierda), altura(nodo.derecha));

        // Balancear el nodo
        return balancear(nodo, tienda.getIdTienda());
    }

    private int altura(Nodo nodo) {
        return nodo == null ? 0 : nodo.altura;
    }

    private int obtenerBalance(Nodo nodo) {
        return nodo == null ? 0 : altura(nodo.izquierda) - altura(nodo.derecha);
    }

    private Nodo balancear(Nodo nodo, int clave) {
        int balance = obtenerBalance(nodo);

        // Rotación simple a la derecha
        if (balance > 1 && clave < nodo.izquierda.tienda.getIdTienda()) {
            return rotarDerecha(nodo);
        }

        // Rotación simple a la izquierda
        if (balance < -1 && clave > nodo.derecha.tienda.getIdTienda()) {
            return rotarIzquierda(nodo);
        }

        // Rotación doble a la derecha
        if (balance > 1 && clave > nodo.izquierda.tienda.getIdTienda()) {
            nodo.izquierda = rotarIzquierda(nodo.izquierda);
            return rotarDerecha(nodo);
        }

        // Rotación doble a la izquierda
        if (balance < -1 && clave < nodo.derecha.tienda.getIdTienda()) {
            nodo.derecha = rotarDerecha(nodo.derecha);
            return rotarIzquierda(nodo);
        }

        return nodo;
    }

    private Nodo rotarDerecha(Nodo y) {
        Nodo x = y.izquierda;
        Nodo T2 = x.derecha;

        // Rotar
        x.derecha = y;
        y.izquierda = T2;

        // Actualizar alturas
        y.altura = Math.max(altura(y.izquierda), altura(y.derecha)) + 1;
        x.altura = Math.max(altura(x.izquierda), altura(x.derecha)) + 1;

        return x;
    }

    private Nodo rotarIzquierda(Nodo x) {
        Nodo y = x.derecha;
        Nodo T2 = y.izquierda;

        // Rotar
        y.izquierda = x;
        x.derecha = T2;

        // Actualizar alturas
        x.altura = Math.max(altura(x.izquierda), altura(x.derecha)) + 1;
        y.altura = Math.max(altura(y.izquierda), altura(y.derecha)) + 1;

        return y;
    }

    // Método para buscar la tienda más cercana
    public Tienda buscarCercano(String ubicacionUsuario) {
        // Simulación de búsqueda. Podrías implementar una métrica de distancia real.
        return raiz != null ? raiz.tienda : null;
    }
}
