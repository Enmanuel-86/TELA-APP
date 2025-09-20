from typing import Tuple, List, Optional, Dict, Union
from sqlalchemy import text
from excepciones.base_datos_error import BaseDatosError
from modelos import DetalleCargo, Empleado, CargoEmpleado, FuncionCargo, TipoCargo, Especialidad
from repositorios.usuarios.auditoria_repositorio import auditoria_repositorio
from repositorios.repositorio_base import RepositorioBase
from conexiones.conexion import conexion_bd


class DetalleCargoRepositorio(RepositorioBase):
    def __init__(self):
        self.conexion_bd = conexion_bd
        self.entidad = "EMPLEADOS"
    
    def registrar(self, campos: Dict) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                nuevo_detalle_cargo = DetalleCargo(**campos)
                
                sesion.add(nuevo_detalle_cargo)
                sesion.commit()
                sesion.refresh(nuevo_detalle_cargo)
                print("Se registró el nuevo detalle del cargo correctamente")
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL REGISTRAR EL DETALLE DEL CARGO: {error}")
    
    def obtener_todos(self) -> List[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                detalles_cargo = sesion.execute(text(
                    """
                        SELECT
                            detalles_cargo.detalle_cargo_id,
                            empleados.cedula,
                            empleados.primer_nombre,
                            empleados.segundo_nombre,
                            empleados.tercer_nombre,
                            empleados.apellido_paterno,
                            empleados.apellido_materno,
                            tipos_cargo.tipo_cargo,
                            empleados.situacion
                        FROM tb_detalles_cargo AS detalles_cargo
                        INNER JOIN tb_empleados AS empleados ON detalles_cargo.empleado_id = empleados.empleado_id
                        INNER JOIN tb_tipos_cargo AS tipos_cargo ON detalles_cargo.tipo_cargo_id = tipos_cargo.tipo_cargo_id
                        WHERE empleados.situacion = 'Activo';
                    """
                )).fetchall()
                
                return detalles_cargo
        except Exception as error:
            print(f"ERROR AL OBTENER LOS DETALLES DEL CARGO: {error}")
    
    def obtener_por_id(self, empleado_id: int) -> List[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                detalle_cargo = sesion.execute(text(
                    """
                        SELECT
                            detalles_cargo.detalle_cargo_id,
                            empleados.cedula,
                            empleados.primer_nombre,
                            empleados.segundo_nombre,
                            empleados.tercer_nombre,
                            empleados.apellido_paterno,
                            empleados.apellido_materno,
                            tipos_cargo.tipo_cargo,
                            empleados.situacion
                        FROM tb_detalles_cargo AS detalles_cargo
                        INNER JOIN tb_empleados AS empleados ON detalles_cargo.empleado_id = empleados.empleado_id
                        INNER JOIN tb_tipos_cargo AS tipos_cargo ON detalles_cargo.tipo_cargo_id = tipos_cargo.tipo_cargo_id
                        WHERE empleados.situacion = 'Activo' AND empleados.empleado_id = :empleado_id;
                    """
                ), {"empleado_id": empleado_id}).fetchone()
                
                if not(detalle_cargo):
                    raise BaseDatosError("DETALLE_CARGO_NO_EXISTE", "Los detalles del cargo de este empleado no existen")
                
                return detalle_cargo
        except BaseDatosError as error:
            raise error
        except Exception as error:
            print(f"ERROR AL OBTENER LOS DETALLES DEL CARGO: {error}")
    
    def obtener_por_cedula(self, cedula: str) -> Optional[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                detalle_cargo = sesion.execute(text(
                    """
                        SELECT
                            detalles_cargo.detalle_cargo_id,
                            empleados.cedula,
                            empleados.primer_nombre,
                            empleados.segundo_nombre,
                            empleados.tercer_nombre,
                            empleados.apellido_paterno,
                            empleados.apellido_materno,
                            tipos_cargo.tipo_cargo,
                            empleados.situacion
                        FROM tb_detalles_cargo AS detalles_cargo
                        INNER JOIN tb_empleados AS empleados ON detalles_cargo.empleado_id = empleados.empleado_id
                        INNER JOIN tb_tipos_cargo AS tipos_cargo ON detalles_cargo.tipo_cargo_id = tipos_cargo.tipo_cargo_id
                        WHERE empleados.situacion = 'Activo' AND empleados.cedula = :cedula;
                    """
                ), {"cedula": cedula}).fetchone()
                
                if not(detalle_cargo):
                    raise BaseDatosError("DETALLE_CARGO_NO_EXISTE", "Este empleado no existe")
                
                return detalle_cargo
        except BaseDatosError as error:
            raise error
        except Exception as error:
            print(f"ERROR AL OBTENER AL EMPLEADO POR CÉDULA: {error}")
    
    def obtener_por_tipo_cargo(self, tipo_cargo_id: int, situacion: str) -> List[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                detalles_cargo = sesion.execute(text(
                    """
                        SELECT
                            detalles_cargo.detalle_cargo_id,
                            empleados.cedula,
                            empleados.primer_nombre,
                            empleados.segundo_nombre,
                            empleados.tercer_nombre,
                            empleados.apellido_paterno,
                            empleados.apellido_materno,
                            tipos_cargo.tipo_cargo,
                            empleados.situacion
                        FROM tb_detalles_cargo AS detalles_cargo
                        INNER JOIN tb_empleados AS empleados ON detalles_cargo.empleado_id = empleados.empleado_id
                        INNER JOIN tb_tipos_cargo AS tipos_cargo ON detalles_cargo.tipo_cargo_id = tipos_cargo.tipo_cargo_id
                        WHERE empleados.situacion = :situacion AND tipos_cargo.tipo_cargo_id = :tipo_cargo_id;
                    """
                ), {"tipo_cargo_id": tipo_cargo_id, "situacion": situacion}).fetchall()
                
                if not(detalles_cargo):
                    raise BaseDatosError("DETALLE_CARGO_NO_EXISTE", f"No hay empleados con este tipo de cargo y que sean {situacion}")
                
                return detalles_cargo
        except BaseDatosError as error:
            raise error
        except Exception as error:
            print(f"ERROR AL OBTENER AL EMPLEADO POR TIPO DE CARGO: {error}")
    
    def obtener_por_especialidad(self, especialidad_id: int, situacion: str = "Activo") -> List[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                detalles_cargo = sesion.execute(text(
                    """
                        SELECT
                            detalles_cargo.detalle_cargo_id,
                            especialidades.especialidad_id,
                            empleados.cedula,
                            empleados.primer_nombre,
                            empleados.segundo_nombre,
                            empleados.tercer_nombre,
                            empleados.apellido_paterno,
                            empleados.apellido_materno,
                            tipos_cargo.tipo_cargo,
                            empleados.situacion
                        FROM tb_detalles_cargo AS detalles_cargo
                        INNER JOIN tb_empleados AS empleados ON detalles_cargo.empleado_id = empleados.empleado_id
                        INNER JOIN tb_tipos_cargo AS tipos_cargo ON detalles_cargo.tipo_cargo_id = tipos_cargo.tipo_cargo_id
                        INNER JOIN tb_especialidades AS especialidades ON detalles_cargo.especialidad_id = especialidades.especialidad_id
                        WHERE empleados.situacion = :situacion AND especialidades.especialidad_id = :especialidad_id;
                    """
                ), {"especialidad_id": especialidad_id, "situacion": situacion}).fetchall()
                
                if not(detalles_cargo):
                    raise BaseDatosError("DETALLE_CARGO_NO_EXISTE", f"No hay empleados que imparten esta especialidad y que sean {situacion}")
                
                return detalles_cargo
        except BaseDatosError as error:
            raise error
        except Exception as error:
            print(f"ERROR AL OBTENER AL EMPLEADO POR TIPO DE CARGO: {error}")
    
    def obtener_por_tipo_cargo_o_especialidad_o_cedula(self, tipo_cargo_id: int, especialidad_id: int = None, cedula: str = None, situacion: str = "Activo") -> Union[List[Tuple], Tuple]:
        try:
            if (cedula):
                if (self.obtener_por_cedula(cedula)):
                    return self.obtener_por_cedula(cedula)
            
            if ((tipo_cargo_id) and (especialidad_id)):
                if ((self.obtener_por_tipo_cargo(tipo_cargo_id, situacion)) and (self.obtener_por_especialidad(especialidad_id, situacion))):
                    return self.obtener_por_especialidad(especialidad_id, situacion)
            
            if (tipo_cargo_id):
                if (self.obtener_por_tipo_cargo(tipo_cargo_id, situacion)):
                    return self.obtener_por_tipo_cargo(tipo_cargo_id, situacion)
        except BaseDatosError as error:
            raise error
        except Exception as error:
            print(f"ERROR AL OBTENER AL EMPLEADO POR TIPO DE CARGO O ESPECIALIDAD O CÉDULA: {error}")
    
    def obtener_detalles_cargo_empleados(self) -> List[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                detalle_cargo = sesion.execute(text(
                    """
                        SELECT
                            empleados.empleado_id,
                            cargos_empleados.codigo_cargo,
                            cargos_empleados.cargo,
                            funciones_cargo.funcion_cargo,
                            tipos_cargo.tipo_cargo,
                            detalles_cargo.titulo_cargo,
                            detalles_cargo.labores_cargo,
                            empleados.fecha_ingreso_institucion,
                            empleados.fecha_ingreso_ministerio,
                            STRFTIME('%Y', 'NOW', 'LOCALTIME') - STRFTIME('%Y', empleados.fecha_ingreso_ministerio) -
                            CASE 
                                WHEN STRFTIME('%m', 'NOW', 'LOCALTIME') < STRFTIME('%m', empleados.fecha_ingreso_ministerio) AND STRFTIME('%d', 'NOW', 'LOCALTIME') = STRFTIME('%d', empleados.fecha_ingreso_ministerio) THEN 1
                                WHEN STRFTIME('%m', 'NOW', 'LOCALTIME') = STRFTIME('%m', empleados.fecha_ingreso_ministerio) AND STRFTIME('%d', 'NOW', 'LOCALTIME') < STRFTIME('%d', empleados.fecha_ingreso_ministerio) THEN 1
                                WHEN STRFTIME('%m', 'NOW', 'LOCALTIME') < STRFTIME('%m', empleados.fecha_ingreso_ministerio) AND STRFTIME('%d', 'NOW', 'LOCALTIME') < STRFTIME('%d', empleados.fecha_ingreso_ministerio) THEN 1
                                ELSE 0
                            END AS tiempo_servicio,
                            especialidades.especialidad
                        FROM tb_detalles_cargo AS detalles_cargo
                        INNER JOIN tb_empleados AS empleados ON detalles_cargo.empleado_id = empleados.empleado_id
                        INNER JOIN tb_cargos_empleados AS cargos_empleados ON detalles_cargo.cargo_id = cargos_empleados.cargo_id
                        INNER JOIN tb_funciones_cargo AS funciones_cargo ON detalles_cargo.funcion_cargo_id = funciones_cargo.funcion_cargo_id
                        INNER JOIN tb_tipos_cargo AS tipos_cargo ON detalles_cargo.tipo_cargo_id = tipos_cargo.tipo_cargo_id
                        LEFT JOIN tb_especialidades AS especialidades ON detalles_cargo.especialidad_id = especialidades.especialidad_id;
                    """
                )).fetchall()
                
                return detalle_cargo
        except Exception as error:
            print(f"ERROR AL OBTENER LOS DETALLES DEL CARGO: {error}")
    
    def obtener_detalles_cargo(self, empleado_id: int) -> Tuple:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                detalle_cargo = sesion.execute(text(
                    """
                        SELECT
                            empleados.empleado_id,
                            cargos_empleados.codigo_cargo,
                            cargos_empleados.cargo,
                            funciones_cargo.funcion_cargo,
                            tipos_cargo.tipo_cargo,
                            detalles_cargo.titulo_cargo,
                            detalles_cargo.labores_cargo,
                            empleados.fecha_ingreso_institucion,
                            empleados.fecha_ingreso_ministerio,
                            STRFTIME('%Y', 'NOW', 'LOCALTIME') - STRFTIME('%Y', empleados.fecha_ingreso_ministerio) -
                            CASE 
                                WHEN STRFTIME('%m', 'NOW', 'LOCALTIME') < STRFTIME('%m', empleados.fecha_ingreso_ministerio) AND STRFTIME('%d', 'NOW', 'LOCALTIME') = STRFTIME('%d', empleados.fecha_ingreso_ministerio) THEN 1
                                WHEN STRFTIME('%m', 'NOW', 'LOCALTIME') = STRFTIME('%m', empleados.fecha_ingreso_ministerio) AND STRFTIME('%d', 'NOW', 'LOCALTIME') < STRFTIME('%d', empleados.fecha_ingreso_ministerio) THEN 1
                                WHEN STRFTIME('%m', 'NOW', 'LOCALTIME') < STRFTIME('%m', empleados.fecha_ingreso_ministerio) AND STRFTIME('%d', 'NOW', 'LOCALTIME') < STRFTIME('%d', empleados.fecha_ingreso_ministerio) THEN 1
                                ELSE 0
                            END AS tiempo_servicio,
                            especialidades.especialidad
                        FROM tb_detalles_cargo AS detalles_cargo
                        INNER JOIN tb_empleados AS empleados ON detalles_cargo.empleado_id = empleados.empleado_id
                        INNER JOIN tb_cargos_empleados AS cargos_empleados ON detalles_cargo.cargo_id = cargos_empleados.cargo_id
                        INNER JOIN tb_funciones_cargo AS funciones_cargo ON detalles_cargo.funcion_cargo_id = funciones_cargo.funcion_cargo_id
                        INNER JOIN tb_tipos_cargo AS tipos_cargo ON detalles_cargo.tipo_cargo_id = tipos_cargo.tipo_cargo_id
                        LEFT JOIN tb_especialidades AS especialidades ON detalles_cargo.especialidad_id = especialidades.especialidad_id
                        WHERE empleados.empleado_id = :empleado_id;
                    """
                ), {"empleado_id": empleado_id}).fetchone()
                
                return detalle_cargo
        except Exception as error:
            print(f"ERROR AL OBTENER LOS DETALLES DEL CARGO: {error}")
    
    def conteo_empleados_por_funcion_cargo(self) -> List[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                consulta = "SELECT * FROM vw_conteo_tipo_personal;"
                
                conteo_empleados_funcion_cargo = sesion.execute(text(consulta)).fetchall()
                
                return conteo_empleados_funcion_cargo
        except Exception as error:
            print(f"ERROR AL OBTENER EL CONTEO DE EMPLEADOS POR FUNCION DE CARGO: {error}")
    
    def conteo_matricula_empleados(self) -> List[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                consulta = """
                    SELECT
                        SUM(CASE WHEN empleados.sexo = 'M' THEN 1 ELSE 0 END) AS total_varones,
                        SUM(CASE WHEN empleados.sexo = 'F' THEN 1 ELSE 0 END) AS total_hembras,
                        (SUM(CASE WHEN empleados.sexo = 'M' THEN 1 ELSE 0 END)) + (SUM(CASE WHEN empleados.sexo = 'F' THEN 1 ELSE 0 END)) AS total_general
                    FROM tb_empleados AS empleados;
                """
                
                conteo_empleados_matricula = sesion.execute(text(consulta)).fetchall()
                
                return conteo_empleados_matricula
        except Exception as error:
            print(f"ERROR AL OBTENER LA MATRICULA DE LOS EMPLEADOS: {error}")

    def actualizar(self, empleado_id: int, campos_detalle_cargo: Dict) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                detalle_cargo = sesion.query(DetalleCargo).filter(DetalleCargo.empleado_id == empleado_id).first()
                empleado = sesion.query(Empleado).filter(Empleado.empleado_id == empleado_id).first()
                diccionario_detalles_cargo = {campo: valor for campo, valor in vars(detalle_cargo).items() if not(campo.startswith("_")) and not(campo == "detalle_cargo_id") and not(campo == "empleado_id")}
                
                (cargo_empleado_anterior,) = sesion.execute(text(
                    """
                        SELECT
                            cargos_empleados.cargo
                        FROM tb_detalles_cargo AS detalles_cargo
                        INNER JOIN tb_cargos_empleados AS cargos_empleados ON detalles_cargo.cargo_id = cargos_empleados.cargo_id
                        INNER JOIN tb_empleados AS empleados ON detalles_cargo.empleado_id = empleados.empleado_id
                        WHERE empleados.empleado_id = :empleado_id;
                    """
                ), {"empleado_id": empleado_id}).fetchone()
                
                (funcion_cargo_anterior,) = sesion.execute(text(
                    """
                        SELECT
                            funciones_cargo.funcion_cargo
                        FROM tb_detalles_cargo AS detalles_cargo
                        INNER JOIN tb_funciones_cargo AS funciones_cargo ON detalles_cargo.funcion_cargo_id = funciones_cargo.funcion_cargo_id
                        INNER JOIN tb_empleados AS empleados ON detalles_cargo.empleado_id = empleados.empleado_id
                        WHERE empleados.empleado_id = :empleado_id;
                    """
                ), {"empleado_id": empleado_id}).fetchone()
                
                (tipo_cargo_anterior,) = sesion.execute(text(
                    """
                        SELECT
                            tipos_cargo.tipo_cargo
                        FROM tb_detalles_cargo AS detalles_cargo
                        INNER JOIN tb_tipos_cargo AS tipos_cargo ON detalles_cargo.tipo_cargo_id = tipos_cargo.tipo_cargo_id
                        INNER JOIN tb_empleados AS empleados ON detalles_cargo.empleado_id = empleados.empleado_id
                        WHERE empleados.empleado_id = :empleado_id;
                    """
                ), {"empleado_id": empleado_id}).fetchone()
                
                (especialidad_anterior,) = sesion.execute(text(
                    """
                        SELECT
                            especialidades.especialidad
                        FROM tb_detalles_cargo AS detalles_cargo
                        INNER JOIN tb_especialidades AS especialidades ON detalles_cargo.especialidad_id = especialidades.especialidad_id
                        INNER JOIN tb_empleados AS empleados ON detalles_cargo.empleado_id = empleados.empleado_id
                        WHERE empleados.empleado_id = :empleado_id;
                    """
                ), {"empleado_id": empleado_id}).fetchone()
                
                if not(especialidad_anterior):
                    especialidad_anterior = ""
                
                campos = {
                    "cargo_id": "CARGO",
                    "funcion_cargo_id": "FUNCIÓN DEL CARGO",
                    "tipo_cargo_id": "TIPO DE CARGO",
                    "especialidad_id": "ESPECIALIDAD QUE IMPARTE",
                    "titulo_cargo": "TÍTULO DEL CARGO",
                    "labores_cargo": "LABORES DEL CARGO"
                }
                
                for clave in diccionario_detalles_cargo.keys():
                    if not(campos_detalle_cargo.get(clave) == diccionario_detalles_cargo.get(clave)):
                        campo_actualizado = campos.get(clave)
                        
                        nuevo_cargo_id = campos_detalle_cargo.get("cargo_id")
                        nueva_funcion_cargo_id = campos_detalle_cargo.get("funcion_cargo_id")
                        nuevo_tipo_cargo_id = campos_detalle_cargo.get("tipo_cargo_id")
                        nueva_especialidad_id = campos_detalle_cargo.get("especialidad_id")
                        
                        if (clave == "cargo_id"):
                            (cargo_empleado_actual,) = sesion.query(CargoEmpleado.cargo).filter(CargoEmpleado.cargo_id == nuevo_cargo_id).first()
                            accion = f"ACTUALIZÓ EL CAMPO: {campo_actualizado}. ANTES: {cargo_empleado_anterior}. AHORA: {cargo_empleado_actual}. CÉDULA DEL EMPLEADO AFECTADO: {empleado.cedula}"
                            
                            sesion.query(DetalleCargo).filter(DetalleCargo.empleado_id == empleado_id).update({clave: nuevo_cargo_id})
                            sesion.commit()
                        elif (clave == "funcion_cargo_id"):
                            (funcion_cargo_actual,) = sesion.query(FuncionCargo.funcion_cargo).filter(FuncionCargo.funcion_cargo_id == nueva_funcion_cargo_id).first()
                            accion = f"ACTUALIZÓ EL CAMPO: {campo_actualizado}. ANTES: {funcion_cargo_anterior}. AHORA: {funcion_cargo_actual}. CÉDULA DEL EMPLEADO AFECTADO: {empleado.cedula}"
                            
                            sesion.query(DetalleCargo).filter(DetalleCargo.empleado_id == empleado_id).update({clave: nueva_funcion_cargo_id})
                            sesion.commit()
                        elif (clave == "tipo_cargo_id"):
                            (tipo_cargo_actual,) = sesion.query(TipoCargo.tipo_cargo).filter(TipoCargo.tipo_cargo_id == nuevo_tipo_cargo_id).first()
                            accion = f"ACTUALIZÓ EL CAMPO: {campo_actualizado}. ANTES: {tipo_cargo_anterior}. AHORA: {tipo_cargo_actual}. CÉDULA DEL EMPLEADO AFECTADO: {empleado.cedula}"
                            
                            sesion.query(DetalleCargo).filter(DetalleCargo.empleado_id == empleado_id).update({clave: nuevo_tipo_cargo_id})
                            sesion.commit()
                        elif (clave == "especialidad_id"):
                            if (nueva_especialidad_id):
                                (especialidad_actual,) = sesion.query(Especialidad.especialidad).filter(Especialidad.especialidad_id == nueva_especialidad_id).first()
                            else:
                                especialidad_actual = ""
                            accion = f"ACTUALIZÓ EL CAMPO: {campo_actualizado}. ANTES: {especialidad_anterior}. AHORA: {especialidad_actual}. CÉDULA DEL EMPLEADO AFECTADO: {empleado.cedula}"
                            
                            sesion.query(DetalleCargo).filter(DetalleCargo.empleado_id == empleado_id).update({clave: nueva_especialidad_id})
                            sesion.commit()
                        else:
                            valor_campo_anterior = diccionario_detalles_cargo.get(clave) if diccionario_detalles_cargo.get(clave) else ""
                            valor_campo_actual = campos_detalle_cargo.get(clave)
                            accion = f"ACTUALIZÓ EL CAMPO: {campo_actualizado}. ANTES: {valor_campo_anterior}. AHORA: {valor_campo_actual}. CÉDULA DEL EMPLEADO AFECTADO: {empleado.cedula}"
                            
                            sesion.query(DetalleCargo).filter(DetalleCargo.empleado_id == empleado_id).update({clave: valor_campo_actual})
                            sesion.commit()
                            
                        auditoria_repositorio.registrar(self.entidad, accion)
                        print(f"Se actualizó el campo: {campo_actualizado} correctamente \n")
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL ACTUALIZAR LOS CAMPOS: {error}")


if __name__ == "__main__":
    detalle_cargo_repositorio = DetalleCargoRepositorio()
    
    """campos_detalle_cargo = {
        "empleado_id": 7,
        "cargo_id": 1,
        "funcion_cargo_id": 1,
        "especialidad_id": 1,
        "tipo_cargo_id": 1,
        "titulo_cargo": "BACHILLER",
        "labores_cargo": None
    }
    
    detalle_cargo_repositorio.registrar(campos_detalle_cargo)"""
    
    """todos_detalles_cargo = detalle_cargo_repositorio.obtener_todos()
    
    for detalle_cargo in todos_detalles_cargo:
        print(detalle_cargo)"""
    
    
    """try:
        todos_empleados = detalle_cargo_repositorio.obtener_por_tipo_cargo_o_especialidad_o_cedula(2, 1, "18128319")
        if (type(todos_empleados) == list):
            for registro in todos_empleados:
                print(registro)
        else:
            print(todos_empleados)
    except BaseDatosError as error:
        print(error)"""
    
    """campos_detalle_cargo = {
        "cargo_id": 1,
        "funcion_cargo_id": 1,
        "tipo_cargo_id": 2,
        "especialidad_id": 1,
        "titulo_cargo": "LICENCIADO",
        "labores_cargo": None
    }
    
    detalle_cargo_repositorio.actualizar(4, campos_detalle_cargo)"""
    
    """try:
        empleados = detalle_cargo_repositorio.obtener_por_tipo_cargo_o_especialidad_o_cedula(2, None, None, "Activo")
        print(empleados)
    except BaseDatosError as error:
        print(error)"""