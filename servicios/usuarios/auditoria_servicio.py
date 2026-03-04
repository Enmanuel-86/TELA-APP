from typing import List, Tuple, Optional
from datetime import date
from excepciones.base_datos_error import BaseDatosError
from repositorios.usuarios.auditoria_repositorio import AuditoriaRepositorio
from repositorios.repositorio_base import RepositorioBase


class AuditoriaServicio:
    def __init__(self, repositorio: RepositorioBase):
        self.repositorio = repositorio
    
    def obtener_todos_auditorias(self) -> List[Tuple]:
        return self.repositorio.obtener_todos()
    
    def obtener_auditoria_por_id(self, auditoria_id: int) -> Optional[Tuple]:
        try:
            return self.repositorio.obtener_por_id(auditoria_id)
        except BaseDatosError as error:
            raise error
    
    def obtener_auditorias_por_fecha_rol_y_usuario(self, fecha_accion: date, tipo_rol: Optional[str] = None, nombre_usuario: Optional[str] = None) -> Optional[List[Tuple]]:
        try:
            return self.repositorio.obtener_por_fecha_rol_y_usuario(fecha_accion, tipo_rol, nombre_usuario)
        except BaseDatosError as error:
            raise error


if __name__ == "__main__":
    auditoria_repositorio = AuditoriaRepositorio()
    auditoria_servicio = AuditoriaServicio(auditoria_repositorio)
    
    """registros = auditoria_servicio.obtener_todos_auditorias()
    
    for registro in registros:
        print(registro)"""
    
    """auditoria = auditoria_servicio.obtener_auditoria_por_id(40)
    
    if auditoria is not(None):
        print(auditoria)"""