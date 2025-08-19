from typing import Tuple, List, Optional, Dict
from sqlalchemy import text
from repositorios.repositorio_base import RepositorioBase
from excepciones.base_datos_error import BaseDatosError
from modelos import InfoBancariaAlumno, Alumno, Inscripcion
from repositorios.usuarios.auditoria_repositorio import auditoria_repositorio
from conexiones.conexion import conexion_bd


class InfoBancarioAlumnoRepositorio(RepositorioBase):
    def __init__(self):
        self.conexion_bd = conexion_bd
        self.entidad = "INFO BANCARIA DE ALUMNOS"
    
    def registrar(self, campos: Dict) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                nuevo_info_bancaria_alumno = InfoBancariaAlumno(**campos)
                
                sesion.add(nuevo_info_bancaria_alumno)
                sesion.commit()
                sesion.refresh(nuevo_info_bancaria_alumno)
                print("Se registró la info bancaria del alumno correctamente")
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL REGISTRAR LA INFO BANCARIA DEL ALUMNO: {error}")
    
    def obtener_todos(self) -> List[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                info_bancaria_alumnos = sesion.query(
                    InfoBancariaAlumno.info_banc_alumno_id,
                    Alumno.alumno_id,
                    InfoBancariaAlumno.tipo_cuenta,
                    InfoBancariaAlumno.num_cuenta
                ).join(Alumno.info_bancaria_alumno).all()
                
                return info_bancaria_alumnos
        except Exception as error:
            print(f"ERROR AL OBTENER LAS INFO BANCARIA DE ALUMNOS: {error}")
    
    def obtener_por_id(self, info_banc_alumno_id: int) -> Optional[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                info_bancaria_alumno = sesion.query(
                    InfoBancariaAlumno.info_banc_alumno_id,
                    Alumno.alumno_id,
                    InfoBancariaAlumno.tipo_cuenta,
                    InfoBancariaAlumno.num_cuenta
                ).join(Alumno.info_bancaria_alumno).filter(InfoBancariaAlumno.info_banc_alumno_id == info_banc_alumno_id).first()
                
                if not(info_bancaria_alumno):
                    raise BaseDatosError("INFO_BANCARIA_ALUMNO_NO_EXISTE", "Este alumno no posee información bancaria")
                
                return info_bancaria_alumno
        except BaseDatosError as error:
            raise error
        except Exception as error:
            print(f"ERROR AL OBTENER LA INFO BANCARIA DE ALUMNO: {error}")
    
    def obtener_por_alumno_id(self, alumno_id: int) -> List[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                info_bancaria_alumno = sesion.query(
                    InfoBancariaAlumno.info_banc_alumno_id,
                    Alumno.alumno_id,
                    InfoBancariaAlumno.tipo_cuenta,
                    InfoBancariaAlumno.num_cuenta
                ).join(Alumno.info_bancaria_alumno).filter(InfoBancariaAlumno.alumno_id == alumno_id).all()
                
                if not(info_bancaria_alumno):
                    raise BaseDatosError("INFO_BANCARIA_ALUMNO_NO_EXISTE", "Este alumno no posee información bancaria")
                
                return info_bancaria_alumno
        except BaseDatosError as error:
            raise error
        except Exception as error:
            print(f"ERROR AL OBTENER LA INFO BANCARIA DE ALUMNO: {error}")
    
    def obtener_por_num_cuenta(self, num_cuenta: str) -> Optional[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                consulta = "SELECT 1 FROM tb_info_bancaria_alumnos WHERE num_cuenta = :num_cuenta;"
                info_bancaria_alumno = sesion.execute(text(consulta), {"num_cuenta": num_cuenta}).fetchone()
                return info_bancaria_alumno
        except Exception as error:
            print(f"ERROR AL OBTENER LA INFO BANCARIA DE ALUMNO: {error}")
    
    def actualizar(self, info_banc_alumno_id: int, campos_info_bancaria_alumno: Dict) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                info_bancaria_alumno = sesion.query(InfoBancariaAlumno).filter_by(info_banc_alumno_id = info_banc_alumno_id).first()
                alumno = sesion.query(Alumno).join(Alumno.info_bancaria_alumno).filter(InfoBancariaAlumno.info_banc_alumno_id == info_banc_alumno_id).first()
                alumno_id = alumno.alumno_id
                inscripcion_alumno = sesion.query(Inscripcion).filter(Inscripcion.alumno_id == alumno_id).first()
                diccionario_info_bancaria_alumno = {campo: valor for campo, valor in vars(info_bancaria_alumno).items() if not(campo.startswith("_")) and not(campo == "info_banc_alumno_id") and not(campo == "alumno_id")}
                
                campos = {
                    "tipo_cuenta": "TIPO DE CUENTA",
                    "num_cuenta": "NÚMERO DE CUENTA"
                }
                
                for clave in diccionario_info_bancaria_alumno.keys():
                    if not(campos_info_bancaria_alumno.get(clave) == diccionario_info_bancaria_alumno.get(clave)):
                        campo_actualizado = campos.get(clave)
                        
                        valor_campo_anterior = diccionario_info_bancaria_alumno.get(clave)
                        valor_campo_actual = campos_info_bancaria_alumno.get(clave)
                        
                        accion = f"ACTUALIZÓ EL CAMPO: {campo_actualizado}. ANTES: {valor_campo_anterior}. AHORA: {valor_campo_actual}. MATRICULA: {inscripcion_alumno.num_matricula}"
                        auditoria_repositorio.registrar(self.entidad, accion)
                        
                        sesion.query(InfoBancariaAlumno).filter_by(info_banc_alumno_id = info_banc_alumno_id).update({clave: valor_campo_actual})
                        sesion.commit()
                        print(f"Se actualizó el campo: {campo_actualizado} correctamente \n")
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL ACTUALIZAR LOS CAMPOS: {error}")
    
    def eliminar(self, info_banc_alumno_id: int) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                info_bancaria_alumno = sesion.query(InfoBancariaAlumno).filter_by(info_banc_alumno_id = info_banc_alumno_id).first()
                
                if not(info_bancaria_alumno):
                    raise BaseDatosError("INFO_BANCARIA_ALUMNO_NO_EXISTE", "Esta info bancaria del alumno no existe")
                
                inscripcion_alumno = sesion.query(Inscripcion).filter(Inscripcion.alumno_id == info_bancaria_alumno.alumno_id).first()
                
                accion = f"ELIMINÓ EL REGISTRO DEL TIPO DE CUENTA {info_bancaria_alumno.tipo_cuenta} Y NÚMERO DE CUENTA {info_bancaria_alumno.num_cuenta}. MATRICULA: {inscripcion_alumno.num_matricula}"
                auditoria_repositorio.registrar(self.entidad, accion)
                
                sesion.delete(info_bancaria_alumno)
                sesion.commit()
                print("Se eliminó la info bancaria de alumno correctamente")
        except BaseDatosError as error:
            sesion.rollback()
            raise error
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL ELIMINAR LA INFO BANCARIA DE ALUMNO: {error}")


if __name__ == "__main__":
    info_bancaria_alumno_repositorio = InfoBancarioAlumnoRepositorio()
    
    """campos_info_bancaria_alumno = {
        "alumno_id": 13,
        "tipo_cuenta": "CORRIENTE",
        "num_cuenta": "12367943"
    }
    
    info_bancaria_alumno_repositorio.registrar(campos_info_bancaria_alumno)"""
    
    """todos_info_bancaria_alumno_repositorio = info_bancaria_alumno_repositorio.obtener_todos()
    
    for registro in todos_info_bancaria_alumno_repositorio:
        print(registro)"""
    
    #print(info_bancaria_alumno_repositorio.obtener_por_id(2))
    
    """campos_info_bancaria_alumno = {
        "tipo_cuenta": "AHORRO",
        "num_cuenta": "123679673"
    }
    
    info_bancaria_alumno_repositorio.actualizar(2, campos_info_bancaria_alumno)"""
    
    #info_bancaria_alumno_repositorio.eliminar(2)
    
    #print(info_bancaria_alumno_repositorio.obtener_por_num_cuenta("010203045067"))
    
    """try:
        todos_info_bancaria = info_bancaria_alumno_repositorio.obtener_por_alumno_id(1)
        for registro in todos_info_bancaria:
            print(registro)
    except BaseDatosError as error:
        print(error)"""