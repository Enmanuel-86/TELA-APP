from configuraciones.configuracion import app_configuracion
from typing import Tuple, List, Optional, Dict
from sqlalchemy import text
from excepciones.base_datos_error import BaseDatosError
from modelos import Usuario
from repositorios.usuarios.auditoria_repositorio import auditoria_repositorio
from repositorios.repositorio_base import RepositorioBase
from conexiones.conexion import conexion_bd


class UsuarioRepositorio(RepositorioBase):
    def __init__(self):
        self.conexion_bd = conexion_bd
        self.entidad = "USUARIOS"
        
    def registrar(self, campos: Dict) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                nuevo_usuario = Usuario(**campos)
                
                empleado_id = campos.get("empleado_id")
                rol_id = campos.get("rol_id")
                nombre_usuario = campos.get("nombre_usuario")
                
                sesion.add(nuevo_usuario)
                sesion.commit()
                sesion.refresh(nuevo_usuario)
                print("Se registró el usuario correctamente")
                
                (cedula_empleado,) = sesion.execute(text("SELECT cedula FROM tb_empleados WHERE empleado_id = :empleado_id;"), 
                {"empleado_id": empleado_id}).fetchone()
                
                (rol,) = sesion.execute(text("SELECT tipo_rol FROM tb_roles WHERE rol_id = :rol_id;"), 
                {"rol_id": rol_id}).fetchone()
                
                accion = f"REGISTRÓ A: {nombre_usuario}. CÉDULA DEL EMPLEADO: {cedula_empleado}. ROL: {rol}"
                
                auditoria_repositorio.registrar(self.entidad, accion)
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL REGISTRAR EL USUARIO: {error}")
    
    def obtener_todos(self) -> List[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                usuarios = sesion.execute(text(
                    """
                        SELECT
                            usuarios.usuario_id,
                            empleados.cedula,
                            empleados.primer_nombre,
                            empleados.apellido_paterno,
                            usuarios.nombre_usuario,
                            roles.tipo_rol
                        FROM tb_usuarios AS usuarios
                        INNER JOIN tb_roles AS roles ON usuarios.rol_id = roles.rol_id
                        INNER JOIN tb_empleados AS empleados ON usuarios.empleado_id = empleados.empleado_id;
                    """
                )).fetchall()
                
                return usuarios
        except Exception as error:
            print(f"ERROR AL OBTENER LOS USUARIOS: {error}")
    
    def obtener_por_id(self, usuario_id: int) -> Optional[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                usuario = sesion.execute(text(
                    """
                        SELECT
                            usuarios.usuario_id,
                            empleados.cedula,
                            empleados.primer_nombre,
                            empleados.apellido_paterno,
                            usuarios.nombre_usuario,
                            roles.tipo_rol
                        FROM tb_usuarios AS usuarios
                        INNER JOIN tb_roles AS roles ON usuarios.rol_id = roles.rol_id
                        INNER JOIN tb_empleados AS empleados ON usuarios.empleado_id = empleados.empleado_id
                        WHERE usuarios.usuario_id = :usuario_id;
                    """
                ), {"usuario_id": usuario_id}).fetchone()
                
                if not(usuario):
                    raise BaseDatosError("USUARIO_NO_EXISTE", "Este usuario no existe")
                
                return usuario
        except BaseDatosError as error:
            raise error
        except Exception as error:
            print(f"ERROR AL OBTENER EL USUARIO: {error}")
    
    def obtener_por_empleado_id(self, empleado_id: int) -> Optional[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                usuario = sesion.execute(text(
                    """
                        SELECT
                            usuarios.usuario_id,
                            empleados.empleado_id,
                            empleados.cedula,
                            empleados.primer_nombre,
                            empleados.apellido_paterno,
                            usuarios.nombre_usuario,
                            roles.tipo_rol,
                            usuarios.clave_usuario
                        FROM tb_usuarios AS usuarios
                        INNER JOIN tb_roles AS roles ON usuarios.rol_id = roles.rol_id
                        INNER JOIN tb_empleados AS empleados ON usuarios.empleado_id = empleados.empleado_id
                        WHERE empleados.empleado_id = :empleado_id;
                    """
                ), {"empleado_id": empleado_id}).fetchone()
                
                return usuario
        except Exception as error:
            print(f"ERROR AL OBTENER EL USUARIO POR EL ID DEL EMPLEADO: {error}")
    
    def obtener_por_nombre_usuario(self, nombre_usuario: str) -> Optional[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                usuario = sesion.execute(text(
                    """
                        SELECT
                            usuarios.usuario_id,
                            empleados.cedula,
                            empleados.primer_nombre,
                            empleados.apellido_paterno,
                            usuarios.nombre_usuario,
                            roles.tipo_rol
                        FROM tb_usuarios AS usuarios
                        INNER JOIN tb_roles AS roles ON usuarios.rol_id = roles.rol_id
                        INNER JOIN tb_empleados AS empleados ON usuarios.empleado_id = empleados.empleado_id
                        WHERE usuarios.nombre_usuario = :nombre_usuario;
                    """
                ), {"nombre_usuario": nombre_usuario}).fetchone()
                
                return usuario
        except Exception as error:
            print(f"ERROR AL OBTENER EL USUARIO POR SU NOMBRE DE USUARIO: {error}")
    
    def obtener_por_rol_o_cedula_empleado(self, rol_id: int, cedula_empleado: Optional[str] = None) -> Optional[List[Tuple]]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                consulta = """
                    SELECT
                        usuarios.usuario_id,
                        empleados.cedula,
                        empleados.primer_nombre,
                        empleados.apellido_paterno,
                        usuarios.nombre_usuario,
                        roles.tipo_rol
                    FROM tb_usuarios AS usuarios
                    INNER JOIN tb_roles AS roles ON usuarios.rol_id = roles.rol_id
                    INNER JOIN tb_empleados AS empleados ON usuarios.empleado_id = empleados.empleado_id
                    WHERE roles.rol_id = :rol_id
                """
                
                paramametros = {"rol_id": rol_id}
                condiciones_adicionales = []
                
                if (cedula_empleado):
                    condiciones_adicionales.append("empleados.cedula = :cedula")
                    paramametros["cedula"] = cedula_empleado
                
                if (condiciones_adicionales):
                    consulta += " AND " + " AND ".join(condiciones_adicionales)
                
                usuarios = sesion.execute(text(consulta), paramametros).fetchall()
                
                if not (usuarios):
                    raise BaseDatosError("NO_HAY_USUARIOS_CON_ROL_O_CEDULA", "No hay usuarios con ese rol o cédula registrados.")
                
                return usuarios
        except BaseDatosError as error:
            raise error
        except Exception as error:
            print(f"ERROR AL OBTENER USUARIOS POR EL ROL Y/O CÉDULA: {error}")
    
    def actualizar(self, usuario_id: int, campos_usuario: Dict) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                usuario = sesion.query(Usuario).filter(Usuario.usuario_id == usuario_id).first()
                USUARIO_ID = app_configuracion.USUARIO_ID
                diccionario_usuario = {campo: valor for campo, valor in vars(usuario).items() if not(campo.startswith("_")) and not(campo == "usuario_id") and not(campo == "empleado_id")}
                
                campos = {
                    "rol_id": "ROL DEL USUARIO",
                    "nombre_usuario": "NOMBRE DE USUARIO",
                    "clave_usuario": "CLAVE DE USUARIO"
                }
                
                for clave in diccionario_usuario.keys():
                    if not(campos_usuario.get(clave) == diccionario_usuario.get(clave)):
                        campo_actualizado = campos.get(clave)
                        
                        valor_campo_anterior = diccionario_usuario.get(clave)
                        valor_campo_actual = campos_usuario.get(clave)
                        
                        if ((usuario_id == USUARIO_ID) and clave == "rol_id"):
                            raise BaseDatosError("CAMBIAR_ROL_PROPIO", "No puedes cambiar tu propio rol")
                        
                        if (usuario.rol == "DIRECTOR"):
                            raise BaseDatosError("CAMBIAR_ROL_DIRECTOR", "No puedes cambiarle el rol a un DIRECTOR")
                        
                        if not(clave == "clave_usuario"):
                            accion = f"ACTUALIZÓ EL CAMPO: {campo_actualizado}. ANTES: {valor_campo_anterior}. AHORA: {valor_campo_actual}. NOMBRE DE USUARIO AFECTADO: {usuario.nombre_usuario}"
                            auditoria_repositorio.registrar(self.entidad, accion)
                        
                        sesion.query(Usuario).filter(Usuario.usuario_id == usuario_id).update({clave: valor_campo_actual})
                        sesion.commit()
                        print(f"Se actualizó el campo: {campo_actualizado} correctamente")
        except BaseDatosError as error:
            sesion.rollback()
            raise error
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL ACTUALIZAR LOS CAMPOS: {error}")
    
    def eliminar(self, usuario_id: int) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                usuario = sesion.query(Usuario).filter(Usuario.usuario_id == usuario_id).first()
                USUARIO_ID = app_configuracion.USUARIO_ID
                todos_usuarios = self.obtener_todos()
                contador_directores = 0
                
                if not(usuario):
                    raise BaseDatosError("USUARIO_NO_EXISTE", "Este usuario no existe")
                
                if ((usuario.rol.tipo_rol == "DIRECTOR") and (usuario_id != USUARIO_ID)):
                    raise BaseDatosError("ELIMINAR_DIRECTOR", "No se puede eliminar a los DIRECTORES")
                
                for cada_usuario in todos_usuarios:
                    if (cada_usuario[5] == "DIRECTOR"):
                        contador_directores += 1
                
                if ((usuario_id == USUARIO_ID) and (contador_directores == 1)):
                    raise BaseDatosError("UNICO_DIRECTOR", "Primero tienes que designarle a otro empleado el rol de DIRECTOR")
                
                (cedula,) = sesion.execute(text("SELECT cedula FROM tb_empleados WHERE empleado_id = :empleado_id;"),
                {"empleado_id": usuario.empleado_id}).fetchone()
                
                (rol,) = sesion.execute(text("SELECT tipo_rol FROM tb_roles WHERE rol_id = :rol_id;"),
                {"rol_id": usuario.rol_id}).fetchone()
                
                accion = f"ELIMINÓ A: {usuario.nombre_usuario}. CÉDULA DEL EMPLEADO: {cedula}. ROL: {rol}"
                
                auditoria_repositorio.registrar(self.entidad, accion)
                
                sesion.delete(usuario)
                sesion.commit()
                print("Se eliminó el usuario correctamente")
        except BaseDatosError as error:
            sesion.rollback()
            raise error
        except Exception as error:
            sesion.rollback()
            print(f"Error al eliminar el usuario: {error}")
    
    def autenticar(self, nombre_usuario_ingresado: str, clave_usuario_ingresado: str) -> Optional[int]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                usuario = sesion.query(Usuario).filter(
                    Usuario.nombre_usuario == nombre_usuario_ingresado,
                    Usuario.clave_usuario == clave_usuario_ingresado
                ).first()
                
                if not(usuario):
                    raise BaseDatosError("SESION_FALLIDA", "El usuario y/o contraseña son incorrectos")
                
                print("Sesión iniciada correctamente")
                
                return usuario.usuario_id
        except BaseDatosError as error:
            raise error
        except Exception as error:
            print(f"Error al autenticar al usuario: {error}")


if __name__ == "__main__":
    usuario = UsuarioRepositorio()
    
    campos_usuario = {
        "empleado_id": 5,
        "rol_id": 3,
        "nombre_usuario": "gabriel1",
        "clave_usuario": "1234567"
    }
    
    #usuario.registrar(campos_usuario)
    
    #print(usuario.obtener_todos())
    #print(usuario.obtener_por_id(1))
    #print(usuario.obtener_por_nombre_usuario("douglas345"))
    
    #USUARIO_ID = usuario.autenticar("douglas345", "1234")
    #print(f"ID del usuario: {USUARIO_ID}")
    
    #usuario.eliminar(2)
    
    #print(usuario.obtener_por_id(2))