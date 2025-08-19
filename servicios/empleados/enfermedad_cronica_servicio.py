from typing import Tuple, List, Optional, Dict
from excepciones.base_datos_error import BaseDatosError
from repositorios.empleados.enfermedad_cronica_repositorio import EnfermedadCronicaRepositorio
from repositorios.repositorio_base import RepositorioBase


class EnfermedadCronicaServicio:
    def __init__(self, repositorio: RepositorioBase):
        self.repositorio = repositorio
    
    def validar_enfermedad_cronica(self, enfermedad_cronica: str) -> List[str]:
        errores = []
        
        if not(enfermedad_cronica):
            errores.append("Enfermedad crónica: No puede estar vacío.")
        elif (enfermedad_cronica):
            enfermedad_cronica_sin_espacios = enfermedad_cronica.replace(" ", "")
            if (len(enfermedad_cronica_sin_espacios) == 0):
                errores.append("Enfermedad crónica: No puede estar vacío.")
        
            if (len(enfermedad_cronica) > 35):
                errores.append("Enfermedad crónica: No puede contener más de 35 caracteres.")
        
        return errores
    
    def validar_campos_enfermedades_cronicas(self, enfermedad_cronica: str) -> List[str]:
        error_enfermedad_cronica = self.validar_enfermedad_cronica(enfermedad_cronica)
        errores_totales = error_enfermedad_cronica
        
        return errores_totales
    
    def registrar_enfermedad_cronica(self, campos: Dict) -> None:
        self.repositorio.registrar(campos)
    
    def obtener_todos_enfermedades_cronicas(self) -> List[Tuple]:
        return self.repositorio.obtener_todos()
    
    def obtener_enfermedad_cronica_por_id(self, enferm_cronica_id: int) -> Optional[Tuple]:
        try:
            return self.repositorio.obtener_por_id(enferm_cronica_id)
        except BaseDatosError as error:
            raise error
    
    def actualizar_enfermedad_cronica(self, enferm_cronica_id: int, campos_enfermedad_cronica: Dict) -> None:
        self.repositorio.actualizar(enferm_cronica_id, campos_enfermedad_cronica)
    
    def eliminar_enfermedad_cronica(self, enferm_cronica_id: int) -> None:
        try:
            self.repositorio.eliminar(enferm_cronica_id)
        except BaseDatosError as error:
            raise error


if __name__ == "__main__":
    enfermedad_cronica_repositorio = EnfermedadCronicaRepositorio()
    enfermedad_cronica_servicio = EnfermedadCronicaServicio(enfermedad_cronica_repositorio)
    
    """campos_enfermedad_cronica = {
        "enfermedad_cronica": "ASMA"
    }
    
    enfermedad_cronica_servicio.registrar_enfermedad_cronica(campos_enfermedad_cronica)"""
    
    """todos_enfermedades_cronicas = enfermedad_cronica_servicio.obtener_todos_enfermedades_cronicas()
    
    for registro in todos_enfermedades_cronicas:
        print(registro)"""
    
    #print(enfermedad_cronica_servicio.obtener_enfermedad_cronica_por_id(3))
    
    """campos_enfermedad_cronica = {
        "enfermedad_cronica": "DIARREA"
    }
    
    enfermedad_cronica_servicio.actualizar_enfermedad_cronica(3, campos_enfermedad_cronica)"""
    
    #enfermedad_cronica_servicio.eliminar_enfermedad_cronica(1)
    #enfermedad_cronica_servicio.eliminar_enfermedad_cronica(3)