from typing import Tuple, List, Dict
from datetime import date
from sqlalchemy import text
from excepciones.base_datos_error import BaseDatosError
from modelos import InfoClinicaAlumno, Alumno, Diagnostico, Inscripcion
from repositorios.usuarios.auditoria_repositorio import auditoria_repositorio
from repositorios.repositorio_base import RepositorioBase
from conexiones.conexion import conexion_bd


class InfoClinicaAlumnoRepositorio(RepositorioBase):
    def __init__(self):
        self.conexion_bd = conexion_bd
        self.entidad = "INFO CLÍNICA DE ALUMNOS"
    
    def registrar(self, campos: Dict) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                nueva_info_clinica_alumno = InfoClinicaAlumno(**campos)
                
                sesion.add(nueva_info_clinica_alumno)
                sesion.commit()
                sesion.refresh(nueva_info_clinica_alumno)
                print("Se registró la info clínica de alumno correctamente")
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL REGISTRAR LA INFO CLÍNICA DE ALUMNO: {error}")
    
    def obtener_todos(self) -> List[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                info_clinica_alumnos = sesion.query(
                    InfoClinicaAlumno.info_clin_alumno_id,
                    Alumno.alumno_id,
                    Diagnostico.diagnostico,
                    InfoClinicaAlumno.fecha_diagnostico,
                    InfoClinicaAlumno.medico_tratante,
                    InfoClinicaAlumno.certificacion_discap,
                    InfoClinicaAlumno.fecha_vencimiento_certif,
                    InfoClinicaAlumno.medicacion
                ).join(InfoClinicaAlumno.alumno).join(InfoClinicaAlumno.diagnostico).all()
                
                return info_clinica_alumnos
        except Exception as error:
            print(f"ERROR AL OBTENER LA INFO CLÍNICA DE LOS ALUMNOS: {error}")
    
    def obtener_por_id(self, info_clin_alumno_id: int) -> Tuple:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                info_clinica_alumno = sesion.query(
                    InfoClinicaAlumno.info_clin_alumno_id,
                    Alumno.alumno_id,
                    Diagnostico.diagnostico,
                    InfoClinicaAlumno.fecha_diagnostico,
                    InfoClinicaAlumno.medico_tratante,
                    InfoClinicaAlumno.certificacion_discap,
                    InfoClinicaAlumno.fecha_vencimiento_certif,
                    InfoClinicaAlumno.medicacion
                ).join(InfoClinicaAlumno.alumno).join(InfoClinicaAlumno.diagnostico).filter(InfoClinicaAlumno.info_clin_alumno_id == info_clin_alumno_id).first()
                
                return info_clinica_alumno
        except Exception as error:
            print(f"ERROR AL OBTENER LA INFO CLÍNICA DEL ALUMNO: {error}")
    
    def obtener_por_alumno_id(self, alumno_id: int) -> List[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                info_clinica_alumno = sesion.query(
                    InfoClinicaAlumno.info_clin_alumno_id,
                    Alumno.alumno_id,
                    Diagnostico.diagnostico,
                    InfoClinicaAlumno.fecha_diagnostico,
                    InfoClinicaAlumno.medico_tratante,
                    InfoClinicaAlumno.certificacion_discap,
                    InfoClinicaAlumno.fecha_vencimiento_certif,
                    InfoClinicaAlumno.medicacion
                ).join(InfoClinicaAlumno.alumno).join(InfoClinicaAlumno.diagnostico).filter(Alumno.alumno_id == alumno_id).all()
                
                return info_clinica_alumno
        except Exception as error:
            print(f"ERROR AL OBTENER LA INFO CLÍNICA DEL ALUMNO: {error}")
    
    def obtener_por_certificacion_discap(self, certificacion_discap: str) -> int:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                consulta = "SELECT 1 FROM tb_info_clinica_alumnos WHERE certificacion_discap = :certificacion_discap;"
                info_clinica_alumno = sesion.execute(text(consulta), {"certificacion_discap": certificacion_discap}).fetchone()
                return info_clinica_alumno
        except Exception as error:
            print(f"ERROR AL OBTENER LA INFO CLÍNICA DEL ALUMNO POR EL CERTIFICADO DE DISCAPACIDAD: {error}")
    
    def actualizar(self, info_clin_alumno_id: int, campos_info_clinica_alumno: Dict) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                info_clinica_alumno = sesion.query(InfoClinicaAlumno).filter_by(info_clin_alumno_id = info_clin_alumno_id).first()
                diagnostico_anterior = sesion.query(Diagnostico).join(InfoClinicaAlumno.diagnostico).filter(InfoClinicaAlumno.info_clin_alumno_id == info_clin_alumno_id).first()
                alumno = sesion.query(Alumno).join(InfoClinicaAlumno.alumno).filter(InfoClinicaAlumno.info_clin_alumno_id == info_clin_alumno_id).first()
                alumno_id = alumno.alumno_id
                inscripcion_alumno = sesion.query(Inscripcion).filter(Inscripcion.alumno_id == alumno_id).first()
                diccionario_info_clinica_alumno = {campo: valor for campo, valor in vars(info_clinica_alumno).items() if not(campo.startswith("_")) and campo not in ("info_clin_alumno_id", "alumno_id")}
                
                campos = {
                    "diagnostico_id": "DIAGNÓSTICO",
                    "fecha_diagnostico": "FECHA DEL DIAGNÓSTICO",
                    "medico_tratante": "MÉDICO TRATANTE",
                    "certificacion_discap": "CERTIFICACIÓN DE DISCAPACIDAD",
                    "fecha_vencimiento_certif": "FECHA DE VENCIMIENTO DEL CERTIFICADO DE DISCAPACIDAD",
                    "medicacion": "MEDICACIÓN",
                    "observacion_adicional": "OBSERVACIÓN ADICIONAL"
                }
                
                for clave in diccionario_info_clinica_alumno.keys():
                    if not(campos_info_clinica_alumno.get(clave) == diccionario_info_clinica_alumno.get(clave)):
                        campo_actualizado = campos.get(clave)
                        
                        if (clave == "diagnostico_id"):
                            valor_campo_actual = campos_info_clinica_alumno.get("diagnostico_id")
                            diagnostico_actual = sesion.query(Diagnostico).filter(Diagnostico.diagnostico_id == valor_campo_actual).first()
                            
                            accion = f"ACTUALIZÓ EL CAMPO: {campo_actualizado}. ANTES: {diagnostico_anterior.diagnostico}. AHORA: {diagnostico_actual.diagnostico}. MATRICULA: {inscripcion_alumno.num_matricula}"
                            auditoria_repositorio.registrar(self.entidad, accion)
                        else:
                            valor_campo_anterior = diccionario_info_clinica_alumno.get(clave)
                            valor_campo_actual = campos_info_clinica_alumno.get(clave)
                            
                            accion = f"ACTUALIZÓ EL CAMPO: {campo_actualizado}. ANTES: {valor_campo_anterior}. AHORA: {valor_campo_actual}. MATRICULA: {inscripcion_alumno.num_matricula}"
                            auditoria_repositorio.registrar(self.entidad, accion)
                        
                        sesion.query(InfoClinicaAlumno).filter_by(info_clin_alumno_id = info_clin_alumno_id).update({clave: valor_campo_actual})
                        sesion.commit()
                        print(f"Se actualizó el campo: {campo_actualizado} correctamente \n")
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL ACTUALIZAR LOS CAMPOS: {error}")
    
    def eliminar(self, info_clin_alumno_id: int) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                info_clinica_alumno = sesion.query(InfoClinicaAlumno).filter_by(info_clin_alumno_id = info_clin_alumno_id).first()
                
                if not(info_clinica_alumno):
                    raise BaseDatosError("INFO_CLINICA_ALUMNO_NO_EXISTE", "Esta info clínica del alumno no existe")
                
                diagnostico = sesion.query(Diagnostico).join(InfoClinicaAlumno.diagnostico).filter(InfoClinicaAlumno.info_clin_alumno_id == info_clin_alumno_id).first()
                alumno = sesion.query(Alumno).join(InfoClinicaAlumno.alumno).filter(InfoClinicaAlumno.info_clin_alumno_id == info_clin_alumno_id).first()
                alumno_id = alumno.alumno_id
                inscripcion_alumno = sesion.query(Inscripcion).filter(Inscripcion.alumno_id == alumno_id).first()
                
                accion = f"ELIMINÓ LA INFO CLÍNICA DEL ALUMNO {alumno.primer_nombre} {alumno.apellido_paterno} CON EL DIAGNÓSTICO {diagnostico.diagnostico}. MATRICULA: {inscripcion_alumno.num_matricula}"
                auditoria_repositorio.registrar(self.entidad, accion)
                
                sesion.delete(info_clinica_alumno)
                sesion.commit()
                print("Se eliminó la info clínica del alumno correctamente")
        except BaseDatosError as error:
            sesion.rollback()
            raise error
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL ELIMINAR LA INFO CLÍNICA DEL ALUMNO: {error}")


if __name__ == "__main__":
    info_clinica_alumno_repositorio = InfoClinicaAlumnoRepositorio()
    
    """campos_info_clinica_alumno = {
        "alumno_id": 2,
        "diagnostico_id": 2,
        "fecha_diagnostico": date(2010, 4, 12),
        "medico_tratante": "DR. JOSÉ CONTRERAS",
        "certificacion_discap": "D-345678",
        "fecha_vencimiento_certif": date(2015, 6, 14),
        "medicacion": None,
        "observacion_adicional": None
    }
    
    info_clinica_alumno_repositorio.registrar(campos_info_clinica_alumno)"""
    
    """todos_info_clinica_alumnos = info_clinica_alumno_repositorio.obtener_todos()
    
    for registro in todos_info_clinica_alumnos:
        print(registro)"""
    
    #print(info_clinica_alumno_repositorio.obtener_por_id(2))
    
    """todos_info_clinica_alumno = info_clinica_alumno_repositorio.obtener_por_alumno_id(1)
    
    for registro in todos_info_clinica_alumno:
        print(registro)"""
    
    """campos_info_clinica_alumno = {
        "diagnostico_id": 2,
        "fecha_diagnostico": date(2011, 4, 12),
        "medico_tratante": "DR. JOSÉ CONRERAS",
        "certificacion_discap": "D-346641",
        "fecha_vencimiento_certif": date(2017, 6, 14),
        "medicacion": "X-PASTILLA",
        "observacion_adicional": None,
    }
    
    info_clinica_alumno_repositorio.actualizar(4, campos_info_clinica_alumno)"""
    
    #info_clinica_alumno_repositorio.eliminar(4)
    #info_clinica_alumno_repositorio.eliminar(3)