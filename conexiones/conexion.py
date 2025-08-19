from conexiones.conexion_base import BaseDatos
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from configuraciones.configuracion import app_configuracion

RUTA_BD = app_configuracion.RUTA_BD

Base = declarative_base()


class SqliteBaseDatos(BaseDatos):
    def __init__(self, BASE_DATOS_URL: str = f"sqlite:///{RUTA_BD}", Base: declarative_base = Base):
        self.BASE_DATOS_URL = BASE_DATOS_URL
        self.motor_bd = None
        self.SessionLocal = None
        self.Base = Base
    
    def conectar(self):
        try:
            self.motor_bd = create_engine(self.BASE_DATOS_URL)
            self.SessionLocal = sessionmaker(self.motor_bd)
            print(f"Se ha conectado a la base de datos: {RUTA_BD}")
            return self.motor_bd
        except Exception as error:
            print(f"Error al conectar: {error}")
            return None
    
    def obtener_sesion_bd(self):
        if not self.motor_bd:
            raise Exception("Primero tienes que hacer la conexion")
        return self.SessionLocal()

    def desconectar(self):
        if self.motor_bd:
            self.motor_bd.dispose()

conexion_bd = SqliteBaseDatos()
conexion_bd.conectar()


if __name__ == "__main__":
    #bd = SqliteBaseDatos()
    
    #bd.conectar()
    pass