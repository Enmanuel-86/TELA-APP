from typing import Tuple, List, Optional, Dict
from repositorios.repositorio_base import RepositorioBase
from modelos import Representante, Alumno
from repositorios.usuarios.auditoria_repositorio import auditoria_repositorio
from conexiones.conexion import conexion_bd
from recursos_graficos_y_logicos.utilidades.funciones_sistema import FuncionSistema


class RepresentanteRepositorio(RepositorioBase):
    def __init__(self):
        self.conexion_bd = conexion_bd
        self.entidad = "REPRESENTANTES"
    
    def registrar(self, campos: Dict) -> int:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                ruta_foto_perfil = campos["foto_perfil"]
                foto_perfil = FuncionSistema.cargar_foto_perfil(ruta_foto_perfil)
                campos["foto_perfil"] = foto_perfil
                
                nuevo_representante = Representante(**campos)
                
                sesion.add(nuevo_representante)
                sesion.commit()
                sesion.refresh(nuevo_representante)
                print("Se registró el representante correctamente")
                
                accion = f"REGISTRÓ A {nuevo_representante.nombre} {nuevo_representante.apellido}. CÉDULA: {nuevo_representante.cedula}"
                auditoria_repositorio.registrar(self.entidad, accion)
                return nuevo_representante.representante_id
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL REGISTRAR EL REPRESENTANTE: {error}")
    
    def obtener_todos(self) -> List[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                representantes = sesion.query(
                    Representante.representante_id,
                    Representante.cedula,
                    Representante.nombre,
                    Representante.apellido,
                    Representante.direccion_residencia,
                    Representante.num_telefono,
                    Representante.num_telefono_adicional,
                    Representante.carga_familiar,
                    Representante.estado_civil,
                    Representante.foto_perfil
                ).all()
                return representantes
        except Exception as error:
            print(f"ERROR AL OBTENER TODOS LOS REPRESENTANTES: {error}")
    
    def obtener_por_id(self, representante_id: int) -> Optional[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                representante = sesion.query(
                    Representante.representante_id,
                    Representante.cedula,
                    Representante.nombre,
                    Representante.apellido,
                    Representante.direccion_residencia,
                    Representante.num_telefono,
                    Representante.num_telefono_adicional,
                    Representante.carga_familiar,
                    Representante.estado_civil,
                    Representante.foto_perfil
                ).filter_by(representante_id = representante_id).first()
                return representante
        except Exception as error:
            print(f"ERROR AL OBTENER EL REPRESENTANTE: {error}")
    
    def obtener_por_cedula(self, cedula: str) -> Optional[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                representante = sesion.query(
                    Representante.representante_id,
                    Representante.cedula,
                    Representante.nombre,
                    Representante.apellido,
                    Representante.direccion_residencia,
                    Representante.num_telefono,
                    Representante.num_telefono_adicional,
                    Representante.carga_familiar,
                    Representante.estado_civil,
                    Representante.foto_perfil
                ).filter_by(cedula = cedula).first()
                
                return representante
        except Exception as error:
            print(f"ERROR AL OBTENER EL REPRESENTANTE: {error}")
    
    def obtener_todos_o_por_cedula(self, cedula: str = None) -> List[Tuple]:
        try:
            if not(cedula):
                return self.obtener_todos()
            else:
                return self.obtener_por_cedula(cedula)
        except Exception as error:
            print(f"ERROR AL OBTENER A LOS REPRESENTANTES O AL REPRESENTANTE: {error}")
    
    def obtener_alumnos_representados(self, representante_id: int) -> List[Tuple]:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                alumnos_representados = sesion.query(
                    Representante.representante_id,
                    Alumno.alumno_id,
                    Alumno.cedula,
                    Alumno.primer_nombre,
                    Alumno.apellido_paterno
                ).join(Representante.alumno).filter(Representante.representante_id == representante_id).all()
                
                return alumnos_representados
        except Exception as error:
            print(f"ERROR AL OBTENER LOS ALUMNOS REPRESENTADOS: {error}")
    
    def actualizar(self, representante_id: int, campos_representante: Dict) -> None:
        try:
            with self.conexion_bd.obtener_sesion_bd() as sesion:
                representante = sesion.query(Representante).filter_by(representante_id = representante_id).first()
                diccionario_representante = {campo: valor for campo, valor in vars(representante).items() if not(campo.startswith("_")) and not(campo == "representante_id")}
                
                campos = {
                    "cedula": "CÉDULA",
                    "nombre": "NOMBRE",
                    "apellido": "APELLIDO",
                    "direccion_residencia": "DIRECCIÓN DE RESIDENCIA",
                    "num_telefono": "NÚMERO DE TELÉFONO",
                    "num_telefono_adicional": "NÚMERO DE TELÉFONO ADICIONAL",
                    "carga_familiar": "CARGA FAMILIAR",
                    "estado_civil": "ESTADO CIVIL",
                    "foto_perfil": "FOTO DE PERFIL"
                }
                
                for clave in diccionario_representante.keys():
                    if not(campos_representante.get(clave) == diccionario_representante.get(clave)):
                        campo_actualizado = campos.get(clave)
                        
                        if (clave == "foto_perfil"):
                            ruta_foto_perfil = campos_representante.get(clave)
                            foto_perfil = FuncionSistema.cargar_foto_perfil(ruta_foto_perfil)
                            
                            valor_campo_actual = foto_perfil
                            
                            accion = f"ACTUALIZÓ EL CAMPO: {campo_actualizado}. CÉDULA DEL REPRESENTANTE AFECTADO: {representante.cedula}"
                        else:
                            valor_campo_anterior = diccionario_representante.get(clave)
                            valor_campo_actual = campos_representante.get(clave)
                            
                            accion = f"ACTUALIZÓ EL CAMPO: {campo_actualizado}. ANTES: {valor_campo_anterior}. AHORA: {valor_campo_actual}. CÉDULA DEL REPRESENTANTE AFECTADO: {representante.cedula}"
                            auditoria_repositorio.registrar(self.entidad, accion)
                        
                        sesion.query(Representante).filter_by(representante_id = representante_id).update({clave: valor_campo_actual})
                        sesion.commit()
                        print(f"Se actualizó el campo: {campo_actualizado} correctamente \n")
        except Exception as error:
            sesion.rollback()
            print(f"ERROR AL ACTUALIZAR LOS CAMPOS: {error}")

representante_repositorio = RepresentanteRepositorio()

if __name__ == "__main__":
    representante_repositorio = RepresentanteRepositorio()
    
    """campos_representante = {
        "cedula": "9821456",
        "nombre": "JOSÉ",
        "apellido": "GÓMEZ",
        "direccion_residencia": "BOYACÁ 2",
        "num_telefono": "0412123678",
        "carga_familiar": 4,
        "estado_civil": None
    }
    
    representante_repositorio.registrar(campos_representante)"""
    
    """todos_representantes = representante_repositorio.obtener_todos()
    
    for registro in todos_representantes:
        print(registro)"""
    
    
    #print(representante_repositorio.obtener_por_id(1))
    
    """todos_representantes = representante_repositorio.obtener_alumnos_representados(2)
    
    if type(todos_representantes) == list:
        for registro in todos_representantes:
            print(registro)
    else:
        print(todos_representantes)"""
    
    
    """todos_representantes = representante_repositorio.obtener_todos_o_por_cedula("123456")
    
    if type(todos_representantes) == list:
        for registro in todos_representantes:
            print(registro)
    else:
        print(todos_representantes)"""
    
    """campos_representante = {
        "cedula": "9821456",
        "nombre": "ANGEL",
        "apellido": "GÓMEZ",
        "direccion_residencia": "BOYACÁ 2",
        "num_telefono": "0412123678",
        "carga_familiar": 4,
        "estado_civil": "Soltero/a"
    }
    
    representante_repositorio.actualizar(3, campos_representante)"""