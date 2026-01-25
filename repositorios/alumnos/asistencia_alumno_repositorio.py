from typing import Tuple, List, Optional, Dict
from sqlalchemy import text
from datetime import date
from excepciones.base_datos_error import BaseDatosError
from modelos import AsistenciaAlumno, Especialidad, Inscripcion, Alumno
from repositorios.repositorio_base import RepositorioBase
from conexiones.conexion import conexion_bd


class AsistenciaAlumnoRepositorio(RepositorioBase):
    def __init__(self):
        self.conexion_bd = conexion_bd
        self.entidad = "ASISTENCIA DE ALUMNOS"
    
    def registrar(self, campos: Dict) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                nueva_asistencia_alumno = AsistenciaAlumno(**campos)
                
                sesion.add(nueva_asistencia_alumno)
                sesion.commit()
                sesion.refresh(nueva_asistencia_alumno)
                print("Se registró la asistencia del alumno correctamente")
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL OBTENER LA ASISTENCIA DEL ALUMNO: {error}")
    
    def obtener_todos(self) -> List[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                asistencias_alumnos = (
                    sesion.query(
                        AsistenciaAlumno.asist_alumno_id,
                        Especialidad.especialidad_id,
                        Especialidad.especialidad,
                        Inscripcion.num_matricula,
                        Alumno.primer_nombre,
                        Alumno.apellido_paterno,
                        AsistenciaAlumno.fecha_asistencia,
                        AsistenciaAlumno.estado_asistencia,
                        AsistenciaAlumno.dia_no_laborable
                    )
                    .join(AsistenciaAlumno.inscripcion)
                    .join(Inscripcion.especialidad)
                    .join(Inscripcion.alumno)
                    .order_by(AsistenciaAlumno.fecha_asistencia)
                ).all()
                
                return asistencias_alumnos
        except Exception as error:
            print(f"ERROR AL OBTENER LAS ASISTENCIAS DE LOS ALUMNOS: {error}")
    
    def obtener_por_id(self, asist_alumno_id: int) -> Optional[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                asistencia_alumno = (
                    sesion.query(
                        AsistenciaAlumno.asist_alumno_id,
                        Especialidad.especialidad_id,
                        Especialidad.especialidad,
                        Inscripcion.num_matricula,
                        Alumno.primer_nombre,
                        Alumno.apellido_paterno,
                        AsistenciaAlumno.fecha_asistencia,
                        AsistenciaAlumno.estado_asistencia,
                        AsistenciaAlumno.dia_no_laborable
                    )
                    .join(AsistenciaAlumno.inscripcion)
                    .join(Inscripcion.especialidad)
                    .join(Inscripcion.alumno)
                    .order_by(AsistenciaAlumno.fecha_asistencia)
                ).filter(AsistenciaAlumno.asist_alumno_id == asist_alumno_id).first()
                
                if not(asistencia_alumno):
                    raise BaseDatosError("ASISTENCIA_ALUMNO_NO_EXISTE", "Esta asistencia de alumno no existe")
                
                return asistencia_alumno
        except Exception as error:
            print(f"ERROR AL OBTENER LA ASISTENCIA DE ALUMNO: {error}")
    
    def obtener_por_inscripcion_id_y_fecha(self, inscripcion_id: int, fecha_asistencia: date) -> Optional[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                consulta = """
                    SELECT *
                    FROM tb_asistencia_alumnos
                    WHERE inscripcion_id = :inscripcion_id AND fecha_asistencia = :fecha_asistencia;
                """
                asistencia_alumno = sesion.execute(text(consulta), {
                    "inscripcion_id": inscripcion_id,
                    "fecha_asistencia": fecha_asistencia
                }).fetchone()
                
                return asistencia_alumno
        except Exception:
            return None
    
    def obtener_por_fecha_asistencia(self, fecha_asistencia: date) -> List[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                asistencia_alumnos = (
                    sesion.query(
                        AsistenciaAlumno.asist_alumno_id,
                        Especialidad.especialidad_id,
                        Especialidad.especialidad,
                        Inscripcion.num_matricula,
                        Alumno.primer_nombre,
                        Alumno.apellido_paterno,
                        AsistenciaAlumno.fecha_asistencia,
                        AsistenciaAlumno.estado_asistencia,
                        AsistenciaAlumno.dia_no_laborable
                    )
                    .join(AsistenciaAlumno.inscripcion)
                    .join(Inscripcion.especialidad)
                    .join(Inscripcion.alumno)
                    .order_by(AsistenciaAlumno.fecha_asistencia)
                ).filter(AsistenciaAlumno.fecha_asistencia == fecha_asistencia).all()
                return asistencia_alumnos
        except Exception as error:
            print(f"ERROR AL OBTENER LA ASISTENCIA DIARIA DE ALUMNO: {error}")
    
    def obtener_por_fecha_asistencia_y_especialidad(self, fecha_asistencia: date, especialidad_id: int) -> List[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                asistencia_alumnos = (
                    sesion.query(
                        AsistenciaAlumno.asist_alumno_id,
                        Especialidad.especialidad_id,
                        Especialidad.especialidad,
                        Inscripcion.num_matricula,
                        Alumno.primer_nombre,
                        Alumno.apellido_paterno,
                        AsistenciaAlumno.fecha_asistencia,
                        AsistenciaAlumno.estado_asistencia,
                        AsistenciaAlumno.dia_no_laborable
                    )
                    .join(AsistenciaAlumno.inscripcion)
                    .join(Inscripcion.especialidad)
                    .join(Inscripcion.alumno)
                    .order_by(AsistenciaAlumno.fecha_asistencia)
                ).filter(AsistenciaAlumno.fecha_asistencia == fecha_asistencia).filter(Especialidad.especialidad_id == especialidad_id).all()
                return asistencia_alumnos
        except Exception as error:
            print(f"ERROR AL OBTENER LA ASISTENCIA DIARIA DE ALUMNO: {error}")
    
    def obtener_asistencia_mensual(self) -> List[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                consulta = """
                    SELECT 
                        especialidad,
                        fecha_asistencia,
                        dia_no_laborable,
                        varones_presentes,
                        hembras_presentes,
                        (varones_presentes + hembras_presentes) AS total_presentes,
                        varones_ausentes,
                        hembras_ausentes,
                        (varones_ausentes + hembras_ausentes) AS total_ausentes
                    FROM vw_registro_asistencia_alumnos;
                """
                
                asistencias_alumnos_mensual = sesion.execute(text(consulta)).fetchall()
                return asistencias_alumnos_mensual
        except Exception as error:
            print(f"ERROR AL OBTENER TODOS LOS ALUMNOS: {error}")
    
    def obtener_por_especialidad_y_anio_mes(self, especialidad_id: int, anio_mes: str) -> List[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                consulta = """
                    SELECT 
                        especialidad,
                        fecha_asistencia,
                        dia_no_laborable,
                        varones_presentes,
                        hembras_presentes,
                        (varones_presentes + hembras_presentes) AS total_presentes,
                        varones_ausentes,
                        hembras_ausentes,
                        (varones_ausentes + hembras_ausentes) AS total_ausentes
                    FROM vw_registro_asistencia_alumnos
                    WHERE especialidad_id = :especialidad_id AND STRFTIME('%Y-%m', fecha_asistencia) = :anio_mes;
                """
                
                asistencias_alumnos_mensual = sesion.execute(text(consulta), {
                    "especialidad_id": especialidad_id,
                    "anio_mes": anio_mes
                }).fetchall()
                
                return asistencias_alumnos_mensual
        except Exception as error:
            print(f"ERROR AL OBTENER LAS ASISTENCIAS DE ALUMNOS POR ESPECIALIDAD, AÑO Y MES: {error}")
    
    def obtener_sumatoria_asistencias_inasistencias(self, especialidad_id: int, anio_mes: str) -> Optional[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                consulta = """
                    SELECT *
                    FROM vw_sumatorias_asistencias_inasistencias
                    WHERE especialidad_id = :especialidad_id AND anio_mes = :anio_mes;
                """
                
                sumatoria_asistencias_inasistencias = sesion.execute(text(consulta), {
                    "especialidad_id": especialidad_id,
                    "anio_mes": anio_mes
                }).first()
                
                return sumatoria_asistencias_inasistencias
        except Exception as error:
            print(f"ERROR AL OBTENER LA SUMATORIA DE ASISTENCIAS E INASISTENCIAS: {error}")
    
    def obtener_dias_habiles(self, especialidad_id: int, anio_mes: str) -> Optional[int]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                consulta_dias_habiles = """
                    SELECT 
                        COUNT(*) dias_habiles
                    FROM vw_registro_asistencia_alumnos
                    WHERE dia_no_laborable IS NULL 
                    AND especialidad_id = :especialidad_id 
                    AND STRFTIME('%Y-%m', fecha_asistencia) = :anio_mes;
                """
                
                (dias_habiles,) = sesion.execute(text(consulta_dias_habiles), {
                    "especialidad_id": especialidad_id,
                    "anio_mes": anio_mes
                }).fetchone()
                
                return dias_habiles
        except Exception:
            return None
    
    def obtener_promedio_asistencias_inasistencias(self, especialidad_id: int, anio_mes: str) -> Optional[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                dias_habiles = self.obtener_dias_habiles(especialidad_id, anio_mes)
                
                consulta_promedio_asistencias_inasistencias = """
                    SELECT 
                        especialidad_id,
                        especialidad,
                        anio_mes,
                        ROUND(sumatoria_varones_presentes / :dias_habiles) AS promedio_varones_presentes,
                        ROUND(sumatoria_hembras_presentes / :dias_habiles) AS promedio_hembras_presentes,
                        ROUND((sumatoria_varones_presentes / :dias_habiles) + ROUND(sumatoria_hembras_presentes / :dias_habiles)) AS promedio_general_presentes,
                        ROUND(sumatoria_varones_ausentes / :dias_habiles) AS promedio_varones_ausentes,
                        ROUND(sumatoria_hembras_ausentes / :dias_habiles) AS promedio_hembras_ausentes,
                        ROUND((sumatoria_varones_ausentes / :dias_habiles) + ROUND(sumatoria_hembras_ausentes / :dias_habiles)) AS promedio_general_ausentes
                    FROM vw_sumatorias_asistencias_inasistencias
                    WHERE especialidad_id = :especialidad_id AND anio_mes = :anio_mes;
                """
                
                promedio_asistencias_inasistencias = sesion.execute(text(consulta_promedio_asistencias_inasistencias), {
                    "dias_habiles": dias_habiles,
                    "especialidad_id": especialidad_id,
                    "anio_mes": anio_mes
                }).fetchone()
                
                return promedio_asistencias_inasistencias
        except Exception as error:
            print(f"ERROR AL OBTENER EL PROMEDIO DE ASISTENCIAS E INASISTENCIA DE ALUMNOS: {error}")
    
    def obtener_porcentaje_asistencias_inasistencias(self, especialidad_id: int, anio_mes: str) -> Optional[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                consulta = """
                    SELECT * 
                    FROM vw_porcentajes_asistencias_inasistencias 
                    WHERE especialidad_id = :especialidad_id AND anio_mes = :anio_mes;
                """
                
                porcentaje_asistencias_inasistencias = sesion.execute(text(consulta), {
                    "especialidad_id": especialidad_id,
                    "anio_mes": anio_mes
                }).fetchone()
                
                return porcentaje_asistencias_inasistencias
        except Exception as error:
            print(f"ERROR AL OBTENER EL PORCENTAJE DE ASISTENCIAS E INASISTENCIAS DE ALUMNOS: {error}")
    
    def obtener_matricula_completa_alumnos(self, especialidad_id: int) -> Optional[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                consulta = """
                    SELECT
                        especialidad_id,
                        especialidad,
                        total_varones_iniciales,
                        total_hembras_iniciales,
                        (total_varones_iniciales + total_hembras_iniciales) AS total_matricula_inicial,
                        total_varones_ingresados,
                        total_hembras_ingresadas,
                        (total_varones_ingresados + total_hembras_ingresadas) AS total_matricula_ingresos,
                        total_varones_egresados,
                        total_hembras_egresadas,
                        (total_varones_egresados + total_hembras_egresadas) AS total_matricula_egresos,
                        total_varones_rotados,
                        total_hembras_rotadas,
                        (total_varones_rotados + total_hembras_rotadas) AS total_matricula_rotados,
                        matricula_total_varones,
                        matricula_total_hembras,
                        (matricula_total_varones + matricula_total_hembras) AS total_matricula_final
                    FROM vw_matricula_completa_alumnos
                    WHERE especialidad_id = :especialidad_id;
                """
                
                matricula_completa_alumnos = sesion.execute(text(consulta), {"especialidad_id": especialidad_id}).fetchone()
                return matricula_completa_alumnos
        except Exception as error:
            print(f"ERROR AL OBTENER LA MATRICULA COMPLETA DE ALUMNOS: {error}")
    
    def actualizar(self, asist_alumno_id: int, campos_asistencia_alumno: Dict) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                asistencia_alumno = sesion.query(AsistenciaAlumno).filter_by(asist_alumno_id = asist_alumno_id).first()
                
                campos = {
                    "fecha_asistencia": "FECHA DE ASISTENCIA",
                    "estado_asistencia": "ESTADO DE ASISTENCIA",
                    "dia_no_laborable": "DÍA NO LABORABLE"
                }
                
                diccionario_asistencia_alumno = {campo: valor for campo, valor in vars(asistencia_alumno).items() if not(campo.startswith("_")) and campo not in("asist_alumno_id", "especialidad_id", "inscripcion_id")}
                
                for clave in diccionario_asistencia_alumno.keys():
                    if not(campos_asistencia_alumno.get(clave) == diccionario_asistencia_alumno.get(clave)):
                        campo_actualizado = campos.get(clave)
                        valor_campo_actual = campos_asistencia_alumno.get(clave)
                        
                        sesion.query(AsistenciaAlumno).filter(AsistenciaAlumno.asist_alumno_id == asist_alumno_id).update({clave: valor_campo_actual})
                        sesion.commit()
                        print(f"Se actualizó el campo: {campo_actualizado} correctamente \n")
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL ACTUALIZAR LOS CAMPOS: {error}")
    
    def eliminar(self, asist_alumno_id: int) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                asistencia_alumno = sesion.query(AsistenciaAlumno).filter_by(asist_alumno_id = asist_alumno_id).first()
                
                if not(asistencia_alumno):
                    raise BaseDatosError("ASISTENCIA_ALUMNO_NO_EXISTE", "Esta asistencia de alumno no existe")
                
                sesion.delete(asistencia_alumno)
                sesion.commit()
                print("Se eliminó la asistencia del alumno correctamente")
        except BaseDatosError as error:
            sesion.rollback()
            raise error
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL ELIMINAR LA ASISTENCIA DEL ALUMNO: {error}")


if __name__ == "__main__":
    asistencia_alumno_repositorio = AsistenciaAlumnoRepositorio()
    
    """campos_asistencia_alumno = {
        "inscripcion_id": 1,
        "fecha_asistencia": date.today(),
        "estado_asistencia": 1,
        "dia_no_laborable": None
    }
    
    asistencia_alumno_repositorio.registrar(campos_asistencia_alumno)"""
    
    """todos_asistencia_alumno = asistencia_alumno_repositorio.obtener_todos()
    
    for registro in todos_asistencia_alumno:
        print(registro)"""
    
    """try:
        print(asistencia_alumno_repositorio.obtener_por_id(10))
    except BaseDatosError as error:
        print(error)"""
    
    """try:
        asistencia_mensual_general = asistencia_alumno_repositorio.obtener_asistencia_mensual()
        for registro in asistencia_mensual_general:
            print(registro)
    except BaseDatosError as error:
        print(error)"""
    
    try:
        asistencia_mensual_por_especialidad_anio_mes = asistencia_alumno_repositorio.obtener_por_especialidad_y_anio_mes(1, "2024-05")
        for registro in asistencia_mensual_por_especialidad_anio_mes:
            print(registro)
    except BaseDatosError as error:
        print(error)
    
    #sumatoria_asistencias_inasistencias_mensual = asistencia_alumno_repositorio.obtener_sumatoria_asistencias_inasistencias(1, "2024-05")
    #print(sumatoria_asistencias_inasistencias_mensual)
    
    #promedio_asistencia_inasistencia_mensual = asistencia_alumno_repositorio.obtener_promedio_asistencias_inasistencias(1, "2024-05")
    #print(promedio_asistencia_inasistencia_mensual)
    
    #matricula_completa_varones_hembras = asistencia_alumno_repositorio.obtener_matricula_varones_hembras(1)
    #print(matricula_completa_varones_hembras)
    
    #matricula_completa_alumnos = asistencia_alumno_repositorio.obtener_matricula_completa_alumnos(1)
    #print(matricula_completa_alumnos)
    
    """campos_asistencia_alumno = {
        "fecha_asistencia": date.today(),
        "estado_asistencia": 0,
        "dia_no_laborable": None
    }
    
    asistencia_alumno_repositorio.actualizar(346, campos_asistencia_alumno)"""
    
    #asistencia_alumno_repositorio.eliminar(346)