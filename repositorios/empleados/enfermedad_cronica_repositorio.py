from typing import Tuple, List, Optional, Dict
from excepciones.base_datos_error import BaseDatosError
from modelos import EnfermedadCronica
from repositorios.usuarios.auditoria_repositorio import auditoria_repositorio
from repositorios.repositorio_base import RepositorioBase
from conexiones.conexion import conexion_bd


class EnfermedadCronicaRepositorio(RepositorioBase):
    def __init__(self):
        self.conexion_bd = conexion_bd
        self.entidad = "ENFERMEDADES CRÓNICAS"
    
    def registrar(self, campos: Dict) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                nueva_enfermedad_cronica = EnfermedadCronica(**campos)
                
                enfermedad_cronica = campos.get("enfermedad_cronica")
                
                sesion.add(nueva_enfermedad_cronica)
                sesion.commit()
                sesion.refresh(nueva_enfermedad_cronica)
                print("Se registró la enfermedad crónica correctamente")
                
                accion = f"REGISTRÓ LA ENFERMEDAD CRÓNICA {enfermedad_cronica}"
                
                auditoria_repositorio.registrar(self.entidad, accion)
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL REGISTRAR LA ENFERMEDAD CRÓNICA: {error}")
    
    def obtener_todos(self) -> List[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                enfermedades_cronicas = sesion.query(EnfermedadCronica.enferm_cronica_id, EnfermedadCronica.enfermedad_cronica).all()
                return enfermedades_cronicas
        except Exception as error:
            print(f"ERROR AL OBTENER LAS ENFERMEDADES CRÓNICAS: {error}")
    
    def obtener_por_id(self, enferm_cronica_id: int) -> Optional[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                enfermedad_cronica = sesion.query(
                    EnfermedadCronica.enferm_cronica_id,
                    EnfermedadCronica.enfermedad_cronica
                ).filter_by(enferm_cronica_id = enferm_cronica_id).first()
                
                if not(enfermedad_cronica):
                    raise BaseDatosError("ENFERMEDAD_CRONICA_NO_EXISTE", "Esta enfermedad crónica no existe")
                
                return enfermedad_cronica
        except BaseDatosError as error:
            raise error
        except Exception as error:
            print(f"ERROR AL OBTENER LA ENFERMEDAD CRÓNICA: {error}")
    
    def actualizar(self, enferm_cronica_id: int, campos_enfermedad_cronica: Dict) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                enfermedad_cronica = sesion.query(EnfermedadCronica).filter(EnfermedadCronica.enferm_cronica_id == enferm_cronica_id).first()
                diccionario_enfermedad_cronica = {campo: valor for campo, valor in vars(enfermedad_cronica).items() if not(campo.startswith("_")) and not(campo == "enferm_cronica_id")}
                
                campos = {
                    "enfermedad_cronica": "ENFERMEDAD CRÓNICA"
                }
                
                for clave in diccionario_enfermedad_cronica.keys():
                    if not(campos_enfermedad_cronica.get(clave) == diccionario_enfermedad_cronica.get(clave)):
                        campo_actualizado = campos.get(clave)
                        
                        valor_campo_anterior = diccionario_enfermedad_cronica.get(clave)
                        valor_campo_actual = campos_enfermedad_cronica.get(clave)
                        
                        accion = f"ACTUALIZÓ EL CAMPO: {campo_actualizado}. ANTES: {valor_campo_anterior}. AHORA: {valor_campo_actual}"
                        auditoria_repositorio.registrar(self.entidad, accion)
                        
                        sesion.query(EnfermedadCronica).filter(EnfermedadCronica.enferm_cronica_id == enferm_cronica_id).update({clave: valor_campo_actual})
                        sesion.commit()
                        print(f"Se actualizó el campo: {campo_actualizado} correctamente \n")
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL ACTUALIZAR LOS CAMPOS: {error}")
    
    def eliminar(self, enferm_cronica_id: int) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                enfermedad_cronica = sesion.query(EnfermedadCronica).filter(EnfermedadCronica.enferm_cronica_id == enferm_cronica_id).first()
                
                if not(enfermedad_cronica):
                    raise BaseDatosError("ENFERMEDAD_CRONICA_NO_EXISTE", "Esta enfermedad crónica no existe")
                
                historial_enferm_cronica_asociado = enfermedad_cronica.historial_enfermedades
                
                if (historial_enferm_cronica_asociado):
                    raise BaseDatosError("HISTORIAL_ENFERM_CRONICA_ASOCIADO", "Esta enfermedad crónica está asociada a un historial de enfermedades de 1 o varios empleados y no puede ser eliminado.")
                
                accion = f"ELIMINÓ LA ENFERMEDAD CRÓNICA DE {enfermedad_cronica.enfermedad_cronica}"
                
                auditoria_repositorio.registrar(self.entidad, accion)
                
                sesion.delete(enfermedad_cronica)
                sesion.commit()
                print("Se eliminó la enfermedad crónica correctamente")
        except BaseDatosError as error:
            sesion.rollback()
            raise error
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL ELIMINAR LA ENFERMEDAD CRÓNICA: {error}")


if __name__ == "__main__":
    enfermedad_cronica_repositorio = EnfermedadCronicaRepositorio()
    
    """campos_enfermedad_cronica = {
        "enfermedad_cronica": "LUMBALGIA"
    }
    
    enfermedad_cronica_repositorio.registrar(campos_enfermedad_cronica)"""
    
    """todas_enfermedades_cronicas = enfermedad_cronica_repositorio.obtener_todos()
    
    for registro in todas_enfermedades_cronicas:
        print(registro)"""
    
    #print(enfermedad_cronica_repositorio.obtener_por_id(2))
    
    """campos_enfermedad_cronica = {
        "enfermedad_cronica": "ASMA"
    }
    
    enfermedad_cronica_repositorio.actualizar(3, campos_enfermedad_cronica)"""
    
    #enfermedad_cronica_repositorio.eliminar(40)
    #enfermedad_cronica_repositorio.eliminar(3)