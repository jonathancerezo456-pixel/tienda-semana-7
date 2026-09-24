from cliente import Cliente

class ClienteMinorista(Cliente):
    def __init__(self, nombre):
        super().__init__(nombre)

    def calcularDescuento(self, total):
        descuento = total * 0.05
        total_final = total - descuento
        return total_final
