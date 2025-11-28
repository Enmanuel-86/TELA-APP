import re
from string import digits
from typing import Tuple, List, Optional, Dict
from excepciones.base_datos_error import BaseDatosError
from datetime import date
from repositorios.empleados.empleado_repositorio import EmpleadoRepositorio
from repositorios.repositorio_base import RepositorioBase


class EmpleadoServicio:
    def __init__(self, repositorio: RepositorioBase):
        self.repositorio = repositorio
    
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
    
    def validar_cedula(self, cedula: str, empleado_id: Optional[int] = None) -> List[str]:
        errores = []
        
        if (not(cedula)):
            errores.append("Cédula: No puede estar vacío.")
        elif (cedula):
            cedula_sin_espacios = cedula.replace(" ", "")
            empleado_a_actualizar_info = None
            contiene_numeros = all(caracter in digits for caracter in cedula)
            if (len(cedula_sin_espacios) == 0):
                errores.append("Cédula: No puede estar vacío.")
        
            if not(contiene_numeros):
                errores.append("Cédula: No debe contener letras, espacios o caracteres especiales.")
            
            if (empleado_id):
                empleado_a_actualizar_info = self.obtener_empleado_por_id(empleado_id)
                
            try:
                empleado_ya_existe = self.repositorio.obtener_por_cedula(cedula)
                    
                if (empleado_ya_existe):
                    if (empleado_id is None):
                        errores.append("Cédula: Esta cédula ya está registrada.")
                    elif (empleado_a_actualizar_info):
                        id_empleado_ya_existente = empleado_ya_existe[0]
                        id_empleado_a_actualizar = empleado_a_actualizar_info[0]
                            
                        if (id_empleado_ya_existente != id_empleado_a_actualizar):
                            errores.append("Cédula: Esta cédula ya está registrada.")
            except BaseDatosError:
                pass
            
            if (len(cedula) > 10):
                errores.append("Cédula: No puede contener más de 10 caracteres.")
        
        return errores
    
    def validar_fecha_nacimiento(self, fecha_nacimiento: date) -> List[str]:
        errores = []
        
        if not(fecha_nacimiento):
            errores.append("Fecha de nacimiento: No puede estar vacío.")
        
        return errores
    
    def validar_talla_camisa(self, talla_camisa: str) -> List[str]:
        errores = []
        
        if (not(talla_camisa)):
            errores.append("Talla de camisa: No puede estar vacío.")
        elif (talla_camisa):
            talla_camisa_sin_espacios = talla_camisa.replace(" ", "")
            contiene_espacios = re.search(r"\s", talla_camisa)
            if (len(talla_camisa_sin_espacios) == 0):
                errores.append("Tlla de camisa: No puede estar vacío.")
        
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
    
    def validar_estado_reside(self, estado_reside: str) -> List[str]:
        errores = []
        
        if (not(estado_reside)):
            errores.append("Estado en el que reside: No puede estar vacío.")
        elif (estado_reside):
            estado_reside_sin_espacios = estado_reside.replace(" ", "")
            estructura_estado_reside = re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+$", estado_reside)
            if (len(estado_reside_sin_espacios) == 0):
                errores.append("Estado en el que reside: No puede estar vacío.")
        
            if not(estructura_estado_reside):
                errores.append("Estado en el que reside: No debe contener números o caracteres especiales.")
            
            if (len(estado_reside) > 20):
                errores.append("Estado en el que reside: No puede contener más de 20 caracteres.")
        
        return errores
    
    def validar_municipio(self, municipio: str) -> List[str]:
        errores = []
        
        if (not(municipio)):
            errores.append("Municipio: No puede estar vacío.")
        elif (municipio):
            municipio_sin_espacios = municipio.replace(" ", "")
            estructura_municipio = re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+$", municipio)
            if (len(municipio_sin_espacios) == 0):
                errores.append("Municipio: No puede estar vacío.")
        
            if not(estructura_municipio):
                errores.append("Municipio: No debe contener números o caracteres especiales.")
            
            if (len(municipio) > 20):
                errores.append("Municipio: No puede contener más de 20 caracteres.")
        
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
    
    def validar_numero_telefono(self, num_telefono: str) -> List[str]:
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
    
    def validar_numero_telefono_adicional(self, num_telefono_adicional: str, num_telefono_principal: str) -> List[str]:
        errores = []
        
        if (num_telefono_adicional):
            num_telefono_adicional_sin_espacios = num_telefono_adicional.replace(" ", "")
            contiene_numeros = all(caracter in digits for caracter in num_telefono_adicional)
            
            if (len(num_telefono_adicional_sin_espacios) == 0):
                errores.append("Número de teléfono adicional: No puede estar vacío.")
                
            if not(contiene_numeros):
                errores.append("Número de teléfono adicional: No debe contener letras, espacios o caracteres especiales.")
            
            if (num_telefono_principal):
                if (num_telefono_principal == num_telefono_adicional):
                    errores.append("Número de teléfono adicional: El teléfono secundario no puede ser igual que el principal.")
                
            if (len(num_telefono_adicional) > 15):
                errores.append("Número de teléfono adicional: No puede contener más de 15 caracteres.")
        
        return errores
    
    def validar_correo_electronico(self, correo_electronico: str, empleado_id: Optional[int]) -> List[str]:
        errores = []
        
        if (not(correo_electronico)):
            errores.append("Correo electrónico: No puede estar vacío.")
        elif (correo_electronico):
            correo_electronico_sin_espacios = correo_electronico.replace(" ", "")
            empleado_a_actualizar_info = None
            estructura_correo_electronico = re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]{2,}$", correo_electronico)
            
            if (len(correo_electronico_sin_espacios) == 0):
                errores.append("Correo electrónico: No puede estar vacío.")
            
            if not(estructura_correo_electronico):
                errores.append("Correo electrónico: La estructura del correo electrónico es inválida.")
            
            if (empleado_id):
                empleado_a_actualizar_info = self.obtener_empleado_por_id(empleado_id)
            
            try:
                empleado_ya_existe_correo_principal = self.repositorio.obtener_por_correo(correo_electronico)
                
                if (empleado_ya_existe_correo_principal):
                    if (empleado_id is None):
                        errores.append("Correo electrónico: Este correo electrónico ya está registrado.")
                    elif (empleado_a_actualizar_info):
                        id_empleado_existente_correo_principal = empleado_ya_existe_correo_principal[0]
                        id_empleado_a_actualizar = empleado_a_actualizar_info[0]
                        
                        if (id_empleado_existente_correo_principal != id_empleado_a_actualizar):
                            errores.append("Correo electrónico: Este correo electrónico ya está registrado.")
            except Exception:
                pass
            
            if (len(correo_electronico) > 50):
                errores.append("Correo electrónico: No puede contener más de 50 caracteres.")
        
        return errores
    
    def validar_correo_electronico_adicional(self, correo_electronico_adicional: str, correo_principal: str, empleado_id: Optional[int] = None) -> List[str]:
        errores = []
        
        if (correo_electronico_adicional):
            correo_electronico_adicional_sin_espacios = correo_electronico_adicional.replace(" ", "")
            empleado_a_actualizar_info = None
            estructura_correo_electronico = re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]{2,}$", correo_electronico_adicional)
            
            if (len(correo_electronico_adicional_sin_espacios) == 0):
                errores.append("Correo electrónico adicional: No puede estar vacío.")
        
            if not(estructura_correo_electronico):
                errores.append("Correo electrónico adicional: La estructura del correo electrónico es inválida.")
            
            if (empleado_id):
                empleado_a_actualizar_info = self.obtener_empleado_por_id(empleado_id)
            
            if (correo_principal):
                if (correo_principal == correo_electronico_adicional):
                    errores.append("Correo electrónico adicional: Tu correo secundario no puede ser igual que el principal.")
            
            try:
                empleado_ya_existe_correo_adicional = self.repositorio.obtener_por_correo_adicional(correo_electronico_adicional)
                
                if (empleado_ya_existe_correo_adicional):
                    if (empleado_id is None):
                        errores.append("Correo electrónico adicional: Este correo electrónico ya está registrado.")
                    elif (empleado_a_actualizar_info):
                        id_empleado_existente_correo_adicional = empleado_ya_existe_correo_adicional[0]
                        id_empleado_a_actualizar = empleado_a_actualizar_info[0]
                        
                        if (id_empleado_existente_correo_adicional != id_empleado_a_actualizar):
                            errores.append("Correo electrónico adicional: Este correo electrónico ya está registrado.")
            except Exception:
                pass
            
            if (len(correo_electronico_adicional) > 50):
                errores.append("Correo electrónico adicional: No puede contener más de 50 caracteres.")
        
        return errores
    
    def validar_info_basica_empleado(
        self, primer_nombre: str,
        segundo_nombre: str, tercer_nombre: str, apellido_paterno: str,
        apellido_materno: str, cedula: str, 
        fecha_nacimiento: date, empleado_id: Optional[int] = None
    ) -> List[str]:
        error_primer_nombre = self.validar_primer_nombre(primer_nombre)
        error_segundo_nombre = self.validar_segundo_nombre(segundo_nombre)
        error_tercer_nombre = self.validar_tercer_nombre(tercer_nombre)
        error_apellido_paterno = self.validar_apellido_paterno(apellido_paterno)
        error_apellido_materno = self.validar_apellido_materno(apellido_materno)
        error_cedula = self.validar_cedula(cedula, empleado_id)
        error_fecha_nacimiento = self.validar_fecha_nacimiento(fecha_nacimiento)
        
        errores_totales = error_primer_nombre + error_segundo_nombre + error_tercer_nombre + error_apellido_paterno + error_apellido_materno + error_cedula + error_fecha_nacimiento
        
        return errores_totales
    
    def validar_medidas_empleado(self, talla_camisa: str, talla_pantalon: int, talla_zapatos: int) -> List[str]:
        error_talla_camisa = self.validar_talla_camisa(talla_camisa)
        error_talla_pantalon = self.validar_talla_pantalon(talla_pantalon)
        error_talla_zapatos = self.validar_talla_zapatos(talla_zapatos)
        
        errores_totales = error_talla_camisa + error_talla_pantalon + error_talla_zapatos
        
        return errores_totales
    
    def validar_info_geografica_empleado(self, estado_reside: str, municipio: str, direccion_residencia: str) -> List[str]:
        error_estado_reside = self.validar_estado_reside(estado_reside)
        error_municipio = self.validar_municipio(municipio)
        error_direccion_residencia = self.validar_direccion_residencia(direccion_residencia)
        
        errores_totales = error_estado_reside + error_municipio + error_direccion_residencia
        
        return errores_totales
    
    def validar_info_contacto_empleado(self, num_telefono: str, num_telefono_adicional: str, correo_electronico: str, correo_electronico_adicional: str, empleado_id: Optional[int] = None) -> List[str]:
        error_num_telefono = self.validar_numero_telefono(num_telefono)
        error_num_telefono_adicional = self.validar_numero_telefono_adicional(num_telefono_adicional, num_telefono)
        
        error_correo_electronico = self.validar_correo_electronico(correo_electronico, empleado_id)
        error_correo_electronico_adicional = self.validar_correo_electronico_adicional(correo_electronico_adicional, correo_electronico, empleado_id)
        
        errores_totales = error_num_telefono + error_num_telefono_adicional + error_correo_electronico + error_correo_electronico_adicional
        
        return errores_totales
    
    def registrar_empleado(self, campos: Dict) -> int:
        return self.repositorio.registrar(campos)
    
    def obtener_todos_empleados(self) -> List[Tuple]:
        return self.repositorio.obtener_todos()
    
    def obtener_empleado_por_id(self, empleado_id: int) -> Optional[Tuple]:
        try:
            return self.repositorio.obtener_por_id(empleado_id)
        except BaseDatosError as error:
            raise error
    
    def obtener_info_contacto_empleado(self, empleado_id: int) -> Tuple:
        return self.repositorio.obtener_info_contacto(empleado_id)
    
    def obtener_info_geografica_empleado(self, empleado_id: int) -> Tuple:
        return self.repositorio.obtener_info_geografica(empleado_id)
    
    def obtener_medidas_empleado(self, empleado_id: int) -> Tuple:
        return self.repositorio.obtener_medidas(empleado_id)
    
    def actualizar_empleado(self, empleado_id: int, campos_empleado: Dict) -> None:
        self.repositorio.actualizar(empleado_id, campos_empleado)
    
    def eliminar_empleado(self, empleado_id: int) -> None:
        try:
            self.repositorio.eliminar(empleado_id)
        except BaseDatosError as error:
            raise error


