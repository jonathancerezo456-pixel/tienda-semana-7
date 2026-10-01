from cola import Cola
from pedido import Pedido


class PedidoRepository:
    """
    Patron de diseno Repository.
    Separa el acceso y manejo de datos de la logica principal.
    Usa la Cola implementada manualmente para administrar los pedidos.
    """

    def __init__(self):
        self._cola_pendientes = Cola()
        self._procesados      = []

    def agregar_pedido(self, pedido):
        """Encola un nuevo pedido al final de la fila."""
        self._cola_pendientes.encolar(pedido)

    def procesar_siguiente(self):
        """Desencola y procesa el pedido del frente."""
        pedido = self._cola_pendientes.desencolar()
        pedido.estado = "procesado"
        self._procesados.append(pedido)
        return pedido

    def ver_siguiente(self):
        """Retorna el pedido del frente sin procesarlo."""
        return self._cola_pendientes.frente()

    def hay_pendientes(self):
        """Retorna True si hay pedidos en la cola."""
        return not self._cola_pendientes.esta_vacia()

    def total_pendientes(self):
        return self._cola_pendientes.tamano()

    def listar_pendientes(self):
        return self._cola_pendientes.listar()

    def listar_procesados(self):
        return list(self._procesados)

    def total_procesados(self):
        return len(self._procesados)
