from abc import ABC, abstractmethod


class BaseDatos(ABC):
    @abstractmethod
    def conectar(self):
        pass
    
    @abstractmethod
    def desconectar(self):
        pass