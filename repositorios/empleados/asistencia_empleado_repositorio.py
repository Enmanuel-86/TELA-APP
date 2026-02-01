from typing import Tuple, List, Optional, Dict
from datetime import date, time
from sqlalchemy import text
from excepciones.base_datos_error import BaseDatosError
from modelos import AsistenciaEmpleado
from repositorios.usuarios.auditoria_repositorio import auditoria_repositorio
from repositorios.repositorio_base import RepositorioBase
from conexiones.conexion import conexion_bd


class AsistenciaEmpleadoRepositorio(RepositorioBase):
    def __init__(self):
        self.conexion_bd = conexion_bd
        self.entidad = "ASISTENCIA DE EMPLEADOS"
    
    def registrar(self, campos: Dict) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                if (campos.get("estado_asistencia") == "AUSENTE"):
                    if (campos.get("motivo_inasistencia") == ""):
                        campos["estado_asistencia"] = "II"
                    else:
                        campos["estado_asistencia"] == "IJ"
                    
                    campos["hora_entrada"] = None
                    campos["hora_salida"] = None
                
                nueva_asistencia_empleado = AsistenciaEmpleado(**campos)
                
                sesion.add(nueva_asistencia_empleado)
                sesion.commit()
                sesion.refresh(nueva_asistencia_empleado)
                print("Se registró la asistencia de empleado correctamente")
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL REGISTRAR LA ASISTENCIA DEL EMPLEADO: {error}")
    
    def obtener_todos(self) -> List[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                asistencias_empleados = sesion.execute(text("SELECT * FROM vw_asistencia_empleados;")).fetchall()
                return asistencias_empleados
        except Exception as error:
            print(f"ERROR AL OBTENER LAS ASISTENCIAS DE LOS EMPLEADOS: {error}")
    
    def obtener_por_id(self, asist_empleado_id: int) -> Optional[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                asistencia_empleado = sesion.execute(text(
                    """
                        SELECT * FROM vw_asistencia_empleados WHERE asist_empleado_id = :asist_empleado_id;
                    """
                ), {"asist_empleado_id": asist_empleado_id}).fetchone()
                
                if not(asistencia_empleado):
                    raise BaseDatosError("ASISTENCIA_EMPLEADO_NO_EXISTE", "Esta asistencia no existe")
                
                return asistencia_empleado
        except BaseDatosError as error:
            raise error
        except Exception as error:
            print(f"ERROR AL OBTENER LA ASISTENCIA DEL EMPLEADO: {error}")
    
    def obtener_por_fecha(self, fecha_asistencia: date) -> List[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                asistencia_empleado = sesion.execute(text(
                    """
                        SELECT * FROM vw_asistencia_empleados WHERE fecha_asistencia = :fecha_asistencia;
                    """
                ), {"fecha_asistencia": fecha_asistencia}).fetchall()
                
                if not(asistencia_empleado):
                    raise BaseDatosError("ASISTENCIA_EMPLEADO_NO_EXISTE", "Esta asistencia no existe")
                
                return asistencia_empleado
        except BaseDatosError as error:
            raise error
        except Exception as error:
            print(f"ERROR AL OBTENER LA ASISTENCIA DEL EMPLEADO: {error}")
    
    def obtener_por_empleado_id_y_fecha(self, empleado_id: int, fecha_asistencia: date) -> Optional[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                asistencia_empleado = sesion.execute(text(
                    """
                        SELECT * FROM vw_asistencia_empleados 
                        WHERE fecha_asistencia = :fecha_asistencia AND empleado_id = :empleado_id;
                    """
                ), {"fecha_asistencia": fecha_asistencia, "empleado_id": empleado_id}).fetchone()
                
                return asistencia_empleado
        except Exception:
            return None
    
    def obtener_horas_retraso_mensuales(self, anio_mes: str) -> List[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                horas_retraso_empleado = sesion.execute(text(
                    """
                        SELECT
                            cedula,
                            primer_nombre,
                            apellido_paterno,
                            STRFTIME('%Y-%m', fecha_asistencia) AS anio_mes,
                            SUM(horas_retraso) total_horas_retraso,
                            ROUND(SUM(horas_retraso) / 5.5) AS dias_habiles
                        FROM vw_asistencia_empleados
                        WHERE STRFTIME('%Y-%m', fecha_asistencia) = :anio_mes
                        GROUP BY cedula, anio_mes;
                    """
                ), {"anio_mes": anio_mes}).fetchall()
                
                if not(horas_retraso_empleado):
                    raise BaseDatosError("HORAS_RETRASO_NO_EXISTE", "No existen horas de retraso en este mes y año")
                
                return horas_retraso_empleado
        except BaseDatosError as error:
            raise error
        except Exception as error:
            print(f"ERROR AL OBTENER LAS HORAS DE RETRASO DE LOS EMPLEADOS: {error}")
    
    def obtener_num_inasistencias_mensuales(self, anio_mes: str) -> List[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                num_inasistencias_mensuales_empleado = sesion.execute(text(
                    """
                        SELECT 
                            empleados.cedula,
                            empleados.primer_nombre,
                            empleados.apellido_paterno,
                            STRFTIME('%Y-%m', asistencia_empleados.fecha_asistencia) AS anio_mes,
                            COUNT(*) AS total_inasistencias
                        FROM tb_empleados AS empleados
                        INNER JOIN tb_asistencia_empleados AS asistencia_empleados 
                            ON asistencia_empleados.empleado_id = empleados.empleado_id
                        WHERE hora_entrada IS NULL AND STRFTIME('%Y-%m', asistencia_empleados.fecha_asistencia) = :anio_mes
                        GROUP BY empleados.cedula, anio_mes;
                    """
                ), {"anio_mes": anio_mes}).fetchall()
                
                if not(num_inasistencias_mensuales_empleado):
                    raise BaseDatosError("NUM_INASISTENCIAS_NO_EXISTE", "No existen inasistencias en este mes y año")
                
                return num_inasistencias_mensuales_empleado
        except BaseDatosError as error:
            raise error
        except Exception as error:
            print(f"ERROR AL OBTENER LAS INASISTENCIAS MENSUALES DE LOS EMPLEADOS: {error}")
    
    def actualizar(self, asist_empleado_id: int, campos_asistencia_empleado: Dict) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                asistencia_empleado = sesion.query(AsistenciaEmpleado).filter(AsistenciaEmpleado.asist_empleado_id == asist_empleado_id).first()
                (cedula_empleado,) = sesion.execute(text(
                    """
                        SELECT
                            empleados.cedula
                        FROM tb_asistencia_empleados AS asistencia_empleados
                        INNER JOIN tb_empleados AS empleados ON asistencia_empleados.empleado_id = empleados.empleado_id
                        WHERE asistencia_empleados.asist_empleado_id = :asist_empleado_id;
                    """
                ), {"asist_empleado_id": asist_empleado_id}).fetchone()
                
                diccionario_asistencia_empleado = {campo: valor for campo, valor in vars(asistencia_empleado).items() if not(campo.startswith("_")) and not(campo == "asist_empleado_id") and not(campo == "empleado_id")}
                
                campos = {
                    "fecha_asistencia": "FECHA DE ASISTENCIA",
                    "hora_entrada": "HORA DE ENTRADA",
                    "hora_salida": "HORA DE SALIDA",
                    "estado_asistencia": "ESTADO DE ASISTENCIA",
                    "motivo_retraso": "MOTIVO DE RETRASO",
                    "motivo_inasistencia": "MOTIVO DE INASISTENCIA"
                }
                
                for clave in diccionario_asistencia_empleado.keys():
                    if not(campos_asistencia_empleado.get(clave) == diccionario_asistencia_empleado.get(clave)):
                        campo_actualizado = campos.get(clave)
                        
                        valor_campo_anterior = diccionario_asistencia_empleado.get(clave) if diccionario_asistencia_empleado.get(clave) else ""
                        valor_campo_actual = campos_asistencia_empleado.get(clave)
                        
                        if ((clave == "hora_entrada") or (clave == "hora_salida")):
                            hora_entrada_anterior = diccionario_asistencia_empleado.get("hora_entrada")
                            hora_salida_anterior = diccionario_asistencia_empleado.get("hora_salida")
                            
                            hora_entrada_actual = campos_asistencia_empleado.get("hora_entrada")
                            hora_salida_actual = campos_asistencia_empleado.get("hora_salida")
                            
                            horas_anteriores_vacias = ((hora_entrada_anterior is None) and (hora_salida_anterior is None))
                            horas_actuales_vacias = ((hora_entrada_actual is None) and (hora_salida_actual is None))
                            
                            if ((campos_asistencia_empleado.get("hora_entrada")) and (campos_asistencia_empleado.get("hora_salida"))):
                                hora_anterior = ""
                                hora_actual = ""
                                
                                if not(valor_campo_anterior == ""):
                                    hora_anterior = valor_campo_anterior.strftime('%H:%M')
                                
                                if not (valor_campo_actual == ""):
                                    hora_actual = valor_campo_actual.strftime('%H:%M')
                                
                                accion = f"ACTUALIZÓ EL CAMPO: {campo_actualizado}. ANTES: {hora_anterior}. AHORA: {hora_actual}. CÉDULA DEL EMPLEADO AFECTADO: {cedula_empleado}"
                            elif ((horas_anteriores_vacias) and not(horas_actuales_vacias)):
                                hora_anterior = ""
                                hora_actual = valor_campo_actual.strftime('%H:%M')
                                accion = f"ACTUALIZÓ EL CAMPO: {campo_actualizado}. ANTES: {hora_anterior}. AHORA: {hora_actual}. CÉDULA DEL EMPLEADO AFECTADO: {cedula_empleado}"
                            else:
                                hora_anterior = ""
                                hora_actual = ""
                                accion = f"ACTUALIZÓ EL CAMPO: {campo_actualizado}. ANTES: {hora_anterior}. AHORA: {hora_actual}. CÉDULA DEL EMPLEADO AFECTADO: {cedula_empleado}"
                        elif (clave == "estado_asistencia"):
                            if (campos_asistencia_empleado.get("estado_asistencia") == "AUSENTE"):
                                if (campos_asistencia_empleado.get("motivo_inasistencia") == ""):
                                    valor_campo_actual = "II"
                                else:
                                    valor_campo_actual = "IJ"
                                
                            accion = f"ACTUALIZÓ EL CAMPO: {campo_actualizado}. ANTES: {valor_campo_anterior}. AHORA: {valor_campo_actual}. CÉDULA DEL EMPLEADO AFECTADO: {cedula_empleado}"
                        else:
                            accion = f"ACTUALIZÓ EL CAMPO: {campo_actualizado}. ANTES: {valor_campo_anterior}. AHORA: {valor_campo_actual}. CÉDULA DEL EMPLEADO AFECTADO: {cedula_empleado}"
                            
                        auditoria_repositorio.registrar(self.entidad, accion)
                        sesion.query(AsistenciaEmpleado).filter(AsistenciaEmpleado.asist_empleado_id == asist_empleado_id).update({clave: valor_campo_actual})
                        sesion.commit()
                        print(f"Se actualizó el campo: {campo_actualizado} correctamente \n")
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL ACTUALIZAR LOS CAMPOS: {error}")
    
    def eliminar(self, asist_empleado_id: int) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                asistencia_empleado = sesion.query(AsistenciaEmpleado).filter(AsistenciaEmpleado.asist_empleado_id == asist_empleado_id).first()
                
                if not(asistencia_empleado):
                    raise BaseDatosError("ASISTENCIA_EMPLEADO_NO_EXISTE", "Esta asistencia no existe")
                
                (cedula_empleado,) = sesion.execute(text(
                    """
                        SELECT
                            empleados.cedula
                        FROM tb_asistencia_empleados AS asistencia_empleados
                        INNER JOIN tb_empleados AS empleados ON asistencia_empleados.empleado_id = empleados.empleado_id
                        WHERE asistencia_empleados.asist_empleado_id = :asist_empleado_id;
                    """
                ), {"asist_empleado_id": asist_empleado_id}).fetchone()
                
                accion = f"ELIMINÓ EL REGISTRO DE ASISTENCIA DEL DIA {asistencia_empleado.fecha_asistencia}. CÉDULA DEL EMPLEADO AFECTADO: {cedula_empleado}"
                
                auditoria_repositorio.registrar(self.entidad, accion)
                
                sesion.delete(asistencia_empleado)
                sesion.commit()
                print("Se eliminó la asistencia del empleado correctamente")
        except BaseDatosError as error:
            raise error
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL ELIMINAR LA ASISTENCIA DEL EMPLEADO: {error}")


if __name__ == "__main__":
    asistencia_empleado_repositorio = AsistenciaEmpleadoRepositorio()
    
    """todas_asistencia_empleados = asistencia_empleado_repositorio.obtener_todos()
    
    for registro in todas_asistencia_empleados:
        print(registro)"""
    
    
    #print(asistencia_empleado_repositorio.obtener_por_id(1))

    """todas_asistencias_empleados_fecha = asistencia_empleado_repositorio.obtener_por_fecha(date(2024, 9, 25))
    
    for registro in todas_asistencias_empleados_fecha:
        print(registro)"""
    
    """horas_retraso_mensual = asistencia_empleado_repositorio.obtener_horas_retraso_mensuales("2024-09")
    
    for registro in horas_retraso_mensual:
        print(registro)"""
    
    """num_inasistencias_mensual = asistencia_empleado_repositorio.obtener_num_inasistencias_mensuales("2024-09")
    
    for registro in num_inasistencias_mensual:
        print(registro)"""
    
    """campos_asistencia_empleados = {
        "fecha_asistencia": date(2024, 9, 24),
        "hora_entrada": time(7, 20),
        "hora_salida": time(12, 40),
        "estado_asistencia": "PRESENTE",
        "motivo_retraso": "TRÁFICO",
        "motivo_inasistencia": None
    }
    
    asistencia_empleado_repositorio.actualizar(1, campos_asistencia_empleados)"""
    
    #asistencia_empleado_repositorio.eliminar(40)
    #asistencia_empleado_repositorio.eliminar(1)