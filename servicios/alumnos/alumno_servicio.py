import re
from string import digits
from typing import Tuple, List, Optional, Dict
from datetime import date
from excepciones.base_datos_error import BaseDatosError
from repositorios.repositorio_base import RepositorioBase
from repositorios.alumnos.alumno_repositorio import AlumnoRepositorio


class AlumnoServicio:
    def __init__(self, repositorio: RepositorioBase):
        self.repositorio = repositorio
    
    def validar_cedula(self, cedula: str, alumno_id: Optional[int] = None) -> List[str]:
        errores = []
        
        if (cedula):
            cedula_sin_espacios = cedula.replace(" ", "")
            alumno_a_actualizar = None
            contiene_numeros = all(caracter in digits for caracter in cedula)
            
            if (alumno_id):
                alumno_a_actualizar = self.obtener_alumno_por_id(alumno_id)
            
            try:
                alumno_ya_existe = self.obtener_alumno_por_cedula(cedula)
                
                if (alumno_ya_existe):
                    id_alumno_existente = alumno_ya_existe[0]
                    id_alumno_a_actualizar = alumno_a_actualizar[0]
                    
                    if ((alumno_id is None) or (id_alumno_existente != id_alumno_a_actualizar)):
                        errores.append("Cédula del alumno: Esta cédula ya está registrada.")
            except BaseDatosError:
                pass
            
            if (len(cedula_sin_espacios) == 0):
                errores.append("Cédula del alumno: No puede contener solo espacios vacíos.")
            
            if not(contiene_numeros):
                errores.append("Cédula del alumno: No debe contener letras, espacios o caracteres especiales.")
            
            if (len(cedula) > 10):
                errores.append("Cédula del alumno: No puede contener más de 10 caracteres.")
        
        return errores
    
    def validar_primer_nombre(self, primer_nombre: str) -> List[str]:
        errores = []
        
        if (not(primer_nombre)):
            errores.append("Primer nombre: No puede estar vacío.")
        elif (primer_nombre):
            primer_nombre_sin_espacios = primer_nombre.replace(" ", "")
            estructura_primer_nombre = re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+$", primer_nombre)
            if (len(primer_nombre_sin_espacios) == 0):
                errores.append("Primer nombre: No puede estar vacío.")
        
            if (not(estructura_primer_nombre)):
                errores.append("Primer nombre: No debe contener números o caracteres especiales.")
        
            if (len(primer_nombre) > 15):
                errores.append("Primer nombre: No puede contener más de 15 caracteres.")
        
        return errores
    
    def validar_segundo_nombre(self, segundo_nombre: str) -> List[str]:
        errores = []
        
        if (segundo_nombre):
            estructura_segundo_nombre = re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+$", segundo_nombre)
            if (not(estructura_segundo_nombre)):
                errores.append("Segundo nombre: No debe contener números o caracteres especiales.")
            
            if (len(segundo_nombre) > 15):
                errores.append("Segundo nombre: No puede contener más de 15 caracteres.")
        
        return errores
    
    def validar_tercer_nombre(self, tercer_nombre: str) -> List[str]:
        errores = []
        
        if (tercer_nombre):
            estructura_tercer_nombre = re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+$", tercer_nombre)
            if (not(estructura_tercer_nombre)):
                errores.append("Tercer nombre: No debe contener números o caracteres especiales.")
            
            if (len(tercer_nombre) > 15):
                errores.append("Tercer nombre: No puede contener más de 15 caracteres.")
        
        return errores
    
    def validar_apellido_paterno(self, apellido_paterno: str) -> List[str]:
        errores = []
        
        if (not(apellido_paterno)):
            errores.append("Apellido paterno: No puede estar vacío.")
        elif (apellido_paterno):
            apellido_paterno_sin_espacios = apellido_paterno.replace(" ", "")
            estructura_apellido_paterno = re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+$", apellido_paterno)
            if (len(apellido_paterno_sin_espacios) == 0):
                errores.append("Apellido paterno: No puede estar vacío.")
        
            if (not(estructura_apellido_paterno)):
                errores.append("Apellido paterno: No debe contener números o caracteres especiales.")
        
            if (len(apellido_paterno) > 15):
                errores.append("Apellido paterno: No puede contener más de 15 caracteres.")
        
        return errores
    
    def validar_apellido_materno(self, apellido_materno: str) -> List[str]:
        errores = []
        
        if (apellido_materno):
            estructura_apellido_materno = re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+$", apellido_materno)
            if not(estructura_apellido_materno):
                errores.append("Apellido materno: No puede contener números o caracteres especiales.")
            
            if (len(apellido_materno) > 15):
                errores.append("Apellido materno: No puede contener más de 15 caracteres.")
        
        return errores
    
    def validar_relacion_con_rep(self, relacion_con_rep: str) -> List[str]:
        errores = []
        
        if not(relacion_con_rep):
            errores.append("Relación con el representante: No puede estar vacío.")
        elif (relacion_con_rep):
            relacion_con_rep_sin_espacios = relacion_con_rep.replace(" ", "")
            if (len(relacion_con_rep_sin_espacios) == 0):
                errores.append("Relación con el representante: No puede estar vacío.")
            
            if (len(relacion_con_rep) > 15):
                errores.append("Relación con el representante: No puede contener más de 15 caracteres.")
        
        return errores
    
    def validar_fecha_nacimiento(self, fecha_nacimiento: str) -> List[str]:
        errores = []
        
        if not(fecha_nacimiento):
            errores.append("Fecha de nacimiento: No puede estar vacío.")
        
        return errores
    
    def validar_lugar_nacimiento(self, lugar_nacimiento: str) -> List[str]:
        errores = []
        
        if (not(lugar_nacimiento)):
            errores.append("Lugar de nacimiento: No puede estar vacío.")
        elif (lugar_nacimiento):
            lugar_nacimiento_sin_espacios = lugar_nacimiento.replace(" ", "")
            if (len(lugar_nacimiento_sin_espacios) == 0):
                errores.append("Lugar de nacimiento: No puede estar vacío.")
        
            if (len(lugar_nacimiento) > 40):
                errores.append("Lugar de nacimiento: No puede contener más de 40 caracteres.")
        
        return errores
    
    def validar_escolaridad(self, escolaridad: str) -> List[str]:
        errores = []
        
        if (escolaridad):
            if (len(escolaridad) > 20):
                errores.append("Escolaridad: No puede contener más de 15 caracteres.")
        
        return errores
    
    def validar_procedencia(self, procedencia: str) -> List[str]:
        errores = []
        
        if (procedencia):
            if (len(procedencia) > 35):
                errores.append("Procedencia: No puede contener más de 35 caracteres.")
        
        return errores
    
    def validar_fecha_ingreso_institucion(self, fecha_ingreso_institucion: date) -> List[str]:
        errores = []
        
        if not(fecha_ingreso_institucion):
            errores.append("Fecha de Ingreso a la Institución: No puede estar vacío.")
        
        return errores
    
    def validar_campos_primera_info_alumno(
        self, cedula: str,
        primer_nombre: str, segundo_nombre: str, tercer_nombre: str,
        apellido_paterno: str, apellido_materno: str,
        relacion_con_rep: str, fecha_ingreso_institucion: date, alumno_id: Optional[int] = None
    ) -> List[str]:
        error_cedula = self.validar_cedula(cedula, alumno_id)
        error_primer_nombre = self.validar_primer_nombre(primer_nombre)
        error_segundo_nombre = self.validar_segundo_nombre(segundo_nombre)
        error_tercer_nombre = self.validar_tercer_nombre(tercer_nombre)
        error_apellido_paterno = self.validar_apellido_paterno(apellido_paterno)
        error_apellido_materno = self.validar_apellido_materno(apellido_materno)
        error_relacion_con_rep = self.validar_relacion_con_rep(relacion_con_rep)
        error_fecha_ingreso_institucion = self.validar_fecha_ingreso_institucion(fecha_ingreso_institucion)
        
        errores_totales = error_cedula + error_primer_nombre + error_segundo_nombre + error_tercer_nombre + error_apellido_paterno + error_apellido_materno + error_relacion_con_rep + error_fecha_ingreso_institucion
        
        return errores_totales
    
    def validar_campos_segunda_info_alumno(self, fecha_nacimiento: date, lugar_nacimiento: str) -> List[str]:
        error_fecha_nacimiento = self.validar_fecha_nacimiento(fecha_nacimiento)
        error_lugar_nacimiento = self.validar_lugar_nacimiento(lugar_nacimiento)
        
        errores_totales = error_fecha_nacimiento + error_lugar_nacimiento
        
        return errores_totales
    
    def validar_info_academica(self, escolaridad: str, procedencia: str) -> List[str]:
        error_escolaridad = self.validar_escolaridad(escolaridad)
        error_procedencia = self.validar_procedencia(procedencia)
        
        errores_totales = error_escolaridad + error_procedencia
        
        return errores_totales
    
    def registrar_alumno(self, campos: Dict) -> int:
        return self.repositorio.registrar(campos)
    
    def obtener_todos_alumnos(self) -> List[Tuple]:
        return self.repositorio.obtener_todos()
    
    def obtener_alumno_por_id(self, alumno_id: int) -> Optional[Tuple]:
        return self.repositorio.obtener_por_id(alumno_id)
    
    def obtener_alumno_por_cedula(self, cedula: str) -> Optional[Tuple]:
        return self.repositorio.obtener_por_cedula(cedula)
    
    def obtener_datos_representante(self, alumno_id: int) -> Tuple:
        return self.repositorio.obtener_datos_representante(alumno_id)
    
    def obtener_info_academica_alumno(self, alumno_id: int) -> Tuple:
        return self.repositorio.obtener_info_academica(alumno_id)
    
    def actualizar_alumno(self, alumno_id: int, campos_alumno: Dict) -> None:
        self.repositorio.actualizar(alumno_id, campos_alumno)
    
    def eliminar_alumno(self, alumno_id: int) -> None:
        self.repositorio.eliminar(alumno_id)