if __name__ == "__main__":
    empleado_repositorio = EmpleadoRepositorio()
    empleado_servicio = EmpleadoServicio(empleado_repositorio)
    
    """campos_empleado = {
        "cedula": "30932925",
        "primer_nombre": "GABRIEL",
        "segundo_nombre": None,
        "apellido_paterno": "CHACÓN",
        "apellido_materno": None,
        "fecha_nacimiento": date(2004, 10, 11),
        "sexo": None,
        "tiene_hijos_menores": None,
        "fecha_ingreso_institucion": None,
        "fecha_ingreso_ministerio": date(2025, 1, 10),
        "talla_camisa": "S",
        "talla_pantalon": 30,
        "talla_zapatos": 45,
        "num_telefono": None,
        "correo_electronico": "alonsochacon@gmail.com",
        "estado_reside": "ANZOÁTEGUI",
        "municipio": "SIMÓN BOLÍVAR",
        "direccion_residencia": "BOYACA 2",
        "situacion": None
    }
    
    empleado_servicio.registrar_empleado(campos_empleado)"""
    
    """todos_empleados = empleado_servicio.obtener_todos_empleados()
    
    for registro in todos_empleados:
        print(registro)"""
    
    #print(empleado_servicio.obtener_empleado_por_id(3))
    
    #print(empleado_servicio.obtener_info_contacto_empleado(3))
    #print(empleado_servicio.obtener_info_geografica_empleado(3))
    #print(empleado_servicio.obtener_medidas_empleado(3))
    
    """campos_empleado = {
        "cedula": "30932925",
        "primer_nombre": "GABRIEL",
        "segundo_nombre": "ALONSO",
        "apellido_paterno": "CHACÓN",
        "apellido_materno": "CONTRERAS",
        "fecha_nacimiento": date(2004, 10, 11),
        "sexo": "M",
        "tiene_hijos_menores": 0,
        "fecha_ingreso_institucion": date.today(),
        "fecha_ingreso_ministerio": date(2025, 1, 10),
        "talla_camisa": "S",
        "talla_pantalon": 30,
        "talla_zapatos": 45,
        "num_telefono": "04124372808",
        "num_telefono_adicional": "0412567832",
        "correo_electronico": "alonsochacon@gmail.com",
        "correo_electronico_adicional": "otrocorreo@gmail.com", 
        "estado_reside": "ANZOÁTEGUI",
        "municipio": "SIMÓN BOLÍVAR",
        "direccion_residencia": "BOYACA 2",
        "situacion": "Activo"
    }
    
    empleado_servicio.actualizar_empleado(5, campos_empleado)"""
    
    #empleado_servicio.eliminar_empleado(1)
    #empleado_servicio.eliminar_empleado(40)
    #empleado_servicio.eliminar_empleado(11)
    
    """primer_nombre = input("- Ingrese el primer nombre: ")
    segundo_nombre = input("- Ingrese el segundo nombre: ")
    apellido_paterno = input("- Ingrese el apellido paterno: ")
    apellido_materno = input("- Ingrese el apellido materno: ")
    cedula = input("- Ingrese su cédula: ")
    dia_nacimiento = int(input("- Ingrese el día de nacimiento: "))
    mes_nacimiento = int(input("- Ingrese el mes de nacimiento: "))
    anio_nacimiento = int(input("- Ingrese el año de nacimiento: "))
    fecha_nacimiento = date(anio_nacimiento, mes_nacimiento, dia_nacimiento)
    sexo = input("- Ingrese su sexo: ")
    tiene_hijos_menores = int(input("- Tiene hijos menores de edad (1 para si, 0 para no): "))
    
    errores_totales = empleado_servicio.validar_info_basica_empleado(
        primer_nombre, segundo_nombre,
        apellido_materno, apellido_materno,
        cedula, fecha_nacimiento
    )
    
    if (errores_totales):
        print("\n".join(errores_totales))
    else:
        print("Registro del empleado existoso")"""
    
    
    """talla_camisa = input("- Ingrese la talla de camisa: ")
    talla_pantalon = int(input("- Ingrese la talla de pantalón: "))
    talla_zapatos = int(input("- Ingrese la tala de zapatos: "))
    
    errores_totales = empleado_servicio.validar_medidas_empleado(talla_camisa, talla_pantalon, talla_zapatos)
    
    if (errores_totales):
        print("\n".join(errores_totales))
    else:
        print("Registro de las medidas del empleado exitoso")"""
    
    """estado_reside = input("- Ingrese el estado en el que reside: ")
    municipio = input("- Ingrese el municipio: ")
    direccion_residencia = input("- Ingrese su dirección de residencia: ")
    
    errores_totales = empleado_servicio.validar_info_geografica_empleado(estado_reside, municipio, direccion_residencia)
    
    if (errores_totales):
        print("\n".join(errores_totales))
    else:
        print("Registro de la info geográfica exitosa")"""
    
    
    """num_telefono = "0412456875"
    num_telefono_adicional = "0431345678"
    
    correo_electronico = "uncorreoejemplo@gmail.com"
    correo_electronico_adicional  ="otrocorreoejemplo@gmail.com"
    
    errores_totales = empleado_servicio.validar_info_contacto_empleado(num_telefono, num_telefono_adicional, correo_electronico, correo_electronico_adicional)
    
    if (errores_totales):
        print("\n".join(errores_totales))
    else:
        print("Registro de la info de contacto exitosa")"""
    
    
    """empleado_a_actualizar = {
        "id": 1,
        "cedula": "17536256"
    }
    
    id_empleado_a_actualizar = empleado_a_actualizar.get("id")
    nueva_cedula = "17536256"
    
    errores = empleado_servicio.validar_cedula(nueva_cedula, id_empleado_a_actualizar)
    
    if (errores):
        print("\n".join(errores))
    else:
        print("Eres el mismo empleado, todo bien")"""
    
    """empleado_a_actualizar = {
        "id": 1,
        "correo_principal": "lazarinadedios@hotmail.com"
    }
    
    id_empleado_a_actualizar = empleado_a_actualizar.get("id")
    nuevo_correo_principal = "lazarinadedios@hotmail.com"
    
    errores = empleado_servicio.validar_correo_electronico(nuevo_correo_principal, id_empleado_a_actualizar)
    
    if (errores):
        print("\n".join(errores))
    else:
        print("Eres el mismo empleado, todo bien con el correo")"""
    
    
    
    
    """empleado_a_actualizar = {
        "id": 1,
        "correo_principal": "lazarinadedios@hotmail.com",
        "correo_adicional": "lazarinadedios@hotmail.com"
    }
    
    correo_principal_empleadao = empleado_a_actualizar.get("correo_principal")
    correo_secundario_empleado = empleado_a_actualizar.get("correo_adicional")
    id_empleado_a_actualizar = empleado_a_actualizar.get("id")
    
    errores = empleado_servicio.validar_correo_electronico(
        correo_principal_empleadao,
        correo_secundario_empleado,
        id_empleado_a_actualizar
    )
    
    errores = empleado_servicio.validar_correo_electronico_adicional(
        correo_secundario_empleado,
        correo_principal_empleadao,
        id_empleado_a_actualizar
    )
    
    if (errores):
        print("\n".join(errores))
    else:
        print("Todo bien.")"""
    
    
    
    """empleado_a_actualizar = {
        "id": 1,
        "num_principal": "04160839587",
        "num_secundario": "04160839587"
    }
    
    num_principal_empleado = empleado_a_actualizar.get("num_principal")
    num_secundario_empleado = empleado_a_actualizar.get("num_secundario")
    id_empleado_a_actualizar = empleado_a_actualizar.get("id")
    
    errores = empleado_servicio.validar_numero_telefono(
        num_principal_empleado,
        num_secundario_empleado,
        id_empleado_a_actualizar
    )
    
    errores = empleado_servicio.validar_numero_telefono_adicional(
        num_secundario_empleado,
        num_principal_empleado,
        id_empleado_a_actualizar
    )
    
    if (errores):
        print("\n".join(errores))
    else:
        print("todo bien")"""