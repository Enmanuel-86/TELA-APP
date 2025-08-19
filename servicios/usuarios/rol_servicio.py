from typing import List, Tuple, Optional, Dict
from excepciones.base_datos_error import BaseDatosError
from repositorios.usuarios.rol_repositorio import RolRepositorio
from repositorios.repositorio_base import RepositorioBase


class RolServicio:
    def __init__(self, repositorio: RepositorioBase):
        self.repositorio = repositorio
    
    def validar_tipo_rol(self, tipo_rol: str) -> List[str]:
        errores = []
        
        if (not(tipo_rol)):
            errores.append("Tipo de rol: No puede estar vacío.")
        elif (tipo_rol):
            rol_sin_espacios = tipo_rol.replace(" ", "")
            if (len(rol_sin_espacios) == 0):
                errores.append("Tipo de rol: No puede estar vacío.")
        
            if (len(tipo_rol) > 25):
                errores.append("Tipo de rol: Máximo debe contener 25 caracteres.")
        
        return errores
    
    def validar_campos_rol(self, tipo_rol: str) -> List[str]:
        error_tipo_rol = self.validar_tipo_rol(tipo_rol)
        
        errores_totales = error_tipo_rol
        return errores_totales
    
    def registrar_rol(self, campos: Dict) -> None:
        self.repositorio.registrar(campos)
    
    def obtener_todos_roles(self) -> List[Tuple]:
        return self.repositorio.obtener_todos()

    def obtener_rol_por_id(self, rol_id: int) -> Optional[Tuple]:
        try:
            return self.repositorio.obtener_por_id(rol_id)
        except BaseDatosError as error:
            raise error
    
    def actualizar_rol(self, rol_id: int, campos_rol: Dict) -> None:
        self.repositorio.actualizar(rol_id, campos_rol)
    
    def eliminar_rol(self, rol_id: int) -> None:
        try:
            self.repositorio.eliminar(rol_id)
        except BaseDatosError as error:
            raise error


if __name__ == "__main__":
    rol_repositorio = RolRepositorio()
    rol_servicio = RolServicio(rol_repositorio)
    
    tipo_rol = input("- Ingrese el tipo de rol a registrar: ")
    
    campos_rol = {"tipo_rol": tipo_rol}
    
    errores_totales = rol_servicio.validar_registro_rol(tipo_rol)
    
    if errores_totales:
        print("\n".join(errores_totales))
    else:
        rol_servicio.registrar_rol(campos_rol)
    
    #print(rol_servicio.obtener_todos_roles())
    #rol_servicio.obtener_rol_por_id(3)
    
    #print(rol_servicio.obtener_rol_por_id(1))
    
    
    #rol_servicio.eliminar_rol(3)