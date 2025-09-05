import re
from typing import Tuple, List, Dict, Union
from excepciones.base_datos_error import BaseDatosError
from datetime import date
from repositorios.empleados.detalle_cargo_repositorio import DetalleCargoRepositorio
from repositorios.repositorio_base import RepositorioBase


class DetalleCargoServicio:
    def __init__(self, repositorio: RepositorioBase):
        self.repositorio = repositorio
    
    def validar_cargo_id(self, cargo_id: int) -> List[str]:
        errores = []
        
        if not(cargo_id):
            errores.append("Cargo del empleado: Tiene que asignarle un cargo.")
        
        return errores
    
    def validar_funcion_cargo_id(self, funcion_cargo_id: int) -> List[str]:
        errores = []
        
        if not(funcion_cargo_id):
            errores.append("Función del cargo: Tiene que asignarle una función del cargo.")
        
        return errores
    
    def validar_tipo_cargo_id(self, tipo_cargo_id: int) -> List[str]:
        errores = []
        
        if not(tipo_cargo_id):
            errores.append("Tipo de cargo: Tiene que asignarle un tipo de cargo.")
        
        return errores
    
    def validar_titulo_cargo(self, titulo_cargo: str) -> List[str]:
        errores = []
        
        if (not(titulo_cargo)):
            errores.append("Título del cargo: No puede estar vacío.")
        elif (titulo_cargo):
            titulo_cargo_sin_espacios = titulo_cargo.replace(" ", "")
            estructura_titulo_cargo = re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+$", titulo_cargo)
            if (len(titulo_cargo_sin_espacios) == 0):
                errores.append("Título del cargo: No puede estar vacío.")
        
            if not(estructura_titulo_cargo):
                errores.append("Título del cargo: No puede contener números o caracteres especiales.")
            
            if (len(titulo_cargo) > 100):
                errores.append("Título del cargo: No puede contener más de 100 caracteres.")
        
        return errores
    
    def validar_labores_cargo(self, labores_cargo: str) -> List[str]:
        errores = []
        
        if (labores_cargo):
            estructura_labores_cargo = re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+$", labores_cargo)
            if not(estructura_labores_cargo):
                errores.append("Labores del cargo: No debe contener números o caracteres especiales.")
        
            if (len(labores_cargo) > 50):
                errores.append("Labores del cargo: No debe contener más de 50 caracteres.")
        
        return errores
    
    def validar_fecha_ingreso_ministerio(self, fecha_ingreso_ministerio: date) -> List[str]:
        errores = []
        
        if not(fecha_ingreso_ministerio):
            errores.append("Fecha de ingreso al Ministerio: No puede estar vacío.")
        
        return errores
    
    def validar_detalles_cargo(
        self, cargo_id: int,
        funcion_cargo_id: int, tipo_cargo_id: int,
        titulo_cargo: str, labores_cargo: str,
        fecha_ingreso_ministerio: date
    ) -> List[str]:
        error_cargo_id = self.validar_cargo_id(cargo_id)
        error_funcion_cargo_id = self.validar_funcion_cargo_id(funcion_cargo_id)
        error_tipo_cargo_id = self.validar_tipo_cargo_id(tipo_cargo_id)
        error_titulo_cargo = self.validar_titulo_cargo(titulo_cargo)
        error_labores_cargo = self.validar_labores_cargo(labores_cargo)
        error_fecha_ingreso_ministerio = self.validar_fecha_ingreso_ministerio(fecha_ingreso_ministerio)
        
        errores_totales = error_cargo_id + error_funcion_cargo_id + error_tipo_cargo_id + error_titulo_cargo + error_labores_cargo + error_fecha_ingreso_ministerio
        
        return errores_totales
    
    def registrar_detalle_cargo(self, campos: Dict) -> None:
        self.repositorio.registrar(campos)
    
    def obtener_todos_detalles_cargo(self) -> List[Tuple]:
        return self.repositorio.obtener_todos()
    
    def obtener_detalles_cargo_por_id(self, empleado_id: int) -> Tuple:
        return self.repositorio.obtener_por_id(empleado_id)
    
    def obtener_detalles_cargo_empleados(self) -> List[Tuple]:
        return self.repositorio.obtener_detalles_cargo_empleados()
    
    def obtener_detalles_cargo_por_especialidad(self, especialidad_id: int) -> List[Tuple]:
        try:
            return self.repositorio.obtener_por_especialidad(especialidad_id)
        except BaseDatosError as error:
            raise error
    
    def obtener_detalles_cargo_por_tipo_cargo_o_especialidad_o_cedula(self, tipo_cargo_id: int, especialidad_id: int = None, cedula: str = None) -> Union[List[Tuple], Tuple]:
        try:
            return self.repositorio.obtener_por_tipo_cargo_o_especialidad_o_cedula(tipo_cargo_id, especialidad_id, cedula)
        except BaseDatosError as error:
            raise error
    
    def obtener_detalles_cargo(self, empleado_id: int) -> Tuple:
        return self.repositorio.obtener_detalles_cargo(empleado_id)
    
    def conteo_empleados_por_funcion_cargo(self) -> List[Tuple]:
        return self.repositorio.conteo_empleados_por_funcion_cargo()
    
    def conteo_matricula_empleados(self) -> List[Tuple]:
        return self.repositorio.conteo_matricula_empleados()
    
    def actualizar_detalle_cargo(self, empleado_id: int, campos_detalle_cargo: Dict) -> None:
        self.repositorio.actualizar(empleado_id, campos_detalle_cargo)


