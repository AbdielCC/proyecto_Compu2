class NodoAVL:
    def __init__(self, clave, dato):
        self.clave = clave
        self.dato = dato
        self.izquierda = None
        self.derecha = None
        self.altura = 1


class ArbolAVL:
    def __init__(self):
        self.raiz = None

    def insertar(self, dato):
        self.raiz = self._insertar(self.raiz, dato)

    def _insertar(self, nodo, dato):
        if not nodo:
            return NodoAVL(dato[0], dato[1])
        if dato[0] < nodo.clave:
            nodo.izquierda = self._insertar(nodo.izquierda, dato)
        else:
            nodo.derecha = self._insertar(nodo.derecha, dato)
        nodo.altura = 1 + max(self._altura(nodo.izquierda), self._altura(nodo.derecha))
        return self._balancear(nodo)

    def en_orden(self):
        resultado = []
        self._en_orden(self.raiz, resultado)
        return resultado

    def _en_orden(self, nodo, resultado):
        if nodo:
            self._en_orden(nodo.izquierda, resultado)
            resultado.append((nodo.clave, nodo.dato))
            self._en_orden(nodo.derecha, resultado)

    def _altura(self, nodo):
        return nodo.altura if nodo else 0

    def _balancear(self, nodo):
        balance = self._altura(nodo.izquierda) - self._altura(nodo.derecha)
        if balance > 1:
            if self._altura(nodo.izquierda.izquierda) >= self._altura(nodo.izquierda.derecha):
                return self._rotar_derecha(nodo)
            else:
                nodo.izquierda = self._rotar_izquierda(nodo.izquierda)
                return self._rotar_derecha(nodo)
        if balance < -1:
            if self._altura(nodo.derecha.derecha) >= self._altura(nodo.derecha.izquierda):
                return self._rotar_izquierda(nodo)
            else:
                nodo.derecha = self._rotar_derecha(nodo.derecha)
                return self._rotar_izquierda(nodo)
        return nodo

    def _rotar_derecha(self, nodo):
        nueva_raiz = nodo.izquierda
        nodo.izquierda = nueva_raiz.derecha
        nueva_raiz.derecha = nodo
        nodo.altura = 1 + max(self._altura(nodo.izquierda), self._altura(nodo.derecha))
        nueva_raiz.altura = 1 + max(self._altura(nueva_raiz.izquierda), self._altura(nueva_raiz.derecha))
        return nueva_raiz

    def _rotar_izquierda(self, nodo):
        nueva_raiz = nodo.derecha
        nodo.derecha = nueva_raiz.izquierda
        nueva_raiz.izquierda = nodo
        nodo.altura = 1 + max(self._altura(nodo.izquierda), self._altura(nodo.derecha))
        nueva_raiz.altura = 1 + max(self._altura(nueva_raiz.izquierda), self._altura(nueva_raiz.derecha))
        return nueva_raiz
