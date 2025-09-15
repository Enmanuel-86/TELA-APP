from typing import Tuple, List, Optional, Dict
from excepciones.base_datos_error import BaseDatosError
from datetime import date, time
from repositorios.empleados.asistencia_empleado_repositorio import AsistenciaEmpleadoRepositorio
from repositorios.repositorio_base import RepositorioBase


class AsistenciaEmpleadoServicio:
    def __init__(self, repositorio: RepositorioBase):
        self.repositorio = repositorio
    
    def validar_empleado_id_y_fecha(self, empleado_id: int, fecha_asistencia: date) -> List[str]:
        errores = []
        
        if (self.obtener_asistencia_por_empleado_id_y_fecha(empleado_id, fecha_asistencia)):
            errores.append("Asistencia: No puedes marcar la asistencia de un mismo empleado en el mismo día.")
        
        return errores
    
    def validar_fecha_asistencia(self, fecha_asistencia: date) -> List[str]:
        errores = []
        
        if not(fecha_asistencia):
            errores.append("Fecha de asistencia: Tiene que asignarle una fecha a la asistencia.")
        
        return errores
    
    def validar_estado_asistencia(self, estado_asistencia: str) -> List[str]:
        errores = []
        
        if not(estado_asistencia):
            errores.append("Estado de asistencia: Tiene que seleccionar un estado de asistencia.")
        
        return errores
    
    def validar_motivo_retraso(self, motivo_retraso: str) -> List[str]:
        errores = []
        
        if (motivo_retraso):
            if (len(motivo_retraso) > 100):
                errores.append("Motivo de retraso: No puede contener más de 100 caracteres.")
        
        return errores
    
    def validar_motivo_inasistencia(self, motivo_inasistencia: str) -> List[str]:
        errores = []
        
        if (motivo_inasistencia):
            if (len(motivo_inasistencia) > 100):
                errores.append("Motivo de inasistencia: No puede contener más de 100 caracteres.")
        
        return errores
    
    def validar_asistencia_empleado(
        self, empleado_id: int,
        fecha_asistencia: date, estado_asistencia: str,
        motivo_retraso: str, motivo_inasistencia: str
    ) -> List[str]:
        error_empleado_id_y_fecha = self.validar_empleado_id_y_fecha(empleado_id, fecha_asistencia)
        error_fecha_asistencia = self.validar_fecha_asistencia(fecha_asistencia)
        error_estado_asistencia = self.validar_estado_asistencia(estado_asistencia)
        error_motivo_retraso = self.validar_motivo_retraso(motivo_retraso)
        error_motivo_inasistencia = self.validar_motivo_inasistencia(motivo_inasistencia)
        
        errores_totales = error_empleado_id_y_fecha + error_fecha_asistencia + error_estado_asistencia + error_motivo_retraso + error_motivo_inasistencia
        
        return errores_totales
    
    def registrar_asistencia_empleado(self, campos: Dict) -> None:
        self.repositorio.registrar(campos)
    
    def obtener_todos_asistencia_empleado(self) -> List[Tuple]:
        return self.repositorio.obtener_todos()
    
    def obtener_asistencia_empleado_por_id(self, asist_empleado_id: int) -> Optional[Tuple]:
        try:
            return self.repositorio.obtener_por_id(asist_empleado_id)
        except BaseDatosError as error:
            raise error
    
    def obtener_asistencia_empleado_por_fecha(self, fecha_asistencia: date) -> List[Tuple]:
        try:
            return self.repositorio.obtener_por_fecha(fecha_asistencia)
        except BaseDatosError as error:
            raise error
    
    def obtener_asistencia_por_empleado_id_y_fecha(self, empleado_id: int, fecha_asistencia: date) -> Optional[Tuple]:
        return self.repositorio.obtener_por_empleado_id_y_fecha(empleado_id, fecha_asistencia)
    
    def obtener_horas_retraso_mensuales_empleado(self, anio_mes: str) -> List[Tuple]:
        try:
            return self.repositorio.obtener_horas_retraso_mensuales(anio_mes)
        except BaseDatosError as error:
            raise error
    
    def obtener_num_inasistencias_mensuales_empleado(self, anio_mes: str) -> List[Tuple]:
        try:
            return self.repositorio.obtener_num_inasistencias_mensuales(anio_mes)
        except BaseDatosError as error:
            raise error
    
    def actualizar(self, asist_empleado_id: int, campos_asistencia_empleado: Dict) -> None:
        self.repositorio.actualizar(asist_empleado_id, campos_asistencia_empleado)
    
    def eliminar(self, asist_empleado_id: int) -> None:
        try:
            self.repositorio.eliminar(asist_empleado_id)
        except BaseDatosError as error:
            raise error


