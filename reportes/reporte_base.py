from abc import ABC, abstractmethod
from typing import List, Any


class ReporteBase(ABC):
    @abstractmethod
    def exportar(datos: List) -> Any:
        pass