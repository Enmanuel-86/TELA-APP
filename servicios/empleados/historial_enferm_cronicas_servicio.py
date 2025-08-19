from typing import Tuple, List, Optional, Dict
from excepciones.base_datos_error import BaseDatosError
from repositorios.empleados.historial_enferm_cronicas_repositorio import HistorialEnfermCronicasRepositorio
from repositorios.repositorio_base import RepositorioBase


class HistorialEnfermCronicasServicio:
    def __init__(self, repositorio: RepositorioBase):
        self.repositorio = repositorio
    
    def registrar_historial_enferm_cronica(self, campos: Dict) -> None:
        self.repositorio.registrar(campos)
    
    def obtener_todos_historial_enferm_cronicas(self) -> List[Tuple]:
        return self.repositorio.obtener_todos()
    
    def obtener_historial_enferm_cronica_por_id(self, hist_enferm_cronica_id: int) -> Optional[Tuple]:
        try:
            return self.repositorio.obtener_por_id(hist_enferm_cronica_id)
        except BaseDatosError as error:
            raise error
    
    def obtener_historial_enferm_cronica_por_empleado_id(self, empleado_id: int) -> List[Tuple]:
        try:
            return self.repositorio.obtener_por_empleado_id(empleado_id)
        except BaseDatosError as error:
            raise error
    
    def actualizar_historial_enferm_cronica(self, hist_enferm_cronica_id: int, campos_historial_enferm_cronicas: Dict) -> None:
        self.repositorio.actualizar(hist_enferm_cronica_id, campos_historial_enferm_cronicas)
    
    def eliminar_historial_enferm_cronica(self, hist_enferm_cronica_id: int) -> None:
        try:
            self.repositorio.eliminar(hist_enferm_cronica_id)
        except BaseDatosError as error:
            raise error


if __name__ == "__main__":
    historial_enferm_cronicas_repositorio = HistorialEnfermCronicasRepositorio()
    historial_enferm_cronicas_servicio = HistorialEnfermCronicasServicio(historial_enferm_cronicas_repositorio)
    
    """campos_historial_enferm_cronicas = {
        "empleado_id": 4,
        "enferm_cronica_id": 1
    }
    
    historial_enferm_cronicas_servicio.registrar_historial_enferm_cronica(campos_historial_enferm_cronicas)"""
    
    """todos_historial_enferm_cronicas = historial_enferm_cronicas_servicio.obtener_todos_historial_enferm_cronicas()
    
    for registro in todos_historial_enferm_cronicas:
        print(registro)"""
    
    
    #print(historial_enferm_cronicas_servicio.obtener_historial_enferm_cronica_por_id(2))
    
    """todos_historial_enferm_cronicas = historial_enferm_cronicas_servicio.obtener_historial_enferm_cronica_por_empleado_id(2)
    
    if (type(todos_historial_enferm_cronicas) == list):
        for registro in todos_historial_enferm_cronicas:
            print(registro)
    else:
        print(todos_historial_enferm_cronicas)"""
    
    
    """campos_historial_enferm_cronicas = {
        "enferm_cronica_id": 2
    }
    
    historial_enferm_cronicas_servicio.actualizar_historial_enferm_cronica(4, campos_historial_enferm_cronicas)"""
    
    #historial_enferm_cronicas_servicio.eliminar_historial_enferm_cronica(4)