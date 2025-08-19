from typing import List, Tuple, Optional, Dict
from excepciones.base_datos_error import BaseDatosError
from modelos import Rol
from repositorios.usuarios.auditoria_repositorio import auditoria_repositorio
from repositorios.repositorio_base import RepositorioBase
from conexiones.conexion import conexion_bd


class RolRepositorio(RepositorioBase):
    def __init__(self):
        self.conexion_bd = conexion_bd
        self.entidad = "ROLES"
    
    def registrar(self, campos: Dict) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                nuevo_rol = Rol()
                
                tipo_rol = campos.get("tipo_rol")
                
                sesion.add(nuevo_rol)
                sesion.commit()
                sesion.refresh(nuevo_rol)
                print("Se registró el rol correctamente")
                
                entidad = self.entidad
                accion = f"REGISTRÓ EL ROL DE: {tipo_rol}"
                
                auditoria_repositorio.registrar(entidad, accion)
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL REGISTRAR EL ROL: {error}")
    
    def obtener_todos(self) -> List[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                roles = sesion.query(Rol.rol_id, Rol.tipo_rol).all()
                return roles
        except Exception as error:
            print(f"ERROR AL OBTENER LOS ROLES: {error}")
    
    def obtener_por_id(self, rol_id: int) -> Optional[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                rol = sesion.query(Rol.rol_id, Rol.tipo_rol).filter(Rol.rol_id == rol_id).first()
                
                if not(rol):
                    raise BaseDatosError("ROL_NO_EXISTE", "Este rol no existe")
                
                return rol
        except BaseDatosError as error:
            raise error
        except Exception as error:
            print(f"ERROR AL OBTENER EL ROL: {error}")
    
    def actualizar(self, rol_id: int, campos_rol: Dict) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                rol = sesion.query(Rol).filter(Rol.rol_id == rol_id).first()
                diccionario_rol = {campo: valor for campo, valor in vars(rol).items() if not(campo.startswith("_")) and not(campo == "rol_id")}
                
                campos = {
                    "tipo_rol": "TIPO DE ROL"
                }
                
                for clave in diccionario_rol.keys():
                    if not(campos_rol.get(clave) == diccionario_rol.get(clave)):
                        campo_actualizado = campos.get(clave)
                        
                        valor_campo_anterior = diccionario_rol.get(clave)
                        valor_campo_actual = campos_rol.get(clave)
                        
                        accion = f"ACTUALIZÓ EL CAMPO: {campo_actualizado}. ANTES: {valor_campo_anterior}. AHORA: {valor_campo_actual}"
                        auditoria_repositorio.registrar(self.entidad, accion)
                        
                        sesion.query(Rol).filter(Rol.rol_id == rol_id).update({clave: valor_campo_actual})
                        sesion.commit()
                        print(f"Se actualizó el campo: {campo_actualizado} correctamente \n")
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL ACTUALIZAR LOS CAMPOS: {error}")
    
    def eliminar(self, rol_id: int) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                rol = sesion.query(Rol).filter(Rol.rol_id == rol_id).first()
                
                if not(rol):
                    raise BaseDatosError("ROL_NO_EXISTE", "Este rol no existe")
                
                rol_asociado_a_usuarios = rol.usuario
                
                if rol_asociado_a_usuarios:
                    raise BaseDatosError("ROL_ASOCIADO", "Este rol está asociado a 1 o más usuarios y no puede ser eliminado")
                
                accion = f"ELIMINÓ EL ROL DE: {rol.tipo_rol}"
                
                auditoria_repositorio.registrar(self.entidad, accion)
                
                sesion.delete(rol)
                sesion.commit()
                print("Se eliminó el rol correctamente")
        except BaseDatosError as error:
            sesion.rollback()
            raise error
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL ELIMINAR EL ROL: {error}")


if __name__ == "__main__":
    rol = RolRepositorio()
    
    campos_rol = {"tipo_rol": "DOCENTE"}
    
    #rol.registrar(campos_rol)
    
    #print(rol.obtener_por_id(1))
    #print(rol.obtener_todos())
    
    #rol.eliminar(2)