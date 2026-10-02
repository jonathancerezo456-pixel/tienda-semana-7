from datetime import datetime


class Pedido:
    """Pedido de un cliente en la tienda. Se usa con la Cola para gestionar la atencion."""

    _contador = 1  # ID autoincrementable

    def __init__(self, cliente, producto, cantidad, precio, id_pedido=None, fecha=None):
        if id_pedido is not None:
            self.__id = id_pedido
            if id_pedido >= Pedido._contador:
                Pedido._contador = id_pedido + 1
        else:
            self.__id = Pedido._contador
            Pedido._contador += 1

        self.__cliente  = cliente
        self.__producto = producto
        self.__cantidad = cantidad
        self.__precio   = precio
        self.__fecha    = fecha if fecha else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.__estado   = "pendiente"

    @property
    def id(self):        return self.__id
    @property
    def cliente(self):   return self.__cliente
    @property
    def producto(self):  return self.__producto
    @property
    def cantidad(self):  return self.__cantidad
    @property
    def precio(self):    return self.__precio
    @property
    def total(self):     return self.__cantidad * self.__precio
    @property
    def fecha(self):     return self.__fecha
    @property
    def estado(self):    return self.__estado

    @estado.setter
    def estado(self, valor):
        if valor not in {"pendiente", "procesado", "cancelado"}:
            raise ValueError("Estado invalido. Opciones: pendiente, procesado, cancelado")
        self.__estado = valor

    def to_dict(self):
        return {
            "id": self.__id,
            "cliente": self.__cliente,
            "producto": self.__producto,
            "cantidad": self.__cantidad,
            "precio": self.__precio,
            "total": self.total,
            "fecha": self.__fecha,
            "estado": self.__estado
        }

    @classmethod
    def from_dict(cls, data):
        p = cls(
            cliente=data["cliente"],
            producto=data["producto"],
            cantidad=data["cantidad"],
            precio=data["precio"],
            id_pedido=data.get("id"),
            fecha=data.get("fecha")
        )
        p.estado = data.get("estado", "pendiente")
        return p

    def __str__(self):
        return (f"Pedido #{self.__id} | {self.__cliente} | "
                f"{self.__producto} x{self.__cantidad} | "
                f"${self.total:.2f} | [{self.__estado}]")
