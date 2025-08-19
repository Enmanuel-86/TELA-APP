from typing import Tuple, List, Optional, Dict
from datetime import time
from excepciones.base_datos_error import BaseDatosError
from modelos import TipoCargo
from repositorios.usuarios.auditoria_repositorio import auditoria_repositorio
from repositorios.repositorio_base import RepositorioBase
from conexiones.conexion import conexion_bd


class TipoCargoRepositorio(RepositorioBase):
    def __init__(self):
        self.conexion_bd = conexion_bd
        self.entidad = "TIPOS DE CARGO"
    
    def registrar(self, campos: Dict) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                nuevo_tipo_cargo = TipoCargo(**campos)
                
                tipo_cargo = campos.get("tipo_cargo")
                
                sesion.add(nuevo_tipo_cargo)
                sesion.commit()
                sesion.refresh(nuevo_tipo_cargo)
                print("Se registró el nuevo tipo de cargo correctamente")
                
                accion = f"REGISTRÓ EL TIPO DE CARGO: {tipo_cargo}"
                
                auditoria_repositorio.registrar(self.entidad, accion)
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL REGISTRAR EL TIPO DE CARGO {error}")
    
    def obtener_todos(self) -> List[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                tipos_cargo = sesion.query(TipoCargo.tipo_cargo_id, TipoCargo.tipo_cargo).all()
                return tipos_cargo
        except Exception as error:
            print(f"ERROR AL OBTENER TODOS LOS TIPOS DE CARGO: {error}")
    
    def obtener_por_id(self, tipo_cargo_id: int) -> Optional[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                tipo_cargo = sesion.query(
                    TipoCargo.tipo_cargo_id,
                    TipoCargo.tipo_cargo,
                    TipoCargo.horario_llegada
                ).filter_by(tipo_cargo_id = tipo_cargo_id).first()
                
                if not(tipo_cargo):
                    raise BaseDatosError("TIPO_CARGO_NO_EXISTE", "Este tipo de cargo no existe")
                
                return tipo_cargo
        except BaseDatosError as error:
            raise error
        except Exception as error:
            print(f"ERROR AL OBTENER EL TIPO DE CARGO: {error}")
    
    def actualizar(self, tipo_cargo_id: int, campos_tipo_cargo: Dict) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                tipo_cargo = sesion.query(TipoCargo).filter(TipoCargo.tipo_cargo_id == tipo_cargo_id).first()
                diccionario_tipo_cargo = {campo: valor for campo, valor in vars(tipo_cargo).items() if not(campo.startswith("_")) and not(campo == "tipo_cargo_id")}
                
                campos = {
                    "tipo_cargo": "TIPO DE CARGO",
                    "horario_llegada": "HORARIO DE LLEGADA"
                }
                
                for clave in diccionario_tipo_cargo.keys():
                    if not(campos_tipo_cargo.get(clave) == diccionario_tipo_cargo.get(clave)):
                        campo_actualizado = campos.get(clave)
                        
                        valor_campo_anterior = diccionario_tipo_cargo.get(clave)
                        valor_campo_actual = campos_tipo_cargo.get(clave)
                        
                        accion = f"ACTUALIZÓ EL CAMPO: {campo_actualizado}. ANTES: {valor_campo_anterior}. AHORA: {valor_campo_actual}. TIPO DE CARGO AFECTADO: {tipo_cargo.tipo_cargo}"
                        auditoria_repositorio.registrar(self.entidad, accion)
                        
                        sesion.query(TipoCargo).filter(TipoCargo.tipo_cargo_id == tipo_cargo_id).update({clave: valor_campo_actual})
                        sesion.commit()
                        print(f"Se actualizó el campo {campo_actualizado} correctamente \n")
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL ACTUALIZAR LOS CAMPOS: {error}")
    
    def eliminar(self, tipo_cargo_id: int) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                tipo_cargo = sesion.query(TipoCargo).filter(TipoCargo.tipo_cargo_id == tipo_cargo_id).first()
                
                if not(tipo_cargo):
                    raise BaseDatosError("TIPO_CARGO_NO_EXISTE", "Este tipo de cargo no existe")
                
                detalle_cargo_asociado = tipo_cargo.detalle_cargo
                
                if detalle_cargo_asociado:
                    raise BaseDatosError("DETALLE_CARGO_ASOCIADO", "Este tipo de cargo está asociado a 1 o varios empleados y no puede ser eliminado")
                
                accion = f"ELIMINÓ EL TIPO DE CARGO {tipo_cargo.tipo_cargo}"
                
                auditoria_repositorio.registrar(self.entidad, accion)
                
                sesion.delete(tipo_cargo)
                sesion.commit()
                print("Se eliminó el tipo de cargo correctamente")
        except BaseDatosError as error:
            sesion.rollback()
            raise error
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL ELIMINAR EL TIPO DE CARGO: {error}")


if __name__ == "__main__":
    tipo_cargo_repositorio = TipoCargoRepositorio()
    
    """campos_tipo_cargo = {
        "tipo_cargo": "DOCENTE",
        "horario_llegada": time(9, 0)
    }
    
    tipo_cargo_repositorio.registrar(campos_tipo_cargo)"""
    
    """todos_tipos_cargo = tipo_cargo_repositorio.obtener_todos()
    
    for tipo_cargo in todos_tipos_cargo:
        print(f"TIPO DE CARGO: {tipo_cargo[0]}. HORARIO LLEGADA: {tipo_cargo[1]}")"""
    
    """tipo_cargo = tipo_cargo_repositorio.obtener_por_id(1)[0]
    horario_llegada = tipo_cargo_repositorio.obtener_por_id(1)[1].strftime("%H:%M:%S")
    
    print(f"TIPO DE CARGO: {tipo_cargo}. HORARIO LLEGADA: {horario_llegada}")"""
    
    #tipo_cargo_repositorio.eliminar(1)
    #tipo_cargo_repositorio.eliminar(2)