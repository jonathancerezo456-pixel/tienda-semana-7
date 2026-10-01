class NodoCola:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None


class Cola:
    """Cola FIFO implementada manualmente con nodos enlazados.
    No usa queue.Queue ni collections.deque."""

    def __init__(self):
        self._frente = None
        self._final  = None
        self._tamano = 0

    def encolar(self, elemento):
        """Agrega un elemento al final de la cola."""
        nuevo = NodoCola(elemento)
        if self._final is None:
            self._frente = nuevo
            self._final  = nuevo
        else:
            self._final.siguiente = nuevo
            self._final = nuevo
        self._tamano += 1

    def desencolar(self):
        """Elimina y retorna el elemento del frente. Lanza IndexError si esta vacia."""
        if self.esta_vacia():
            raise IndexError("No se puede desencolar: la cola esta vacia.")
        dato = self._frente.dato
        self._frente = self._frente.siguiente
        if self._frente is None:
            self._final = None
        self._tamano -= 1
        return dato

    def frente(self):
        """Retorna el elemento del frente sin eliminarlo."""
        if self.esta_vacia():
            raise IndexError("La cola esta vacia.")
        return self._frente.dato

    def esta_vacia(self):
        """Retorna True si la cola no tiene elementos."""
        return self._tamano == 0

    def tamano(self):
        """Retorna la cantidad de elementos en la cola."""
        return self._tamano

    def listar(self):
        """Retorna lista de elementos en orden frente->final."""
        resultado = []
        actual = self._frente
        while actual is not None:
            resultado.append(actual.dato)
            actual = actual.siguiente
        return resultado

    def __len__(self):
        return self._tamano

    def __str__(self):
        if self.esta_vacia():
            return "Cola vacia []"
        return "Frente -> " + " -> ".join(str(e) for e in self.listar()) + " <- Final"
