from producto import Producto

class ProductoElectronico(Producto):
    def __init__(self, nombre, precio, cantidad, garantia, marca):
        super().__init__(nombre, precio, cantidad)
        self.__garantia = garantia
        self.__marca = marca

    def get_garantia(self):
        return self.__garantia

    def set_garantia(self, garantia):
        self.__garantia = garantia

    def get_marca(self):
        return self.__marca

    def set_marca(self, marca):
        self.__marca = marca