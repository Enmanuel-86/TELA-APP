from typing import Tuple, List, Optional, Dict
from sqlalchemy import text
from excepciones.base_datos_error import BaseDatosError
from modelos import InfoClinicaEmpleado, Diagnostico
from repositorios.usuarios.auditoria_repositorio import auditoria_repositorio
from repositorios.repositorio_base import RepositorioBase
from conexiones.conexion import conexion_bd


class InfoClinicaEmpleadoRepositorio(RepositorioBase):
    def __init__(self):
        self.conexion_bd = conexion_bd
        self.entidad = "INFO CLÍNICA DE EMPLEADOS"
    
    def registrar(self, campos: Dict) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                nueva_info_clinica_empleado = InfoClinicaEmpleado(**campos)
                
                sesion.add(nueva_info_clinica_empleado)
                sesion.commit()
                sesion.refresh(nueva_info_clinica_empleado)
                print("Se registró la info clínica del empleado correctamente")
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL REGISTRAR LA INFO CLÍNICA DEL EMPLEADO: {error}")
    
    def obtener_todos(self) -> List[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                info_clinica_empleados = sesion.execute(text(
                    """
                        SELECT
                            info_clinica_empleados.info_clin_empleado_id,
                            empleados.empleado_id,
                            diagnosticos.diagnostico
                        FROM tb_info_clinica_empleados AS info_clinica_empleados
                        INNER JOIN tb_empleados AS empleados ON info_clinica_empleados.empleado_id = empleados.empleado_id
                        INNER JOIN tb_diagnosticos AS diagnosticos ON info_clinica_empleados.diagnostico_id = diagnosticos.diagnostico_id;
                    """
                )).fetchall()
                
                return info_clinica_empleados
        except Exception as error:
            print(f"ERROR AL OBTENER LAS INFO CLÍNICA DE LOS EMPLEADOS: {error}")
    
    def obtener_por_id(self, info_clin_empleado_id: int) -> Optional[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                info_clinica_empleado = sesion.execute(text(
                    """
                        SELECT
                            info_clinica_empleados.info_clin_empleado_id,
                            empleados.empleado_id,
                            diagnosticos.diagnostico
                        FROM tb_info_clinica_empleados AS info_clinica_empleados
                        INNER JOIN tb_empleados AS empleados ON info_clinica_empleados.empleado_id = empleados.empleado_id
                        INNER JOIN tb_diagnosticos AS diagnosticos ON info_clinica_empleados.diagnostico_id = diagnosticos.diagnostico_id
                        WHERE info_clinica_empleados.info_clin_empleado_id = :info_clin_empleado_id;
                    """
                ), {"info_clin_empleado_id": info_clin_empleado_id}).fetchone()
                
                return info_clinica_empleado
        except Exception as error:
            print(f"ERROR AL OBTENER LA INFO CLÍNICA DEL EMPLEADO: {error}")
    
    def obtener_por_empleado_id(self, empleado_id: int) -> List[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                info_clinica_empleado = sesion.execute(text(
                    """
                        SELECT
                            info_clinica_empleados.info_clin_empleado_id,
                            empleados.empleado_id,
                            diagnosticos.diagnostico
                        FROM tb_info_clinica_empleados AS info_clinica_empleados
                        INNER JOIN tb_empleados AS empleados ON info_clinica_empleados.empleado_id = empleados.empleado_id
                        INNER JOIN tb_diagnosticos AS diagnosticos ON info_clinica_empleados.diagnostico_id = diagnosticos.diagnostico_id
                        WHERE empleados.empleado_id = :empleado_id;
                    """
                ), {"empleado_id": empleado_id}).fetchall()
                
                if not(info_clinica_empleado):
                    raise BaseDatosError("EMPLEADO_NO_TIENE_INFO_CLINICA", "Este empleado no posee información clínica.")
                
                return info_clinica_empleado
        except BaseDatosError as error:
            raise error
        except Exception as error:
            print(f"ERROR AL OBTENER LA INFO CLÍNICA DEL EMPLEADO: {error}")
    
    def actualizar(self, info_clin_empleado_id: int, campos_info_clinica_empleado: Dict) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                info_clinica_empleado = sesion.query(InfoClinicaEmpleado).filter(InfoClinicaEmpleado.info_clin_empleado_id == info_clin_empleado_id).first()
                
                (cedula_empleado,) = sesion.execute(text(
                    """
                        SELECT
                            empleados.cedula
                        FROM tb_info_clinica_empleados AS info_clinica_empleados
                        INNER JOIN tb_empleados AS empleados ON info_clinica_empleados.empleado_id = empleados.empleado_id
                        WHERE info_clinica_empleados.info_clin_empleado_id = :info_clin_empleado_id;
                    """
                ), {"info_clin_empleado_id": info_clin_empleado_id}).fetchone()
                
                (diagnostico_anterior,) = sesion.execute(text(
                    """
                        SELECT
                            diagnosticos.diagnostico
                        FROM tb_info_clinica_empleados AS info_clinica_empleados
                        INNER JOIN tb_diagnosticos AS diagnosticos ON info_clinica_empleados.diagnostico_id = diagnosticos.diagnostico_id
                        WHERE info_clinica_empleados.info_clin_empleado_id = :info_clin_empleado_id;
                    """
                ), {"info_clin_empleado_id": info_clin_empleado_id}).fetchone()
                
                diccionario_info_clinica_empleado = {campo: valor for campo, valor in vars(info_clinica_empleado).items() if not(campo.startswith("_")) and not(campo == "info_clin_empleado_id") and not(campo == "empleado_id")}
                
                campos = {
                    "diagnostico_id": "DIAGNÓSTICO"
                }
                
                for clave in diccionario_info_clinica_empleado.keys():
                    if not(campos_info_clinica_empleado.get(clave) == diccionario_info_clinica_empleado.get(clave)):
                        campo_actualizado = campos.get(clave)
                        nuevo_diagnostico_id = campos_info_clinica_empleado.get("diagnostico_id")
                        
                        (diagnostico_actual,) = sesion.query(Diagnostico.diagnostico).filter(Diagnostico.diagnostico_id == nuevo_diagnostico_id).first()
                        
                        valor_campo_actual = campos_info_clinica_empleado.get(clave)
                        
                        accion = f"ACTUALIZÓ EL CAMPO: {campo_actualizado}. ANTES: {diagnostico_anterior}. AHORA: {diagnostico_actual}. CÉDULA DEL EMPLEADO AFECTADO: {cedula_empleado}"
                        
                        auditoria_repositorio.registrar(self.entidad, accion)
                        
                        sesion.query(InfoClinicaEmpleado).filter(InfoClinicaEmpleado.info_clin_empleado_id == info_clin_empleado_id).update({clave: valor_campo_actual})
                        sesion.commit()
                        print(f"Se actualizó el campo: {campo_actualizado} correctamente \n")
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL ACTUALIZAR LOS CAMPOS: {error}")
    
    def eliminar(self, info_clin_empleado_id: int) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                info_clinica_empleado = sesion.query(InfoClinicaEmpleado).filter(InfoClinicaEmpleado.info_clin_empleado_id == info_clin_empleado_id).first()
                
                if not(info_clinica_empleado):
                    raise BaseDatosError("INFO_CLINICA_EMPLEADO_NO_EXISTE", "Esta información clínica no existe")
                
                (cedula_empleado,) = sesion.execute(text(
                    """
                        SELECT
                            empleados.cedula
                        FROM tb_info_clinica_empleados AS info_clinica_empleados
                        INNER JOIN tb_empleados AS empleados ON info_clinica_empleados.empleado_id = empleados.empleado_id
                        WHERE info_clinica_empleados.info_clin_empleado_id = :info_clin_empleado_id;
                    """
                ), {"info_clin_empleado_id": info_clin_empleado_id}).fetchone()
                
                (diagnostico,) = sesion.execute(text(
                    """
                        SELECT
                            diagnosticos.diagnostico
                        FROM tb_info_clinica_empleados AS info_clinica_empleados
                        INNER JOIN tb_diagnosticos AS diagnosticos ON info_clinica_empleados.diagnostico_id = diagnosticos.diagnostico_id
                        WHERE info_clinica_empleados.info_clin_empleado_id = :info_clin_empleado_id;
                    """
                ), {"info_clin_empleado_id": info_clin_empleado_id}).fetchone()
                
                accion = f"ELIMINÓ EL DIAGNÓSTICO DE {diagnostico}. CÉDULA DEL EMPLEADO AFECTADO: {cedula_empleado}"
                
                auditoria_repositorio.registrar(self.entidad, accion)
                
                sesion.delete(info_clinica_empleado)
                sesion.commit()
                print("Se eliminó la información clínica del empleado correctamente")
        except BaseDatosError as error:
            sesion.rollback()
            raise error
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL ELIMINAR LA INFO CLÍNICA DEL EMPLEADO: {error}")


if __name__ == "__main__":
    info_clinica_empleado_repositorio = InfoClinicaEmpleadoRepositorio()
    
    """campos_info_clinica_empleado = {
        "empleado_id": 2,
        "diagnostico_id": 2
    }
    
    info_clinica_empleado_repositorio.registrar(campos_info_clinica_empleado)"""
    
    """todos_info_clinica_empleado = info_clinica_empleado_repositorio.obtener_todos()
    
    for registro in todos_info_clinica_empleado:
        print(registro)"""
    
    
    #print(info_clinica_empleado_repositorio.obtener_por_id(1))
    #print(info_clinica_empleado_repositorio.obtener_por_id(2))
    
    """todos_info_clinica_empleado = info_clinica_empleado_repositorio.obtener_por_empleado_id(2)
    
    if (type(todos_info_clinica_empleado) == list):
        for registro in todos_info_clinica_empleado:
            print(registro)
    else:
        print(todos_info_clinica_empleado)"""
    
    
    """campos_info_clinica_empleado = {
        "diagnostico_id": 1
    }
    
    info_clinica_empleado_repositorio.actualizar(3, campos_info_clinica_empleado)"""
    
    #info_clinica_empleado_repositorio.eliminar(40)
    #info_clinica_empleado_repositorio.eliminar(3)