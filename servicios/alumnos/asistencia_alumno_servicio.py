from typing import Tuple, List, Optional, Dict
from datetime import date
from excepciones.base_datos_error import BaseDatosError
from repositorios.repositorio_base import RepositorioBase
from repositorios.alumnos.asistencia_alumno_repositorio import AsistenciaAlumnoRepositorio


class AsistenciaAlumnoServicio:
    def __init__(self, repositorio: RepositorioBase):
        self.repositorio = repositorio
    
    def validar_inscripcion_id_y_fecha(self, inscripcion_id: int, fecha_asistencia: date) -> List[str]:
        errores = []
        
        if (self.obtener_asistencia_por_inscripcion_id_y_fecha(inscripcion_id, fecha_asistencia)):
            errores.append("Asistencia: No puedes marcar la asistencia de un mismo alumno en el mismo día.")
        
        return errores
    
    def validar_asistencia_alumno(self, inscripcion_id: int, fecha_asistencia: date) -> List[str]:
        error_inscripcion_id_y_fecha = self.validar_inscripcion_id_y_fecha(inscripcion_id, fecha_asistencia)
        
        errores_totales = error_inscripcion_id_y_fecha
        return errores_totales
    
    def registrar_asistencia_alumno(self, campos: Dict) -> None:
        self.repositorio.registrar(campos)
    
    def obtener_todos_asistencia_alumnos(self) -> List[Tuple]:
        return self.repositorio.obtener_todos()
    
    def obtener_asistencia_alumno_por_id(self, asist_alumno_id: int) -> Optional[Tuple]:
        try:
            return self.repositorio.obtener_por_id(asist_alumno_id)
        except BaseDatosError as error:
            raise error
    
    def obtener_asistencia_por_inscripcion_id_y_fecha(self, inscripcion_id: int, fecha_asistencia: date) -> Optional[Tuple]:
        return self.repositorio.obtener_por_inscripcion_id_y_fecha(inscripcion_id, fecha_asistencia)
    
    def obtener_asistencia_mensual(self) -> List[Tuple]:
        return self.repositorio.obtener_asistencia_mensual()
    
    def obtener_por_fecha_asistencia(self, fecha_asistencia: date) -> List[Tuple]:
        return self.repositorio.obtener_por_fecha_asistencia(fecha_asistencia)
    
    def obtener_asistencia_por_especialidad_y_anio_mes(self, especialidad_id: int, anio_mes: str) -> List[Tuple]:
        return self.repositorio.obtener_por_especialidad_y_anio_mes(especialidad_id, anio_mes)
    
    def obtener_sumatoria_asistencias_inasistencias(self, especialidad_id: int, anio_mes: str) -> Optional[Tuple]:
        return self.repositorio.obtener_sumatoria_asistencias_inasistencias(especialidad_id, anio_mes)
    
    def obtener_promedio_asistencias_inasistencias(self, especialidad_id: int, anio_mes: str) -> Optional[Tuple]:
        return self.repositorio.obtener_promedio_asistencias_inasistencias(especialidad_id, anio_mes)
    
    def obtener_porcentaje_asistencias_inasistencias(self, especialidad_id: int, anio_mes: str) -> Optional[Tuple]:
        return self.repositorio.obtener_porcentaje_asistencias_inasistencias(especialidad_id, anio_mes)
    
    def obtener_matricula_completa_alumnos(self, especialidad_id: int) -> Optional[Tuple]:
        return self.repositorio.obtener_matricula_completa_alumnos(especialidad_id)
    
    def actualizar_asistencia_alumno(self, asist_alumno_id: int, campos_asistencia_alumno: Dict) -> None:
        self.repositorio.actualizar(asist_alumno_id, campos_asistencia_alumno)
    
    def eliminar_asistencia_alumno(self, asist_alumno_id: int) -> None:
        try:
            self.repositorio.eliminar(asist_alumno_id)
        except BaseDatosError as error:
            raise error


if __name__ == "__main__":
    asistencia_alumno_repositorio = AsistenciaAlumnoRepositorio()
    asistencia_alumno_servicio = AsistenciaAlumnoServicio(asistencia_alumno_repositorio)
    
    """campos_asistencia_alumnos = {
        "inscripcion_id": 15,
        "fecha_asistencia": date.today(),
        "estado_asistencia": 1,
        "dia_no_laborable": None
    }
    
    asistencia_alumno_servicio.registrar_asistencia_alumno(campos_asistencia_alumnos)"""
    
    """todos_asistencia_alumnos = asistencia_alumno_servicio.obtener_todos_asistencia_alumnos()
    
    for registro in todos_asistencia_alumnos:
        print(registro)"""
    
    """try:
        print(asistencia_alumno_servicio.obtener_asistencia_alumno_por_id(40))
    except BaseDatosError as error:
        print(error)"""
    
    """todos_asistencia_mensual = asistencia_alumno_servicio.obtener_asistencia_mensual()
    
    for registro in todos_asistencia_mensual:
        print(registro)"""
    
    """todos_asistencia_por_fecha = asistencia_alumno_servicio.obtener_por_fecha_asistencia(date(2024, 5, 2))
    
    for registro in todos_asistencia_por_fecha:
        print(registro)"""
    
    """todos_asistencia_especialidad_anio_mes = asistencia_alumno_servicio.obtener_asistencia_por_especialidad_y_anio_mes(1, "2024-05")
    
    for registro in todos_asistencia_especialidad_anio_mes:
        print(registro)"""
        
    """sumatoria_asistencias_inasistencias = asistencia_alumno_servicio.obtener_sumatoria_asistencias_inasistencias(1, "2024-05")
    print(sumatoria_asistencias_inasistencias)"""
    
    """promedio_asistencias_inasistencias = asistencia_alumno_servicio.obtener_promedio_asistencias_inasistencias(1, "2024-05")
    print(promedio_asistencias_inasistencias)"""
    
    #print(asistencia_alumno_servicio.obtener_matricula_completa_alumnos(1))
    
    """campos_asistencia_alumnos = {
        "inscripcion_id": 15,
        "fecha_asistencia": date.today(),
        "estado_asistencia": None,
        "dia_no_laborable": "DIA FERIADO TAL"
    }
    
    asistencia_alumno_servicio.actualizar_asistencia_alumno(346, campos_asistencia_alumnos)"""
    
    """try:
        asistencia_alumno_servicio.eliminar_asistencia_alumno(346)
    except BaseDatosError as error:
        print(error)"""
    
    
    """errores_totales = asistencia_alumno_servicio.validar_asistencia_alumno(6, date(2024, 5, 2))
    
    if errores_totales:
        print("\n".join(errores_totales))"""