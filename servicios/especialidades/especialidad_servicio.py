from typing import Tuple, List, Optional, Dict
from excepciones.base_datos_error import BaseDatosError
from repositorios.especialidades.especialidad_repositorio import EspecialidadRepositorio
from repositorios.repositorio_base import RepositorioBase


class EspecialidadServicio:
    def __init__(self, repositorio: RepositorioBase):
        self.repositorio = repositorio
    
    def validar_especialidad(self, especialidad: str) -> List[str]:
        errores = []
        especialidad_sin_espacios = especialidad.replace(" ", "")
        
        if not(especialidad):
            errores.append("Especialidad: No puede estar vacío.")
        elif (especialidad):
            if (len(especialidad_sin_espacios) == 0):
                errores.append("Especialidad: No puede estar vacío.")
            
            if (len(especialidad) > 40):
                errores.append("Especialidad: No puede contener más de 40 caracteres.")
        
        return errores
    
    def validar_campos_especialidad(self, especialidad: str) -> List[str]:
        error_especialidad = self.validar_especialidad(especialidad)
        errores_totales = error_especialidad
        
        return errores_totales
    
    def registrar_especialidad(self, campos: Dict) -> None:
        self.repositorio.registrar(campos)
    
    def obtener_todos_especialidades(self) -> List[Tuple]:
        return self.repositorio.obtener_todos()
    
    def obtener_especialidad_por_id(self, especialidad_id: int) -> Optional[Tuple]:
        try:
            return self.repositorio.obtener_por_id(especialidad_id)
        except BaseDatosError as error:
            raise error
    
    def actualizar_especialidad(self, especialidad_id: int, campos_especialidad: Dict) -> None:
        self.repositorio.actualizar(especialidad_id, campos_especialidad)
    
    def eliminar_especialidad(self, especialidad_id: int) -> None:
        try:
            self.repositorio.eliminar(especialidad_id)
        except BaseDatosError as error:
            raise error


if __name__ == "__main__":
    especialidad_repositorio = EspecialidadRepositorio()
    especialidad_servicio = EspecialidadServicio(especialidad_repositorio)
    
    """campos_especialidad = {
        "especialidad": "HOTELERÍA"
    }
    
    especialidad_servicio.registrar_especialidad(campos_especialidad)"""
    
    """todos_especialidades = especialidad_servicio.obtener_todos_especialidades()
    
    if (type(todos_especialidades) == list):
        for registro in todos_especialidades:
            print(registro)
    else:
        print(todos_especialidades)"""
    
    
    """campos_especialidad = {
        "especialidad": "BISUTERÍA"
    }
    
    especialidad_servicio.actualizar_especialidad(2, campos_especialidad)"""
    
    #especialidad_servicio.eliminar_especialidad(2)
    
    """especialidad = input("- Ingrese la especialidad: ")
    
    errores_totales = especialidad_servicio.validar_campos_especialidad(especialidad)
    
    if errores_totales:
        print("\n".join(errores_totales))
    else:
        print("Registro de la especialidad con éxito.")"""
    
    
    """"
    todos_especialidades = especialidad_servicio.obtener_todos_especialidades()
    
    for registro in todos_especialidades:
        print(registro)
        
    """