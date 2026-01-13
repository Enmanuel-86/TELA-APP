from typing import Tuple, List, Optional, Dict
from sqlalchemy import text
from excepciones.base_datos_error import BaseDatosError
from modelos import HistorialEnfermCronicas, EnfermedadCronica
from repositorios.usuarios.auditoria_repositorio import auditoria_repositorio
from repositorios.repositorio_base import RepositorioBase
from conexiones.conexion import conexion_bd


class HistorialEnfermCronicasRepositorio(RepositorioBase):
    def __init__(self):
        self.conexion_bd = conexion_bd
        self.entidad = "HISTORIAL ENFERMEDADES CRÓNICAS"
    
    def registrar(self, campos: Dict) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                nuevo_historial_enferm_cronica = HistorialEnfermCronicas(**campos)
                
                sesion.add(nuevo_historial_enferm_cronica)
                sesion.commit()
                sesion.refresh(nuevo_historial_enferm_cronica)
                print("Se registró la enfermedad crónica al historial del empleado correctamente")
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL REGISTRAR LA ENFERMEDAD CRÓNICA AL HISTORIAL DEL EMPLEADO: {error}")
    
    def obtener_todos(self) -> List[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                historial_enfermedades_cronicas = sesion.execute(text(
                    """
                        SELECT
                            historial_enferm_cronicas.hist_enferm_cronica_id,
                            empleados.empleado_id,
                            enfermedades_cronicas.enfermedad_cronica
                        FROM tb_historial_enferm_cronicas AS historial_enferm_cronicas
                        INNER JOIN tb_empleados AS empleados ON historial_enferm_cronicas.empleado_id = empleados.empleado_id
                        INNER JOIN tb_enfermedades_cronicas AS enfermedades_cronicas ON historial_enferm_cronicas.enferm_cronica_id = enfermedades_cronicas.enferm_cronica_id;
                    """
                )).fetchall()
                
                return historial_enfermedades_cronicas
        except Exception as error:
            print(f"ERROR AL OBTENER EL HISTORIAL DE ENFERMEDADES CRÓNICAS DE LOS EMPLEADOS: {error}")
    
    def obtener_por_id(self, hist_enferm_cronica_id: int) -> Optional[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                historial_enfermedad_cronica = sesion.execute(text(
                    """
                        SELECT
                            historial_enferm_cronicas.hist_enferm_cronica_id,
                            empleados.empleado_id,
                            enfermedades_cronicas.enfermedad_cronica
                        FROM tb_historial_enferm_cronicas AS historial_enferm_cronicas
                        INNER JOIN tb_empleados AS empleados ON historial_enferm_cronicas.empleado_id = empleados.empleado_id
                        INNER JOIN tb_enfermedades_cronicas AS enfermedades_cronicas ON historial_enferm_cronicas.enferm_cronica_id = enfermedades_cronicas.enferm_cronica_id
                        WHERE historial_enferm_cronicas.hist_enferm_cronica_id = :hist_enferm_cronica_id;
                    """
                ), {"hist_enferm_cronica_id": hist_enferm_cronica_id}).fetchone()
                
                if not(historial_enfermedad_cronica):
                    raise BaseDatosError("HISTORIAL_ENFERM_CRONICA_NO_EXISTE", "No está la enfermedad crónica registrada en el historial")
                
                return historial_enfermedad_cronica
        except BaseDatosError as error:
            raise error
        except Exception as error:
            print(f"ERROR AL OBTENER EL HISTORIAL DE ENFERMEDADES CRÓNICAS DEL EMPLEADO: {error}")
    
    def obtener_por_empleado_id(self, empleado_id: int) -> List[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                historial_enfermedades_cronicas = sesion.execute(text(
                    """
                        SELECT
                            historial_enferm_cronicas.hist_enferm_cronica_id,
                            empleados.empleado_id,
                            enfermedades_cronicas.enfermedad_cronica
                        FROM tb_historial_enferm_cronicas AS historial_enferm_cronicas
                        INNER JOIN tb_empleados AS empleados ON historial_enferm_cronicas.empleado_id = empleados.empleado_id
                        INNER JOIN tb_enfermedades_cronicas AS enfermedades_cronicas ON historial_enferm_cronicas.enferm_cronica_id = enfermedades_cronicas.enferm_cronica_id
                        WHERE empleados.empleado_id = :empleado_id;
                    """
                ), {"empleado_id": empleado_id}).fetchall()
                
                return historial_enfermedades_cronicas
        except Exception as error:
            print(f"ERROR AL OBTENER EL HISTORIAL DE ENFERMEDADES CRÓNICAS DEL EMPLEADO: {error}")
    
    def actualizar(self, hist_enferm_cronica_id: int, campos_hist_enferm_cronicas: Dict) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                historial_enfermedad_cronica = sesion.query(HistorialEnfermCronicas).filter(HistorialEnfermCronicas.hist_enferm_cronica_id == hist_enferm_cronica_id).first()
                
                (cedula_empleado,) = sesion.execute(text(
                    """
                        SELECT
                            empleados.cedula
                        FROM tb_historial_enferm_cronicas AS historial_enferm_cronicas
                        INNER JOIN tb_empleados AS empleados ON historial_enferm_cronicas.empleado_id = empleados.empleado_id
                        WHERE historial_enferm_cronicas.hist_enferm_cronica_id = :hist_enferm_cronica_id;
                    """
                ), {"hist_enferm_cronica_id": hist_enferm_cronica_id}).fetchone()
                
                (enfermedad_cronica_anterior,) = sesion.execute(text(
                    """
                        SELECT
                            enfermedades_cronicas.enfermedad_cronica
                        FROM tb_historial_enferm_cronicas AS historial_enferm_cronicas
                        INNER JOIN tb_enfermedades_cronicas AS enfermedades_cronicas ON historial_enferm_cronicas.enferm_cronica_id = enfermedades_cronicas.enferm_cronica_id
                        WHERE historial_enferm_cronicas.hist_enferm_cronica_id = :hist_enferm_cronica_id;
                    """
                ), {"hist_enferm_cronica_id": hist_enferm_cronica_id}).fetchone()
                
                diccionario_historial_enferm_cronica = {campo: valor for campo, valor in vars(historial_enfermedad_cronica).items() if not(campo.startswith("_")) and not(campo == "hist_enferm_cronica_id") and not(campo == "empleado_id")}
                
                campos = {
                    "enferm_cronica_id": "ENFERMEDAD CRÓNICA"
                }
                
                for clave in diccionario_historial_enferm_cronica.keys():
                    if not(campos_hist_enferm_cronicas.get(clave) == diccionario_historial_enferm_cronica.get(clave)):
                        campo_actualizado = campos.get(clave)
                        nueva_enfermedad_cronica_id = campos_hist_enferm_cronicas.get("enferm_cronica_id")
                        
                        (enfermedad_cronica_actual,) = sesion.query(EnfermedadCronica.enfermedad_cronica).filter(EnfermedadCronica.enferm_cronica_id == nueva_enfermedad_cronica_id).first()
                        
                        valor_campo_actual = campos_hist_enferm_cronicas.get(clave)
                        
                        accion = f"ACTUALIZÓ EL CAMPO: {campo_actualizado}. ANTES: {enfermedad_cronica_anterior}. AHORA: {enfermedad_cronica_actual}. CÉDULA DEL EMPLEADO AFECTADO: {cedula_empleado}"
                        
                        auditoria_repositorio.registrar(self.entidad, accion)
                        
                        sesion.query(HistorialEnfermCronicas).filter(HistorialEnfermCronicas.hist_enferm_cronica_id == hist_enferm_cronica_id).update({clave: valor_campo_actual})
                        sesion.commit()
                        print(f"Se actualizó el campo: {campo_actualizado} correctamente \n")
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL ACTUALIZAR LOS CAMPOS: {error}")
    
    def eliminar(self, hist_enferm_cronica_id: int) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                historial_enferm_cronica = sesion.query(HistorialEnfermCronicas).filter(HistorialEnfermCronicas.hist_enferm_cronica_id == hist_enferm_cronica_id).first()
                
                if not(historial_enferm_cronica):
                    raise BaseDatosError("HISTORIAL_ENFERM_CRONICA_NO_EXISTE", "No está la enfermedad crónica registrada en el historial")
                
                (cedula_empleado,) = sesion.execute(text(
                    """
                        SELECT
                            empleados.cedula
                        FROM tb_historial_enferm_cronicas AS historial_enferm_cronicas
                        INNER JOIN tb_empleados AS empleados ON historial_enferm_cronicas.empleado_id = empleados.empleado_id
                        WHERE historial_enferm_cronicas.hist_enferm_cronica_id = :hist_enferm_cronica_id;
                    """
                ), {"hist_enferm_cronica_id": hist_enferm_cronica_id}).fetchone()
                
                (enfermedad_cronica,) = sesion.execute(text(
                    """
                        SELECT
                            enfermedades_cronicas.enfermedad_cronica
                        FROM tb_historial_enferm_cronicas AS historial_enferm_cronicas
                        INNER JOIN tb_enfermedades_cronicas AS enfermedades_cronicas ON historial_enferm_cronicas.enferm_cronica_id = enfermedades_cronicas.enferm_cronica_id
                        WHERE historial_enferm_cronicas.hist_enferm_cronica_id = :hist_enferm_cronica_id;
                    """
                ), {"hist_enferm_cronica_id": hist_enferm_cronica_id}).fetchone()
                
                accion = f"ELIMINÓ LA ENFERMEDAD CRÓNICA DE {enfermedad_cronica} DEL HISTORIAL. CÉDULA DEL EMPLEADO AFECTADO: {cedula_empleado}"
                
                auditoria_repositorio.registrar(self.entidad, accion)
                
                sesion.delete(historial_enferm_cronica)
                sesion.commit()
                print("Se eliminó la enfermedad crónica del historial del empleado correctamente")
        except BaseDatosError as error:
            raise error
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL ELIMINAR LA ENFERMEDAD CRÓNICA DEL HISTORIAL DEL EMPLEADO: {error}")


if __name__ == "__main__":
    hist_enferm_cronicas_repositorio = HistorialEnfermCronicasRepositorio()
    
    """campos_historial_enfermedad_cronica = {
        "empleado_id": 2,
        "enferm_cronica_id": 2
    }
    
    hist_enferm_cronicas_repositorio.registrar(campos_historial_enfermedad_cronica)"""
    
    """todos_historial_enfermedades_cronicas = hist_enferm_cronicas_repositorio.obtener_todos()
    
    for registro in todos_historial_enfermedades_cronicas:
        print(registro)"""
    
    #print(hist_enferm_cronicas_repositorio.obtener_por_id(2))
    
    """todos_historial_enfermedades_cronicas = hist_enferm_cronicas_repositorio.obtener_por_empleado_id(1)
    
    if (type(todos_historial_enfermedades_cronicas) == list):
        for registro in todos_historial_enfermedades_cronicas:
            print(registro)
    else:
        print(todos_historial_enfermedades_cronicas)"""
    
    
    """campos_historial_enfermedades_cronicas = {
        "enferm_cronica_id": 2
    }
    
    hist_enferm_cronicas_repositorio.actualizar(3, campos_historial_enfermedades_cronicas)"""
    
    #hist_enferm_cronicas_repositorio.eliminar(4)