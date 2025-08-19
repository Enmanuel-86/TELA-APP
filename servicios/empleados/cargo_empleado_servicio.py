from typing import Tuple, List, Optional, Dict
from excepciones.base_datos_error import BaseDatosError
from repositorios.empleados.cargo_empleado_repositorio import CargoEmpleadoRepositorio
from repositorios.repositorio_base import RepositorioBase


class CargoEmpleadoServicio:
    def __init__(self, repositorio: RepositorioBase):
        self.repositorio = repositorio
    
    def validar_codigo_cargo(self, codigo_cargo: str) -> List[str]:
        errores = []
        
        if not(codigo_cargo):
            errores.append("Código de cargo: No puede estar vacío.")
        elif (codigo_cargo):
            codigo_cargo_sin_espacios = codigo_cargo.replace(" ", "")
            ya_existe_codigo_cargo = self.obtener_cargo_por_codigo_cargo(codigo_cargo)
            if (len(codigo_cargo_sin_espacios) == 0):
                errores.append("Código de cargo: No puede estar vacío.")
        
            if (ya_existe_codigo_cargo):
                errores.append("Código de cargo: Este código de cargo ya está registrado.")
            
            if (len(codigo_cargo) > 15):
                errores.append("Código de cargo: No puede contener más de 15 caracteres.")
        
        return errores
    
    def validar_cargo(self, cargo: str) -> List[str]:
        errores = []
        
        if not(cargo):
            errores.append("Cargo: No puede estar vacío.")
        elif (cargo):
            cargo_sin_espacios = cargo.replace(" ", "")
            if (len(cargo_sin_espacios) == 0):
                errores.append("Cargo: No puede estar vacío.")
        
            if (len(cargo) > 35):
                errores.append("Cargo: No puede contener más de 35 caracteres.")
        
        return errores
    
    def validar_campos_cargo_empleado(self, codigo_cargo: str, cargo: str) -> List[str]:
        error_codigo_cargo = self.validar_codigo_cargo(codigo_cargo)
        error_cargo = self.validar_cargo(cargo)
        
        errores_totales = error_codigo_cargo + error_cargo
        
        return errores_totales
    
    def registrar_cargo_empleado(self, campos: Dict) -> None:
        self.repositorio.registrar(campos)
    
    def obtener_todos_cargos_empleados(self) -> List[Tuple]:
        return self.repositorio.obtener_todos()
    
    def obtener_cargo_empleado_por_id(self, cargo_id: int) -> Optional[Tuple]:
        try:
            return self.repositorio.obtener_por_id(cargo_id)
        except BaseDatosError as error:
            raise error
    
    def obtener_cargo_por_codigo_cargo(self, codigo_cargo: str) -> Optional[Tuple]:
        return self.repositorio.obtener_por_codigo_cargo(codigo_cargo)
    
    def actualizar_cargo_empleado(self, cargo_id: int, campos_cargos_empleados: Dict) -> None:
        self.repositorio.actualizar(cargo_id, campos_cargos_empleados)
    
    def eliminar_cargo_empleado(self, cargo_id: int) -> None:
        try:
            self.repositorio.eliminar(cargo_id)
        except BaseDatosError as error:
            raise error


if __name__ == "__main__":
    cargo_empleado_repositorio = CargoEmpleadoRepositorio()
    cargo_empleado_servicio = CargoEmpleadoServicio(cargo_empleado_repositorio)
    
    """campos_cargos_empleados = {
        "codigo_cargo": "100023456",
        "cargo": "DOCENTE IV"
    }
    
    cargo_empleado_servicio.registrar_cargo_empleado(campos_cargos_empleados)"""
    
    """todos_cargos_empleados = cargo_empleado_servicio.obtener_todos_cargos_empleados()
    
    for registro in todos_cargos_empleados:
        print(registro)"""
    
    
    #print(cargo_empleado_servicio.obtener_cargo_empleado_por_id(2))
    #print(cargo_empleado_servicio.obtener_cargo_por_codigo_cargo("100000C"))
    
    """campos_cargos_empleados = {
        "codigo_cargo": "123456789",
        "cargo": "DOCENTE V"
    }
    
    cargo_empleado_servicio.actualizar_cargo_empleado(3, campos_cargos_empleados)"""
    
    #cargo_empleado_servicio.eliminar_cargo_empleado(1)
    #cargo_empleado_servicio.eliminar_cargo_empleado(3)
    
    codigo_cargo = input("- Ingrese el código de cargo: ")
    cargo = input("- Ingrese el cargo: ")
    
    errores_totales = cargo_empleado_servicio.validar_campos_cargo_empleado(codigo_cargo, cargo)
    
    if errores_totales:
        print("\n".join(errores_totales))
    else:
        print("Registro del cargo empleado exitoso.")