from typing import Tuple, List, Optional, Dict
from string import digits
from repositorios.empleados.info_laboral_repositorio import InfoLaboralRepositorio
from repositorios.repositorio_base import RepositorioBase


class InfoLaboralServicio:
    def __init__(self, repositorio: RepositorioBase):
        self.repositorio = repositorio
    
    def validar_cod_depend_cobra(self, cod_depend_cobra: str) -> List[str]:
        errores = []
        
        if not(cod_depend_cobra):
            errores.append("Código de dependencia por donde cobra: No puede estar vacío.")
        elif (cod_depend_cobra):
            cod_depend_cobra_sin_espacios = cod_depend_cobra.replace(" ", "")
            contiene_numeros = all(caracter in digits for caracter in cod_depend_cobra)
            if (len(cod_depend_cobra_sin_espacios) == 0):
                errores.append("Código de dependencia por donde cobra: No puede estar vacío.")
        
            if not(contiene_numeros):
                errores.append("Código de dependencia por donde cobra: No puede contener letras, espacios o caracteres especiales.")
            
            if (len(cod_depend_cobra) > 9):
                errores.append("Código de dependencia por donde cobra: No puede contener más de 9 caracteres.")
        
        return errores
    
    def validar_institucion_labora(self, institucion_labora: str) -> List[str]:
        errores = []
        
        if not(institucion_labora):
            errores.append("Institución por donde labora: No puede estar vacío.")
        elif (institucion_labora):
            institucion_labora_sin_espacios = institucion_labora.replace(" ", "")
            if (len(institucion_labora_sin_espacios) == 0):
                errores.append("Institución por donde labora: No puede estar vacío.")
        
            if (len(institucion_labora) > 25):
                errores.append("Institución por donde labora: No puede contener más de 25 caracteres.")
        
        return errores
    
    def validar_campos_info_laboral(self, cod_depend_cobra: str, institucion_labora: str) -> List[str]:
        error_cod_depend_cobra = self.validar_cod_depend_cobra(cod_depend_cobra)
        error_institucion_labora = self.validar_institucion_labora(institucion_labora)
        
        errores_totales = error_cod_depend_cobra + error_institucion_labora
        
        return errores_totales
    
    def registrar_info_laboral(self, campos: Dict) -> None:
        self.repositorio.registrar(campos)
    
    def obtener_todos_info_laboral(self) -> List[Tuple]:
        return self.repositorio.obtener_todos()
    
    def obtener_info_laboral_por_id(self, info_lab_id: int) -> Optional[Tuple]:
        return self.repositorio.obtener_por_id(info_lab_id)
    
    def obtener_info_laboral_por_empleado_id(self, empleado_id: int) -> Optional[Tuple]:
        return self.repositorio.obtener_por_empleado_id(empleado_id)
    
    def actualizar_info_laboral(self, empleado_id: int, campos_info_laboral: Dict) -> None:
        self.repositorio.actualizar(empleado_id, campos_info_laboral)


if __name__ == "__main__":
    info_laboral_repositorio = InfoLaboralRepositorio()
    info_laboral_servicio = InfoLaboralServicio(info_laboral_repositorio)
    
    """campos_info_laboral = {
        "empleado_id": 4,
        "cod_depend_cobra": "006505199",
        "institucion_labora": "TEV TRONCONAL I"
    }
    
    info_laboral_servicio.registrar_info_laboral(campos_info_laboral)"""
    
    """todos_info_laboral = info_laboral_servicio.obtener_todos_info_laboral()
    
    for registro in todos_info_laboral:
        print(registro)"""
    
    
    #print(info_laboral_servicio.obtener_info_laboral_por_id(4))
    #print(info_laboral_servicio.obtener_info_laboral_por_empleado_id(3))
    
    """campos_info_laboral = {
        "cod_depend_cobra": "006705188",
        "institucion_labora": "TEV TRONCONAL IV"
    }
    
    info_laboral_servicio.actualizar_info_laboral(4, campos_info_laboral)"""
    
    cod_depend_cobra = input("- Ingrese el código de dependencia por donde cobra: ")
    institucion_labora = input("- Ingrese la institución por donde labora: ")
    
    errores_totales = info_laboral_servicio.validar_campos_info_laboral(cod_depend_cobra, institucion_labora)
    
    if errores_totales:
        print("\n".join(errores_totales))
    else:
        print("Registro de la info laboral exitoso.")