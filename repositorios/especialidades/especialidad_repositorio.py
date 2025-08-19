from typing import Tuple, List, Optional, Dict
from excepciones.base_datos_error import BaseDatosError
from modelos import Especialidad
from repositorios.usuarios.auditoria_repositorio import auditoria_repositorio
from repositorios.repositorio_base import RepositorioBase
from conexiones.conexion import conexion_bd


class EspecialidadRepositorio(RepositorioBase):
    def __init__(self):
        self.conexion_bd = conexion_bd
        self.entidad = "ESPECIALIDADES"
    
    def registrar(self, campos: Dict) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                nueva_especialidad = Especialidad(**campos)
                
                especialidad = campos.get("especialidad")
                
                sesion.add(nueva_especialidad)
                sesion.commit()
                sesion.refresh(nueva_especialidad)
                print("Se registró la especialidad correctamente")
                
                accion = f"REGISTRÓ LA ESPECIALIDAD {especialidad}"
                
                auditoria_repositorio.registrar(self.entidad, accion)
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL REGISTRAR LA ESPECIALIDAD: {error}")
    
    def obtener_todos(self) -> List[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                especialidades = sesion.query(Especialidad.especialidad_id, Especialidad.especialidad).all()
                return especialidades
        except Exception as error:
            print(f"ERROR AL OBTENER LAS ESPECIALIDADES: {error}")
    
    def obtener_por_id(self, especialidad_id: int) -> Optional[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                especialidad = sesion.query(Especialidad.especialidad_id, Especialidad.especialidad).filter(Especialidad.especialidad_id == especialidad_id).first()
                
                if not(especialidad):
                    raise BaseDatosError("ESPECIALIDAD_NO_EXISTE", "Esta especialidad no existe")
                
                return especialidad
        except BaseDatosError as error:
            raise error
        except Exception as error:
            print(f"ERROR AL OBTENER LA ESPECIALIDAD: {error}")
    
    def actualizar(self, especialidad_id: int, campos_especialidad: Dict) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                especialidad = sesion.query(Especialidad).filter(Especialidad.especialidad_id == especialidad_id).first()
                diccionario_especialidad = {campo: valor for campo, valor in vars(especialidad) if not(campo.startswith("_")) and not(campo == "especialidad_id")}
                
                campos = {
                    "especialidad": "ESPECIALIDAD"
                }
                
                for clave in diccionario_especialidad.keys():
                    if not(campos_especialidad.get(clave) == diccionario_especialidad.get(clave)):
                        campo_actualizado = campos.get(clave)
                        
                        valor_campo_anterior = diccionario_especialidad.get(clave)
                        valor_campo_actual = campos_especialidad.get(clave)
                        
                        accion = f"ACTUALIZÓ EL CAMPO: {campo_actualizado}. ANTES: {valor_campo_anterior}. AHORA: {valor_campo_actual}"
                        auditoria_repositorio.registrar(self.entidad, accion)
                        
                        sesion.query(Especialidad).filter(Especialidad.especialidad_id == especialidad_id).update({clave: valor_campo_actual})
                        sesion.commit()
                        print(f"Se actualizó el campo: {campo_actualizado} correctamente \n")
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL ACTUALIZAR LOS CAMPOS: {error}")
    
    def eliminar(self, especialidad_id: int) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                especialidad = sesion.query(Especialidad).filter(Especialidad.especialidad_id == especialidad_id).first()
                
                if not(especialidad):
                    raise BaseDatosError("ESPECIALIDAD_NO_EXISTE", "Esta especialidad no existe")
                
                detalle_cargo_asociado = especialidad.detalle_cargo
                inscripcion_asociada = especialidad.inscripcion
                
                if detalle_cargo_asociado:
                    raise BaseDatosError("DETALLE_CARGO_ASOCIADO", "Esta especialidad está asociada a un empleado que la imparte y no puede ser eliminado")
                
                if inscripcion_asociada:
                    raise BaseDatosError("INSCRIPCION_ASOCIADA", "Esta especialidad están alumnos inscritos y no puede ser eliminado")
                
                accion = f"ELIMINÓ LA ESPECIALIDAD {especialidad.especialidad}"
                
                auditoria_repositorio.registrar(self.entidad, accion)
                
                sesion.delete(especialidad)
                sesion.commit()
                print("Se eliminó la especialidad correctamente")
        except BaseDatosError as error:
            sesion.rollback()
            raise error
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL ELIMINAR LA ESPECIALIDAD: {error}")


if __name__ == "__main__":
    especialidad_repositorio = EspecialidadRepositorio()
    
    campos_especialidad = {"especialidad": "CARPINTERIA"}
    
    #especialidad_repositorio.registrar(campos_carpinteria)
    
    """todas_especialidades = especialidad_repositorio.obtener_todos()
    
    for especialidad in todas_especialidades:
        print(especialidad)"""
    
    
    """especialidad = especialidad_repositorio.obtener_por_id(1)
    
    if especialidad is not(None):
        print(especialidad)"""
    
    #especialidad_repositorio.eliminar(1)
    #especialidad_repositorio.eliminar(2)