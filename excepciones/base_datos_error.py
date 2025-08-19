class BaseDatosError(Exception):
    def __init__(self, codigo_error, mensaje):
        super().__init__(mensaje)
        self.codigo_error = codigo_error

if __name__ == "__main__":
    numero_1 = 1
    numero_2 = 0
    
    try:
        if numero_1 == 0 or numero_2 == 0:
            raise BaseDatosError("DIVISION_POR_CERO", "ERROR AL QUERER DIVIDIR POR CERO")
        print(numero_1 / numero_2)
    except BaseDatosError as error:
        if error.codigo_error == "DIVISION_POR_CERO":
            print(f"CÓDIGO ERROR: {error.codigo_error}. MENSAJE: {error}")
    except Exception as error:
        print(f"ERROR INESPERADO: {error}")