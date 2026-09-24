from abc import ABC, abstractmethod

class Cliente(ABC):
    def __init__(self, nombre):
        self.__nombre = nombre

    def get_nombre(self):
        return self.__nombre

    def set_nombre(self, nombre):
        self.__nombre = nombre

    @abstractmethod
    def calcularDescuento(self, total):
        pass
