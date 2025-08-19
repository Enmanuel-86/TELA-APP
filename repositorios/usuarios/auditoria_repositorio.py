from configuraciones.configuracion import app_configuracion
from typing import List, Tuple, Optional
from sqlalchemy import text
from excepciones.base_datos_error import BaseDatosError
from modelos import Auditoria
from conexiones.conexion import conexion_bd
from datetime import datetime
from repositorios.repositorio_base import RepositorioBase


class AuditoriaRepositorio(RepositorioBase):
    def __init__(self):
        self.conexion_bd = conexion_bd
    
    def registrar(self, entidad_afectada: str, accion: str) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                nueva_auditoria = Auditoria()
                
                nueva_auditoria.usuario_id = app_configuracion.USUARIO_ID
                nueva_auditoria.entidad_afectada = entidad_afectada
                nueva_auditoria.accion = accion
                nueva_auditoria.fecha_accion = datetime.now()
                
                sesion.add(nueva_auditoria)
                sesion.commit()
                sesion.refresh(nueva_auditoria)
                print("Se registro la auditoria correctamente")
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL REGISTRAR LA AUDITORÍA: {error}")
    
    def obtener_todos(self) -> List[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                auditorias = sesion.execute(text(
                    """
                        SELECT
                            auditorias.auditoria_id,
                            usuarios.nombre_usuario,
                            empleados.cedula,
                            empleados.primer_nombre,
                            roles.tipo_rol,
                            auditorias.entidad_afectada,
                            auditorias.accion,
                            STRFTIME('%Y-%m-%d', auditorias.fecha_accion) AS fecha_accion,
                            STRFTIME('%H:%M', auditorias.fecha_accion) AS hora_accion
                        FROM tb_auditorias AS auditorias
                        INNER JOIN tb_usuarios AS usuarios ON auditorias.usuario_id = usuarios.usuario_id
                        INNER JOIN tb_roles AS roles ON usuarios.rol_id = roles.rol_id
                        INNER JOIN tb_empleados AS empleados ON usuarios.empleado_id = empleados.empleado_id;
                    """
                )).fetchall()
                return auditorias
        except Exception as error:
            print(f"ERROR AL OBTENER LAS AUDITORÍAS: {error}")
    
    def obtener_por_id(self, auditoria_id: int) -> Optional[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                auditoria = sesion.execute(text(
                    """
                        SELECT 
                            auditorias.auditoria_id,
                            usuarios.nombre_usuario,
                            empleados.cedula,
                            empleados.primer_nombre,
                            roles.tipo_rol,
                            auditorias.entidad_afectada,
                            auditorias.accion,
                            STRFTIME('%Y-%m-%d', auditorias.fecha_accion) AS fecha_accion,
                            STRFTIME('%H:%M', auditorias.fecha_accion) AS hora_accion
                        FROM tb_auditorias AS auditorias
                        INNER JOIN tb_usuarios AS usuarios ON auditorias.usuario_id = usuarios.usuario_id
                        INNER JOIN tb_roles AS roles ON usuarios.rol_id = roles.rol_id
                        INNER JOIN tb_empleados AS empleados ON usuarios.empleado_id = empleados.empleado_id
                        WHERE auditorias.auditoria_id = :auditoria_id;
                    """
                ), {"auditoria_id": auditoria_id}).fetchone()
                
                if not(auditoria):
                    raise BaseDatosError("AUDITORIA_NO_EXISTE", "Este registro de auditoría no existe")
                
                return auditoria
        except BaseDatosError as error:
            raise error
        except Exception as error:
            print(f"ERROR AL OBTENER LA AUDITORÍA: {error}")

auditoria_repositorio = AuditoriaRepositorio()

if __name__ == "__main__":
    """todos_auditorias = auditoria_repositorio.obtener_todos()
    
    for registro in todos_auditorias:
        print(registro)"""
    
    
    #print(auditoria.obtener_por_id(2))