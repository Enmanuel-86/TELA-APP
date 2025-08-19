from conexiones.conexion import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Especialidad(Base):
    __tablename__ = "tb_especialidades"
    
    especialidad_id = Column(Integer, primary_key = True, autoincrement = True)
    especialidad = Column(String(40), nullable = False)
    
    detalle_cargo = relationship("DetalleCargo", back_populates = "especialidad", cascade="save-update, merge")
    inscripcion = relationship("Inscripcion", back_populates = "especialidad", cascade="save-update, merge")