if __name__ == "__main__":
    asistencia_empleado_repositorio = AsistenciaEmpleadoRepositorio()
    asistencia_empleado_servicio = AsistenciaEmpleadoServicio(asistencia_empleado_repositorio)
    
    """campos_asistencia_empleados = {
        "empleado_id": 2,
        "fecha_asistencia": date.today(),
        "hora_entrada": time(7, 0),
        "hora_salida": time(12, 30),
        "estado_asistencia": "PRESENTE",
        "motivo_retraso": None,
        "motivo_inasistencia": None
    }
    
    asistencia_empleado_servicio.registrar_asistencia_empleado(campos_asistencia_empleados)"""
    
    """todos_asistencia_empleados = asistencia_empleado_servicio.obtener_todos_asistencia_empleado()
    
    for registro in todos_asistencia_empleados:
        print(registro)"""
    
    #print(asistencia_empleado_servicio.obtener_asistencia_empleado_por_id(1))
    
    """todos_asistencia_empleados = asistencia_empleado_servicio.obtener_asistencia_empleado_por_fecha(date(2024, 9, 24))
    
    for registro in todos_asistencia_empleados:
        print(registro)"""
    
    
    """todas_horas_retraso_mensuales = asistencia_empleado_servicio.obtener_horas_retraso_mensuales_empleado("2024-09")
    
    for registro in todas_horas_retraso_mensuales:
        print(registro)"""
    
    
    """todas_inasistencias_mensuales = asistencia_empleado_servicio.obtener_num_inasistencias_mensuales_empleado("2024-09")
    
    for registro in todas_inasistencias_mensuales:
        print(registro)"""
    
    
    """campos_asistencia_empleados = {
        "fecha_asistencia": date(2024, 9, 24),
        "hora_entrada": time(7, 20),
        "hora_salida": time(12, 40),
        "estado_asistencia": "PRESENTE",
        "motivo_retraso": "TRÁFICO",
        "motivo_inasistencia": None
    }
    
    asistencia_empleado_servicio.actualizar(9, campos_asistencia_empleados)"""
    
    #asistencia_empleado_servicio.eliminar(9)
    
    """empleado_id = input("- Ingrese el ID del empleado: ")
    if empleado_id:
        empleado_id = int(empleado_id)
    
    dia_asistencia = int(input("- Ingrese el día de la asistencia: "))
    mes_asistencia = int(input("- Ingrese el mes de la asistencia: "))
    anio_asistencia = int(input("- Ingrese el año de la asistencia: "))
    
    fecha_asistencia = date(anio_asistencia, mes_asistencia, dia_asistencia)
    
    hora_entrada_asistencia = int(input("- Ingrese la hora de entrada de asistencia: "))
    minuto_entrada_asistencia = int(input("- Ingrese el minuto de entrada de asistencia: "))
    hora_entrada = time(hora_entrada_asistencia, minuto_entrada_asistencia)
    
    hora_salida_asistencia = int(input("- Ingrese la hora de salida de asistencia: "))
    minuto_salida_asistencia = int(input("- Ingrese el minuto de salida de asistencia: "))
    hora_salida = time(hora_salida_asistencia, minuto_salida_asistencia)
    
    estado_asistencia = input("- Ingrese el estado de asistencia: ")
    
    motivo_retraso = input("- Ingrese el motivo de retraso: ")
    motivo_retraso_sin_espacios = motivo_retraso.replace(" ", "")
    if (not(motivo_retraso)):
        motivo_retraso = None
    elif (motivo_retraso):
        if (len(motivo_retraso_sin_espacios) == 0):
            motivo_retraso = None
    
    motivo_inasistencia = input("- Ingrese el motivo de inasistencia: ")
    motivo_inasistencia_sin_espacios = motivo_inasistencia.replace(" ","")
    if (not(motivo_inasistencia)):
        motivo_inasistencia = None
    elif (motivo_inasistencia):
        if(len(motivo_inasistencia_sin_espacios) == 0):
            motivo_inasistencia = None
    
    
    errores_totales = asistencia_empleado_servicio.validar_asistencia_empleado(
        empleado_id, fecha_asistencia,
        estado_asistencia, motivo_retraso,
        motivo_inasistencia
    )
    
    if errores_totales:
        print("\n".join(errores_totales))
    else:
        print("Registro de la asistencia exitoso")"""
    
    """errores = asistencia_empleado_servicio.validar_empleado_id_y_fecha(
        1, date(2024, 9, 26)
    )
    
    if errores:
        print("\n".join(errores))
    else:
        print("Asistencia registrada")"""