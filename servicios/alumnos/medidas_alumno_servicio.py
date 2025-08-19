import re
from typing import Tuple, List, Dict
from repositorios.repositorio_base import RepositorioBase
from repositorios.alumnos.medidas_alumno_repositorio import MedidasAlumnoRepositorio


class MedidasAlumnoServicio:
    def __init__(self, repositorio: RepositorioBase):
        self.repositorio = repositorio
    
    def validar_estatura(self, estatura: float) -> List[str]:
        errores = []
        
        if not(estatura):
            errores.append("Estatura: No puede estar vacío.")
        elif (estatura):
            if (type(estatura) == float or type(estatura) == int):
                if (estatura < 0):
                    errores.append("Estatura: No puede ser un valor negativo.")
            else:
                errores.append("Estatura: Tiene que ser un valor numérico.")
        
        return errores
    
    def validar_peso(self, peso: float) -> List[str]:
        errores = []
        
        if not(peso):
            errores.append("Peso: No puede estar vacío.")
        elif (peso):
            if (type(peso) == float or type(peso) == int):
                if (peso < 0):
                    errores.append("Peso: No puede ser un valor negativo.")
            else:
                errores.append("Peso: Tiene que ser un valor numérico.")
        
        return errores
    
    def validar_talla_camisa(self, talla_camisa: str) -> List[str]:
        errores = []
        
        if not(talla_camisa):
            errores.append("Talla de camisa: No puede estar vacío.")
        elif (talla_camisa):
            talla_camisa_sin_espacios = talla_camisa.replace(" ", "")
            contiene_espacios = re.search(r"\s", talla_camisa)
            if (len(talla_camisa_sin_espacios) == 0):
                errores.append("Talla de camisa: No puede estar vacío.")
        
            if (contiene_espacios):
                errores.append("Talla de camisa: No debe contener espacios.")
            
            if (len(talla_camisa) > 3):
                errores.append("Talla de camisa: No puede contener más de 3 caracteres.")
        
        return errores
    
    def validar_talla_pantalon(self, talla_pantalon: int) -> List[str]:
        errores = []
        
        if (talla_pantalon):
            if (type(talla_pantalon) == int):
                if (talla_pantalon < 0):
                    errores.append("Talla de pantalón: No puede ser un valor negativo.")
            else:
                errores.append("Talla de pantalón: Tiene que ser un valor numérico.")
        
        return errores
    
    def validar_talla_zapatos(self, talla_zapatos: int) -> List[str]:
        errores = []

        if (talla_zapatos):
            if (type(talla_zapatos) == int):
                if (talla_zapatos < 0):
                    errores.append("Talla de zapatos: No puede ser un valor negativo.")
            else:
                errores.append("Talla de zapatos: Tiene que ser un valor numérico.")
        
        return errores
    
    def validar_campos_medidas_alumnos(
        self, estatura: float,
        peso: float, talla_camisa: str,
        talla_pantalon: int, talla_zapatos: int
    ) -> List[str]:
        error_estatura = self.validar_estatura(estatura)
        error_peso = self.validar_peso(peso)
        error_talla_camisa = self.validar_talla_camisa(talla_camisa)
        error_talla_pantalon = self.validar_talla_pantalon(talla_pantalon)
        error_talla_zapatos = self.validar_talla_zapatos(talla_zapatos)
        
        errores_totales = error_estatura + error_peso + error_talla_camisa + error_talla_pantalon + error_talla_zapatos
        
        return errores_totales
    
    def registrar_medidas_alumno(self, campos: Dict) -> None:
        self.repositorio.registrar(campos)
    
    def obtener_todos_medidas_alumnos(self) -> List[Tuple]:
        return self.repositorio.obtener_todos()
    
    def obtener_medidas_alumno_por_id(self, alumno_id: int) -> Tuple:
        return self.repositorio.obtener_por_id(alumno_id)
    
    def actualizar_medidas_alumno(self, alumno_id: int, campo_medidas_alumno: Dict) -> None:
        self.repositorio.actualizar(alumno_id, campo_medidas_alumno)


if __name__ == "__main__":
    medidas_alumnos_repositorio = MedidasAlumnoRepositorio()
    medidas_alumnos_servicio = MedidasAlumnoServicio(medidas_alumnos_repositorio)
    
    """todos_medidas_alumnos = medidas_alumnos_servicio.obtener_todos_medidas_alumnos()
    
    for registro in todos_medidas_alumnos:
        print(registro)"""
    
    #print(medidas_alumnos_servicio.obtener_medidas_alumno_por_id(10))
    
    """campos_medidas_alumno = {
        "estatura": 1.87,
        "peso": 49.5,
        "talla_camisa": "M",
        "talla_pantalon": 30,
        "talla_zapatos": 46
    }
    
    medidas_alumnos_servicio.actualizar_medidas_alumno(10, campos_medidas_alumno)"""
    
    """campos_medidas_alumno = {
        "estatura": 1.87,
        "peso": 49.5,
        "talla_camisa": "M",
        "talla_pantalon": 30,
        "talla_zapatos": 46
    }
    
    errores_totales = medidas_alumnos_servicio.validar_campos_medidas_alumnos(
        campos_medidas_alumno.get("estatura"),
        campos_medidas_alumno.get("peso"),
        campos_medidas_alumno.get("talla_camisa"),
        campos_medidas_alumno.get("talla_pantalon"),
        campos_medidas_alumno.get("talla_zapatos")
    )
    
    if errores_totales:
        print("\n".join(errores_totales))
    else:
        print("Registro de medidas exitosa.")"""