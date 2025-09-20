from typing import Tuple, List, Optional, Dict
from repositorios.repositorio_base import RepositorioBase
from datetime import date
from excepciones.base_datos_error import BaseDatosError
from sqlalchemy import text
from modelos import Alumno, Representante, Inscripcion
from repositorios.usuarios.auditoria_repositorio import auditoria_repositorio
from repositorios.alumnos.representante_repositorio import representante_repositorio
from conexiones.conexion import conexion_bd


class AlumnoRepositorio(RepositorioBase):
    def __init__(self):
        self.conexion_bd = conexion_bd
        self.entidad = "ALUMNOS"
    
    def registrar(self, campos: Dict) -> int:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                nuevo_alumno = Alumno(**campos)
                
                sesion.add(nuevo_alumno)
                sesion.commit()
                sesion.refresh(nuevo_alumno)
                print("Se registró el alumno correctamente")
                return nuevo_alumno.alumno_id
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL REGISTRAR EL ALUMNO: {error}")
    
    def obtener_todos(self) -> List[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                consulta = """
                    SELECT 
                        alumnos.alumno_id,
                        alumnos.cedula,
                        alumnos.primer_nombre,
                        alumnos.segundo_nombre,
                        alumnos.tercer_nombre,
                        alumnos.apellido_paterno,
                        alumnos.apellido_materno,
                        alumnos.fecha_nacimiento,
                        STRFTIME('%Y', 'NOW', 'LOCALTIME') - STRFTIME('%Y', alumnos.fecha_nacimiento) -
                        CASE 
                            WHEN STRFTIME('%m', 'NOW', 'LOCALTIME') < STRFTIME('%m', alumnos.fecha_nacimiento) AND STRFTIME('%d', 'NOW', 'LOCALTIME') = STRFTIME('%d', alumnos.fecha_nacimiento) THEN 1
                            WHEN STRFTIME('%m', 'NOW', 'LOCALTIME') = STRFTIME('%m', alumnos.fecha_nacimiento) AND STRFTIME('%d', 'NOW', 'LOCALTIME') < STRFTIME('%d', alumnos.fecha_nacimiento) THEN 1
                            WHEN STRFTIME('%m', 'NOW', 'LOCALTIME') < STRFTIME('%m', alumnos.fecha_nacimiento) AND STRFTIME('%d', 'NOW', 'LOCALTIME') < STRFTIME('%d', alumnos.fecha_nacimiento) THEN 1
                            ELSE 0
                        END AS edad,
                        alumnos.lugar_nacimiento,
                        alumnos.sexo,
                        alumnos.cma,
                        alumnos.imt,
                        alumnos.fecha_ingreso_institucion,
                        alumnos.situacion
                    FROM tb_alumnos AS alumnos
                    WHERE alumnos.situacion = 'Ingresado' OR alumnos.situacion = 'Inicial';
                """
                alumnos = sesion.execute(text(consulta)).fetchall()
                
                return alumnos
        except Exception as error:
            print(f"ERROR AL OBTENER LOS ALUMNOS: {error}")
    
    def obtener_por_id(self, alumno_id: int) -> Optional[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                consulta = """
                    SELECT 
                        alumnos.alumno_id,
                        alumnos.cedula,
                        alumnos.primer_nombre,
                        alumnos.segundo_nombre,
                        alumnos.tercer_nombre,
                        alumnos.apellido_paterno,
                        alumnos.apellido_materno,
                        alumnos.fecha_nacimiento,
                        STRFTIME('%Y', 'NOW', 'LOCALTIME') - STRFTIME('%Y', alumnos.fecha_nacimiento) -
                        CASE 
                            WHEN STRFTIME('%m', 'NOW', 'LOCALTIME') < STRFTIME('%m', alumnos.fecha_nacimiento) AND STRFTIME('%d', 'NOW', 'LOCALTIME') = STRFTIME('%d', alumnos.fecha_nacimiento) THEN 1
                            WHEN STRFTIME('%m', 'NOW', 'LOCALTIME') = STRFTIME('%m', alumnos.fecha_nacimiento) AND STRFTIME('%d', 'NOW', 'LOCALTIME') < STRFTIME('%d', alumnos.fecha_nacimiento) THEN 1
                            WHEN STRFTIME('%m', 'NOW', 'LOCALTIME') < STRFTIME('%m', alumnos.fecha_nacimiento) AND STRFTIME('%d', 'NOW', 'LOCALTIME') < STRFTIME('%d', alumnos.fecha_nacimiento) THEN 1
                            ELSE 0
                        END AS edad,
                        alumnos.lugar_nacimiento,
                        alumnos.sexo,
                        alumnos.cma,
                        alumnos.imt,
                        alumnos.fecha_ingreso_institucion,
                        alumnos.situacion
                    FROM tb_alumnos AS alumnos
                    WHERE (alumnos.situacion = 'Ingresado' OR alumnos.situacion = 'Inicial') AND alumnos.alumno_id = :alumno_id;
                """
                alumno = sesion.execute(text(consulta), {"alumno_id": alumno_id}).fetchone()
                
                if not(alumno):
                    raise BaseDatosError("ALUMNO_NO_EXISTE", "Este alumno no existe")
                
                return alumno
        except BaseDatosError as error:
            raise error
        except Exception as error:
            print(f"ERROR AL OBTENER EL ALUMNO: {error}")
    
    def obtener_por_cedula(self, cedula: str) -> Optional[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                consulta = """
                    SELECT 
                        alumnos.alumno_id,
                        alumnos.cedula,
                        alumnos.primer_nombre,
                        alumnos.segundo_nombre,
                        alumnos.tercer_nombre,
                        alumnos.apellido_paterno,
                        alumnos.apellido_materno,
                        alumnos.fecha_nacimiento,
                        STRFTIME('%Y', 'NOW', 'LOCALTIME') - STRFTIME('%Y', alumnos.fecha_nacimiento) -
                        CASE 
                            WHEN STRFTIME('%m', 'NOW', 'LOCALTIME') < STRFTIME('%m', alumnos.fecha_nacimiento) AND STRFTIME('%d', 'NOW', 'LOCALTIME') = STRFTIME('%d', alumnos.fecha_nacimiento) THEN 1
                            WHEN STRFTIME('%m', 'NOW', 'LOCALTIME') = STRFTIME('%m', alumnos.fecha_nacimiento) AND STRFTIME('%d', 'NOW', 'LOCALTIME') < STRFTIME('%d', alumnos.fecha_nacimiento) THEN 1
                            WHEN STRFTIME('%m', 'NOW', 'LOCALTIME') < STRFTIME('%m', alumnos.fecha_nacimiento) AND STRFTIME('%d', 'NOW', 'LOCALTIME') < STRFTIME('%d', alumnos.fecha_nacimiento) THEN 1
                            ELSE 0
                        END AS edad,
                        alumnos.lugar_nacimiento,
                        alumnos.sexo,
                        alumnos.cma,
                        alumnos.imt,
                        alumnos.fecha_ingreso_institucion,
                        alumnos.situacion
                    FROM tb_alumnos AS alumnos
                    WHERE (alumnos.situacion = 'Ingresado' OR alumnos.situacion = 'Inicial') AND alumnos.cedula = :cedula;
                """
                alumno = sesion.execute(text(consulta), {"cedula": cedula}).fetchone()
                return alumno
        except Exception as error:
            print(f"ERROR AL OBTENER EL ALUMNO: {error}")
    
    def obtener_datos_representante(self, alumno_id: int) -> Tuple:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                representante_alumno = sesion.query(
                    Alumno.alumno_id,
                    Representante.representante_id,
                    Representante.cedula,
                    Representante.nombre,
                    Representante.apellido,
                    Representante.direccion_residencia,
                    Representante.num_telefono,
                    Representante.num_telefono_adicional,
                    Representante.carga_familiar,
                    Representante.estado_civil
                ).join(Alumno.representante).filter(Alumno.alumno_id == alumno_id).first()
                
                return representante_alumno
        except Exception as error:
            print(f"ERROR AL OBTENER LOS DATOS DEL REPRESENTANTE DEL ALUMNO: {error}")
    
    def obtener_info_academica(self, alumno_id: int) -> Tuple:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                info_academica = sesion.query(
                    Alumno.alumno_id,
                    Alumno.escolaridad,
                    Alumno.procedencia
                ).filter_by(alumno_id = alumno_id).first()
                
                return info_academica
        except Exception as error:
            print(f"ERROR AL OBTENER LA INFO ACADÉMICA DEL ALUMNO: {error}")
    
    def actualizar(self, alumno_id: int, campos_alumno: Dict) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                alumno = sesion.query(Alumno).filter_by(alumno_id = alumno_id).first()
                representante_alumno = sesion.query(Representante).join(Alumno.representante).filter(Alumno.alumno_id == alumno_id).first()
                inscripcion_alumno = sesion.query(Inscripcion).join(Inscripcion.alumno).filter(Inscripcion.alumno_id == alumno_id).first()
                diccionario_alumno = {campo: valor for campo, valor in vars(alumno).items() if not(campo.startswith("_")) and not(campo == "alumno_id")}
                
                campos = {
                    "representante_id": "REPRESENTANTE",
                    "cedula": "CÉDULA",
                    "primer_nombre": "PRIMER NOMBRE",
                    "segundo_nombre": "SEGUNDO NOMBRE",
                    "tercer_nombre": "TERCER NOMBRE",
                    "apellido_paterno": "APELLIDO PATERNO",
                    "apellido_materno": "APELLIDO MATERNO",
                    "fecha_nacimiento": "FECHA DE NACIMIENTO",
                    "lugar_nacimiento": "LUGAR DE NACIMIENTO",
                    "sexo": "SEXO",
                    "cma": "CMA",
                    "imt": "IMT",
                    "fecha_ingreso_institucion": "FECHA DE INGRESO A LA INSTITUCIÓN",
                    "relacion_con_rep": "RELACIÓN CON SU REPRESENTANTE",
                    "escolaridad": "ESCOLARIDAD",
                    "procedencia": "PROCEDENCIA",
                    "situacion": "SITUACIÓN"
                }
                
                for clave in diccionario_alumno.keys():
                    if not(campos_alumno.get(clave) == diccionario_alumno.get(clave)):
                        campo_actualizado = campos.get(clave)
                        
                        if (clave == "cma" or clave == "imt"):
                            valor_anterior = "SI" if (diccionario_alumno.get(clave) == 1) else "NO"
                            valor_actual = "SI" if (campos_alumno.get(clave) == 1) else "NO"
                            
                            valor_campo_anterior = diccionario_alumno.get(clave)
                            valor_campo_actual = campos_alumno.get(clave)
                            
                            accion = f"ACTUALIZÓ EL CAMPO: {campo_actualizado}. ANTES: {valor_anterior}. AHORA: {valor_actual}. MATRICULA: {inscripcion_alumno.num_matricula}"
                        elif (clave == "representante_id"):
                            valor_campo_anterior = diccionario_alumno.get(clave)
                            valor_campo_actual = campos_alumno.get(clave)
                            
                            nuevo_representante_id = campos_alumno.get("representante_id")
                            nuevo_representante = sesion.query(Representante).filter(Representante.representante_id == nuevo_representante_id).first()
                            
                            accion = f"ACTUALIZÓ EL CAMPO: {campo_actualizado}. ANTES: {representante_alumno.nombre} {representante_alumno.apellido}. AHORA: {nuevo_representante.nombre} {nuevo_representante.apellido}. MATRICULA: {inscripcion_alumno.num_matricula}"
                        else:
                            valor_campo_anterior = diccionario_alumno.get(clave) if (diccionario_alumno.get(clave)) else ""
                            valor_campo_actual = campos_alumno.get(clave)
                            
                            accion = f"ACTUALIZÓ EL CAMPO: {campo_actualizado}. ANTES: {valor_campo_anterior}. AHORA: {valor_campo_actual}. MATRICULA: {inscripcion_alumno.num_matricula}"
                        
                        auditoria_repositorio.registrar(self.entidad, accion)
                        
                        sesion.query(Alumno).filter_by(alumno_id = alumno_id).update({clave: valor_campo_actual})
                        sesion.commit()
                        print(f"Se actualizó el campo: {campo_actualizado} correctamente \n")
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL ACTUALIZAR LOS CAMPOS: {error}")
    
    def eliminar(self, alumno_id: int) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                alumno = sesion.query(Alumno).filter_by(alumno_id = alumno_id).first()
                representante = sesion.query(Representante).join(Alumno.representante).filter(Alumno.alumno_id == alumno_id).first()
                inscripcion_alumno = sesion.query(Inscripcion).join(Inscripcion.alumno).filter(Inscripcion.alumno_id == alumno_id).first()
                
                contador_alumnos_representados = len(representante_repositorio.obtener_alumnos_representados(representante.representante_id))
                
                if not(alumno):
                    raise BaseDatosError("ALUMNO_NO_EXISTE", "Este alumno no existe")
                
                if (contador_alumnos_representados == 1):
                    accion = f"ELIMINÓ A {alumno.primer_nombre} {alumno.apellido_paterno}. MATRICULA: {inscripcion_alumno.num_matricula}"
                    auditoria_repositorio.registrar(self.entidad, accion)
                    
                    accion_2 = f"ELIMINÓ A {representante.nombre} {representante.apellido}. CÉDULA DEL REPRESENTANTE AFECTADO: {representante.cedula}"
                    auditoria_repositorio.registrar(representante_repositorio.entidad, accion_2)
                    
                    sesion.delete(representante)
                    print("Se eliminó al representante correctamente")
                else:
                    accion = f"ELIMINÓ A {alumno.primer_nombre} {alumno.apellido_paterno}. MATRICULA: {inscripcion_alumno.num_matricula}"
                    auditoria_repositorio.registrar(self.entidad, accion)
                
                sesion.delete(alumno)
                sesion.commit()
                print("Se eliminó el alumno correctamente")
        except BaseDatosError as error:
            sesion.rollback()
            raise error
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL ELIMINAR AL ALUMNO: {error}")


if __name__ == "__main__":
    alumno_repositorio = AlumnoRepositorio()
    
    """campos_alumno = {
        "representante_id": 2,
        "cedula": "9821397",
        "primer_nombre": "ALEJANDRO",
        "segundo_nombre": None,
        "apellido_paterno": "CHACÓN",
        "apellido_materno": "CONTRERAS",
        "fecha_nacimiento": date(2004, 10, 11),
        "lugar_nacimiento": "PUERTO LA CRUZ",
        "sexo": None,
        "cma": None,
        "imt": None,
        "fecha_ingreso_institucion": date.today(),
        "relacion_con_rep": "PADRE",
        "escolaridad": "6to grado aprobado",
        "procedencia": None,
        "situacion": "Inicial"
    }
    
    alumno_repositorio.registrar(campos_alumno)"""
    
    """todos_alumnos = alumno_repositorio.obtener_todos()
    
    for registro in todos_alumnos:
        print(registro)"""
    
    #print(alumno_repositorio.obtener_datos_representante(17))
    #print(alumno_repositorio.obtener_por_id(5))
    #print(alumno_repositorio.obtener_datos_representante(3))
    #print(alumno_repositorio.obtener_info_academica(9))
    
    """campos_alumno = {
        "representante_id": 2,
        "cedula": "30932925",
        "primer_nombre": "GABRIEL",
        "segundo_nombre": "ALONSO",
        "apellido_paterno": "CHACÓN",
        "apellido_materno": "CONTRERAS",
        "fecha_nacimiento": date(2004, 10, 11),
        "lugar_nacimiento": "PUERTO LA CRUZ",
        "sexo": "M",
        "cma": 0,
        "imt": 0,
        "fecha_ingreso_institucion": date(2025, 1, 15),
        "relacion_con_rep": "PADRE",
        "escolaridad": "6to grado aprobado",
        "procedencia": "Foráneo/a",
        "situacion": "Inicial"
    }
    
    alumno_repositorio.actualizar(17, campos_alumno)"""
    
    #alumno_repositorio.eliminar(16)
    #alumno_repositorio.eliminar(19)
    #alumno_repositorio.eliminar(21)