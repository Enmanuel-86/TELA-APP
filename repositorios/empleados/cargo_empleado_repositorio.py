from typing import Tuple, List, Optional, Dict
from excepciones.base_datos_error import BaseDatosError
from modelos import CargoEmpleado
from repositorios.usuarios.auditoria_repositorio import auditoria_repositorio
from repositorios.repositorio_base import RepositorioBase
from conexiones.conexion import conexion_bd


class CargoEmpleadoRepositorio(RepositorioBase):
    def __init__(self):
        self.conexion_bd = conexion_bd
        self.entidad = "CARGOS"
    
    def registrar(self, campos: Dict) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                nuevo_cargo = CargoEmpleado(**campos)
                
                codigo_cargo = campos.get("codigo_cargo")
                cargo = campos.get("cargo")
                
                sesion.add(nuevo_cargo)
                sesion.commit()
                sesion.refresh(nuevo_cargo)
                print("Se registró el cargo del empleado correctamente")
                
                accion = f"REGISTRÓ EL CARGO DE {cargo}. CÓDIGO DE CARGO: {codigo_cargo}"
                
                auditoria_repositorio.registrar(self.entidad, accion)
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL REGISTRAR EL CARGO DEL EMPLEADO: {error}")
    
    def obtener_todos(self) -> List[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                cargos_empleados = sesion.query(CargoEmpleado.cargo_id, CargoEmpleado.codigo_cargo, CargoEmpleado.cargo).all()
                return cargos_empleados
        except Exception as error:
            print(f"ERROR AL OBTENER TODOS LOS CARGOS DE LOS EMPLEADOS: {error}")
    
    def obtener_por_id(self, cargo_id: int) -> Optional[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                cargo_empleado = sesion.query(
                    CargoEmpleado.cargo_id,
                    CargoEmpleado.codigo_cargo,
                    CargoEmpleado.cargo
                ).filter(CargoEmpleado.cargo_id == cargo_id).first()
                
                if not(cargo_empleado):
                    raise BaseDatosError("CARGO_EMPLEADO_NO_EXISTE", "Este cargo del empleado no existe")
                
                return cargo_empleado
        except BaseDatosError as error:
            raise error
        except Exception as error:
            print(f"ERROR AL OBTENER EL CARGO DEL EMPLEADO: {error}")
    
    def obtener_por_codigo_cargo(self, codigo_cargo: str) -> Optional[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                cargo_empleado = sesion.query(
                    CargoEmpleado.cargo_id,
                    CargoEmpleado.codigo_cargo,
                    CargoEmpleado.cargo
                ).filter(CargoEmpleado.codigo_cargo == codigo_cargo).first()
                
                return cargo_empleado
        except Exception as error:
            print(f"ERROR AL OBTENER EL CARGO DEL EMPLEADO: {error}")
    
    def actualizar(self, cargo_id: int, campos_cargo: Dict) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                cargo = sesion.query(CargoEmpleado).filter(CargoEmpleado.cargo_id == cargo_id).first()
                diccionario_cargo = {campo: valor for campo, valor in vars(cargo).items() if not(campo.startswith("_")) and not(campo == "cargo_id")}
                
                campos = {
                    "codigo_cargo": "CÓDIGO DE CARGO",
                    "cargo": "CARGO"
                }
                
                for clave in diccionario_cargo.keys():
                    if not(campos_cargo.get(clave) == diccionario_cargo.get(clave)):
                        campo_actualizado = campos.get(clave)
                        
                        valor_campo_anterior = diccionario_cargo.get(clave)
                        valor_campo_actual = campos_cargo.get(clave)
                        
                        codigo_cargo = cargo.codigo_cargo
                        
                        accion = f"ACTUALIZÓ EL CAMPO: {campo_actualizado}. ANTES: {valor_campo_anterior}. AHORA: {valor_campo_actual}. CÓDIGO DEL CARGO AFECTADO: {codigo_cargo}"
                        auditoria_repositorio.registrar(self.entidad, accion)
                        
                        sesion.query(CargoEmpleado).filter(CargoEmpleado.cargo_id == cargo_id).update({clave: valor_campo_actual})
                        sesion.commit()
                        print(f"Se actualizó el campo: {campo_actualizado} correctamente \n")
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL ACTUALIZAR LOS CAMPOS: {error}")
    
    def eliminar(self, cargo_id: int) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                cargo_empleado = sesion.query(CargoEmpleado).filter(CargoEmpleado.cargo_id == cargo_id).first()
                
                if not(cargo_empleado):
                    raise BaseDatosError("CARGO_EMPLEADO_NO_EXISTE", "Este cargo del empleado no existe")
                
                detalle_cargo_asociado = cargo_empleado.detalle_cargo
                
                if detalle_cargo_asociado:
                    raise BaseDatosError("DETALLE_CARGO_ASOCIADO", "Este cargo está asociado a 1 o varios empleados y no puede ser eliminado")
                
                accion = f"ELIMINÓ EL CARGO DE {cargo_empleado.cargo}. CÓDIGO DE CARGO: {cargo_empleado.codigo_cargo}"
                
                auditoria_repositorio.registrar(self.entidad, accion)
                
                sesion.delete(cargo_empleado)
                sesion.commit()
                print("Se eliminó el cargo correctamente")
        except BaseDatosError as error:
            sesion.rollback()
            raise error
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL ELIMINAR EL CARGO: {error}")


if __name__ == "__main__":
    cargo_empleado_repositorio = CargoEmpleadoRepositorio()
    
    campos_cargo_empleado = {
        "codigo_cargo": "10004",
        "cargo": "OBRERO"
    }
    
    #cargo_empleado_repositorio.registrar(campos_cargo_empleado)
    
    """todos_cargos = cargo_empleado_repositorio.obtener_todos()
    
    for cargo in todos_cargos:
        print(cargo)"""
    
    #print(cargo_empleado_repositorio.obtener_por_id(2))
    
    #Intentar eliminar un cargo que está asociado a 1 o varios empleados
    #cargo_empleado_repositorio.eliminar(1)
    
    #Eliminando un cargo que no está asociado a un empleado
    #cargo_empleado_repositorio.eliminar(3)