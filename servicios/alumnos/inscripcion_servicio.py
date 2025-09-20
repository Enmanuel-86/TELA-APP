import re
from typing import Tuple, List, Optional, Dict, Union
from datetime import date
from excepciones.base_datos_error import BaseDatosError
from repositorios.alumnos.inscripcion_repositorio import InscripcionRepositorio
from repositorios.repositorio_base import RepositorioBase


class InscripcionServicio:
    def __init__(self, repositorio: RepositorioBase):
        self.repositorio = repositorio
    
    def validar_especialidad_id(self, especialidad_id: int) -> List[str]:
        errores = []
        
        if not(especialidad_id):
            errores.append("Especialidad: No puede estar vacío.")
        
        return errores
    
    def validar_fecha_inscripcion(self, fecha_inscripcion: date) -> List[str]:
        errores = []
        
        if not(fecha_inscripcion):
            errores.append("Fecha de inscripción: No puede estar vacío.")
        
        return errores
    
    def validar_periodo_escolar(self, periodo_escolar: str) -> List[str]:
        errores = []
        
        if not(periodo_escolar):
            errores.append("Periodo escolar: No puede estar vacío.")
        elif (periodo_escolar):
            periodo_escolar_sin_espacios = periodo_escolar.replace(" ", "")
            estructura_periodo_escolar = re.match(r"^[0-9-]+$", periodo_escolar)
            if (len(periodo_escolar_sin_espacios) == 0):
                errores.append("Periodo escolar: No puede estar vacío.")
            
            if not(estructura_periodo_escolar):
                errores.append("Periodo escolar: La estructura de este campo es inválida.")
            
            if (len(periodo_escolar) > 9):
                errores.append("Periodo escolar: No puede contener más de 9 caracteres.")
        
        return errores
    
    def valdiar_campos_inscripcion(self, especialidad_id: int, fecha_inscripcion: date, periodo_escolar: str) -> List[str]:
        error_especialidad_id = self.validar_especialidad_id(especialidad_id)
        error_fecha_inscripcion = self.validar_fecha_inscripcion(fecha_inscripcion)
        error_periodo_escolar = self.validar_periodo_escolar(periodo_escolar)
        
        errores_totales = error_especialidad_id + error_fecha_inscripcion + error_periodo_escolar
        return errores_totales
    
    def registrar_inscripcion(self, campos: Dict) -> None:
        self.repositorio.registrar(campos)
    
    def obtener_todos_inscripciones(self) -> List[Tuple]:
        return self.repositorio.obtener_todos()
    
    def obtener_inscripcion_por_id(self, alumno_id: int) -> Optional[Tuple]:
        try:
            return self.repositorio.obtener_por_id(alumno_id)
        except BaseDatosError as error:
            raise error
    
    def obtener_inscripcion_por_num_matricula(self, num_matricula: str) -> Optional[Tuple]:
        try:
            return self.repositorio.obtener_por_num_matricula(num_matricula)
        except BaseDatosError as error:
            raise error
    
    def obtener_inscripcion_por_especialidad(self, especialidad_id: int) -> List[Tuple]:
        try:
            return self.repositorio.obtener_por_especialidad(especialidad_id)
        except BaseDatosError as error:
            raise error
    
    def obtener_inscripcion_por_cedula(self, cedula: str) -> Optional[Tuple]:
        try:
            return self.repositorio.obtener_por_cedula(cedula)
        except BaseDatosError as error:
            raise error
    
    def obtener_inscripcion_por_especialidad_o_cedula(self, especialidad_id: int, cedula: str = None) -> Union[List[Tuple], Tuple]:
        try:
            return self.repositorio.obtener_por_especialidad_o_cedula(especialidad_id, cedula)
        except BaseDatosError as error:
            raise error
    
    def obtener_inscripcion_por_especialidad_o_matricula(self, especialidad_id: int, num_matricula: str = None) -> Union[List[Tuple], Tuple]:
        try:
            return self.repositorio.obtener_por_especialidad_o_matricula(especialidad_id, num_matricula)
        except BaseDatosError as error:
            raise error
    
    def obtener_inscripcion_por_cedula_situacion_especialidad(self, especialidad_id: int, cedula: str = None, situacion: str = "Inactivo") -> Union[List[Tuple], Tuple]:
        try:
            return self.repositorio.obtener_por_cedula_situacion_especialidad(especialidad_id, cedula, situacion)
        except BaseDatosError as error:
            raise error
    
    def obtener_inscripcion_por_matricula_situacion_especialidad(self, especialidad_id: int, num_matricula: str = None, situacion: str = "Inactivo") -> Union[List[Tuple], Tuple]:
        try:
            return self.repositorio.obtener_por_matricula_situacion_especialidad(especialidad_id, num_matricula, situacion)
        except BaseDatosError as error:
            raise error
    
    def actualizar_inscripcion(self, alumno_id: int, campos_inscripcion: Dict) -> None:
        self.repositorio.actualizar(alumno_id, campos_inscripcion)


if __name__ == "__main__":
    inscripcion_repositorio = InscripcionRepositorio()
    inscripcion_servicio = InscripcionServicio(inscripcion_repositorio)
    
    """campos_inscripcion = {
        "num_matricula": None,
        "alumno_id": 16,
        "especialidad_id": 1,
        "fecha_inscripcion": None,
        "periodo_escolar": "2025-2026"
    }
    
    inscripcion_servicio.registrar_inscripcion(campos_inscripcion)"""
    
    """todos_inscripciones = inscripcion_servicio.obtener_todos_inscripciones()
    
    for registro in todos_inscripciones:
        print(registro)"""
    
    """try:
        print(inscripcion_servicio.obtener_inscripcion_por_id(5))
    except BaseDatosError as error:
        print(error)"""
    
    """try:
        print(inscripcion_servicio.obtener_inscripcion_por_num_matricula("MAT-323dw41"))
    except BaseDatosError as error:
        print(error)"""
    
    """try:
        todos_inscripciones = inscripcion_servicio.obtener_inscripcion_por_especialidad(2)
        for registro in todos_inscripciones:
            print(registro)
    except BaseDatosError as error:
        print(error)"""
    
    """try:
        print(inscripcion_servicio.obtener_inscripcion_por_cedula("35.342.903"))
    except BaseDatosError as error:
        print(error)"""
    
    """try:
        todos_inscripciones = inscripcion_servicio.obtener_inscripcion_por_especialidad_o_cedula(1, "35.342.903")
        if type(todos_inscripciones) == list:
            for registro in todos_inscripciones:
                print(registro)
        else:
            print(todos_inscripciones)
    except BaseDatosError as error:
        print(error)"""
    
    """try:
        todos_inscripciones = inscripcion_servicio.obtener_inscripcion_por_especialidad_o_matricula(1, "MAT-323dw41")
        if type(todos_inscripciones) == list:
            for registro in todos_inscripciones:
                print(registro)
        else:
            print(todos_inscripciones)
    except BaseDatosError as error:
        print(error)"""
    
    
    """campos_inscripcion = {
        "especialidad_id": 1,
        "fecha_inscripcion": date(2025, 6, 5),
        "periodo_escolar": "2026-2027"
    }
    
    inscripcion_servicio.actualizar_inscripcion(16, campos_inscripcion)"""