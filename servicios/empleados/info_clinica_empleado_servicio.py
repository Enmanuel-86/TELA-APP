from typing import Tuple, List, Optional, Dict
from excepciones.base_datos_error import BaseDatosError
from repositorios.empleados.info_clinica_empleado_repositorio import InfoClinicaEmpleadoRepositorio
from repositorios.repositorio_base import RepositorioBase


class InfoClinicaEmpleadoServicio:
    def __init__(self, repositorio: RepositorioBase):
        self.repositorio = repositorio
    
    def registrar_info_clinica_empleado(self, campos: Dict) -> None:
        self.repositorio.registrar(campos)
    
    def obtener_todos_info_clinica(self) -> List[Tuple]:
        return self.repositorio.obtener_todos()
    
    def obtener_info_clinica_por_id(self, info_clin_empleado_id: int) -> Optional[Tuple]:
        try:
            return self.repositorio.obtener_por_id(info_clin_empleado_id)
        except BaseDatosError as error:
            raise error
    
    def obtener_info_clinica_por_empleado_id(self, empleado_id: int) -> List[Tuple]:
        try:
            return self.repositorio.obtener_por_empleado_id(empleado_id)
        except BaseDatosError as error:
            raise error
    
    def actualizar_info_clinica(self, info_clin_empleado_id: int, campos_info_clinica_empleado: Dict) -> None:
        self.repositorio.actualizar(info_clin_empleado_id, campos_info_clinica_empleado)
    
    def eliminar_info_clinica(self, info_clin_empleado_id: int) -> None:
        try:
            self.repositorio.eliminar(info_clin_empleado_id)
        except BaseDatosError as error:
            raise error


if __name__ == "__main__":
    info_clinica_empleado_repositorio = InfoClinicaEmpleadoRepositorio()
    info_clinica_empleado_servicio = InfoClinicaEmpleadoServicio(info_clinica_empleado_repositorio)
    
    
    """campos_info_clinica_empleado = {
        "empleado_id": 2,
        "diagnostico_id": 3
    }
    
    info_clinica_empleado_servicio.registrar_info_clinica_empleado(campos_info_clinica_empleado)"""
    
    """todos_info_clinica_empleado = info_clinica_empleado_servicio.obtener_todos_info_clinica()
    
    for registro in todos_info_clinica_empleado:
        print(registro)"""
    
    
    #print(info_clinica_empleado_servicio.obtener_info_clinica_por_id(3))
    
    """todos_info_clinica_empleado = info_clinica_empleado_servicio.obtener_info_clinica_por_empleado_id(2)
    
    if (type(todos_info_clinica_empleado) == list):
        for registro in todos_info_clinica_empleado:
            print(registro)
    else:
        print(todos_info_clinica_empleado)"""
    
    
    """campos_info_clinica_empleado = {
        "diagnostico_id": "1"
    }
    
    info_clinica_empleado_servicio.actualizar_info_clinica(3, campos_info_clinica_empleado)"""
    
    #info_clinica_empleado_servicio.eliminar_info_clinica(3)