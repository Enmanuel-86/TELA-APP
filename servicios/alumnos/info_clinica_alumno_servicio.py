import re
from typing import Tuple, List, Dict
from datetime import date
from excepciones.base_datos_error import BaseDatosError
from repositorios.repositorio_base import RepositorioBase
from repositorios.alumnos.info_clinica_alumno_repositorio import InfoClinicaAlumnoRepositorio


class InfoClinicaAlumnoServicio:
    def __init__(self, repositorio: RepositorioBase):
        self.repositorio = repositorio
    
    def validar_diagnostico_id(self, diagnostico_id: int) -> List[str]:
        errores = []
        
        if not(diagnostico_id):
            errores.append("Diagnóstico: No puede estar vacío.")
        
        return errores
    
    def validar_fecha_diagnostico(self, fecha_diagnostico: date) -> List[str]:
        errores = []
        
        if not(fecha_diagnostico):
            errores.append("Fecha del diagnóstico: No puede estar vacío.")
        
        return errores
    
    def validar_medico_tratante(self, medico_tratante: str) -> List[str]:
        errores = []
        
        if not(medico_tratante):
            errores.append("Médico tratante: No puede estar vacío.")
        elif (medico_tratante):
            medico_tratante_sin_espacios = medico_tratante.replace(" ", "")
            estructura_medico_tratante = re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ. ]+$", medico_tratante)
            if (len(medico_tratante_sin_espacios) == 0):
                errores.append("Médico tratante: No puede estar vacío.")
            
            if not(estructura_medico_tratante):
                errores.append("Médico tratante: No debe contener números o caracteres especiales.")
            
            if (len(medico_tratante) > 35):
                errores.append("Médico tratante: No puede contener más de 35 caracteres.")
        
        return errores
    
    def validar_certificacion_discap(self, certificacion_discap: str) -> List[str]:
        errores = []
        
        if not(certificacion_discap):
            errores.append("Certificación de discapacidad: No puede estar vacío.")
        elif (certificacion_discap):
            certificacion_discap_sin_espacios = certificacion_discap.replace(" ", "")
            ya_existe = self.obtener_info_clinica_por_certificacion_discap(certificacion_discap)
            
            if (len(certificacion_discap_sin_espacios) == 0):
                errores.append("Certificación de discapacidad: No puede estar vacío.")
            
            if (ya_existe):
                errores.append("Certificación de discapacidad: Este certificado ya está registrado.")
            
            if (len(certificacion_discap) > 15):
                errores.append("Certificación de discapacidad: No puede contener más de 15 caracteres.")
        
        return errores
    
    def validar_fecha_vencimiento_certif(self, fecha_vencimiento_certif: date) -> List[str]:
        errores = []
        
        if not(fecha_vencimiento_certif):
            errores.append("Fecha de vencimiento del certificado de discapacidad: No puede estar vacío.")
        
        return errores
    
    def validar_medicacion(self, medicacion: str) -> List[str]:
        errores = []
        
        if (medicacion):
            if (len(medicacion) > 30):
                errores.append("Medicación: No puede contener más de 30 caracteres.")
        
        return errores
    
    def validar_observacion_adicional(self, observacion_adicional: str) -> List[str]:
        errores = []
        
        if (observacion_adicional):
            if (len(observacion_adicional) > 150):
                errores.append("Observación Adicional: No puede contener más de 150 caracteres.")
        
        return errores
    
    def valdidar_campos_info_clinica_alumno(
        self, diagnostico_id: int,
        fecha_diagnostico: date, medico_tratante: str,
        certificacion_discap: str, fecha_vencimiento_certif: date,
        medicacion: str, observacion_adicional: str
    ) -> List[str]:
        error_diagnostico_id = self.validar_diagnostico_id(diagnostico_id)
        error_fecha_diagnostico = self.validar_fecha_diagnostico(fecha_diagnostico)
        error_medico_tratante = self.validar_medico_tratante(medico_tratante)
        error_certificacion_discap = self.validar_certificacion_discap(certificacion_discap)
        error_fecha_vencimiento_certif = self.validar_fecha_vencimiento_certif(fecha_vencimiento_certif)
        error_medicacion = self.validar_medicacion(medicacion)
        error_observacion_adicional = self.validar_observacion_adicional(observacion_adicional)
        
        errores_totales = error_diagnostico_id + error_fecha_diagnostico + error_medico_tratante + error_certificacion_discap + error_fecha_vencimiento_certif + error_medicacion + error_observacion_adicional
        
        return errores_totales
    
    def registrar_info_clinica_alumno(self, campos: Dict) -> None:
        self.repositorio.registrar(campos)
    
    def obtener_todos_info_clinica_alumno(self) -> List[Tuple]:
        return self.repositorio.obtener_todos()
    
    def obtener_info_clinica_alumno_por_id(self, info_clin_alumno_id: int) -> Tuple:
        return self.repositorio.obtener_por_id(info_clin_alumno_id)
    
    def obtener_info_clinica_por_alumno_id(self, alumno_id: int) -> List[Tuple]:
        return self.repositorio.obtener_por_alumno_id(alumno_id)
    
    def obtener_info_clinica_por_certificacion_discap(self, certificacion_discap: str) -> int:
        return self.repositorio.obtener_por_certificacion_discap(certificacion_discap)
    
    def actualizar_info_clinica_alumno(self, info_clin_alumno_id: int, campos_info_clinica_alumno: Dict) -> None:
        self.repositorio.actualizar(info_clin_alumno_id, campos_info_clinica_alumno)
    
    def eliminar_info_clinica_alumno(self, info_clin_alumno_id: int) -> None:
        try:
            self.repositorio.eliminar(info_clin_alumno_id)
        except BaseDatosError as error:
            raise error


