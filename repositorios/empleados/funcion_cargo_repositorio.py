from typing import Tuple, List, Optional, Dict
from excepciones.base_datos_error import BaseDatosError
from modelos import FuncionCargo
from repositorios.usuarios.auditoria_repositorio import auditoria_repositorio
from repositorios.repositorio_base import RepositorioBase
from conexiones.conexion import conexion_bd


class FuncionCargoRepositorio(RepositorioBase):
    def __init__(self):
        self.conexion_bd = conexion_bd
        self.entidad = "FUNCIONES DEL CARGO"
    
    def registrar(self, campos: Dict) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                nueva_funcion_cargo = FuncionCargo(**campos)
                
                funcion_cargo = campos.get("funcion_cargo")
                
                sesion.add(nueva_funcion_cargo)
                sesion.commit()
                sesion.refresh(nueva_funcion_cargo)
                print("Se registró la función del cargo correctamente")
                
                accion = f"REGISTRÓ LA FUNCIÓN DEL CARGO DE {funcion_cargo}"
                
                auditoria_repositorio.registrar(self.entidad, accion)
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL REGISTRAR LA FUNCIÓN DEL CARGO: {error}")
    
    def obtener_todos(self) -> List[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                funciones_cargo = sesion.query(FuncionCargo.funcion_cargo_id, FuncionCargo.funcion_cargo).all()
                return funciones_cargo
        except Exception as error:
            print(f"ERROR AL OBTENER LAS FUNCIONES DEL CARGO: {error}")
    
    def obtener_por_id(self, funcion_cargo_id: int) -> Optional[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                funcion_cargo = sesion.query(
                    FuncionCargo.funcion_cargo_id,
                    FuncionCargo.funcion_cargo
                ).filter_by(funcion_cargo_id = funcion_cargo_id).first()
                
                if not(funcion_cargo):
                    raise BaseDatosError("FUNCION_CARGO_NO_EXISTE", "Esta función del cargo no existe")
                
                return funcion_cargo
        except BaseDatosError as error:
            raise error
        except Exception as error:
            print(f"ERROR AL OBTENER LA FUNCIÓN DEL CARGO: {error}")
    
    def actualizar(self, funcion_cargo_id: int, campos_funcion_cargo: Dict) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                funcion_cargo = sesion.query(FuncionCargo).filter(FuncionCargo.funcion_cargo_id == funcion_cargo_id).first()
                diccionario_funcion_cargo = {campo: valor for campo, valor in vars(funcion_cargo).items() if not(campo.startswith("_")) and not(campo == "funcion_cargo_id")}
                
                campos = {
                    "funcion_cargo": "FUNCIÓN DEL CARGO"
                }
                
                for clave in diccionario_funcion_cargo.keys():
                    if not(campos_funcion_cargo.get(clave) == diccionario_funcion_cargo.get(clave)):
                        campo_actualizado = campos.get(clave)
                        
                        valor_campo_anterior = diccionario_funcion_cargo.get(clave)
                        valor_campo_actual = campos_funcion_cargo.get(clave)
                        
                        accion = f"ACTUALIZÓ EL CAMPO: {campo_actualizado}. ANTES: {valor_campo_anterior}. AHORA: {valor_campo_actual}. FUNCIÓN DEL CARGO AFECTADO: {funcion_cargo.funcion_cargo}"
                        auditoria_repositorio.registrar(self.entidad, accion)
                        
                        sesion.query(FuncionCargo).filter(FuncionCargo.funcion_cargo_id == funcion_cargo_id).update({clave: valor_campo_actual})
                        sesion.commit()
                        print(f"Se actualizó el campo: {campo_actualizado} correctamente \n")
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL ACTUALIZAR LOS CAMPOS: {error}")
    
    def eliminar(self, funcion_cargo_id: int) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                funcion_cargo = sesion.query(FuncionCargo).filter(FuncionCargo.funcion_cargo_id == funcion_cargo_id).first()
                
                if not(funcion_cargo):
                    raise BaseDatosError("FUNCION_CARGO_NO_EXISTE", "Esta función del cargo no existe")
                
                detalle_cargo_asociado = funcion_cargo.detalle_cargo
                
                if detalle_cargo_asociado:
                    raise BaseDatosError("DETALLE_CARGO_ASOCIADO", "Esta función del cargo está asociada a 1 o más empleados y no puede ser eliminado")
                
                accion = f"ELIMINÓ LA FUNCIÓN DEL CARGO DE {funcion_cargo.funcion_cargo}"
                
                auditoria_repositorio.registrar(self.entidad, accion)
                
                sesion.delete(funcion_cargo)
                sesion.commit()
                print("Se eliminó la función del cargo correctamente")
        except BaseDatosError as error:
            sesion.rollback()
            raise error
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL ELIMINAR LA FUNCIÓN DEL CARGO: {error}")


if __name__ == "__main__":
    funcion_cargo_repositorio = FuncionCargoRepositorio()
    
    campos_funcion_cargo = {"funcion_cargo": "SECRETARIO"}
    
    #funcion_cargo_repositorio.registrar(campos_funcion_cargo)
    
    """todas_funciones_cargo = funcion_cargo_repositorio.obtener_todos()
    
    for funcion_cargo in todas_funciones_cargo:
        print(funcion_cargo)"""
    
    #print(funcion_cargo_repositorio.obtener_por_id(1))
    
    #funcion_cargo_repositorio.eliminar(9)
    #funcion_cargo_repositorio.eliminar(1)
    #funcion_cargo_repositorio.eliminar(2)