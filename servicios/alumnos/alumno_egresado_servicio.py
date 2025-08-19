from typing import Tuple, List, Optional, Dict, Union
from datetime import date
from excepciones.base_datos_error import BaseDatosError
from repositorios.repositorio_base import RepositorioBase
from repositorios.alumnos.alumno_egresado_repositorio import AlumnoEgresadoRepositorio


class AlumnoEgresadoServicio:
    def __init__(self, repositorio: RepositorioBase):
        self.repositorio = repositorio
    
    def validar_alumno_id(self, alumno_id: int) -> List[str]:
        errores = []
        try:
            if not(alumno_id):
                errores.append("Alumno: No puede estar vacío.")
            elif (alumno_id):
                ya_esta_egresado = self.obtener_alumno_egresado_por_id(alumno_id)
                if (ya_esta_egresado):
                    errores.append("Alumno: Este alumno ya está egresado.")
        except BaseDatosError:
            pass
        
        return errores
    
    def validar_fecha_emision(self, fecha_emision: date) -> List[str]:
        errores = []
        
        if not(fecha_emision):
            errores.append("Fecha de emisión: No puede estar vacío.")
        
        return errores
    
    def validar_razon_egreso(self, razon_egreso: str) -> List[str]:
        errores = []
        
        if not(razon_egreso):
            errores.append("Razón de egreso: No puede estar vacío.")
        elif (razon_egreso):
            razon_egreso_sin_espacios = razon_egreso.replace(" ", "")
            if (len(razon_egreso_sin_espacios) == 0):
                errores.append("Razón de egreso: No puede estar vacío.")
            
            if (len(razon_egreso) > 50):
                errores.append("Razón de egreso: No puede contener más de 50 caracteres.")
        
        return errores
    
    def validar_campos_egreso(self, alumno_id: int, fecha_emision: date, razon_egreso: str) -> List[str]:
        error_alumno_id = self.validar_alumno_id(alumno_id)
        error_fecha_emision = self.validar_fecha_emision(fecha_emision)
        error_razon_egreso = self.validar_razon_egreso(razon_egreso)
        
        errores_totales = error_alumno_id + error_fecha_emision + error_razon_egreso
        return errores_totales
    
    def registrar_alumno_egresado(self, campos: Dict) -> None:
        self.repositorio.registrar(campos)
    
    def obtener_todos_alumnos_egresados(self) -> List[Tuple]:
        return self.repositorio.obtener_todos()
    
    def obtener_alumno_egresado_por_id(self, alumno_id: int) -> Optional[Tuple]:
        try:
            return self.repositorio.obtener_por_id(alumno_id)
        except BaseDatosError as error:
            raise error
    
    def obtener_alumno_egresado_por_cedula(self, cedula: str) -> Optional[Tuple]:
        try:
            return self.repositorio.obtener_por_cedula(cedula)
        except BaseDatosError as error:
            raise error
    
    def obtener_alumno_egresado_por_num_matricula(self, num_matricula: str) -> Optional[Tuple]:
        try:
            return self.repositorio.obtener_por_num_matricula(num_matricula)
        except BaseDatosError as error:
            raise error
    
    def obtener_alumno_egresado_por_especialidad(self, especialidad_id: int) -> List[Tuple]:
        try:
            return self.repositorio.obtener_por_especialidad(especialidad_id)
        except BaseDatosError as error:
            raise error
    
    def obtener_alumno_egresado_por_especialidad_o_cedula(self, especialidad_id: int, cedula: str = None) -> Union[List[Tuple], Tuple]:
        try:
            return self.repositorio.obtener_por_especialidad_o_cedula(especialidad_id, cedula)
        except BaseDatosError as error:
            raise error
    
    def obtener_alumno_egresado_por_especialidad_o_matricula(self, especialidad_id: int, num_matricula: str = None) -> Union[List[Tuple], Tuple]:
        try:
            return self.repositorio.obtener_por_especialidad_o_matricula(especialidad_id, num_matricula)
        except BaseDatosError as error:
            raise error
    
    def actualizar_alumno_egresado(self, alumno_id: int, campos_alumno_egresado: Dict) -> None:
        self.repositorio.actualizar(alumno_id, campos_alumno_egresado)
    
    def eliminar_alumno_egresado(self, alumno_id: int) -> None:
        try:
            self.repositorio.eliminar(alumno_id)
        except BaseDatosError as error:
            raise error


if __name__ == "__main__":
    alumno_egresado_repositorio = AlumnoEgresadoRepositorio()
    alumno_egresado_servicio = AlumnoEgresadoServicio(alumno_egresado_repositorio)
    
    """campos_alumno_egresado = {
        "alumno_id": 16,
        "fecha_emision": date.today(),
        "razon_egreso": "IRSE DE VIAJE"
    }
    
    alumno_egresado_servicio.registrar_alumno_egresado(campos_alumno_egresado)"""
    
    """todos_alumno_egresados = alumno_egresado_servicio.obtener_todos_alumnos_egresados()
    
    for registro in todos_alumno_egresados:
        print(registro)"""
    
    """try:
        print(alumno_egresado_servicio.obtener_alumno_egresado_por_id(16))
    except BaseDatosError as error:
        print(error)"""
    
    """try:
        print(alumno_egresado_servicio.obtener_alumno_egresado_por_cedula("9821397"))
    except BaseDatosError as error:
        print(error)"""
    
    """try:
        print(alumno_egresado_servicio.obtener_alumno_egresado_por_num_matricula("MAT-5qa2341"))
    except BaseDatosError as error:
        print(error)"""
    
    """try:
        todos_alumnos_egresados = alumno_egresado_servicio.obtener_alumno_egresado_por_especialidad(1)
        for registro in todos_alumnos_egresados:
            print(registro)
    except BaseDatosError as error:
        print(error)"""
    
    """try:
        todos_alumnos_egresados = alumno_egresado_servicio.obtener_alumno_egresado_por_especialidad_o_cedula(1, "9821397")
        if type(todos_alumnos_egresados) == list:
            for registro in todos_alumnos_egresados:
                print(registro)
        else:
            print(todos_alumnos_egresados)
    except BaseDatosError as error:
        print(error)"""
    
    """try:
        todos_alumnos_egresados = alumno_egresado_servicio.obtener_alumno_egresado_por_especialidad_o_matricula(1, "MAT-5qa2341")
        if type(todos_alumnos_egresados) == list:
            for registro in todos_alumnos_egresados:
                print(registro)
        else:
            print(todos_alumnos_egresados)
    except BaseDatosError as error:
        print(error)"""
    
    """campos_alumno_egresado = {
        "fecha_emision": date(2025, 1, 17),
        "razon_egreso": "OTRA COSA"
    }
    
    alumno_egresado_servicio.actualizar_alumno_egresado(16, campos_alumno_egresado)"""
    
    """try:
        alumno_egresado_servicio.eliminar_alumno_egresado(14)
    except BaseDatosError as error:
        print(error)"""
    
    """campos_alumno_egresado = {
        "alumno_id": 15,
        "fecha_emision": date.today(),
        "razon_egreso": "IRSE DE VIAJE"
    }
    
    errores_totales = alumno_egresado_servicio.validar_campos_egreso(
        campos_alumno_egresado.get("alumno_id"),
        campos_alumno_egresado.get("fecha_emision"),
        campos_alumno_egresado.get("razon_egreso")
    )
    
    if errores_totales:
        print("\n".join(errores_totales))
    else:
        print("Registro del egreso del alumno exitoso.")"""