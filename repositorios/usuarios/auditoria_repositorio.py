from configuraciones.configuracion import app_configuracion
from typing import List, Tuple, Optional
from sqlalchemy import text
from excepciones.base_datos_error import BaseDatosError
from modelos import Auditoria
from conexiones.conexion import conexion_bd
from datetime import datetime, date
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
    
    def obtener_por_fecha_rol_y_usuario(self, fecha_accion: date, tipo_rol: Optional[str] = None, nombre_usuario: Optional[str] = None) -> Optional[List[Tuple]]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                consulta = """
                        SELECT 
                            auditoria_id,
                            nombre_usuario,
                            cedula,
                            primer_nombre,
                            tipo_rol,
                            entidad_afectada,
                            accion,
                            fecha_accion,
                            hora_accion
                        FROM vw_auditorias_sistema
                        WHERE fecha_accion = :fecha_accion
                    """
                
                parametros = {"fecha_accion": fecha_accion}
                condiciones_adicionales = []
                
                if (tipo_rol):
                    condiciones_adicionales.append("tipo_rol = :tipo_rol")
                    parametros["tipo_rol"] = tipo_rol
                
                if (nombre_usuario):
                    condiciones_adicionales.append("nombre_usuario = :nombre_usuario")
                    parametros["nombre_usuario"] = nombre_usuario
                
                if (condiciones_adicionales):
                    consulta += " AND " + " AND ".join(condiciones_adicionales)
                
                auditorias = sesion.execute(text(consulta), parametros).fetchall()
                
                if not(auditorias):
                    raise BaseDatosError("NO_HAY_AUDITORIAS", "No hay registros de auditoría en esta fecha, ni filtrados por el tipo de rol y nombre de usuario ingresados.")
                
                return auditorias
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
    
    try:
        fecha_actual = date(2026, 2, 22)
        
        auditorias = auditoria_repositorio.obtener_por_fecha_rol_y_usuario(fecha_actual, "DIRECTOR", "douglas345")
        
        for registro in auditorias:
            print(registro)
    except BaseDatosError as error:
        print(f"ERROR: {error}")