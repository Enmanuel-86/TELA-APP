from sqlalchemy import text
from typing import List, Tuple, Optional
from excepciones.base_datos_error import BaseDatosError
from modelos import Permiso
from conexiones.conexion import conexion_bd


class PermisoRepositorio:
    def __init__(self):
        self.conexion_bd = conexion_bd
    
    def obtener_todos(self) -> List[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                permisos = sesion.query(Permiso.permiso_id, Permiso.tipo_permiso).all()
                return permisos
        except Exception as error:
            print(f"ERROR AL OBTENER LOS PERMISOS: {error}")
    
    def obtener_por_id(self, permiso_id: int) -> Optional[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                permiso = sesion.query(Permiso.permiso_id, Permiso.tipo_permiso).filter(Permiso.permiso_id == permiso_id).first()
                
                if not(permiso):
                    raise BaseDatosError("PERMISO_NO_EXISTE", "Este permiso no existe")
                
                return permiso
        except BaseDatosError as error:
            raise error
        except Exception as error:
            print(f"ERROR AL OBTENER EL PERMISO: {error}")
    
    def verificar_permiso_usuario(self, usuario_id: int, tipo_permiso: str) -> Optional[bool]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                usuario_permiso = sesion.execute(text(
                    """
                        SELECT
                            COUNT(*) > 0
                        FROM tb_usuarios AS usuarios
                        INNER JOIN tb_roles AS roles ON usuarios.rol_id = roles.rol_id
                        INNER JOIN tb_permisos_x_rol AS permisos_x_rol ON permisos_x_rol.rol_id = roles.rol_id
                        INNER JOIN tb_permisos AS permisos ON permisos_x_rol.permiso_id = permisos.permiso_id
                        WHERE usuarios.usuario_id = :usuario_id AND permisos.tipo_permiso = :tipo_permiso;
                    """
                ), {"usuario_id": usuario_id, "tipo_permiso": tipo_permiso}).fetchone()
                
                if not(usuario_permiso[0]):
                    raise BaseDatosError("USUARIO_NO_TIENE_PERMISO", "No tienes el permiso requerido para realizar esta acción")
                
                return True
        except BaseDatosError as error:
            raise error
        except Exception as error:
            print(f"ERROR AL VERIFICAR EL PERMISO DEL USUARIO: {error}")


if __name__ == "__main__":
    permiso = PermisoRepositorio()
    
    """registros = permiso.obtener_todos()
    
    for registro in registros:
        print(registro)"""
    
    #print(permiso.obtener_por_id(1))