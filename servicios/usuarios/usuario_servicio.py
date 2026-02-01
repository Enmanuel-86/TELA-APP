import re
from typing import List, Tuple, Optional, Dict
from excepciones.base_datos_error import BaseDatosError
from repositorios.usuarios.usuario_repositorio import UsuarioRepositorio
from repositorios.repositorio_base import RepositorioBase


class UsuarioServicio:
    def __init__(self, repositorio: RepositorioBase):
        self.repositorio = repositorio
    
    def validar_empleado_id(self, empleado_id: int, usuario_id: Optional[int] = None) -> List[str]:
        errores = []
        usuario_a_actualizar = None
        
        if not(empleado_id):
            errores.append("Empleado asociado: El usuario tiene que asignarse a un empleado.")
        
        if (usuario_id):
            usuario_a_actualizar = self.repositorio.obtener_por_id(usuario_id)
            
            try:
                usuario_ya_existe = self.obtener_usuario_por_empleado_id(empleado_id)
                
                if (usuario_ya_existe):
                    id_usuario_existente = usuario_ya_existe[0]
                    id_usuario_a_actualizar = usuario_a_actualizar[0]
                    
                    if((usuario_id is None) or (id_usuario_existente != id_usuario_a_actualizar)):
                        errores.append("Empleado asociado: Este empleado ya tiene un usuario")
            except BaseDatosError:
                pass
            
        return errores
    
    def validar_rol_id(self, rol_id: int) -> List[str]:
        errores = []
        
        if not(rol_id):
            errores.append("Rol del usuario: Al usuario tiene que asignarle un rol.")
            
        return errores
    
    def validar_nombre_usuario(self, nombre_usuario: str, usuario_id: Optional[int] = None) -> List[str]:
        errores = []
        
        if (not(nombre_usuario)):
            errores.append("Nombre de usuario: No puede estar vacío.")
        elif (nombre_usuario):
            nombre_usuario_sin_espacios = nombre_usuario.replace(" ", "")
            usuario_a_actualizar = None
            contiene_espacios = re.search(r"\s", nombre_usuario)
            
            if (usuario_id):
                usuario_a_actualizar = self.repositorio.obtener_por_id(usuario_id)
            
            try:
                usuario_ya_existe = self.obtener_usuario_por_nombre_usuario(nombre_usuario)
                
                if (usuario_ya_existe):
                    id_usuario_existente = usuario_ya_existe[0]
                    id_usuario_a_actualizar = usuario_a_actualizar[0]
                    
                    if ((usuario_id is None) or (id_usuario_existente != id_usuario_a_actualizar)):
                        errores.append("Nombre de usuario: Este nombre de usuario ya existe.")
            except BaseDatosError:
                pass
            
            if (len(nombre_usuario_sin_espacios) == 0):
                errores.append("Nombre de usuario: No puede estar vacío.")
        
            if (contiene_espacios):
                errores.append("Nombre de usuario: No debe contener espacios.")
            
            if ((len(nombre_usuario) < 6) or (len(nombre_usuario) > 10)):
                errores.append("Nombre de usuario: Debe contener como mínimo 6 caracteres y máximo 10.")
            
        return errores
    
    def validar_clave_usuario(self, clave_usuario: str) -> List[str]:
        errores = []
        
        if (not(clave_usuario)):
            errores.append("Clave de usuario: No puede estar vacío.")
        elif (clave_usuario):
            clave_usuario_sin_espacios = clave_usuario.replace(" ", "")
            contiene_espacios = re.search(r"\s", clave_usuario)
            if (len(clave_usuario_sin_espacios) == 0):
                errores.append("Clave de usuario: No puede estar vacío.")
        
            if (contiene_espacios):
                errores.append("Clave de usuario: No debe contener espacios.")
            
            if ((len(clave_usuario) < 6) or (len(clave_usuario) > 12)):
                errores.append("Clave de usuario: Debe contener como mínimo 6 caracteres y máximo 12.")
        
        return errores
    
    def validar_campos_usuario(self, empleado_id: int, rol_id: int, nombre_usuario: str, clave_usuario: str, usuario_id: Optional[int] = None) -> List[str]:
        error_empleado_id = self.validar_empleado_id(empleado_id, usuario_id)
        error_rol_id = self.validar_rol_id(rol_id)
        error_nombre_usuario = self.validar_nombre_usuario(nombre_usuario, usuario_id)
        error_clave_usuario = self.validar_clave_usuario(clave_usuario)
        
        errores_totales = error_empleado_id + error_rol_id + error_nombre_usuario + error_clave_usuario
        
        return errores_totales
    
    def registrar_usuario(self, campos: Dict) -> None:
        self.repositorio.registrar(campos)
    
    def obtener_todos_usuarios(self) -> List[Tuple]:
        return self.repositorio.obtener_todos()
    
    def obtener_usuario_por_id(self, usuario_id: int) -> Optional[Tuple]:
        try:
            return self.repositorio.obtener_por_id(usuario_id)
        except BaseDatosError as error:
            raise error
    
    def obtener_usuario_por_empleado_id(self, empleado_id: int) -> Optional[Tuple]:
        return self.repositorio.obtener_por_empleado_id(empleado_id)
    
    def obtener_usuario_por_nombre_usuario(self, nombre_usuario: str) -> Optional[Tuple]:
        return self.repositorio.obtener_por_nombre_usuario(nombre_usuario)
    
    def obtener_usuario_por_rol_o_cedula_empleado(self, rol_id: int, cedula_empleado: Optional[str] = None) -> Optional[List[Tuple]]:
        try:
            return self.repositorio.obtener_por_rol_o_cedula_empleado(rol_id, cedula_empleado)
        except BaseDatosError as error:
            raise error
    
    def actualizar_usuario(self, usuario_id: int, campos_usuario: Dict) -> None:
        self.repositorio.actualizar(usuario_id, campos_usuario)
    
    def eliminar_usuario(self, usuario_id: int) -> None:
        try:
            self.repositorio.eliminar(usuario_id)
        except BaseDatosError as error:
            raise error
    
    def autenticar_usuario(self, nombre_usuario_ingresado: str, clave_usuario_ingresado: str) -> Optional[int]:
        try:
            return self.repositorio.autenticar(nombre_usuario_ingresado, clave_usuario_ingresado)
        except BaseDatosError as error:
            raise error


