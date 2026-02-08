from typing import Tuple, List, Optional, Dict
from excepciones.base_datos_error import BaseDatosError
from datetime import date
from repositorios.empleados.reposo_empleado_repositorio import ReposoEmpleadoRepositorio
from repositorios.repositorio_base import RepositorioBase


class ReposoEmpleadoServicio:
    def __init__(self, repositorio: RepositorioBase):
        self.repositorio = repositorio
    
    def validar_empleado_id(self, empleado_id: int, reposo_empleado_id: int = None) -> List[str]:
        errores = []
        
        if not(empleado_id):
            errores.append("Empleado: Tiene que asignarle el reposo a un empleado.")
            
        try:
            empleado_ya_tiene_reposo = self.obtener_reposo_por_empleado_id(empleado_id)
            
            if (empleado_ya_tiene_reposo):
                id_reposo_empleado_existente = empleado_ya_tiene_reposo[6]
                
                if ((reposo_empleado_id is None) or (id_reposo_empleado_existente != reposo_empleado_id)):
                    errores.append("Empleado: Este empleado ya tiene un reposo registrado.")
        except BaseDatosError:
            pass
        
        return errores
    
    def validar_motivo_reposo(self, motivo_reposo: str) -> List[str]:
        errores = []
        
        if not(motivo_reposo):
            errores.append("Motivo del reposo: No puede estar vacío.")
        elif (motivo_reposo):
            motivo_reposo_sin_espacios = motivo_reposo.replace(" ", "")
            if (len(motivo_reposo_sin_espacios) == 0):
                errores.append("Motivo del reposo: No puede estar vacío.")
        
            if (len(motivo_reposo) > 100):
                errores.append("Motivo del reposo: No puede contener más de 100 caracteres.")
        
        return errores
    
    def validar_fecha_reingreso(self, fecha_reingreso: date, fecha_emision: date) -> List[str]:
        errores = []
        
        if not(fecha_reingreso):
            errores.append("Fecha de reingreso: No puede estar vacío.")
        
        if (fecha_reingreso < fecha_emision):
            errores.append("Fecha de reingreso: La fecha no puede ser menor a la fecha de emisión.")
        
        return errores
    
    def validar_campos_reposo(self, empleado_id: int, motivo_reposo: str, fecha_reingreso: date, fecha_emision: date, reposo_empleado_id: int = None) -> List[str]:
        error_empleado_id = self.validar_empleado_id(empleado_id, reposo_empleado_id)
        error_motivo_reposo = self.validar_motivo_reposo(motivo_reposo)
        error_fecha_reingreso = self.validar_fecha_reingreso(fecha_reingreso, fecha_emision)
        
        errores_totales = error_empleado_id + error_motivo_reposo + error_fecha_reingreso
        
        return errores_totales
    
    def registrar_reposo(self, campos: Dict) -> None:
        self.repositorio.registrar(campos)
    
    def obtener_todos_reposos(self) -> List[Tuple]:
        return self.repositorio.obtener_todos()
    
    def obtener_reposo_por_id(self, reposo_empleado_id: int) -> Optional[Tuple]:
        try:
            return self.repositorio.obtener_por_id(reposo_empleado_id)
        except BaseDatosError as error:
            raise error
    
    def obtener_reposo_por_empleado_id(self, empleado_id: int) -> Optional[Tuple]:
        try:
            return self.repositorio.obtener_por_empleado_id(empleado_id)
        except BaseDatosError as error:
            raise error
    
    def obtener_reposo_por_fecha_emision_o_cedula(self, fecha_emision: date, cedula_empleado: str = None) -> List[Tuple]:
        try:
            return self.repositorio.obtener_por_fecha_emision_o_cedula(fecha_emision, cedula_empleado)
        except BaseDatosError as error:
            raise error
    
    def actualizar_reposo(self, reposo_empleado_id: int, campos_reposo_empleado: Dict) -> None:
        self.repositorio.actualizar(reposo_empleado_id, campos_reposo_empleado)
    
    def eliminar_reposo(self, reposo_empleado_id: int) -> None:
        try:
            self.repositorio.eliminar(reposo_empleado_id)
        except BaseDatosError as error:
            raise error


if __name__ == "__main__":
    reposo_empleado_repositorio = ReposoEmpleadoRepositorio()
    reposo_empleado_servicio = ReposoEmpleadoServicio(reposo_empleado_repositorio)
    
    """campos_reposo_empleado = {
        "empleado_id": 1,
        "motivo_reposo": "MUERTE DE UN FAMILIAR",
        "fecha_emision": date.today(),
        "fecha_reingreso": date(2025, 6, 4)
    }
    
    reposo_empleado_servicio.registrar_reposo(campos_reposo_empleado)"""
    
    """todos_reposos_empleados = reposo_empleado_servicio.obtener_todos_reposos()
    
    for registro in todos_reposos_empleados:
        print(registro)"""
    
    #print(reposo_empleado_servicio.obtener_reposo_por_id(1))
    #print(reposo_empleado_servicio.obtener_reposo_por_fecha_emision(date(2025, 5, 18)))
    
    """campos_reposo_empleado = {
        "motivo_reposo": "FIEBRE Y TOS",
        "fecha_emision": date.today(),
        "fecha_reingreso": date(2025, 6, 4)
    }
    
    reposo_empleado_servicio.actualizar_reposo(2, campos_reposo_empleado)"""
    
    #reposo_empleado_servicio.eliminar_reposo(2)
    
    empleado_id = input("- Ingrese el ID del empleado: ")
    if not(empleado_id):
        empleado_id = None
    else:
        empleado_id = int(empleado_id)
    
    
    motivo_reposo = input("- Ingrese el motivo del reposo: ")
    
    dia_emision = input("- Ingrese el día de emisión: ")
    if not(dia_emision):
        dia_emision = None
    else:
        dia_emision = int(dia_emision)
    
    mes_emision = input("- Ingrese el mes de emisión: ")
    if not(mes_emision):
        mes_emision = None
    else:
        mes_emision = int(mes_emision)
    
    anio_emision = input("- Ingrese el año de emisión: ")
    if not(anio_emision):
        anio_emision = None
    else:
        anio_emision = int(anio_emision)
    
    if (not(dia_emision) or not(mes_emision) or not(anio_emision)):
        fecha_emision = date.today()
    else:
        fecha_emision = date(anio_emision, mes_emision, dia_emision)
    
    dia_reingreso = input("- Ingrese el día de reingreso: ")
    if not(dia_reingreso):
        dia_reingreso = None
    else:
        dia_reingreso = int(dia_reingreso)
    
    mes_reingreso = input("- Ingrese el mes de reingreso: ")
    if not(mes_reingreso):
        mes_reingreso = None
    else:
        mes_reingreso = int(mes_reingreso)
    
    anio_reingreso = input("- Ingrese el año de reingreso: ")
    if not(anio_reingreso):
        anio_reingreso = None
    else:
        anio_reingreso = int(anio_reingreso)
    
    fecha_reingreso = date(anio_reingreso, mes_reingreso, dia_reingreso)
    
    errores_totales = reposo_empleado_servicio.validar_campos_reposo(
        empleado_id, motivo_reposo,
        fecha_reingreso, fecha_emision
    )
    
    if errores_totales:
        print("\n".join(errores_totales))
    else:
        print("Registro del reposo exitoso.")