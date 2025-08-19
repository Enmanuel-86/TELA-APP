from conexiones.conexion import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class EnfermedadCronica(Base):
    __tablename__ = "tb_enfermedades_cronicas"
    
    enferm_cronica_id = Column(Integer, primary_key = True, autoincrement = True)
    enfermedad_cronica = Column(String(35), nullable = False)
    
    historial_enfermedades = relationship("HistorialEnfermCronicas", back_populates = "enfermedad_cronica", cascade="save-update, merge")