from typing import Tuple, List, Optional, Dict
from datetime import date
from sqlalchemy import text
from excepciones.base_datos_error import BaseDatosError
from modelos import ReposoEmpleado, Empleado
from repositorios.usuarios.auditoria_repositorio import auditoria_repositorio
from repositorios.repositorio_base import RepositorioBase
from conexiones.conexion import conexion_bd


class ReposoEmpleadoRepositorio(RepositorioBase):
    def __init__(self):
        self.conexion_bd = conexion_bd
        self.entidad = "REPOSO DE EMPLEADOS"
    
    def registrar(self, campos: Dict) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                nuevo_reposo_empleado = ReposoEmpleado(**campos)
                empleado_id = campos.get("empleado_id")
                empleado = sesion.query(Empleado).filter(Empleado.empleado_id == empleado_id).first()
                
                sesion.add(nuevo_reposo_empleado)
                sesion.commit()
                sesion.refresh(nuevo_reposo_empleado)
                print("Se registró el reposo de empleado correctamente")
                
                accion = f"REGISTRÓ UN REPOSO PARA EL EMPLEADO {empleado.primer_nombre} {empleado.apellido_paterno}. CÉDULA DEL EMPLEADO AFECTADO: {empleado.cedula}"
                
                auditoria_repositorio.registrar(self.entidad, accion)
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL REGISTRAR EL REPOSO DE EMPLEADO: {error}")
    
    def obtener_todos(self) -> List[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                reposos_empleados = sesion.execute(text(
                    """
                        SELECT 
                            empleados.cedula,
                            empleados.primer_nombre,
                            empleados.apellido_paterno,
                            reposos_empleados.motivo_reposo,
                            reposos_empleados.fecha_emision,
                            reposos_empleados.fecha_reingreso
                        FROM tb_empleados AS empleados
                        INNER JOIN tb_reposos_empleados AS reposos_empleados ON reposos_empleados.empleado_id = empleados.empleado_id;
                    """
                )).fetchall()
                
                return reposos_empleados
        except Exception as error:
            print(f"ERROR AL OBTENER LOS REPOSOS DE EMPLEADOS: {error}")
    
    def obtener_por_id(self, reposo_empleado_id: int) -> Optional[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                reposo_empleado = sesion.execute(text(
                    """
                        SELECT 
                            empleados.cedula,
                            empleados.primer_nombre,
                            empleados.apellido_paterno,
                            reposos_empleados.motivo_reposo,
                            reposos_empleados.fecha_emision,
                            reposos_empleados.fecha_reingreso
                        FROM tb_empleados AS empleados
                        INNER JOIN tb_reposos_empleados AS reposos_empleados ON reposos_empleados.empleado_id = empleados.empleado_id
                        WHERE reposos_empleados.reposo_empleado_id = :reposo_empleado_id;
                    """
                ), {"reposo_empleado_id": reposo_empleado_id}).fetchone()
                
                if not(reposo_empleado):
                    raise BaseDatosError("REPOSO_EMPLEADO_NO_EXISTE", "Este registro de reposo no existe")
                
                return reposo_empleado
        except BaseDatosError as error:
            raise error
        except Exception as error:
            print(f"ERROR AL OBTENER EL REPOSO DEL EMPLEADO: {error}")
    
    def obtener_por_fecha_emision(self, fecha_emision: date) -> List[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                reposos_empleados = sesion.execute(text(
                    """
                        SELECT 
                            empleados.cedula,
                            empleados.primer_nombre,
                            empleados.apellido_paterno,
                            reposos_empleados.motivo_reposo,
                            reposos_empleados.fecha_emision,
                            reposos_empleados.fecha_reingreso
                        FROM tb_empleados AS empleados
                        INNER JOIN tb_reposos_empleados AS reposos_empleados ON reposos_empleados.empleado_id = empleados.empleado_id
                        WHERE reposos_empleados.fecha_emision = :fecha_emision;
                    """
                ), {"fecha_emision": fecha_emision}).fetchall()
                
                if not(reposos_empleados):
                    raise BaseDatosError("REPOSOS_EMPLEADOS_NO_EXISTEN", "No existen reposos solicitados este día")
                
                return reposos_empleados
        except BaseDatosError as error:
            raise error
        except Exception as error:
            print(f"ERROR AL OBTENER EL REPOSO DE EMPLEADO POR FECHA DE EMISIÓN: {error}")
    
    def actualizar(self, reposo_empleado_id: int, campos_reposo_empleado: Dict) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                reposo_empleado = sesion.query(ReposoEmpleado).filter(ReposoEmpleado.reposo_empleado_id == reposo_empleado_id).first()
                (cedula_empleado,) = sesion.execute(text(
                    """
                        SELECT
                            empleados.cedula
                        FROM tb_reposos_empleados AS reposos_empleados
                        INNER JOIN tb_empleados AS empleados ON reposos_empleados.empleado_id = empleados.empleado_id
                        WHERE reposos_empleados.reposo_empleado_id = :reposo_empleado_id;
                    """
                ), {"reposo_empleado_id": reposo_empleado_id}).fetchone()
                
                diccionario_reposo_empleado = {campo: valor for campo, valor in vars(reposo_empleado).items() if not(campo.startswith("_")) and not(campo == "reposo_empleado_id") and not(campo == "empleado_id")}
                
                campos = {
                    "motivo_reposo": "MOTIVO DE REPOSO",
                    "fecha_emision": "FECHA DE EMISIÓN",
                    "fecha_reingreso": "FECHA DE REINGRESO"
                }
                
                for clave in diccionario_reposo_empleado.keys():
                    if not(campos_reposo_empleado.get(clave) == diccionario_reposo_empleado.get(clave)):
                        campo_actualizado = campos.get(clave)
                        
                        valor_campo_anterior = diccionario_reposo_empleado.get(clave)
                        valor_campo_actual = campos_reposo_empleado.get(clave)
                        
                        accion = f"ACTUALIZÓ EL CAMPO: {campo_actualizado}. ANTES: {valor_campo_anterior}. AHORA: {valor_campo_actual}. CÉDULA DEL EMPLEADO AFECTADO: {cedula_empleado}"
                        
                        auditoria_repositorio.registrar(self.entidad, accion)
                        
                        sesion.query(ReposoEmpleado).filter(ReposoEmpleado.reposo_empleado_id == reposo_empleado_id).update({clave: valor_campo_actual})
                        sesion.commit()
                        print(f"Se actualizó el campo: {campo_actualizado} correctamente \n")
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL ACTUALIZAR LOS CAMPOS: {error}")
    
    def eliminar(self, reposo_empleado_id: int) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                reposo_empleado = sesion.query(ReposoEmpleado).filter(ReposoEmpleado.reposo_empleado_id == reposo_empleado_id).first()
                
                if not(reposo_empleado):
                    raise BaseDatosError("REPOSO_EMPLEADO_NO_EXISTE", "Este registro de reposo no existe")
                
                (cedula_empleado,) = sesion.execute(text(
                    """
                        SELECT
                            empleados.cedula
                        FROM tb_reposos_empleados AS reposos_empleados
                        INNER JOIN tb_empleados AS empleados ON reposos_empleados.empleado_id = empleados.empleado_id
                        WHERE reposos_empleados.reposo_empleado_id = :reposo_empleado_id;
                    """
                ), {"reposo_empleado_id": reposo_empleado_id}).fetchone()
                
                accion = f"ELIMINÓ EL REPOSO EMITIDO EL DÍA {reposo_empleado.fecha_emision}. CÉDULA DEL EMPLEADO AFECTADO: {cedula_empleado}"
                
                auditoria_repositorio.registrar(self.entidad, accion)
                
                sesion.delete(reposo_empleado)
                sesion.commit()
                print("Se eliminó el reposo del empleado correctamente")
        except BaseDatosError as error:
            sesion.rollback()
            raise error
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL ELIMINAR EL REPOSO DEL EMPLEADO: {error}")


if __name__ == "__main__":
    reposo_empleado_repositorio = ReposoEmpleadoRepositorio()
    
    """campos_reposo_empleado = {
        "empleado_id": 1,
        "motivo_reposo": "FRACTURA DE TOBILLO",
        "fecha_emision": date.today(),
        "fecha_reingreso": date(2025, 5, 20)
    }
    
    reposo_empleado_repositorio.registrar(campos_reposo_empleado)"""
    
    """todos_reposos_empleados = reposo_empleado_repositorio.obtener_todos()
    
    for registro in todos_reposos_empleados:
        print(registro)"""
    
    """todos_reposos_empleado_fecha = reposo_empleado_repositorio.obtener_por_fecha_emision(date(2024, 9, 9))
    
    for registro in todos_reposos_empleado_fecha:
        print(registro)"""
    
    """campos_reposo_empleado = {
        "motivo_reposo": "FIEBRE",
        "fecha_emision": date(2025, 5, 15),
        "fecha_reingreso": date(2025, 5, 30)
    }
    
    reposo_empleado_repositorio.actualizar(2, campos_reposo_empleado)"""
    
    #reposo_empleado_repositorio.eliminar(40)
    #reposo_empleado_repositorio.eliminar(2)