if __name__ == "__main__":
    info_clinica_alumno_repositorio = InfoClinicaAlumnoRepositorio()
    info_clinica_alumno_servicio = InfoClinicaAlumnoServicio(info_clinica_alumno_repositorio)
    
    """campos_info_clinica_alumno = {
        "alumno_id": 4,
        "diagnostico_id": 1,
        "fecha_diagnostico": date(2006, 5, 13),
        "medico_tratante": "DR. ALEJANDRO",
        "certificacion_discap": "D-234796",
        "fecha_vencimiento_certif": date(2010, 5, 15),
        "medicacion": None,
        "observacion_adicional": None
    }
    
    info_clinica_alumno_servicio.registrar_info_clinica_alumno(campos_info_clinica_alumno)"""
    
    """todos_info_clinica_alumno = info_clinica_alumno_servicio.obtener_todos_info_clinica_alumno()
    
    for registro in todos_info_clinica_alumno:
        print(registro)"""
    
    #print(info_clinica_alumno_servicio.obtener_info_clinica_alumno_por_id(1))
    
    """todos_info_clinica_alumno = info_clinica_alumno_servicio.obtener_info_clinica_por_alumno_id(2)
    
    for registro in todos_info_clinica_alumno:
        print(registro)"""
    
    """campos_info_clinica_alumno = {
        "alumno_id": 4,
        "diagnostico_id": 1,
        "fecha_diagnostico": date(2008, 5, 13),
        "medico_tratante": "DR. ALEJANDRO",
        "certificacion_discap": "D-134796",
        "fecha_vencimiento_certif": date(2012, 5, 15),
        "medicacion": "PARACETAMOL",
        "observacion_adicional": None
    }
    
    info_clinica_alumno_servicio.actualizar_info_clinica_alumno(4, campos_info_clinica_alumno)"""
    
    """try:
        info_clinica_alumno_servicio.eliminar_info_clinica_alumno(4)
    except BaseDatosError as error:
        print(error)"""
    
    """campos_info_clinica_alumno = {
        "diagnostico_id": 1,
        "fecha_diagnostico": date(2008, 5, 13),
        "medico_tratante": "DR. ALEJANDRO",
        "certificacion_discap": "D-134796",
        "fecha_vencimiento_certif": date(2012, 5, 15),
        "medicacion": None,
        "observacion_adicional": None
    }
    
    errores_totales = info_clinica_alumno_servicio.valdidar_campos_info_clinica_alumno(
        campos_info_clinica_alumno.get("diagnostico_id"),
        campos_info_clinica_alumno.get("fecha_diagnostico"),
        campos_info_clinica_alumno.get("medico_tratante"),
        campos_info_clinica_alumno.get("certificacion_discap"),
        campos_info_clinica_alumno.get("fecha_vencimiento_certif"),
        campos_info_clinica_alumno.get("medicacion"),
        campos_info_clinica_alumno.get("observacion_adicional")
    )
    
    if errores_totales:
        print("\n".join(errores_totales))
    else:
        print("Se registró la info clínica de alumno con éxito")"""