from typing import Tuple, List, Optional, Dict
from repositorios.repositorio_base import RepositorioBase
from excepciones.base_datos_error import BaseDatosError
from modelos import Diagnostico
from repositorios.usuarios.auditoria_repositorio import auditoria_repositorio
from repositorios.repositorio_base import RepositorioBase
from conexiones.conexion import conexion_bd


class DiagnosticoRepositorio(RepositorioBase):
    def __init__(self):
        self.conexion_bd = conexion_bd
        self.entidad = "DIAGNÓSTICOS"
    
    def registrar(self, campos: Dict) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                nuevo_diagnostico = Diagnostico(**campos)
                
                diagnostico = campos.get("diagnostico")
                
                sesion.add(nuevo_diagnostico)
                sesion.commit()
                sesion.refresh(nuevo_diagnostico)
                print("Se registró el diagnóstico correctamente")
                
                accion = f"REGISTRÓ EL DIAGNÓSTICO {diagnostico}"
                
                auditoria_repositorio.registrar(self.entidad, accion)
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL REGISTRAR EL DIAGNÓSTICO: {error}")
    
    def obtener_todos(self) -> List[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                diagnosticos = sesion.query(Diagnostico.diagnostico_id, Diagnostico.diagnostico).all()
                return diagnosticos
        except Exception as error:
            print(f"ERROR AL OBTENER LOS DIAGNÓSTICOS: {error}")
    
    def obtener_por_id(self, diagnostico_id: int) -> Optional[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                diagnostico = sesion.query(Diagnostico.diagnostico_id, Diagnostico.diagnostico).filter(Diagnostico.diagnostico_id == diagnostico_id).first()
                
                if not(diagnostico):
                    raise BaseDatosError("DIAGNOSTICO_NO_EXISTE", "Este diagnóstico no existe")
                
                return diagnostico
        except BaseDatosError as error:
            raise error
        except Exception as error:
            print(f"ERROR AL OBTENER EL DIAGNÓSTICO: {error}")
    
    def actualizar(self, diagnostico_id: int, campos_diagnostico: Dict) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                diagnostico = sesion.query(Diagnostico).filter(Diagnostico.diagnostico_id == diagnostico_id).first()
                diccionario_diagnostico = {campo: valor for campo, valor in vars(diagnostico).items() if not(campo.startswith("_")) and not(campo == "diagnostico_id")}
                
                campos = {
                    "diagnostico": "DIAGNÓSTICO"
                }
                
                for clave in diccionario_diagnostico.keys():
                    if not(campos_diagnostico.get(clave) == diccionario_diagnostico.get(clave)):
                        campo_actualizado = campos.get(clave)
                        
                        valor_campo_anterior = diccionario_diagnostico.get(clave)
                        valor_campo_actual = campos_diagnostico.get(clave)
                        
                        accion = f"ACTUALIZÓ EL CAMPO: {campo_actualizado}. ANTES: {valor_campo_anterior}. AHORA: {valor_campo_actual}"
                        auditoria_repositorio.registrar(self.entidad, accion)
                        
                        sesion.query(Diagnostico).filter(Diagnostico.diagnostico_id == diagnostico_id).update({clave: valor_campo_actual})
                        sesion.commit()
                        print(f"Se actualizó el campo: {campo_actualizado} correctamente \n")
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL ACTUALIZAR LOS CAMPOS: {error}")
    
    def eliminar(self, diagnostico_id: int) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                diagnostico = sesion.query(Diagnostico).filter(Diagnostico.diagnostico_id == diagnostico_id).first()
                
                if not(diagnostico):
                    raise BaseDatosError("DIAGNOSTICO_NO_EXISTE", "Este diagnóstico no existe")
                
                info_clinica_empleado_asociado = diagnostico.info_clinica_empleado
                info_clinica_alumno_asociado = diagnostico.info_clinica_alumno
                
                if info_clinica_empleado_asociado:
                    raise BaseDatosError("INFO_CLINICA_EMPLEADO_ASOCIADO", "Este diagnóstico está asociado a la información clínica de 1 o varios empleados y no puede ser eliminado")
                
                if info_clinica_alumno_asociado:
                    raise BaseDatosError("INFO_CLINICA_ALUMNO_ASOCIADO", "Este diagnóstico está asociado a la información clínica de 1 o varios alumnos y no puede ser eliminado")
                
                accion = f"ELIMINÓ EL DIAGNÓSTICO DE {diagnostico.diagnostico}"
                
                auditoria_repositorio.registrar(self.entidad, accion)
                
                sesion.delete(diagnostico)
                sesion.commit()
                print("Se eliminó el diagnóstico correctamente")
        except BaseDatosError as error:
            sesion.rollback()
            raise error
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL ELIMINAR EL DIAGNÓSTICO: {error}")


if __name__ == "__main__":
    diagnostico_repositorio = DiagnosticoRepositorio()
    
    campos_diagnostico = {"diagnostico": "ESQUIZOFRENIA"}
    
    #diagnostico_repositorio.registrar(campos_diagnostico)
    
    """todos_diagnosticos=  diagnostico_repositorio.obtener_todos()
    
    for diagnostico in todos_diagnosticos:
        print(diagnostico)"""
    
    """diagnostico = diagnostico_repositorio.obtener_por_id(3)
    
    if diagnostico is not(None):
        print(diagnostico)"""
    
    #diagnostico_repositorio.eliminar(4)