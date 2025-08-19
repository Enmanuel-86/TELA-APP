from typing import Tuple, List, Optional, Dict
from excepciones.base_datos_error import BaseDatosError
from repositorios.empleados.funcion_cargo_repositorio import FuncionCargoRepositorio
from repositorios.repositorio_base import RepositorioBase


class FuncionCargoServicio:
    def __init__(self, repositorio: RepositorioBase):
        self.repositorio = repositorio
    
    def validar_funcion_cargo(self, funcion_cargo: str) -> List[str]:
        errores = []
        
        if not(funcion_cargo):
            errores.append("Funciones del cargo: No puede estar vacío.")
        elif (funcion_cargo):
            funcion_cargo_sin_espacios = funcion_cargo.replace(" ", "")
            if (len(funcion_cargo_sin_espacios) == 0):
                errores.append("Funciones del cargo: No puede estar vacío.")
        
            if (len(funcion_cargo) > 45):
                errores.append("Funciones del cargo: No puede contener más de 45 caracteres.")
        
        return errores
    
    def validar_campos_funciones_cargo(self, funcion_cargo: str) -> List[str]:
        error_funcion_cargo = self.validar_funcion_cargo(funcion_cargo)
        errores_totales = error_funcion_cargo
        
        return errores_totales
    
    def registrar_funcion_cargo_repositorio(self, campos: Dict) -> None:
        self.repositorio.registrar(campos)
    
    def obtener_todos_funciones_cargo(self) -> List[Tuple]:
        return self.repositorio.obtener_todos()
    
    def obtener_funcion_cargo_por_id(self, funcion_cargo_id: int) -> Optional[Tuple]:
        try:
            return self.repositorio.obtener_por_id(funcion_cargo_id)
        except BaseDatosError as error:
            raise error
    
    def actualizar_funcion_cargo(self, funcion_cargo_id: int, campos_funciones_cargo: Dict) -> None:
        self.repositorio.actualizar(funcion_cargo_id, campos_funciones_cargo)
    
    def eliminar_funcion_cargo(self, funcion_cargo_id: int) -> None:
        try:
            self.repositorio.eliminar(funcion_cargo_id)
        except BaseDatosError as error:
            raise error


if __name__ == "__main__":
    funcion_cargo_repositorio = FuncionCargoRepositorio()
    funcion_cargo_servicio = FuncionCargoServicio(funcion_cargo_repositorio)
    
    """campos_funciones_cargo = {
        "funcion_cargo": "SECRETARIA"
    }
    
    funcion_cargo_servicio.registrar_funcion_cargo_repositorio(campos_funciones_cargo)"""
    
    """todos_funciones_cargo = funcion_cargo_servicio.obtener_todos_funciones_cargo()
    
    for registro in todos_funciones_cargo:
        print(registro)"""
    
    
    #print(funcion_cargo_servicio.obtener_funcion_cargo_por_id(1))
    
    campos_funciones_cargo = {
        "funcion_cargo": "TRAPEAR"
    }
    
    #funcion_cargo_servicio.actualizar_funcion_cargo(2, campos_funciones_cargo)
    
    #funcion_cargo_servicio.eliminar_funcion_cargo(1)
    #funcion_cargo_servicio.eliminar_funcion_cargo(2)
    
    funcion_cargo = input("- Ingrese la función del cargo: ")
    
    errores_totales = funcion_cargo_servicio.validar_campos_funciones_cargo(funcion_cargo)
    
    if errores_totales:
        print("\n".join(errores_totales))
    else:
        print("Registro de la función del cargo exitoso.")