if __name__ == "__main__":
    alumno_repositorio = AlumnoRepositorio()
    alumno_servicio = AlumnoServicio(alumno_repositorio)
    
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
    
    alumno_servicio.registrar_alumno(campos_alumno)"""
    
    """todos_alumnos = alumno_servicio.obtener_todos_alumnos()
    
    for registro in todos_alumnos:
        print(registro)"""
    
    """try:
        print(alumno_servicio.obtener_alumno_por_id(20))
    except BaseDatosError as error:
        print(error)"""
    
    #print(alumno_servicio.obtener_alumno_por_cedula("30932925"))
    #print(alumno_servicio.obtener_datos_representante(7))
    #print(alumno_servicio.obtener_info_academica_alumno(10))
    
    """campos_alumno = {
        "representante_id": 2,
        "cedula": "1821397",
        "primer_nombre": "ALEJANDRO",
        "segundo_nombre": "ALONSO",
        "apellido_paterno": "CHACÓN",
        "apellido_materno": "CONTRERAS",
        "fecha_nacimiento": date(2005, 10, 11),
        "lugar_nacimiento": "PUERTO LA CRUZ",
        "sexo": "M",
        "cma": 0,
        "imt": 0,
        "fecha_ingreso_institucion": date(2025, 1, 15),
        "relacion_con_rep": "PADRE",
        "escolaridad": "5to grado aprobado",
        "procedencia": "PABLO NERUDA",
        "situacion": "Inicial"
    }
    
    alumno_servicio.actualizar_alumno(15, campos_alumno)"""
    
    #alumno_servicio.eliminar_alumno(15)
    
    """campos_alumno = {
        "cedula": "1821397",
        "primer_nombre": "ALEJANDRO",
        "segundo_nombre": "ALONSO",
        "apellido_paterno": "CHACÓN",
        "apellido_materno": "CONTRERAS",
        "fecha_nacimiento": date(2005, 10, 11),
        "lugar_nacimiento": "PUERTO LA CRUZ",
        "relacion_con_rep": "PADRE",
        "escolaridad": "5to grado aprobado",
        "procedencia": "PABLO NERUDA",
        "fecha_ingreso_institucion": date.today()
    }
    
    errores_totales_primer_info = alumno_servicio.validar_campos_primera_info_alumno(
        campos_alumno.get("cedula"),
        campos_alumno.get("primer_nombre"),
        campos_alumno.get("segundo_nombre"),
        campos_alumno.get("apellido_paterno"),
        campos_alumno.get("apellido_materno"),
        campos_alumno.get("relacion_con_rep"),
        campos_alumno.get("fecha_ingreso_institucion")
    )
    
    errores_totales_segunda_info = alumno_servicio.validar_campos_segunda_info_alumno(
        campos_alumno.get("fecha_nacimiento"),
        campos_alumno.get("lugar_nacimiento")
    )
    
    errores_totales_info_academica = alumno_servicio.validar_info_academica(
        campos_alumno.get("escolaridad"),
        campos_alumno.get("procedencia")
    )
    
    if errores_totales_primer_info:
        print("\n".join(errores_totales_primer_info))
    else:
        print("Registro de info básica 1 exitosa.")
    
    if errores_totales_segunda_info:
        print("\n". join(errores_totales_segunda_info))
    else:
        print("Registro de info básica 2 exitosa.")
    
    if errores_totales_info_academica:
        print("\n".join(errores_totales_info_academica))
    else:
        print("Registro de info académica exitosa")"""
    
    
    # Si pongo la cédula: 029548939 (que ya está registrada en la base de datos) lanza el error que deberia lanzar
    # Si pongo la cédula: 30466351 (que le corresponde al alumno_id de aquel alumno que estoy actualizando) no me lanza el error porque es el mismo alumno
    alumno_a_actualizar = {
        "cedula": "30466351",
        "primer_nombre": "Ariana",
        "segundo_nombre": "G",
        "tercer_nombre": None,
        "apellido_paterno": "Mijares",
        "apellido_materno": "G",
        "relacion_con_rep": "Padre",
        "fecha_ingreso_institucion": date(2025, 9, 6),
        "alumno_id": 1
    }
    
    errores = alumno_servicio.validar_campos_primera_info_alumno(**alumno_a_actualizar)
    
    if (errores):
        print("\n".join(errores))
    else:
        print("primera info del alumno validada correctamente")