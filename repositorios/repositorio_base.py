from typing import Tuple, List, Optional
from abc import ABC, abstractmethod


class RepositorioBase(ABC):
    @abstractmethod
    def obtener_todos(self) -> List[Tuple]:
        pass
    
    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Tuple]:
        pass