if __name__ == "__main__":
    usuario_repositorio = UsuarioRepositorio()
    usuario_servicio = UsuarioServicio(usuario_repositorio)
    
    
    """empleado_id = int(input("- Ingrese el ID del empleado: "))
    rol_id = int(input("- Ingrese el ID del rol: "))
    nombre_usuario = input("- Ingrese el nombre de usuario: ")
    clave_usuario = input("- Ingrese la clave de usuario: ")
    
    campos_usuario = {
        "empleado_id": empleado_id,
        "rol_id": rol_id,
        "nombre_usuario": nombre_usuario,
        "clave_usuario": clave_usuario
    }
    
    errores_totales = usuario_servicio.validar_campos_usuario(empleado_id, rol_id, nombre_usuario, clave_usuario)
    
    if errores_totales:
        print("\n".join(errores_totales))
    else:
        usuario_servicio.registrar_usuario(campos_usuario)"""
    
    """print(usuario_servicio.obtener_usuario_por_empleado_id(1))
    print(usuario_servicio.obtener_usuario_por_empleado_id(2))
    print(usuario_servicio.obtener_usuario_por_empleado_id(3))
    
    #No existe
    print(usuario_servicio.obtener_usuario_por_empleado_id(4))"""
    
    #print(usuario_servicio.eliminar_usuario(2))
    
    """nombre_usuario = input("- Ingrese el nombre de usuario: ")
    clave_usuario = input("- Ingrese su clave de usuario: ")
    usuario_autenticado = usuario_servicio.autenticar_usuario(nombre_usuario, clave_usuario)"""
    
    #usuario_servicio.eliminar_usuario(1)
    
    campos_usuario_actualizar = {
        "rol_id": 1,
        "nombre_usuario": "douglas345",
        "clave_usuario": "123456"
    }
    
    empleado_id = 3
    usuario_id = 1
    
    errores = usuario_servicio.validar_campos_usuario(
        empleado_id,
        campos_usuario_actualizar.get("rol_id"),
        campos_usuario_actualizar.get("nombre_usuario"),
        campos_usuario_actualizar.get("clave_usuario"),
        usuario_id
    )
    
    if (errores):
        print("\n".join(errores))
    else:
        print("INFO DEL USUARIO VALIDADA CORRECTAMENTE")