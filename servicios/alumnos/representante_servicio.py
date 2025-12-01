import re
from string import digits
from typing import Tuple, List, Optional, Dict, Union
from repositorios.repositorio_base import RepositorioBase
from repositorios.alumnos.representante_repositorio import RepresentanteRepositorio


class RepresentanteServicio:
    def __init__(self, repositorio: RepositorioBase):
        self.repositorio = repositorio
    
    def validar_cedula(self, cedula: str) -> List[str]:
        errores = []
        
        if not(cedula):
            errores.append("Cédula del representante: No puede estar vacío.")
        elif (cedula):
            cedula_sin_espacios = cedula.replace(" ", "")
            contiene_numeros = all(caracter in digits for caracter in cedula)
            if (len(cedula_sin_espacios) == 0):
                errores.append("Cédula del representante: No puede estar vacío.")
            
            if not(contiene_numeros):
                errores.append("Cédula del representante: No debe contener letras, espacios o caracteres especiales.")
            
            if (len(cedula) > 10):
                errores.append("Cédula del representante: No puede contener más de 10 caracteres.")
        
        return errores
    
    def validar_nombre(self, nombre: str) -> List[str]:
        errores = []
        
        if not(nombre):
            errores.append("Nombre: No puede estar vacío.")
        elif (nombre):
            nombre_sin_espacios = nombre.replace(" ", "")
            estructura_nombre = re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+$", nombre)
            if (len(nombre_sin_espacios) == 0):
                errores.append("Nombre: No puede estar vacío.")
            
            if not(estructura_nombre):
                errores.append("Nombre: No debe contener números o caracteres especiales.")
            
            if (len(nombre) > 15):
                errores.append("Nombre: No puede contener más de 15 caracteres.")
        
        return errores
    
    def validar_apellido(self, apellido: str) -> List[str]:
        errores = []
        
        if not(apellido):
            errores.append("Apellido: No puede estar vacío.")
        elif (apellido):
            apellido_sin_espacios = apellido.replace(" ", "")
            estructura_apellido = re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+$", apellido)
            if (len(apellido_sin_espacios) == 0):
                errores.append("Apellido: No puede estar vacío.")
            
            if not(estructura_apellido):
                errores.append("Apellido: No debe contener números o caracteres especiales.")
            
            if (len(apellido) > 15):
                errores.append("Apellido: No puede contener más de 15 caracteres.")
        
        return errores
    
    def validar_direccion_residencia(self, direccion_residencia: str) -> List[str]:
        errores = []
        
        if (not(direccion_residencia)):
            errores.append("Dirección de residencia: No puede estar vacío.")
        elif (direccion_residencia):
            direccion_residencia_sin_espacios = direccion_residencia.replace(" ", "")
            if (len(direccion_residencia_sin_espacios) == 0):
                errores.append("Dirección de residencia: No puede estar vacío.")
        
            if (len(direccion_residencia) > 100):
                errores.append("Dirección de residencia: No puede contener más de 100 caracteres.")
        
        return errores
    
    def validar_num_telefono(self, num_telefono: str) -> List[str]:
        errores = []
        
        if not(num_telefono):
            errores.append("Número de teléfono: No puede estar vacío.")
        elif (num_telefono):
            num_telefono_sin_espacios = num_telefono.replace(" ", "")
            contiene_numeros = all(caracter in digits for caracter in num_telefono)
            if (len(num_telefono_sin_espacios) == 0):
                errores.append("Número de teléfono: No puede estar vacío.")
            if not(contiene_numeros):
                errores.append("Número de teléfono: No debe contener letras, espacios o caracteres especiales.")
                
            if (len(num_telefono) > 15):
                errores.append("Número de teléfono: No puede contener más de 15 caracteres.")
        
        return errores
    
    def validar_num_telefono_adicional(self, num_telefono_adicional: str) -> List[str]:
        errores = []
        
        if (num_telefono_adicional):
            num_telefono_adicional_sin_espacios = num_telefono_adicional.replace(" ", "")
            contiene_numeros = all(caracter in digits for caracter in num_telefono_adicional)
            if (len(num_telefono_adicional_sin_espacios) == 0):
                errores.append("Número de teléfono adicional: No puede estar vacío.")
            if not(contiene_numeros):
                errores.append("Número de teléfono adicional: No debe contener letras, espacios o caracteres especiales.")
                
            if (len(num_telefono_adicional) > 15):
                errores.append("Número de teléfono adicional: No puede contener más de 15 caracteres.")
        
        return errores
    
    def validar_carga_familiar(self, carga_familiar: int) -> List[str]:
        errores = []
        
        if not(carga_familiar):
            errores.append("Carga familiar: No puede estar vacío.")
        elif (carga_familiar):
            if (type(carga_familiar) == int):
                if (carga_familiar < 0):
                    errores.append("Carga familiar: No puede ser un valor negativo.")
            else:
                errores.append("Carga familiar: Tiene que ser un valor numérico.")
        
        return errores
    
    def validar_estado_civil(self, estado_civil: str) -> List[str]:
        errores = []
        
        if (estado_civil):
            if (len(estado_civil) > 15):
                errores.append("Estado civil: No puede contener más de 15 caracteres.")
                
        return errores
    
    def validar_campos_representante(
        self, cedula: str,
        nombre: str, apellido: str, 
        direccion_residencia: str, num_telefono: str, 
        num_telefono_adicional: str,
        carga_familiar: int, estado_civil: str
    ) -> List[str]:
        error_cedula = self.validar_cedula(cedula)
        error_nombre = self.validar_nombre(nombre)
        error_apellido = self.validar_apellido(apellido)
        error_direccion_residencia = self.validar_direccion_residencia(direccion_residencia)
        error_num_telefono = self.validar_num_telefono(num_telefono)
        error_num_telefono_adicional = self.validar_num_telefono_adicional(num_telefono_adicional)
        error_carga_familiar = self.validar_carga_familiar(carga_familiar)
        error_estado_civil = self.validar_estado_civil(estado_civil)
        
        errores_totales = error_cedula + error_nombre + error_apellido + error_direccion_residencia + error_num_telefono + error_num_telefono_adicional + error_carga_familiar + error_estado_civil
        
        return errores_totales
    
    def registrar_representante(self, campos: Dict) -> int:
        return self.repositorio.registrar(campos)
    
    def obtener_todos_representantes(self) -> List[Tuple]:
        return self.repositorio.obtener_todos()
    
    def obtener_representante_por_id(self, representante_id: int) -> Optional[Tuple]:
        return self.repositorio.obtener_por_id(representante_id)
    
    def obtener_representante_por_cedula(self, cedula: str) -> Optional[Tuple]:
        return self.repositorio.obtener_por_cedula(cedula)
    
    def obtener_todos_o_por_cedula(self, cedula: str = None) -> Union[List[Tuple], Tuple]:
        return self.repositorio.obtener_todos_o_por_cedula(cedula)
    
    def obtener_alumnos_representados(self, representante_id: int) -> List[Tuple]:
        return self.repositorio.obtener_alumnos_representados(representante_id)
    
    def actualizar_representante(self, representante_id: int, campos_representante: Dict) -> None:
        self.repositorio.actualizar(representante_id, campos_representante)


