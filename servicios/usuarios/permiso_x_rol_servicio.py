from typing import List, Tuple, Optional, Dict
from excepciones.base_datos_error import BaseDatosError
from repositorios.usuarios.permiso_x_rol_repositorio import PermisoXRolRepositorio
from repositorios.repositorio_base import RepositorioBase


class PermisoXRolServicio:
    def __init__(self, repositorio: RepositorioBase):
        self.repositorio = repositorio
    
    def registrar_permiso_x_rol(self, campos: Dict) -> None:
        self.repositorio.registrar(campos)
    
    def obtener_todos_permisos_x_rol(self) -> List[Tuple]:
        return self.repositorio.obtener_todos()
    
    def obtener_permiso_x_rol_por_id(self, perm_x_rol_id: int) -> Optional[Tuple]:
        try:
            return self.repositorio.obtener_por_id(perm_x_rol_id)
        except BaseDatosError as error:
            raise error
    
    def actualizar_permiso_x_rol(self, perm_x_rol_id: int, campos_permiso_x_rol: Dict) -> None:
        self.repositorio.actualizar(perm_x_rol_id, campos_permiso_x_rol)
    
    def eliminar_permiso_x_rol(self, perm_x_rol_id: int) -> None:
        try:
            self.repositorio.eliminar(perm_x_rol_id)
        except BaseDatosError as error:
            raise error


if __name__ == "__main__":
    permiso_x_rol_repositorio = PermisoXRolRepositorio()
    permiso_x_rol_servicio = PermisoXRolServicio(permiso_x_rol_repositorio)
    
    campos_permiso_x_rol = {
        "rol_id": 3,
        "permiso_id": 2
    }
    
    #permiso_x_rol_servicio.registrar_permiso_x_rol(campos_permiso_x_rol)
    
    """registros = permiso_x_rol_servicio.obtener_todos_permisos_x_rol()
    
    for registro in registros:
        print(registro)"""
    
    #print(permiso_x_rol_servicio.obtener_permiso_x_rol_por_id(4))