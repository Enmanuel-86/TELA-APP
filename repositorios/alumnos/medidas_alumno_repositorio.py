from typing import Tuple, List, Dict
from repositorios.repositorio_base import RepositorioBase
from modelos import MedidasAlumno, Alumno, Inscripcion
from repositorios.usuarios.auditoria_repositorio import auditoria_repositorio
from conexiones.conexion import conexion_bd


class MedidasAlumnoRepositorio(RepositorioBase):
    def __init__(self):
        self.conexion_bd = conexion_bd
        self.entidad = "ALUMNOS"
    
    def registrar(self, campos: Dict) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                nueva_medidas_alumno = MedidasAlumno(**campos)
                
                sesion.add(nueva_medidas_alumno)
                sesion.commit()
                sesion.refresh(nueva_medidas_alumno)
                print("Se registró las medidas del alumno correctamente")
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL REGISTRAR LAS MEDIDAS DEL ALUMNO: {error}")
    
    def obtener_todos(self) -> List[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                medidas_alumnos = sesion.query(
                    MedidasAlumno.medid_alumno_id,
                    Alumno.alumno_id,
                    MedidasAlumno.estatura,
                    MedidasAlumno.peso,
                    MedidasAlumno.talla_camisa,
                    MedidasAlumno.talla_pantalon,
                    MedidasAlumno.talla_zapatos
                ).join(Alumno.medidas_alumno).all()
                
                return medidas_alumnos
        except Exception as error:
            print(f"ERROR AL OBTENER LAS MEDIDAS DE LOS ALUMNOS: {error}")
    
    def obtener_por_id(self, alumno_id: int) -> Tuple:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                medidas_alumno = sesion.query(
                    MedidasAlumno.medid_alumno_id,
                    Alumno.alumno_id,
                    MedidasAlumno.estatura,
                    MedidasAlumno.peso,
                    MedidasAlumno.talla_camisa,
                    MedidasAlumno.talla_pantalon,
                    MedidasAlumno.talla_zapatos
                ).join(Alumno.medidas_alumno).filter(Alumno.alumno_id == alumno_id).first()
                
                return medidas_alumno
        except Exception as error:
            print(f"ERROR AL OBTENER LAS MEDIDAS DEL ALUMNO: {error}")
    
    def actualizar(self, alumno_id: int, campos_medida_alumno: Dict) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                medidas_alumno = sesion.query(MedidasAlumno).filter_by(alumno_id = alumno_id).first()
                alumno = sesion.query(Alumno).filter_by(alumno_id = alumno_id).first()
                inscripcion_alumno = sesion.query(Inscripcion).join(Inscripcion.alumno).filter(Inscripcion.alumno_id == alumno_id).first()
                diccionario_medidas_alumno = {campo: valor for campo, valor in vars(medidas_alumno).items() if not(campo.startswith("_")) and not(campo == "medid_alumno_id") and not(campo == "alumno_id")}
                
                campos = {
                    "estatura": "ESTATURA",
                    "peso": "PESO",
                    "talla_camisa": "TALLA DE CAMISA",
                    "talla_pantalon": "TALLA DE PANTALÓN",
                    "talla_zapatos": "TALLA DE ZAPATOS"
                }
                
                for clave in diccionario_medidas_alumno.keys():
                    if not(campos_medida_alumno.get(clave) == diccionario_medidas_alumno.get(clave)):
                        campo_actualizado = campos.get(clave)
                        
                        valor_campo_anterior = diccionario_medidas_alumno.get(clave)
                        valor_campo_actual = campos_medida_alumno.get(clave)
                        
                        accion = f"ACTUALIZÓ EL CAMPO: {campo_actualizado}. ANTES: {valor_campo_anterior}. AHORA: {valor_campo_actual}. MATRICULA: {inscripcion_alumno.num_matricula}"
                        auditoria_repositorio.registrar(self.entidad, accion)
                        
                        sesion.query(MedidasAlumno).filter_by(alumno_id = alumno_id).update({clave: valor_campo_actual})
                        sesion.commit()
                        print(f"Se actualizó el campo: {campo_actualizado} correctamente \n")
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL ACTUALIZAR LOS CAMPOS: {error}")


if __name__ == "__main__":
    medidas_alumno_repositorio = MedidasAlumnoRepositorio()
    
    """campos_medidas_alumno = {
        "alumno_id": 21,
        "estatura": 1.87,
        "peso": 59.5,
        "talla_camisa": "S",
        "talla_pantalon": 30,
        "talla_zapatos": 45
    }
    
    medidas_alumno_repositorio.registrar(campos_medidas_alumno)"""
    
    """todos_medidas_alumnos = medidas_alumno_repositorio.obtener_todos()
    
    for registro in todos_medidas_alumnos:
        print(registro)"""
    
    #print(medidas_alumno_repositorio.obtener_por_id(21))
    
    """campos_medidas_alumno = {
        "estatura": 1.87,
        "peso": 56.5,
        "talla_camisa": "M",
        "talla_pantalon": 30,
        "talla_zapatos": 42
    }
    
    medidas_alumno_repositorio.actualizar(21, campos_medidas_alumno)"""