if __name__ == "__main__":
    representante_repositorio = RepresentanteRepositorio()
    representante_servicio = RepresentanteServicio(representante_repositorio)
    
    """campos_representante = {
        "cedula": "9821456",
        "nombre": "JOSÉ",
        "apellido": "GÓMEZ",
        "direccion_residencia": "BOYACÁ 2",
        "num_telefono": "0412123678",
        "carga_familiar": 4,
        "estado_civil": None
    }
    
    representante_servicio.registrar_representante(campos_representante)"""
    
    """todos_representantes = representante_servicio.obtener_todos_representantes()
    
    for registro in todos_representantes:
        print(registro)"""
    
    #print(representante_servicio.obtener_representante_por_id(2))
    #print(representante_servicio.obtener_representante_por_cedula("9821456"))
    
    """todos_representantes = representante_servicio.obtener_alumnos_representados(2)
    
    for registro in todos_representantes:
        print(registro)"""
    
    """todos_representantes = representante_servicio.obtener_todos_o_por_cedula()
    
    if (type(todos_representantes) == list):
        for registro in todos_representantes:
            print(registro)
    else:
        print(todos_representantes)"""
    
    """campos_representante = {
        "cedula": "9821457",
        "nombre": "JOSÉ",
        "apellido": "GÓMES",
        "direccion_residencia": "BOYACÁ 6",
        "num_telefono": "0412423678",
        "carga_familiar": 5,
        "estado_civil": "CASADO"
    }
    
    representante_servicio.actualizar_representante(3, campos_representante)"""
    
    
    """campos_representante = {
        "cedula": "1231457",
        "nombre": "JOSÉ",
        "apellido": "GÓMES",
        "direccion_residencia": "BOYACÁ 6",
        "num_telefono": "0412423678",
        "num_telefono_adicional": "0412357886",
        "carga_familiar": 5,
        "estado_civil": "CASADO"
    }
    
    errores_totales = representante_servicio.validar_campos_representante(
        campos_representante.get("cedula"),
        campos_representante.get("nombre"),
        campos_representante.get("apellido"),
        campos_representante.get("direccion_residencia"),
        campos_representante.get("num_telefono"),
        campos_representante.get("num_telefono_adicional"),
        campos_representante.get("carga_familiar"),
        campos_representante.get("estado_civil")
    )
    
    if errores_totales:
        print("\n".join(errores_totales))
    else:
        print("Registro del representante exitoso.")"""