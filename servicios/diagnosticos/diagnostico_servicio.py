from typing import Tuple, List, Optional, Dict
from excepciones.base_datos_error import BaseDatosError
from repositorios.repositorio_base import RepositorioBase
from repositorios.diagnosticos.diagnostico_repositorio import DiagnosticoRepositorio
from repositorios.repositorio_base import RepositorioBase


class DiagnosticoServicio:
    def __init__(self, repositorio: RepositorioBase):
        self.repositorio = repositorio
    
    def validar_diagnostico(self, diagnostico: str) -> List[str]:
        errores = []
        
        if not(diagnostico):
            errores.append("Diagnóstico: No puede estar vacío.")
        elif (diagnostico):
            diagnostico_sin_espacios = diagnostico.replace(" ", "")
            if (len(diagnostico_sin_espacios) == 0):
                errores.append("Diagnóstico: No puede estar vacío.")
        
            if (len(diagnostico) > 30):
                errores.append("Diagnóstico: No puede contener más de 30 caracteres.")
        
        return errores
    
    def validar_campos_diagnostico(self, diagnostico: str) -> List[str]:
        error_diagnostico = self.validar_diagnostico(diagnostico)
        errores_totales = error_diagnostico
        
        return errores_totales
    
    def registrar_diagnostico(self, campos: Dict) -> None:
        self.repositorio.registrar(campos)
    
    def obtener_todos_diagnosticos(self) -> List[Tuple]:
        return self.repositorio.obtener_todos()
    
    def obtener_diagnostico_por_id(self, diagnostico_id: int) -> Optional[Tuple]:
        try:
            return self.repositorio.obtener_por_id(diagnostico_id)
        except BaseDatosError as error:
            raise error
    
    def actualizar_diagnostico(self, diagnostico_id: int, campos_diagnostico: Dict) -> None:
        self.repositorio.actualizar(diagnostico_id, campos_diagnostico)
    
    def eliminar_diagnostico(self, diagnostico_id: int) -> None:
        try:
            self.repositorio.eliminar(diagnostico_id)
        except BaseDatosError as error:
            raise error


if __name__ == "__main__":
    diagnostico_repositorio = DiagnosticoRepositorio()
    diagnostico_servicio = DiagnosticoServicio(diagnostico_repositorio)
    
    """campos_diagnostico = {
        "diagnostico": "ESQUIZOFRENIA"
    }
    
    diagnostico_servicio.registrar_diagnostico(campos_diagnostico)"""
    
    """todos_diagnosticos = diagnostico_servicio.obtener_todos_diagnosticos()
    
    for registro in todos_diagnosticos:
        print(registro)"""
    
    
    #print(diagnostico_servicio.obtener_diagnostico_por_id(3))
    
    campos_diagnostico = {
        "diagnostico": "TDAH"
    }
    
    #diagnostico_servicio.actualizar_diagnostico(4, campos_diagnostico)
    
    #diagnostico_servicio.eliminar_diagnostico(1)
    #diagnostico_servicio.eliminar_diagnostico(4)