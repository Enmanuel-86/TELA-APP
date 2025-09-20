from typing import Tuple, List, Optional, Dict, Union
from datetime import date
from uuid import uuid4
from excepciones.base_datos_error import BaseDatosError
from modelos import Inscripcion, Alumno, Especialidad
from repositorios.usuarios.auditoria_repositorio import auditoria_repositorio
from repositorios.repositorio_base import RepositorioBase
from conexiones.conexion import conexion_bd
from sqlalchemy import text


class InscripcionRepositorio(RepositorioBase):
    def __init__(self):
        self.conexion_bd = conexion_bd
        self.entidad = "ALUMNOS"
    
    def registrar(self, campos: Dict) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                num_matricula = self.generar_num_matricula()
                campos["num_matricula"] = num_matricula
                
                nueva_inscripcion = Inscripcion(**campos)
                
                sesion.add(nueva_inscripcion)
                sesion.commit()
                sesion.refresh(nueva_inscripcion)
                print("Se registró la inscripción correctamente")
                
                alumno_id = campos.get("alumno_id")
                especialidad_id = campos.get("especialidad_id")
                
                alumno = sesion.query(Alumno).filter_by(alumno_id = alumno_id).first()
                especialidad = sesion.query(Especialidad).filter_by(especialidad_id = especialidad_id).first()
                
                num_matricula_alumno = campos["num_matricula"]
                
                accion = f"REGISTRÓ A {alumno.primer_nombre} {alumno.apellido_paterno} A LA ESPECIALIDAD {especialidad.especialidad}. MATRICULA: {num_matricula_alumno}"
                auditoria_repositorio.registrar(self.entidad, accion)
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL HACER LA INSCRIPCIÓN DEL ALUMNO: {error}")
    
    def obtener_todos(self) -> List[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                consulta = """
                    SELECT
                        alumnos.alumno_id,
                        alumnos.cedula,
                        alumnos.primer_nombre,
                        alumnos.apellido_paterno,
                        especialidades.especialidad,
                        inscripciones.num_matricula,
                        inscripciones.fecha_inscripcion,
                        STRFTIME('%Y', 'NOW', 'LOCALTIME') - STRFTIME('%Y', alumnos.fecha_ingreso_institucion) -
                        CASE 
                            WHEN STRFTIME('%m', 'NOW', 'LOCALTIME') < STRFTIME('%m', alumnos.fecha_ingreso_institucion) AND STRFTIME('%d', 'NOW', 'LOCALTIME') = STRFTIME('%d', alumnos.fecha_ingreso_institucion) THEN 1
                            WHEN STRFTIME('%m', 'NOW', 'LOCALTIME') = STRFTIME('%m', alumnos.fecha_ingreso_institucion) AND STRFTIME('%d', 'NOW', 'LOCALTIME') < STRFTIME('%d', alumnos.fecha_ingreso_institucion) THEN 1
                            WHEN STRFTIME('%m', 'NOW', 'LOCALTIME') < STRFTIME('%m', alumnos.fecha_ingreso_institucion) AND STRFTIME('%d', 'NOW', 'LOCALTIME') < STRFTIME('%d', alumnos.fecha_ingreso_institucion) THEN 1
                            ELSE 0
                        END AS tiempo_en_tela,
                        inscripciones.periodo_escolar,
                        alumnos.situacion,
                        alumnos.relacion_con_rep
                    FROM tb_alumnos AS alumnos
                    INNER JOIN tb_inscripciones AS inscripciones 
                        ON inscripciones.alumno_id = alumnos.alumno_id 
                    INNER JOIN tb_especialidades AS especialidades 
                        ON inscripciones.especialidad_id = especialidades.especialidad_id
                    WHERE alumnos.situacion = 'Ingresado' OR alumnos.situacion = 'Inicial';
                """
                
                alumnos = sesion.execute(text(consulta)).fetchall()
                
                return alumnos
        except Exception as error:
            print(f"ERROR AL OBTENER TODAS LAS INSCRIPCIONES: {error}")
    
    def obtener_por_id(self, alumno_id: int) -> Optional[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                consulta = """
                    SELECT
                        alumnos.alumno_id,
                        alumnos.cedula,
                        alumnos.primer_nombre,
                        alumnos.apellido_paterno,
                        especialidades.especialidad,
                        inscripciones.num_matricula,
                        inscripciones.fecha_inscripcion,
                        STRFTIME('%Y', 'NOW', 'LOCALTIME') - STRFTIME('%Y', alumnos.fecha_ingreso_institucion) -
                        CASE 
                            WHEN STRFTIME('%m', 'NOW', 'LOCALTIME') < STRFTIME('%m', alumnos.fecha_ingreso_institucion) AND STRFTIME('%d', 'NOW', 'LOCALTIME') = STRFTIME('%d', alumnos.fecha_ingreso_institucion) THEN 1
                            WHEN STRFTIME('%m', 'NOW', 'LOCALTIME') = STRFTIME('%m', alumnos.fecha_ingreso_institucion) AND STRFTIME('%d', 'NOW', 'LOCALTIME') < STRFTIME('%d', alumnos.fecha_ingreso_institucion) THEN 1
                            WHEN STRFTIME('%m', 'NOW', 'LOCALTIME') < STRFTIME('%m', alumnos.fecha_ingreso_institucion) AND STRFTIME('%d', 'NOW', 'LOCALTIME') < STRFTIME('%d', alumnos.fecha_ingreso_institucion) THEN 1
                            ELSE 0
                        END AS tiempo_en_tela,
                        inscripciones.periodo_escolar,
                        alumnos.situacion,
                        alumnos.relacion_con_rep
                    FROM tb_alumnos AS alumnos
                    INNER JOIN tb_inscripciones AS inscripciones 
                        ON inscripciones.alumno_id = alumnos.alumno_id 
                    INNER JOIN tb_especialidades AS especialidades 
                        ON inscripciones.especialidad_id = especialidades.especialidad_id
                    WHERE (alumnos.situacion = 'Ingresado' OR alumnos.situacion = 'Inicial') AND alumnos.alumno_id = :alumno_id;
                """
                
                alumno = sesion.execute(text(consulta), {"alumno_id": alumno_id}).fetchone()
                
                if not(alumno):
                    raise BaseDatosError("INSCRIPCION_NO_EXISTE", "Este registro de inscripción no existe")
                
                return alumno
        except BaseDatosError as error:
            raise error
        except Exception as error:
            print(f"ERROR AL OBTENER LA INSCRIPCIÓN: {error}")
    
    def obtener_por_num_matricula(self, num_matricula: str) -> Optional[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                consulta = """
                    SELECT
                        alumnos.alumno_id,
                        alumnos.cedula,
                        alumnos.primer_nombre,
                        alumnos.apellido_paterno,
                        especialidades.especialidad,
                        inscripciones.num_matricula,
                        inscripciones.fecha_inscripcion,
                        STRFTIME('%Y', 'NOW', 'LOCALTIME') - STRFTIME('%Y', alumnos.fecha_ingreso_institucion) -
                        CASE 
                            WHEN STRFTIME('%m', 'NOW', 'LOCALTIME') < STRFTIME('%m', alumnos.fecha_ingreso_institucion) AND STRFTIME('%d', 'NOW', 'LOCALTIME') = STRFTIME('%d', alumnos.fecha_ingreso_institucion) THEN 1
                            WHEN STRFTIME('%m', 'NOW', 'LOCALTIME') = STRFTIME('%m', alumnos.fecha_ingreso_institucion) AND STRFTIME('%d', 'NOW', 'LOCALTIME') < STRFTIME('%d', alumnos.fecha_ingreso_institucion) THEN 1
                            WHEN STRFTIME('%m', 'NOW', 'LOCALTIME') < STRFTIME('%m', alumnos.fecha_ingreso_institucion) AND STRFTIME('%d', 'NOW', 'LOCALTIME') < STRFTIME('%d', alumnos.fecha_ingreso_institucion) THEN 1
                            ELSE 0
                        END AS tiempo_en_tela,
                        inscripciones.periodo_escolar,
                        alumnos.situacion,
                        alumnos.relacion_con_rep
                    FROM tb_alumnos AS alumnos
                    INNER JOIN tb_inscripciones AS inscripciones 
                        ON inscripciones.alumno_id = alumnos.alumno_id 
                    INNER JOIN tb_especialidades AS especialidades 
                        ON inscripciones.especialidad_id = especialidades.especialidad_id
                    WHERE (alumnos.situacion = 'Ingresado' OR alumnos.situacion = 'Inicial') AND inscripciones.num_matricula = :num_matricula;
                """
                
                alumno = sesion.execute(text(consulta), {"num_matricula": num_matricula}).fetchone()
                
                if not(alumno):
                    raise BaseDatosError("INSCRIPCION_NO_EXISTE", "Este registro de inscripción no existe")
                
                return alumno
        except BaseDatosError as error:
            raise error
        except Exception as error:
            print(f"ERROR AL OBTENER LA INSCRIPCIÓN: {error}")
    
    def obtener_por_especialidad(self, especialidad_id: int) -> List[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                consulta = """
                    SELECT
                        alumnos.alumno_id,
                        alumnos.cedula,
                        alumnos.primer_nombre,
                        alumnos.apellido_paterno,
                        especialidades.especialidad,
                        inscripciones.num_matricula,
                        inscripciones.fecha_inscripcion,
                        STRFTIME('%Y', 'NOW', 'LOCALTIME') - STRFTIME('%Y', alumnos.fecha_ingreso_institucion) -
                        CASE 
                            WHEN STRFTIME('%m', 'NOW', 'LOCALTIME') < STRFTIME('%m', alumnos.fecha_ingreso_institucion) AND STRFTIME('%d', 'NOW', 'LOCALTIME') = STRFTIME('%d', alumnos.fecha_ingreso_institucion) THEN 1
                            WHEN STRFTIME('%m', 'NOW', 'LOCALTIME') = STRFTIME('%m', alumnos.fecha_ingreso_institucion) AND STRFTIME('%d', 'NOW', 'LOCALTIME') < STRFTIME('%d', alumnos.fecha_ingreso_institucion) THEN 1
                            WHEN STRFTIME('%m', 'NOW', 'LOCALTIME') < STRFTIME('%m', alumnos.fecha_ingreso_institucion) AND STRFTIME('%d', 'NOW', 'LOCALTIME') < STRFTIME('%d', alumnos.fecha_ingreso_institucion) THEN 1
                            ELSE 0
                        END AS tiempo_en_tela,
                        inscripciones.periodo_escolar,
                        alumnos.situacion,
                        alumnos.relacion_con_rep
                    FROM tb_alumnos AS alumnos
                    INNER JOIN tb_inscripciones AS inscripciones 
                        ON inscripciones.alumno_id = alumnos.alumno_id 
                    INNER JOIN tb_especialidades AS especialidades 
                        ON inscripciones.especialidad_id = especialidades.especialidad_id
                    WHERE (alumnos.situacion = 'Ingresado' OR alumnos.situacion = 'Inicial') AND especialidades.especialidad_id = :especialidad_id;
                """
                
                alumnos = sesion.execute(text(consulta), {"especialidad_id": especialidad_id}).fetchall()
                
                if not(alumnos):
                    raise BaseDatosError("INSCRIPCIONES_NO_EXISTEN", "No hay alumnos inscritos en esta especialidad.")
                
                return alumnos
        except BaseDatosError as error:
            raise error
        except Exception as error:
            print(f"ERROR AL OBTENER LAS INSCRIPCIONES POR ESPECIALIDAD: {error}")
    
    def obtener_por_cedula(self, cedula: str) -> Optional[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                consulta = """
                    SELECT
                        alumnos.alumno_id,
                        alumnos.cedula,
                        alumnos.primer_nombre,
                        alumnos.apellido_paterno,
                        especialidades.especialidad,
                        inscripciones.num_matricula,
                        inscripciones.fecha_inscripcion,
                        STRFTIME('%Y', 'NOW', 'LOCALTIME') - STRFTIME('%Y', alumnos.fecha_ingreso_institucion) -
                        CASE 
                            WHEN STRFTIME('%m', 'NOW', 'LOCALTIME') < STRFTIME('%m', alumnos.fecha_ingreso_institucion) AND STRFTIME('%d', 'NOW', 'LOCALTIME') = STRFTIME('%d', alumnos.fecha_ingreso_institucion) THEN 1
                            WHEN STRFTIME('%m', 'NOW', 'LOCALTIME') = STRFTIME('%m', alumnos.fecha_ingreso_institucion) AND STRFTIME('%d', 'NOW', 'LOCALTIME') < STRFTIME('%d', alumnos.fecha_ingreso_institucion) THEN 1
                            WHEN STRFTIME('%m', 'NOW', 'LOCALTIME') < STRFTIME('%m', alumnos.fecha_ingreso_institucion) AND STRFTIME('%d', 'NOW', 'LOCALTIME') < STRFTIME('%d', alumnos.fecha_ingreso_institucion) THEN 1
                            ELSE 0
                        END AS tiempo_en_tela,
                        inscripciones.periodo_escolar,
                        alumnos.situacion,
                        alumnos.relacion_con_rep
                    FROM tb_alumnos AS alumnos
                    INNER JOIN tb_inscripciones AS inscripciones 
                        ON inscripciones.alumno_id = alumnos.alumno_id 
                    INNER JOIN tb_especialidades AS especialidades 
                        ON inscripciones.especialidad_id = especialidades.especialidad_id
                    WHERE (alumnos.situacion = 'Ingresado' OR alumnos.situacion = 'Inicial') AND alumnos.cedula = :cedula;
                """
                
                alumno = sesion.execute(text(consulta), {"cedula": cedula}).fetchone()
                
                if not(alumno):
                    raise BaseDatosError("INSCRIPCION_NO_EXISTE", "Este registro de inscripción no existe")
                
                return alumno
        except BaseDatosError as error:
            raise error
        except Exception as error:
            print(f"ERROR AL OBTENER LA INSCRIPCIÓN: {error}")
    
    def obtener_por_situacion_y_especialidad(self, situacion: str, especialidad_id: int) -> Optional[List[Tuple]]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                consulta = """
                    SELECT 
                        alumnos.alumno_id,
                        alumnos.cedula,
                        alumnos.primer_nombre,
                        alumnos.apellido_paterno,
                        especialidades.especialidad,
                        inscripciones.num_matricula,
                        inscripciones.fecha_inscripcion,
                        STRFTIME('%Y', 'NOW', 'LOCALTIME') - STRFTIME('%Y', alumnos.fecha_ingreso_institucion) -
                        CASE 
                            WHEN STRFTIME('%m', 'NOW', 'LOCALTIME') < STRFTIME('%m', alumnos.fecha_ingreso_institucion) AND STRFTIME('%d', 'NOW', 'LOCALTIME') = STRFTIME('%d', alumnos.fecha_ingreso_institucion) THEN 1
                            WHEN STRFTIME('%m', 'NOW', 'LOCALTIME') = STRFTIME('%m', alumnos.fecha_ingreso_institucion) AND STRFTIME('%d', 'NOW', 'LOCALTIME') < STRFTIME('%d', alumnos.fecha_ingreso_institucion) THEN 1
                            WHEN STRFTIME('%m', 'NOW', 'LOCALTIME') < STRFTIME('%m', alumnos.fecha_ingreso_institucion) AND STRFTIME('%d', 'NOW', 'LOCALTIME') < STRFTIME('%d', alumnos.fecha_ingreso_institucion) THEN 1
                            ELSE 0
                        END AS tiempo_en_tela,
                        inscripciones.periodo_escolar,
                        alumnos.situacion,
                        alumnos.relacion_con_rep
                    FROM tb_alumnos AS alumnos
                    INNER JOIN tb_inscripciones AS inscripciones 
                        ON inscripciones.alumno_id = alumnos.alumno_id 
                    INNER JOIN tb_especialidades AS especialidades 
                        ON inscripciones.especialidad_id = especialidades.especialidad_id
                    WHERE alumnos.situacion = :situacion AND especialidades.especialidad_id = :especialidad_id;
                """
                
                alumnos = sesion.execute(text(consulta), {
                    "situacion": situacion,
                    "especialidad_id": especialidad_id
                }).fetchone()
                
                if not(alumnos):
                    raise BaseDatosError("INSCRIPCIONES_NO_EXISTEN", "No hay alumnos inscritos en esta especialidad.")
                
                return alumnos
        except BaseDatosError as error:
            raise error
        except Exception as error:
            print(f"ERROR AL OBTENER LAS INSCRIPCIONES POR SU SITUACIÓN/ESTADO: {error}")
    
    def obtener_por_especialidad_o_cedula(self, especialidad_id: int, cedula: str = None) -> Union[List[Tuple], Tuple]:
        try:
            if (cedula):
                if (self.obtener_por_cedula(cedula)):
                    return self.obtener_por_cedula(cedula)
            else:
                return self.obtener_por_especialidad(especialidad_id)
        except BaseDatosError as error:
            raise error
        except Exception as error:
            print(f"ERROR AL OBTENER LA INSCRIPCION/ES POR ESPECIALIDAD O CÉDULA: {error}")
    
    def obtener_por_especialidad_o_matricula(self, especialidad_id: int, num_matricula: str = None) -> Union[List[Tuple], Tuple]:
        try:
            if (num_matricula):
                if (self.obtener_por_num_matricula(num_matricula)):
                    return self.obtener_por_num_matricula(num_matricula)
            else:
                return self.obtener_por_especialidad(especialidad_id)
        except BaseDatosError as error:
            raise error
        except Exception as error:
            print(f"ERROR AL OBTENER LA INSCRIPCION/ES POR ESPECIALIDAD O MATRICULA: {error}")
    
    def obtener_por_cedula_situacion_especialidad(self, especialidad_id: int, cedula: str = None, situacion: str = "Inactivo") -> Union[List[Tuple], Tuple]:
        try:
            if (cedula):
                if (self.obtener_por_cedula(cedula)):
                    return self.obtener_por_cedula(cedula)
            else:
                return self.obtener_por_situacion_y_especialidad(situacion, especialidad_id)
        except BaseDatosError as error:
            raise error
        except Exception as error:
            print(f"ERROR AL OBTENER LAS INSCRIPCIONES POR CÉDULA, SITUACIÓN Y ESPECIALIDAD: {error}")
    
    def obtener_por_matricula_situacion_especialidad(self, especialidad_id: int, num_matricula: str = None, situacion: str = "Inactivo") -> Union[List[Tuple], Tuple]:
        try:
            if (num_matricula):
                if (self.obtener_por_num_matricula(num_matricula)):
                    return self.obtener_por_num_matricula(num_matricula)
            else:
                return self.obtener_por_situacion_y_especialidad(situacion, especialidad_id)
        except BaseDatosError as error:
            raise error
        except Exception as error:
            print(f"ERROR AL OBTENER LAS INSCRIPCIONES POR MATRICULA, SITUACIÓN Y ESPECIALIDAD: {error}")
    
    def actualizar(self, alumno_id: int, campos_inscripcion: Dict) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                inscripcion = sesion.query(Inscripcion).filter_by(alumno_id = alumno_id).first()
                especialidad_id = inscripcion.especialidad_id
                especialidad_anterior = sesion.query(Especialidad).filter_by(especialidad_id = especialidad_id).first()
                diccionario_inscripcion = {campo: valor for campo, valor in vars(inscripcion).items() if not(campo.startswith("_")) and campo not in("inscripcion_id", "alumno_id", "num_matricula")}
                
                campos = {
                    "especialidad_id": "ESPECIALIDAD INSCRITA",
                    "fecha_inscripcion": "FECHA DE INSCRIPCIÓN",
                    "periodo_escolar": "PERIODO ESCOLAR"
                }
                
                for clave in diccionario_inscripcion.keys():
                    if not(campos_inscripcion.get(clave) == diccionario_inscripcion.get(clave)):
                        campo_actualizado = campos.get(clave)
                        
                        if (clave == "especialidad_id"):
                            nuevo_especialidad_id = campos_inscripcion.get("especialidad_id")
                            especialidad_actual = sesion.query(Especialidad).filter_by(especialidad_id = nuevo_especialidad_id).first()
                        
                            valor_campo_actual = campos_inscripcion.get(clave)
                            
                            accion = f"ACTUALIZÓ EL CAMPO: {campo_actualizado}. ANTES: {especialidad_anterior.especialidad}. AHORA: {especialidad_actual.especialidad}. MATRICULA: {inscripcion.num_matricula}"
                            
                            auditoria_repositorio.registrar(self.entidad, accion)
                        elif (clave == "periodo_escolar"):
                            valor_campo_actual = campos_inscripcion.get(clave)
                        else:
                            valor_campo_anterior = diccionario_inscripcion.get(clave)
                            valor_campo_actual = campos_inscripcion.get(clave)
                            
                            accion = f"ACTUALIZÓ EL CAMPO: {campo_actualizado}. ANTES: {valor_campo_anterior}. AHORA: {valor_campo_actual}. MATRICULA: {inscripcion.num_matricula}"
                        
                            auditoria_repositorio.registrar(self.entidad, accion)
                        
                        sesion.query(Inscripcion).filter_by(alumno_id = alumno_id).update({clave: valor_campo_actual})
                        sesion.commit()
                        print(f"Se actualizó el campo: {campo_actualizado} correctamente \n")
        except Exception as error:
            sesion.rollback()
            raise error
    
    def generar_num_matricula(self) -> str:
        try:
            while True:
                codigo = str(uuid4())[:7]
                num_matricula = f"MAT-{codigo}"
                existe_num_matricula = self.obtener_por_num_matricula(num_matricula)
        except BaseDatosError:
            return num_matricula


if __name__ == "__main__":
    inscripcion_repositorio = InscripcionRepositorio()
    
    """campos_inscripcion = {
        "num_matricula": None,
        "alumno_id": 17,
        "especialidad_id": 1,
        "fecha_inscripcion": None,
        "periodo_escolar": "2025-2026"
    }
    
    inscripcion_repositorio.registrar(campos_inscripcion)"""
    
    """todos_inscripciones = inscripcion_repositorio.obtener_todos()
    
    for registro in todos_inscripciones:
        print(registro)"""
    
    
    #print(inscripcion_repositorio.obtener_por_id(17))
    #print(inscripcion_repositorio.obtener_por_cedula("30932925"))
    
    """try:
        inscripciones_por_especialidad = inscripcion_repositorio.obtener_por_especialidad(2)
        for registro in inscripciones_por_especialidad:
            print(registro)
    except BaseDatosError as error:
        print(error)"""
    
    """try:
        inscripcion_por_matricula = inscripcion_repositorio.obtener_por_num_matricula("MAT-125t341")
        print(inscripcion_por_matricula)
    except BaseDatosError as error:
        print(error)"""
    
    """try:
        inscripciones_por_especialidad_o_cedula = inscripcion_repositorio.obtener_por_especialidad_o_cedula(1, "30932925")
        if (type(inscripciones_por_especialidad_o_cedula) == list):
            for registro in inscripciones_por_especialidad_o_cedula:
                print(registro)
        else:
            print(inscripciones_por_especialidad_o_cedula)
    except BaseDatosError as error:
        print(error)"""
    
    """try:
        inscripciones_por_especialidad_o_matricula = inscripcion_repositorio.obtener_por_especialidad_o_matricula(1, "MAT-4a1e5b2")
        if (type(inscripciones_por_especialidad_o_matricula) == list):
            for registro in inscripciones_por_especialidad_o_matricula:
                print(registro)
        else:
            print(inscripciones_por_especialidad_o_matricula)
    except BaseDatosError as error:
        print(error)"""
    
    """campos_inscripcion = {
        "especialidad_id": 1,
        "fecha_inscripcion": date(2025, 5, 29),
        "periodo_escolar": "2026-2027"
    }
    
    inscripcion_repositorio.actualizar(17, campos_inscripcion)"""
    
    """try:
        alumnos = inscripcion_repositorio.obtener_por_cedula_situacion_especialidad(1, None, "Ingresado")
        print(alumnos)
    except BaseDatosError as error:
        print(error)"""
    
    """try:
        alumno = inscripcion_repositorio.obtener_por_matricula_situacion_especialidad(1, None)
        print(alumno)
    except BaseDatosError as error:
        print(error)"""
    
    """try:
        alumno = inscripcion_repositorio.obtener_por_especialidad_o_cedula(1, "43342903")
        print(alumno)
    except BaseDatosError as error:
        print(error)"""
    
    """try:
        alumno = inscripcion_repositorio.obtener_por_especialidad_o_matricula(1, "MAT-5qa2341")
        print(alumno)
    except BaseDatosError as error:
        print(error)"""