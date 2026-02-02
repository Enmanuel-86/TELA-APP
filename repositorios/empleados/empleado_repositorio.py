from typing import Tuple, List, Optional, Dict
from datetime import date
from sqlalchemy import text
from excepciones.base_datos_error import BaseDatosError
from modelos import Empleado
from repositorios.usuarios.auditoria_repositorio import auditoria_repositorio
from repositorios.repositorio_base import RepositorioBase
from conexiones.conexion import conexion_bd
from recursos_graficos_y_logicos.utilidades.funciones_sistema import FuncionSistema


class EmpleadoRepositorio(RepositorioBase):
    def __init__(self):
        self.conexion_bd = conexion_bd
        self.entidad = "EMPLEADOS"
    
    def registrar(self, campos: Dict) -> int:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                ruta_foto_perfil = campos["foto_perfil"]
                foto_perfil = FuncionSistema.cargar_foto_perfil(ruta_foto_perfil)
                campos["foto_perfil"] = foto_perfil
                
                nuevo_empleado = Empleado(**campos)
                
                sesion.add(nuevo_empleado)
                sesion.commit()
                sesion.refresh(nuevo_empleado)
                print("Se registró el empleado correctamente")
                
                primer_nombre = campos.get("primer_nombre")
                apellido_paterno = campos.get("apellido_paterno")
                cedula = campos.get("cedula")
                
                accion = f"REGISTRÓ A {primer_nombre} {apellido_paterno}. CÉDULA: {cedula}"
                
                auditoria_repositorio.registrar(self.entidad, accion)
                
                return nuevo_empleado.empleado_id
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL REGISTRAR EL EMPLEADO: {error}")
    
    def obtener_todos(self) -> List[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                empleados = sesion.execute(text(
                    """
                        SELECT
                            empleado_id,
                            primer_nombre,
                            segundo_nombre,
                            tercer_nombre,
                            apellido_paterno,
                            apellido_materno,
                            cedula,
                            fecha_nacimiento,
                            STRFTIME('%Y', 'NOW', 'LOCALTIME') - STRFTIME('%Y', fecha_nacimiento) -
                            CASE
                                WHEN STRFTIME('%m', 'NOW', 'LOCALTIME') < STRFTIME('%m', fecha_nacimiento) AND STRFTIME('%d', 'NOW', 'LOCALTIME') = STRFTIME('%d', fecha_nacimiento) THEN 1
                                WHEN STRFTIME('%m', 'NOW', 'LOCALTIME') = STRFTIME('%m', fecha_nacimiento) AND STRFTIME('%d', 'NOW', 'LOCALTIME') < STRFTIME('%d', fecha_nacimiento) THEN 1
                                WHEN STRFTIME('%m', 'NOW', 'LOCALTIME') < STRFTIME('%m', fecha_nacimiento) AND STRFTIME('%d', 'NOW', 'LOCALTIME') < STRFTIME('%d', fecha_nacimiento) THEN 1
                                ELSE 0
                            END AS edad,
                            situacion,
                            sexo,
                            tiene_hijos_menores,
                            foto_perfil
                        FROM tb_empleados;
                    """
                )).fetchall()
                
                return empleados
        except Exception as error:
            print(f"ERROR AL OBTENER A LOS EMPLEADOS: {error}")
    
    def obtener_por_id(self, empleado_id: int) -> Optional[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                empleado = sesion.execute(text(
                    """
                        SELECT
                            empleado_id,
                            primer_nombre,
                            segundo_nombre,
                            tercer_nombre,
                            apellido_paterno,
                            apellido_materno,
                            cedula,
                            fecha_nacimiento,
                            STRFTIME('%Y', 'NOW', 'LOCALTIME') - STRFTIME('%Y', fecha_nacimiento) -
                            CASE
                                WHEN STRFTIME('%m', 'NOW', 'LOCALTIME') < STRFTIME('%m', fecha_nacimiento) AND STRFTIME('%d', 'NOW', 'LOCALTIME') = STRFTIME('%d', fecha_nacimiento) THEN 1
                                WHEN STRFTIME('%m', 'NOW', 'LOCALTIME') = STRFTIME('%m', fecha_nacimiento) AND STRFTIME('%d', 'NOW', 'LOCALTIME') < STRFTIME('%d', fecha_nacimiento) THEN 1
                                WHEN STRFTIME('%m', 'NOW', 'LOCALTIME') < STRFTIME('%m', fecha_nacimiento) AND STRFTIME('%d', 'NOW', 'LOCALTIME') < STRFTIME('%d', fecha_nacimiento) THEN 1
                                ELSE 0
                            END AS edad,
                            situacion,
                            sexo,
                            tiene_hijos_menores,
                            foto_perfil
                        FROM tb_empleados
                        WHERE empleado_id = :empleado_id;
                    """
                ), {"empleado_id": empleado_id}).fetchone()
                
                if not(empleado):
                    raise BaseDatosError("EMPLEADO_NO_EXISTE", "Este empleado no existe")
                
                return empleado
        except BaseDatosError as error:
            raise error
        except Exception as error:
            print(f"ERROR AL OBTENER EL EMPLEADO: {error}")
    
    def obtener_por_correo(self, correo_electronico: str) -> Optional[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                empleado = sesion.execute(text(
                    """
                        SELECT
                            empleado_id,
                            primer_nombre,
                            segundo_nombre,
                            tercer_nombre,
                            apellido_paterno,
                            apellido_materno,
                            cedula,
                            fecha_nacimiento,
                            STRFTIME('%Y', 'NOW', 'LOCALTIME') - STRFTIME('%Y', fecha_nacimiento) -
                            CASE
                                WHEN STRFTIME('%m', 'NOW', 'LOCALTIME') < STRFTIME('%m', fecha_nacimiento) AND STRFTIME('%d', 'NOW', 'LOCALTIME') = STRFTIME('%d', fecha_nacimiento) THEN 1
                                WHEN STRFTIME('%m', 'NOW', 'LOCALTIME') = STRFTIME('%m', fecha_nacimiento) AND STRFTIME('%d', 'NOW', 'LOCALTIME') < STRFTIME('%d', fecha_nacimiento) THEN 1
                                WHEN STRFTIME('%m', 'NOW', 'LOCALTIME') < STRFTIME('%m', fecha_nacimiento) AND STRFTIME('%d', 'NOW', 'LOCALTIME') < STRFTIME('%d', fecha_nacimiento) THEN 1
                                ELSE 0
                            END AS edad,
                            situacion,
                            sexo,
                            tiene_hijos_menores
                        FROM tb_empleados
                        WHERE correo_electronico = :correo_electronico;
                    """
                ), {"correo_electronico": correo_electronico}).fetchone()
                
                return empleado
        except Exception as error:
            print(f"ERROR AL OBTENER EL EMPLEADO: {error}")
    
    def obtener_por_correo_adicional(self, correo_electronico_adicional: str) -> Optional[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                empleado = sesion.execute(text(
                    """
                        SELECT
                            empleado_id,
                            primer_nombre,
                            segundo_nombre,
                            tercer_nombre,
                            apellido_paterno,
                            apellido_materno,
                            cedula,
                            fecha_nacimiento,
                            STRFTIME('%Y', 'NOW', 'LOCALTIME') - STRFTIME('%Y', fecha_nacimiento) -
                            CASE
                                WHEN STRFTIME('%m', 'NOW', 'LOCALTIME') < STRFTIME('%m', fecha_nacimiento) AND STRFTIME('%d', 'NOW', 'LOCALTIME') = STRFTIME('%d', fecha_nacimiento) THEN 1
                                WHEN STRFTIME('%m', 'NOW', 'LOCALTIME') = STRFTIME('%m', fecha_nacimiento) AND STRFTIME('%d', 'NOW', 'LOCALTIME') < STRFTIME('%d', fecha_nacimiento) THEN 1
                                WHEN STRFTIME('%m', 'NOW', 'LOCALTIME') < STRFTIME('%m', fecha_nacimiento) AND STRFTIME('%d', 'NOW', 'LOCALTIME') < STRFTIME('%d', fecha_nacimiento) THEN 1
                                ELSE 0
                            END AS edad,
                            situacion,
                            sexo,
                            tiene_hijos_menores
                        FROM tb_empleados
                        WHERE correo_electronico_adicional = :correo_electronico_adicional;
                    """
                ), {"correo_electronico_adicional": correo_electronico_adicional}).fetchone()
                
                return empleado
        except Exception as error:
            print(f"ERROR AL OBTENER EL EMPLEADO: {error}")
    
    def obtener_por_cedula(self, cedula: str) -> Optional[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                empleado = sesion.execute(text(
                    """
                        SELECT
                            empleado_id,
                            primer_nombre,
                            segundo_nombre,
                            tercer_nombre,
                            apellido_paterno,
                            apellido_materno,
                            cedula,
                            fecha_nacimiento,
                            STRFTIME('%Y', 'NOW', 'LOCALTIME') - STRFTIME('%Y', fecha_nacimiento) -
                            CASE
                                WHEN STRFTIME('%m', 'NOW', 'LOCALTIME') < STRFTIME('%m', fecha_nacimiento) AND STRFTIME('%d', 'NOW', 'LOCALTIME') = STRFTIME('%d', fecha_nacimiento) THEN 1
                                WHEN STRFTIME('%m', 'NOW', 'LOCALTIME') = STRFTIME('%m', fecha_nacimiento) AND STRFTIME('%d', 'NOW', 'LOCALTIME') < STRFTIME('%d', fecha_nacimiento) THEN 1
                                WHEN STRFTIME('%m', 'NOW', 'LOCALTIME') < STRFTIME('%m', fecha_nacimiento) AND STRFTIME('%d', 'NOW', 'LOCALTIME') < STRFTIME('%d', fecha_nacimiento) THEN 1
                                ELSE 0
                            END AS edad,
                            situacion,
                            sexo,
                            tiene_hijos_menores,
                            foto_perfil
                        FROM tb_empleados
                        WHERE cedula = :cedula;
                    """
                ), {"cedula": cedula}).fetchone()
                
                return empleado
        except Exception as error:
            print(f"ERROR AL OBTENER EL EMPLEADO: {error}")
            raise error
    
    def obtener_info_contacto(self, empleado_id: int) -> Tuple:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                info_contacto_empleado = sesion.execute(text(
                    """
                        SELECT
                            empleado_id,
                            num_telefono,
                            num_telefono_adicional,
                            correo_electronico,
                            correo_electronico_adicional
                        FROM tb_empleados
                        WHERE empleado_id = :empleado_id;
                    """
                ), {"empleado_id": empleado_id}).fetchone()
                
                return info_contacto_empleado
        except Exception as error:
            print(f"ERROR AL OBTENER LA INFORMACIÓN DE CONTACTO: {error}")
    
    def obtener_info_geografica(self, empleado_id: int) -> Tuple:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                info_geografica_empleado = sesion.execute(text(
                    """
                        SELECT
                            empleado_id,
                            estado_reside,
                            municipio,
                            direccion_residencia
                        FROM tb_empleados
                        WHERE empleado_id = :empleado_id;
                    """
                ), {"empleado_id": empleado_id}).fetchone()
                
                return info_geografica_empleado
        except Exception as error:
            print(f"ERROR AL OBTENER LA INFORMACIÓN GEOGRÁFICA: {error}")
    
    def obtener_medidas(self, empleado_id: int) -> Tuple:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                medidas_empleado = sesion.execute(text(
                    """
                        SELECT
                            empleado_id,
                            talla_camisa,
                            talla_pantalon,
                            talla_zapatos
                        FROM tb_empleados
                        WHERE empleado_id = :empleado_id;
                    """
                ), {"empleado_id": empleado_id}).fetchone()
                
                return medidas_empleado
        except Exception as error:
            print(f"ERROR AL OBTENER LAS MEDIDAS DEL EMPLEADO: {error}")
    
    def actualizar(self, empleado_id: int, campos_empleado: Dict) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                empleado = sesion.query(Empleado).filter(Empleado.empleado_id == empleado_id).first()
                diccionario_empleado = {campo: valor for campo, valor in vars(empleado).items() if not(campo.startswith("_")) and not(campo == "empleado_id")}
                
                campos = {
                    "cedula": "CÉDULA",
                    "primer_nombre": "PRIMER NOMBRE",
                    "segundo_nombre": "SEGUNDO NOMBRE",
                    "tercer_nombre": "TERCER NOMBRE",
                    "apellido_paterno": "APELLIDO PATERNO",
                    "apellido_materno": "APELLIDO MATERNO",
                    "fecha_nacimiento": "FECHA DE NACIMIENTO",
                    "sexo": "SEXO",
                    "tiene_hijos_menores": "TIENE HIJOS MENORES DE EDAD",
                    "fecha_ingreso_institucion": "FECHA DE INGRESO A LA INSTITUCIÓN",
                    "fecha_ingreso_ministerio": "FECHA DE INGRESO AL MINISTERIO",
                    "talla_camisa": "TALLA DE CAMISA",
                    "talla_pantalon": "TALLA DE PANTALÓN",
                    "talla_zapatos": "TALLA DE ZAPATOS",
                    "num_telefono": "NÚMERO DE TELÉFONO",
                    "correo_electronico": "CORREO ELECTRÓNICO",
                    "estado_reside": "ESTADO EN EL QUE RESIDE",
                    "municipio": "MUNICIPIO",
                    "direccion_residencia": "DIRECCIÓN DE RESIDENCIA",
                    "situacion": "SITUACIÓN",
                    "foto_perfil": "FOTO DE PERFIL"
                }
                
                for clave in diccionario_empleado.keys():
                    if not(campos_empleado.get(clave) == diccionario_empleado.get(clave)):
                        campo_actualizado = campos.get(clave)
                        cedula_empleado = empleado.cedula
                        
                        if (clave == "tiene_hijos_menores"):
                            valor_anterior = "SI" if (diccionario_empleado.get("tiene_hijos_menores") == 1) else "NO"
                            valor_actual = "SI" if (campos_empleado.get("tiene_hijos_menores") == 1) else "NO"
                            
                            valor_campo_actual = campos_empleado.get("tiene_hijos_menores")
                        elif (clave == "foto_perfil"):
                            ruta_foto_perfil = campos_empleado.get(clave)
                            foto_perfil = FuncionSistema.cargar_foto_perfil(ruta_foto_perfil)
                            
                            valor_campo_actual = foto_perfil
                            
                            accion = f"ACTUALIZÓ EL CAMPO: {campo_actualizado}. CÉDULA DEL EMPLEADO AFECTADO: {cedula_empleado}"
                        else:
                            valor_anterior = diccionario_empleado.get(clave)
                            valor_actual = campos_empleado.get(clave)
                            
                            valor_campo_actual = campos_empleado.get(clave)

                            accion = f"ACTUALIZÓ EL CAMPO: {campo_actualizado}. ANTES: {valor_anterior}. AHORA: {valor_actual}. CÉDULA DEL EMPLEADO AFECTADO: {cedula_empleado}"
                            
                        auditoria_repositorio.registrar(self.entidad, accion)
                        
                        sesion.query(Empleado).filter(Empleado.empleado_id == empleado_id).update({clave: valor_campo_actual})
                        sesion.commit()
                        print(f"Se actualizó el campo: {campo_actualizado} correctamente \n")
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL ACTUALIZAR LOS CAMPOS: {error}")
    
    def eliminar(self, empleado_id: int) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                empleado = sesion.query(Empleado).filter(Empleado.empleado_id == empleado_id).first()
                
                if not(empleado):
                    raise BaseDatosError("EMPLEADO_NO_EXISTE", "Este empleado no existe")
                
                usuario_asociado = empleado.usuario
                
                if usuario_asociado:
                    raise BaseDatosError("USUARIO_ASOCIADO", "Este empleado está asociado a un usuario y no puede ser eliminado")
                
                accion = f"ELIMINÓ A {empleado.primer_nombre} {empleado.apellido_paterno}. CÉDULA: {empleado.cedula}"
                
                auditoria_repositorio.registrar(self.entidad, accion)
                
                sesion.delete(empleado)
                sesion.commit()
                print("Se eliminó al empleado correctamente")
        except BaseDatosError as error:
            sesion.rollback()
            raise error
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL ELIMINAR AL EMPLEADO: {error}")


if __name__ == "__main__":
    empleado_repositorio = EmpleadoRepositorio()
    
    """nuevo_empleado = {
        "cedula": "30932925",
        "primer_nombre": "GABRIEL",
        "segundo_nombre": None,
        "apellido_paterno": "CHACÓN",
        "apellido_materno": None,
        "fecha_nacimiento": date(2004, 10, 11),
        "sexo": None,
        "tiene_hijos_menores": None,
        "fecha_ingreso_institucion": None,
        "fecha_ingreso_ministerio": date(2025, 1, 10),
        "talla_camisa": "S",
        "talla_pantalon": 30,
        "talla_zapatos": 45,
        "num_telefono": None,
        "correo_electronico": "alonsochacon@gmail.com",
        "estado_reside": "ANZOÁTEGUI",
        "municipio": "SIMÓN BOLÍVAR",
        "direccion_residencia": "BOYACA 2",
        "situacion": None
    }
    
    empleado_repositorio.registrar(nuevo_empleado)"""
    
    """todos_empleados = empleado_repositorio.obtener_todos()
    
    for empleado in todos_empleados:
        print(empleado)"""
    
    #print(empleado_repositorio.obtener_por_id(3))
    #print(empleado_repositorio.obtener_por_id(5))
    
    #empleado_repositorio.actualizar_correo_electronico(5, "gabrielalonso@gmail.com")
    
    #empleado_repositorio.eliminar(6)
    
    """campos_empleado = {
        "cedula": "30932925",
        "primer_nombre": "GABRIEL",
        "segundo_nombre": "ALONSO",
        "apellido_paterno": "CHACÓN",
        "apellido_materno": "CONTRERAS",
        "fecha_nacimiento": date(2004, 10, 11),
        "sexo": "M",
        "tiene_hijos_menores": 0,
        "fecha_ingreso_institucion": date(2025, 5, 5),
        "fecha_ingreso_ministerio": date(2025, 1, 10),
        "talla_camisa": "S",
        "talla_pantalon": 31,
        "talla_zapatos": 45,
        "num_telefono": "No tiene",
        "correo_electronico": "alonsochacon@gmail.com",
        "estado_reside": "ANZOÁTEGUI",
        "municipio": "SIMÓN BOLÍVAR",
        "direccion_residencia": "BOYACA 4",
        "situacion": "Activo"
    }
    
    empleado_repositorio.actualizar(7, campos_empleado)"""