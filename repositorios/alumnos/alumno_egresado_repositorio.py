from typing import Tuple, List, Optional, Dict, Union
from datetime import date
from excepciones.base_datos_error import BaseDatosError
from modelos import AlumnoEgresado, Alumno, Especialidad, Inscripcion
from repositorios.repositorio_base import RepositorioBase
from repositorios.usuarios.auditoria_repositorio import auditoria_repositorio
from conexiones.conexion import conexion_bd


class AlumnoEgresadoRepositorio(RepositorioBase):
    def __init__(self):
        self.conexion_bd = conexion_bd
        self.entidad = "ALUMNOS EGRESADOS"
    
    def registrar(self, campos: Dict) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                nuevo_alumno_egresado = AlumnoEgresado(**campos)
                
                alumno_id = campos.get("alumno_id")
                alumno = sesion.query(Alumno).filter_by(alumno_id = alumno_id).first()
                inscripcion_alumno = sesion.query(Inscripcion).filter_by(alumno_id = alumno_id).first()
                
                especialidad_id = inscripcion_alumno.especialidad_id
                especialidad = sesion.query(Especialidad).filter_by(especialidad_id = especialidad_id).first()
                
                sesion.add(nuevo_alumno_egresado)
                sesion.commit()
                sesion.refresh(nuevo_alumno_egresado)
                print("Se registró el egreso del alumno correctamente")
                
                accion = f"REGISTRÓ EL EGRESO DEL ALUMNO {alumno.primer_nombre} {alumno.apellido_paterno} DE LA ESPECIALIDAD {especialidad.especialidad}. MATRICULA: {inscripcion_alumno.num_matricula}"
                auditoria_repositorio.registrar(self.entidad, accion)
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL EGRESAR AL ALUMNO: {error}")
    
    def obtener_todos(self) -> List[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                alumnos_egresados = (
                    sesion.query(
                        AlumnoEgresado.alumno_egresado_id,
                        Especialidad.especialidad_id,
                        Alumno.alumno_id,
                        Inscripcion.num_matricula,
                        Alumno.cedula,
                        Alumno.primer_nombre,
                        Alumno.segundo_nombre,
                        Alumno.apellido_paterno,
                        Alumno.apellido_materno,
                        AlumnoEgresado.razon_egreso,
                        AlumnoEgresado.fecha_emision
                    )
                    .join(AlumnoEgresado.alumno)
                    .join(Alumno.inscripcion)
                    .join(Inscripcion.especialidad)
                    .order_by(AlumnoEgresado.alumno_egresado_id)
                ).all()
                
                return alumnos_egresados
        except Exception as error:
            print(f"ERROR AL OBTENER A LOS ALUMNOS EGRESADOS: {error}")
    
    def obtener_por_id(self, alumno_id: int) -> Optional[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                alumno_egresado = (
                    sesion.query(
                        AlumnoEgresado.alumno_egresado_id,
                        Especialidad.especialidad_id,
                        Alumno.alumno_id,
                        Inscripcion.num_matricula,
                        Alumno.cedula,
                        Alumno.primer_nombre,
                        Alumno.segundo_nombre,
                        Alumno.apellido_paterno,
                        Alumno.apellido_materno,
                        AlumnoEgresado.razon_egreso,
                        AlumnoEgresado.fecha_emision
                    )
                    .join(AlumnoEgresado.alumno)
                    .join(Alumno.inscripcion)
                    .join(Inscripcion.especialidad)
                    .order_by(AlumnoEgresado.alumno_egresado_id)
                ).filter(AlumnoEgresado.alumno_id == alumno_id).first()
                
                if not(alumno_egresado):
                    raise BaseDatosError("ALUMNO_EGRESADO_NO_EXISTE", "Este registro de alumno egresado no existe")
                
                return alumno_egresado
        except BaseDatosError as error:
            raise error
        except Exception as error:
            print(f"ERROR AL OBTENER AL ALUMNO EGRESADO: {error}")
    
    def obtener_por_cedula(self, cedula: str) -> Optional[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                alumno_egresado = (
                    sesion.query(
                        AlumnoEgresado.alumno_egresado_id,
                        Especialidad.especialidad_id,
                        Alumno.alumno_id,
                        Inscripcion.num_matricula,
                        Alumno.cedula,
                        Alumno.primer_nombre,
                        Alumno.segundo_nombre,
                        Alumno.apellido_paterno,
                        Alumno.apellido_materno,
                        AlumnoEgresado.razon_egreso,
                        AlumnoEgresado.fecha_emision
                    )
                    .join(AlumnoEgresado.alumno)
                    .join(Alumno.inscripcion)
                    .join(Inscripcion.especialidad)
                    .order_by(AlumnoEgresado.alumno_egresado_id)
                ).filter(Alumno.cedula == cedula).first()
                
                if not(alumno_egresado):
                    raise BaseDatosError("ALUMNO_EGRESADO_NO_EXISTE", "Este registro de alumno egresado no existe")
                
                return alumno_egresado
        except BaseDatosError as error:
            raise error
        except Exception as error:
            print(f"ERROR AL OBTENER AL ALUMNO EGRESADO: {error}")
    
    def obtener_por_num_matricula(self, num_matricula: str) -> Optional[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                alumno_egresado = (
                    sesion.query(
                        AlumnoEgresado.alumno_egresado_id,
                        Especialidad.especialidad_id,
                        Alumno.alumno_id,
                        Inscripcion.num_matricula,
                        Alumno.cedula,
                        Alumno.primer_nombre,
                        Alumno.segundo_nombre,
                        Alumno.apellido_paterno,
                        Alumno.apellido_materno,
                        AlumnoEgresado.razon_egreso,
                        AlumnoEgresado.fecha_emision
                    )
                    .join(AlumnoEgresado.alumno)
                    .join(Alumno.inscripcion)
                    .join(Inscripcion.especialidad)
                    .order_by(AlumnoEgresado.alumno_egresado_id)
                ).filter(Inscripcion.num_matricula == num_matricula).first()
                
                if not(alumno_egresado):
                    raise BaseDatosError("ALUMNO_EGRESADO_NO_EXISTE", "Este registro de alumno egresado no existe")
                
                return alumno_egresado
        except BaseDatosError as error:
            raise error
        except Exception as error:
            print(f"ERROR AL OBTENER AL ALUMNO EGRESADO: {error}")
    
    def obtener_por_especialidad(self, especialidad_id: int) -> List[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                alumnos_egresados = (
                    sesion.query(
                        AlumnoEgresado.alumno_egresado_id,
                        Especialidad.especialidad_id,
                        Alumno.alumno_id,
                        Inscripcion.num_matricula,
                        Alumno.cedula,
                        Alumno.primer_nombre,
                        Alumno.segundo_nombre,
                        Alumno.apellido_paterno,
                        Alumno.apellido_materno,
                        AlumnoEgresado.razon_egreso,
                        AlumnoEgresado.fecha_emision
                    )
                    .join(AlumnoEgresado.alumno)
                    .join(Alumno.inscripcion)
                    .join(Inscripcion.especialidad)
                    .order_by(AlumnoEgresado.alumno_egresado_id)
                ).filter(Especialidad.especialidad_id == especialidad_id).all()
                
                if not(alumnos_egresados):
                    raise BaseDatosError("ALUMNOS_EGRESADOS_NO_EXISTEN", "No hay alumnos egresados por esta especialidad")
                
                return alumnos_egresados
        except BaseDatosError as error:
            raise error
        except Exception as error:
            print(f"ERROR AL OBTENER A LOS ALUMNOS EGRESADOS: {error}")
    
    def obtener_por_especialidad_o_cedula(self, especialidad_id: int, cedula: str = None) -> Union[List[Tuple], Tuple]:
        try:
            if not(cedula):
                return self.obtener_por_especialidad(especialidad_id)
            
            if ((self.obtener_por_especialidad(especialidad_id)) and (self.obtener_por_cedula(cedula))):
                return self.obtener_por_cedula(cedula)
        except BaseDatosError as error:
            raise error
        except Exception as error:
            print(f"ERROR AL OBTENER A LOS ALUMNOS EGRESADOS POR ESPECIALIDAD O CÉDULA: {error}")
    
    def obtener_por_especialidad_o_matricula(self, especialidad_id: int, num_matricula: str = None) -> Union[List[Tuple], Tuple]:
        try:
            if not(num_matricula):
                return self.obtener_por_especialidad(especialidad_id)
            
            if ((self.obtener_por_especialidad(especialidad_id)) and (self.obtener_por_num_matricula(num_matricula))):
                return self.obtener_por_num_matricula(num_matricula)
        except BaseDatosError as error:
            raise error
        except Exception as error:
            print(f"ERROR AL OBTENER A LOS ALUMNOS EGRESADOS POR ESPECIALIDAD O MATRICULA: {error}")
    
    def actualizar(self, alumno_id: int, campos_alumno_egresado: Dict) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                alumno_egresado = sesion.query(AlumnoEgresado).filter_by(alumno_id = alumno_id).first()
                inscripcion_alumno = sesion.query(Inscripcion).filter_by(alumno_id = alumno_id).first()
                diccionario_alumno_egresado = {campo: valor for campo, valor in vars(alumno_egresado).items() if not(campo.startswith("_")) and campo not in("alumno_egresado_id", "alumno_id")}
                
                campos = {
                    "fecha_emision": "FECHA DE EMISIÓN",
                    "razon_egreso": "RAZÓN DEL EGRESO"
                }
                
                for clave in diccionario_alumno_egresado.keys():
                    if not(campos_alumno_egresado.get(clave) == diccionario_alumno_egresado.get(clave)):
                        campo_actualizado = campos.get(clave)
                        
                        valor_campo_anterior = diccionario_alumno_egresado.get(clave)
                        valor_campo_actual = campos_alumno_egresado.get(clave)
                        
                        accion = f"ACTUALIZÓ EL CAMPO: {campo_actualizado}. ANTES: {valor_campo_anterior}. AHORA: {valor_campo_actual}. MATRICULA: {inscripcion_alumno.num_matricula}"
                        auditoria_repositorio.registrar(self.entidad, accion)
                        
                        sesion.query(AlumnoEgresado).filter_by(alumno_id = alumno_id).update({clave: valor_campo_actual})
                        sesion.commit()
                        print(f"Se actualizó el campo: {campo_actualizado} correctamente \n")
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL ACTUALIZAR LOS CAMPOS: {error}")
    
    def eliminar(self, alumno_id: int) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                alumno_egresado = sesion.query(AlumnoEgresado).filter_by(alumno_id = alumno_id).first()
                
                if not(alumno_egresado):
                    raise BaseDatosError("ALUMNO_EGRESADO_NO_EXISTE", "Este registro de alumno egresado no existe")
                
                alumno = sesion.query(Alumno).filter_by(alumno_id = alumno_id).first()
                inscripcion_alumno = sesion.query(Inscripcion).filter_by(alumno_id = alumno_id).first()
                especialidad_id = inscripcion_alumno.especialidad_id
                especialidad = sesion.query(Especialidad).filter_by(especialidad_id = especialidad_id).first()
                
                accion = f"ELIMINÓ EL EGRESO DE {alumno.primer_nombre} {alumno.apellido_paterno} DE LA ESPECIALIDAD {especialidad.especialidad}. MATRICULA: {inscripcion_alumno.num_matricula}"
                auditoria_repositorio.registrar(self.entidad, accion)
                
                sesion.delete(alumno_egresado)
                sesion.commit()
                print("Se eliminó el egreso del alumno correctamente")
        except BaseDatosError as error:
            sesion.rollback()
            raise error
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL ELIMINAR EL EGRESO DEL ALUMNO: {error}")


if __name__ == "__main__":
    alumno_egresado_repositorio = AlumnoEgresadoRepositorio()
    
    """campos_alumno_egresado = {
        "alumno_id": 16,
        "fecha_emision": date.today(),
        "razon_egreso": "X RAZÓN n2"
    }
    
    alumno_egresado_repositorio.registrar(campos_alumno_egresado)"""
    
    """todos_alumnos_egresados = alumno_egresado_repositorio.obtener_todos()
    
    for registro in todos_alumnos_egresados:
        print(registro)"""
    
    """try:
        print(alumno_egresado_repositorio.obtener_por_id(17))
    except BaseDatosError as error:
        print(error)"""
    
    """try:
        print(alumno_egresado_repositorio.obtener_por_cedula("30932925"))
    except BaseDatosError as error:
        print(error)"""
    
    """try:
        print(alumno_egresado_repositorio.obtener_por_num_matricula("MAT-4a1e5b2"))
    except BaseDatosError as error:
        print(error)"""
    
    """try:
        todos_alumnos_egresados_por_especialidad_o_cedula = alumno_egresado_repositorio.obtener_por_especialidad_o_cedula(1, "30932925")
        
        if (type(todos_alumnos_egresados_por_especialidad_o_cedula) == list):
            for registro in todos_alumnos_egresados_por_especialidad_o_cedula:
                print(registro)
        else:
            print(todos_alumnos_egresados_por_especialidad_o_cedula)
    except BaseDatosError as error:
        print(error)"""
    
    """campos_alumno_egresado = {
        "fecha_emision": date(2025, 4, 14),
        "razon_egreso": "IRSE A OTRO PAIS"
    }
    
    alumno_egresado_repositorio.actualizar(17, campos_alumno_egresado)"""
    
    #alumno_egresado_repositorio.eliminar(17)