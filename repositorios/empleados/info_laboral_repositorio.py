from typing import Tuple, List, Optional, Dict
from sqlalchemy import text
from modelos import InfoLaboral, Empleado
from repositorios.usuarios.auditoria_repositorio import auditoria_repositorio
from repositorios.repositorio_base import RepositorioBase
from conexiones.conexion import conexion_bd


class InfoLaboralRepositorio(RepositorioBase):
    def __init__(self):
        self.conexion_bd = conexion_bd
        self.entidad = "EMPLEADOS"
    
    def registrar(self, campos: Dict) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                nueva_info_laboral = InfoLaboral(**campos)
                
                sesion.add(nueva_info_laboral)
                sesion.commit()
                sesion.refresh(nueva_info_laboral)
                print("Se registró la información laboral del empleado correctamente")
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL REGISTRAR LA INFORMACIÓN LABORAL DEL EMPLEADO: {error}")
    
    def obtener_todos(self) -> List[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                info_laborales = sesion.execute(text(
                    """
                        SELECT
                            info_laboral.info_lab_id,
                            empleados.cedula,
                            empleados.primer_nombre,
                            empleados.apellido_paterno,
                            info_laboral.cod_depend_cobra,
                            info_laboral.institucion_labora
                        FROM tb_info_laboral AS info_laboral
                        INNER JOIN tb_empleados AS empleados ON info_laboral.empleado_id = empleados.empleado_id;
                    """
                )).fetchall()
                
                return info_laborales
        except Exception as error:
            print(f"ERROR AL OBTENER LAS INFO LABORALES: {error}")
    
    def obtener_por_id(self, info_lab_id: int) -> Optional[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                info_laboral = sesion.execute(text(
                    """
                        SELECT
                            info_laboral.info_lab_id,
                            empleados.cedula,
                            empleados.primer_nombre,
                            empleados.apellido_paterno,
                            info_laboral.cod_depend_cobra,
                            info_laboral.institucion_labora
                        FROM tb_info_laboral AS info_laboral
                        INNER JOIN tb_empleados AS empleados ON info_laboral.empleado_id = empleados.empleado_id
                        WHERE info_laboral.info_lab_id = :info_lab_id;
                    """
                ), {"info_lab_id": info_lab_id}).fetchone()
                
                return info_laboral
        except Exception as error:
            print(f"ERROR AL OBTENER LA INFO LABORAL: {error}")
    
    def obtener_por_empleado_id(self, empleado_id: int) -> Optional[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                info_laboral = sesion.execute(text(
                    """
                        SELECT
                            info_laboral.info_lab_id,
                            empleados.cedula,
                            empleados.primer_nombre,
                            empleados.apellido_paterno,
                            info_laboral.cod_depend_cobra,
                            info_laboral.institucion_labora
                        FROM tb_info_laboral AS info_laboral
                        INNER JOIN tb_empleados AS empleados ON info_laboral.empleado_id = empleados.empleado_id
                        WHERE empleados.empleado_id = :empleado_id;
                    """
                ), {"empleado_id": empleado_id}).fetchone()
                
                return info_laboral
        except Exception as error:
            print(f"ERROR AL OBTENER LA INFO LABORAL: {error}")
    
    def actualizar(self, empleado_id: int, campos_info_laboral: Dict) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                info_laboral = sesion.query(InfoLaboral).filter(InfoLaboral.empleado_id == empleado_id).first()
                empleado = sesion.query(Empleado).filter(Empleado.empleado_id == empleado_id).first()
                diccionario_info_laboral = {campo: valor for campo, valor in vars(info_laboral).items() if not(campo.startswith("_")) and not(campo == "info_lab_id") and not(campo == "empleado_id")}
                
                campos = {
                    "cod_depend_cobra": "CÓDIGO DE DEPENDENCIA POR DONDE COBRA",
                    "institucion_labora": "INSTITUCIÓN DONDE LABORA"
                }
                
                for clave in diccionario_info_laboral.keys():
                    if not(campos_info_laboral.get(clave) == diccionario_info_laboral.get(clave)):
                        campo_actualizado = campos.get(clave)
                        
                        valor_campo_anterior = diccionario_info_laboral.get(clave)
                        valor_campo_actual = campos_info_laboral.get(clave)
                        
                        accion = f"ACTUALIZÓ EL CAMPO: {campo_actualizado}. ANTES: {valor_campo_anterior}. AHORA: {valor_campo_actual}. CÉDULA DEL EMPLEADO AFECTADO: {empleado.cedula}"
                        auditoria_repositorio.registrar(self.entidad, accion)
                        
                        sesion.query(InfoLaboral).filter(InfoLaboral.empleado_id == empleado_id).update({clave: valor_campo_actual})
                        sesion.commit()
                        print(f"Se actualizó el campo: {campo_actualizado} correctamente \n")
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL ACTUALIZAR LOS CAMPOS: {error}")


if __name__ == "__main__":
    info_laboral_repositorio = InfoLaboralRepositorio()
    
    campos_info_laboral = {
        "empleado_id": 5,
        "cod_depend_cobra": "100005",
        "institucion_labora": "TEV TRONCONAL 4"
    }
    
    #info_laboral_repositorio.registrar(campos_info_laboral)
    
    """todas_info_laboral  =info_laboral_repositorio.obtener_todos()
    
    for info_laboral in todas_info_laboral:
        print(info_laboral)"""
    
    #print(info_laboral_repositorio.obtener_por_id(1))
    #print(info_laboral_repositorio.obtener_por_empleado_id(5))