from conexiones.conexion import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Representante(Base):
    __tablename__ = "tb_representantes"
    
    representante_id = Column(Integer, primary_key = True, autoincrement = True)
    cedula = Column(String(10), unique = True, nullable = False)
    nombre = Column(String(15), nullable = False)
    apellido = Column(String(15), nullable = False)
    direccion_residencia = Column(String(100), nullable = False)
    num_telefono = Column(String(15), nullable = False)
    num_telefono_adicional = Column(String(15))
    carga_familiar = Column(Integer, nullable = False)
    estado_civil = Column(String(15), default = "Soltero/a")
    
    alumno = relationship("Alumno", back_populates = "representante", cascade = "save-update, merge")