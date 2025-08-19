from typing import Tuple, List, Optional, Dict
from string import digits
from excepciones.base_datos_error import BaseDatosError
from repositorios.repositorio_base import RepositorioBase
from repositorios.alumnos.info_bancaria_alumno_repositorio import InfoBancarioAlumnoRepositorio


class InfoBancariaAlumnoServicio:
    def __init__(self, repositorio: RepositorioBase):
        self.repositorio = repositorio
    
    def validar_tipo_cuenta(self, tipo_cuenta: str) -> List[str]:
        errores = []
        
        if not(tipo_cuenta):
            errores.append("Tipo de cuenta: No puede estar vacío.")
        elif (tipo_cuenta):
            tipo_cuenta_sin_espacios = tipo_cuenta.replace(" ", "")
            if (len(tipo_cuenta_sin_espacios) == 0):
                errores.append("Tipo de cuenta: No puede estar vacío.")
            
            if (len(tipo_cuenta) > 40):
                errores.append("Tipo de cuenta: No puede contener más de 40 caracteres.")
        
        return errores
    
    def validar_num_cuenta(self, num_cuenta: str) -> List[str]:
        errores = []
        
        if not(num_cuenta):
            errores.append("Número de cuenta: No puede estar vacío.")
        elif (num_cuenta):
            contiene_numeros = all(caracter in digits for caracter in num_cuenta)
            ya_existe_num_cuenta = self.obtener_info_bancaria_por_num_cuenta(num_cuenta)
            if not(contiene_numeros):
                errores.append("Número de cuenta: No debe contener letras, espacios o caracteres especiales.")
            
            if (ya_existe_num_cuenta):
                errores.append("Número de cuenta: Este número de cuenta ya está registrado.")
            
            if (len(num_cuenta) > 20):
                errores.append("Número de cuenta: No puede contener más de 20 caracteres.")
        
        return errores
    
    def validar_campos_info_bancaria_alumno(self, tipo_cuenta: str, num_cuenta: str) -> List[str]:
        error_tipo_cuenta = self.validar_tipo_cuenta(tipo_cuenta)
        error_num_cuenta = self.validar_num_cuenta(num_cuenta)
        
        errores_totales = error_tipo_cuenta + error_num_cuenta
        return errores_totales
    
    def registrar_info_bancaria_alumno(self, campos: Dict) -> None:
        self.repositorio.registrar(campos)
    
    def obtener_todos_info_bancaria(self) -> List[Tuple]:
        return self.repositorio.obtener_todos()
    
    def obtener_info_bancaria_por_id(self, info_banc_alumno_id: int) -> Optional[Tuple]:
        try:
            return self.repositorio.obtener_por_id(info_banc_alumno_id)
        except BaseDatosError as error:
            raise error
    
    def obtener_info_bancaria_por_alumno_id(self, alumno_id: int) -> List[Tuple]:
        try:
            return self.repositorio.obtener_por_alumno_id(alumno_id)
        except BaseDatosError as error:
            raise error
    
    def obtener_info_bancaria_por_num_cuenta(self, num_cuenta: str) -> Optional[Tuple]:
        return self.repositorio.obtener_por_num_cuenta(num_cuenta)
    
    def actualizar_info_bancaria(self, info_banc_alumno_id: int, campos_info_bancaria_alumno: Dict) -> None:
        self.repositorio.actualizar(info_banc_alumno_id, campos_info_bancaria_alumno)
    
    def eliminar_info_bancaria(self, info_banc_alumno_id: int) -> None:
        try:
            self.repositorio.eliminar(info_banc_alumno_id)
        except BaseDatosError as error:
            raise error


if __name__ == "__main__":
    info_bancaria_alumno_repositorio = InfoBancarioAlumnoRepositorio()
    info_bancaria_alumno_servicio = InfoBancariaAlumnoServicio(info_bancaria_alumno_repositorio)
    
    """todos_info_bancaria = info_bancaria_alumno_servicio.obtener_todos_info_bancaria()
    
    for registro in todos_info_bancaria:
        print(registro)"""
    
    """try:
        print(info_bancaria_alumno_servicio.obtener_info_bancaria_por_id(2))
    except BaseDatosError as error:
        print(error)"""
    
    """try:
        todos_info_bancaria = info_bancaria_alumno_servicio.obtener_info_bancaria_por_alumno_id(1)
        for registro in todos_info_bancaria:
            print(registro)
    except BaseDatosError as error:
        print(error)"""
    
    """campos_info_bancaria_alumno = {
        "tipo_cuenta": "CORRIENTE",
        "num_cuenta": "010203045067"
    }
    
    info_bancaria_alumno_servicio.actualizar_info_bancaria(1, campos_info_bancaria_alumno)"""
    
    """campos_info_bancaria_alumno = {
        "alumno_id": 5,
        "tipo_cuenta": "CORRIENTE",
        "num_cuenta": "010256045067"
    }
    
    info_bancaria_alumno_servicio.registrar_info_bancaria_alumno(campos_info_bancaria_alumno)"""
    
    """try:
        info_bancaria_alumno_servicio.eliminar_info_bancaria(1)
    except BaseDatosError as error:
        print(error)"""
    
    """campos_info_bancaria_alumno = {
        "alumno_id": 5,
        "tipo_cuenta": "CORRIENTE",
        "num_cuenta": "010256045067"
    }
    
    errores_totales = info_bancaria_alumno_servicio.validar_campos_info_bancaria_alumno(
        campos_info_bancaria_alumno.get("tipo_cuenta"),
        campos_info_bancaria_alumno.get("num_cuenta")
    )
    
    if errores_totales:
        print("\n".join(errores_totales))
    else:
        print("Registro de info bancaria alumno exitosa")"""