if __name__ == "__main__":
    detalle_cargo_repositorio = DetalleCargoRepositorio()
    detalle_cargo_servicio = DetalleCargoServicio(detalle_cargo_repositorio)
    
    """campos_detalle_cargo = {
        "empleado_id": 6,
        "cargo_id": 1,
        "funcion_cargo_id": 1,
        "especialidad_id": 1,
        "tipo_cargo_id": 1,
        "titulo_cargo": "BACHILLER",
        "labores_cargo": None
    }
    
    detalle_cargo_servicio.registrar_detalle_cargo(campos_detalle_cargo)"""
    
    """todos_detalles_cargo = detalle_cargo_servicio.obtener_todos_detalles_cargo()
    
    for registro in todos_detalles_cargo:
        print(registro)"""
    
    """try:
        todos_detalles_cargo = detalle_cargo_servicio.obtener_detalles_cargo_por_tipo_cargo_o_especialidad_o_cedula(1, None, "30932925")
        
        if (type(todos_detalles_cargo) == list):
            for registro in todos_detalles_cargo:
                print(registro)
        else:
            print(todos_detalles_cargo)
    except BaseDatosError as error:
        print(error)"""
    
    print(detalle_cargo_servicio.obtener_detalles_cargo(3))
    
    """campos_detalle_cargo = {
        "cargo_id": 1,
        "funcion_cargo_id": 1,
        "especialidad_id": None,
        "tipo_cargo_id": 1,
        "titulo_cargo": "BACHILLER",
        "labores_cargo": "SECRETARIO"
    }
    
    detalle_cargo_servicio.actualizar_detalle_cargo(6, campos_detalle_cargo)"""
    
    """cargo_id = input("- Ingrese el ID del cargo: ")
    if cargo_id:
        cargo_id = int(cargo_id)
    
    funcion_cargo_id = input("- Ingrese el ID de la función del cargo: ")
    if funcion_cargo_id:
        funcion_cargo_id = int(funcion_cargo_id)
    
    tipo_cargo_id = input("- Ingrese el ID del tipo de cargo: ")
    if tipo_cargo_id:
        tipo_cargo_id = int(tipo_cargo_id)
    
    especialidad_id = input("- Ingrese el ID de la especialidad: ")
    if especialidad_id:
        especialidad_id = int(especialidad_id)
    
    titulo_cargo = input("- Ingrese el título del cargo: ")
    labores_cargo = input("- Ingrese las labores del cargo: ")
    
    dia_ingreso_ministerio = int(input("- Ingrese el día de ingreso al ministerio: "))
    mes_ingreso_ministerio = int(input("- Ingrese el mes de ingreso al ministerio: "))
    anio_ingreso_ministerio = int(input("- Ingrese el año de ingreso al ministerio: "))
    fecha_ingreso_ministerio = date(anio_ingreso_ministerio, mes_ingreso_ministerio, dia_ingreso_ministerio)
    
    dia_ingreso_institucion = int(input("- Ingrese el día de ingreso a la institución: "))
    mes_ingreso_institucion = int(input("- Ingrese el mes de ingreso a la institución: "))
    anio_ingreso_institucion = int(input("- Ingrese el año de ingreso a la institución: "))
    fecha_ingreso_institucion = date(anio_ingreso_institucion, mes_ingreso_institucion, dia_ingreso_institucion)
    
    errores_totales = detalle_cargo_servicio.validar_detalles_cargo(
        cargo_id, funcion_cargo_id,
        tipo_cargo_id, titulo_cargo,
        labores_cargo, fecha_ingreso_ministerio
    )
    
    if (errores_totales):
        print("\n".join(errores_totales))
    else:
        print("Registro de los detalles del cargo exitosa.")"""