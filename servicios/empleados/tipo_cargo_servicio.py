from typing import Tuple, List, Optional, Dict
from excepciones.base_datos_error import BaseDatosError
from datetime import time
from repositorios.empleados.tipo_cargo_repositorio import TipoCargoRepositorio
from repositorios.repositorio_base import RepositorioBase


class TipoCargoServicio:
    def __init__(self, repositorio: RepositorioBase):
        self.repositorio = repositorio
    
    def validar_tipo_cargo(self, tipo_cargo: str) -> List[str]:
        errores = []
        
        if not(tipo_cargo):
            errores.append("Tipo de cargo: No puede estar vacío.")
        elif (tipo_cargo):
            tipo_cargo_sin_espacios = tipo_cargo.replace(" ", "")
            if (len(tipo_cargo_sin_espacios) == 0):
                errores.append("Tipo de cargo: No puede estar vacío.")
        
            if (len(tipo_cargo) > 25):
                errores.append("Tipo de cargo: No puede contener más de 25 caracteres.")
        
        return errores
    
    def validar_campos_tipo_cargo(self, tipo_cargo: str) -> List[str]:
        error_tipo_cargo = self.validar_tipo_cargo(tipo_cargo)
        errores_totales = error_tipo_cargo
        
        return errores_totales
    
    def registrar_tipo_cargo(self, campos: Dict) -> None:
        self.repositorio.registrar(campos)
    
    def obtener_todos_tipos_cargo(self) -> List[Tuple]:
        return self.repositorio.obtener_todos()
    
    def obtener_tipo_cargo_por_id(self, tipo_cargo_id: int) -> Optional[Tuple]:
        try:
            return self.repositorio.obtener_por_id(tipo_cargo_id)
        except BaseDatosError as error:
            raise error
    
    def actualizar_tipo_cargo(self, tipo_cargo_id: int, campos_tipo_cargo: Dict) -> None:
        return self.repositorio.actualizar(tipo_cargo_id, campos_tipo_cargo)
    
    def eliminar_tipo_cargo(self, tipo_cargo_id: int) -> None:
        try:
            self.repositorio.eliminar(tipo_cargo_id)
        except BaseDatosError as error:
            raise error


if __name__ == "__main__":
    tipo_cargo_repositorio = TipoCargoRepositorio()
    tipo_cargo_servicio = TipoCargoServicio(tipo_cargo_repositorio)
    
    """campos_tipo_cargo = {
        "tipo_cargo": "VIGILANTE",
        "horario_llegada": time(8, 0)
    }
    
    tipo_cargo_servicio.registrar_tipo_cargo(campos_tipo_cargo)"""
    
    """todos_tipo_cargo = tipo_cargo_servicio.obtener_todos_tipos_cargo()
    
    for tipo_cargo in todos_tipo_cargo:
        print(f"TIPO DE CARGO: {tipo_cargo[1]}. HORARIO DE LLEGADA: {tipo_cargo[2]}")"""
    
    """tipo_cargo = tipo_cargo_servicio.obtener_tipo_cargo_por_id(1)[1]
    horario_llegada = tipo_cargo_servicio.obtener_tipo_cargo_por_id(1)[2]
    
    print(f"TIPO DE CARGO: {tipo_cargo}. HORARIO DE LLEGADA: {horario_llegada}")"""
    
    """campos_tipo_cargo = {
        "tipo_cargo": "COCINERO",
        "horario_llegada": time(11, 30)
    }
    
    tipo_cargo_servicio.actualizar_tipo_cargo(2, campos_tipo_cargo)"""
    
    #tipo_cargo_servicio.eliminar_tipo_cargo(1)
    #tipo_cargo_servicio.eliminar_tipo_cargo(2)
    
    tipo_cargo = input("- Ingrese el tipo de cargo: ")
    
    hora_llegada = int(input("- Ingrese la hora de llegada: "))
    minuto_llegada = int(input("- Ingrese el minuto de llegada: "))
    horario_llegada = time(hora_llegada, minuto_llegada)
    
    errores_totales = tipo_cargo_servicio.validar_campos_tipo_cargo(tipo_cargo)
    
    if errores_totales:
        print("\n".join(errores_totales))
    else:
        print("Registro del tipo de cargo exitoso.")