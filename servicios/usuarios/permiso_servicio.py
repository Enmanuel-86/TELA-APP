from typing import List, Tuple, Optional
from excepciones.base_datos_error import BaseDatosError
from repositorios.usuarios.permiso_repositorio import PermisoRepositorio
from repositorios.repositorio_base import RepositorioBase


class PermisoServicio:
    def __init__(self, repositorio: RepositorioBase):
        self.repositorio = repositorio
    
    def obtener_todos_permisos(self) -> List[Tuple]:
        return self.repositorio.obtener_todos()
    
    def obtener_permiso_por_id(self, permiso_id: int) -> Optional[Tuple]:
        try:
            return self.repositorio.obtener_por_id(permiso_id)
        except BaseDatosError as error:
            raise error
    
    def verificar_permiso_usuario(self, usuario_id: int, tipo_permiso: str) -> Optional[bool]:
        try:
            return self.repositorio.verificar_permiso_usuario(usuario_id, tipo_permiso)
        except BaseDatosError as error:
            raise error


if __name__ == "__main__":
    permiso_repositorio = PermisoRepositorio()
    permiso_servicio = PermisoServicio(permiso_repositorio)
    
    """registros = permiso_servicio.obtener_todos_permisos()
    
    for registro in registros:
        print(registro)"""
    
    """permiso = permiso_servicio.obtener_permiso_por_id(4)
    
    if permiso is not(None):
        print(permiso)"""
    
    #permiso_servicio.verificar_permiso_usuario(1, "GESTIONAR OTRA COSA")