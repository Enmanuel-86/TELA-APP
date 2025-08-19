from typing import List, Tuple, Optional, Dict
from sqlalchemy import text
from excepciones.base_datos_error import BaseDatosError
from modelos import PermisoXRol
from repositorios.usuarios.auditoria_repositorio import auditoria_repositorio
from repositorios.repositorio_base import RepositorioBase
from conexiones.conexion import conexion_bd


class PermisoXRolRepositorio(RepositorioBase):
    def __init__(self):
        self.conexion_bd = conexion_bd
        self.entidad = "PERMISOS X ROL"
    
    def registrar(self, campos: Dict) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                nuevo_permiso_x_rol = PermisoXRol(**campos)
                
                rol_id = campos.get("rol_id")
                permiso_id = campos.get("permiso_id")
                
                sesion.add(nuevo_permiso_x_rol)
                sesion.commit()
                sesion.refresh(nuevo_permiso_x_rol)
                print("Se registró el permiso x rol correctamente")
                
                (permiso,) = sesion.execute(text("SELECT tipo_permiso FROM tb_permisos WHERE permiso_id = :permiso_id;"), 
                {"permiso_id": permiso_id}).fetchone()
                
                (rol,) = sesion.execute(text("SELECT tipo_rol FROM tb_roles WHERE rol_id = :rol_id;"), 
                {"rol_id": rol_id}).fetchone()
                
                accion = f"AÑADIÓ EL PERMISO DE {permiso} AL ROL DE {rol}"
                
                auditoria_repositorio.registrar(self.entidad, accion)
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL REGISTRAR EL PERMISO X ROL: {error}")
    
    def obtener_todos(self) -> List[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                permisos_x_rol = sesion.execute(text(
                    """
                        SELECT
                            permisos_x_rol.perm_x_rol_id,
                            roles.tipo_rol,
                            permisos.tipo_permiso
                        FROM tb_permisos_x_rol AS permisos_x_rol
                        INNER JOIN tb_roles AS roles ON permisos_x_rol.rol_id = roles.rol_id
                        INNER JOIN tb_permisos AS permisos ON permisos_x_rol.permiso_id = permisos.permiso_id;
                    """
                )).fetchall()
                return permisos_x_rol
        except Exception as error:
            print(f"ERROR AL OBTENER LOS PERMISOS X ROL: {error}")
    
    def obtener_por_id(self, perm_x_rol_id: int) -> Optional[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                permiso_x_rol = sesion.execute(text(
                    """
                        SELECT
                            permisos_x_rol.perm_x_rol_id,
                            roles.tipo_rol,
                            permisos.tipo_permiso
                        FROM tb_permisos_x_rol AS permisos_x_rol
                        INNER JOIN tb_roles AS roles ON permisos_x_rol.rol_id = roles.rol_id
                        INNER JOIN tb_permisos AS permisos ON permisos_x_rol.permiso_id = permisos.permiso_id
                        WHERE permisos_x_rol.perm_x_rol_id = :perm_x_rol_id;
                    """
                ), {"perm_x_rol_id": perm_x_rol_id}).fetchone()
                
                if not(permiso_x_rol):
                    raise BaseDatosError("PERMISO_X_ROL_NO_EXISTE", "Este permiso x rol no existe")
                
                return permiso_x_rol
        except BaseDatosError as error:
            raise error
        except Exception as error:
            print(f"ERROR AL OBTENER EL PERMISO X ROL: {error}")
    
    def actualizar(self, perm_x_rol_id: int, campos_permiso_x_rol: Dict) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                permiso_x_rol = sesion.query(PermisoXRol).filter(PermisoXRol.perm_x_rol_id == permiso_x_rol).first()
                diccionario_permiso_x_rol = {campo: valor for campo, valor in vars(permiso_x_rol).items() if not(campo.startswith("_")) and not(campo == "perm_x_rol_id") and (campo == "rol_id")}
                
                (rol,) = sesion.execute(text(
                    """
                        SELECT
                            roles.tipo_rol
                        FROM tb_roles AS roles
                        INNER JOIN tb_permisos_x_rol AS permisos_x_rol ON permisos_x_rol.rol_id = roles.rol_id
                        WHERE permisos_x_rol.perm_x_rol_id = :perm_x_rol_id;
                    """
                ), {"perm_x_rol_id": perm_x_rol_id}).fetchone()
                        
                (permiso_anterior,) = sesion.execute(text(
                    """
                        SELECT
                            permisos.tipo_permiso
                        FROM tb_permisos AS permisos
                        INNER JOIN tb_permisos_x_rol AS permisos_x_rol ON permisos_x_rol.permiso_id = permisos.permiso_id
                        WHERE permisos_x_rol.perm_x_rol_id = :perm_x_rol_id;
                    """
                ), {"perm_x_rol_id": perm_x_rol_id}).fetchone()
                
                campos = {
                    "permiso_id": "PERMISO"
                }
                
                for clave in diccionario_permiso_x_rol.keys():
                    if not(campos_permiso_x_rol.get(clave) == diccionario_permiso_x_rol.get(clave)):
                        campo_actualizado = campos.get(clave)
                        nuevo_permiso_id = campos_permiso_x_rol.get("permiso_id")

                        (permiso_actual,) = sesion.execute(text(
                            """
                                SELECT tipo_permiso FROM tb_permisos WHERE permiso_id = :permiso_id;
                            """
                        ), {"permiso_id": nuevo_permiso_id}).fetchone()
                        
                        valor_campo_actual = campos_permiso_x_rol.get(clave)
                        
                        accion = f"ACTUALIZÓ EL CAMPO: {campo_actualizado} DEL ROL {rol}. PERMISO ANTERIOR: {permiso_anterior}. PERMISO ACTUAL: {permiso_actual}"
                        auditoria_repositorio.registrar(self.entidad, accion)
                        
                        sesion.query(PermisoXRol).filter(PermisoXRol.perm_x_rol_id == perm_x_rol_id).update({clave: valor_campo_actual})
                        sesion.commit()
                        print(f"Se actualizó el campo: {campo_actualizado} correctamente \n")
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL ACTUALIZAR LOS CAMPOS: {error}")
    
    def eliminar(self, perm_x_rol_id: int) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                (permiso,) = sesion.execute(text(
                    """
                        SELECT 
                            permisos.tipo_permiso
                        FROM tb_permisos AS permisos
                        INNER JOIN tb_permisos_x_rol AS permisos_x_rol ON permisos_x_rol.permiso_id = permisos.permiso_id
                        WHERE permisos_x_rol.perm_x_rol_id = :perm_x_rol_id;
                    """
                ), {"perm_x_rol_id": perm_x_rol_id}).fetchone()
                
                (rol,) = sesion.execute(text(
                    """
                        SELECT
                            roles.tipo_rol
                        FROM tb_roles AS roles
                        INNER JOIN tb_permisos_x_rol AS permisos_x_rol ON permisos_x_rol.rol_id = roles.rol_id
                        WHERE permisos_x_rol.perm_x_rol_id = :perm_x_rol_id;
                    """
                ), {"perm_x_rol_id": perm_x_rol_id}).fetchone()
                
                permiso_x_rol = sesion.query(PermisoXRol).filter(PermisoXRol.perm_x_rol_id == perm_x_rol_id)
                
                if not(permiso_x_rol):
                    raise BaseDatosError("PERMISO_X_ROL_NO_EXISTE", "Este permiso x rol no existe")
                
                accion = f"ELIMINÓ EL PERMISO DE {permiso} AL ROL DE {rol}"
                
                auditoria_repositorio.registrar(self.entidad, accion)
                
                sesion.delete(permiso_x_rol)
                sesion.commit()
                print("Se eliminó el rol correctamente")
        except BaseDatosError as error:
            sesion.rollback()
            raise error
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL ELIMINAR EL ROL: {error}")

if __name__ == "__main__":
    permiso_x_rol = PermisoXRolRepositorio()
    
    campos_permiso_x_rol = {
        "rol_id": 3,
        "permiso_id": 10
    }
    
    permiso_x_rol.registrar(campos_permiso_x_rol)
    
    """registros = permiso_x_rol.obtener_todos()
    
    for registro in registros:
        print(registro)"""
    
    #print(permiso_x_rol.obtener_por_id(2))