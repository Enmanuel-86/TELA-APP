from abc import ABC, abstractmethod


class Respaldo(ABC):
    @abstractmethod
    def exportar(self):
        pass
    
    @abstractmethod
    def importar(self):
        pass