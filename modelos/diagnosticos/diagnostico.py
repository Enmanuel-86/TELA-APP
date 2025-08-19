from conexiones.conexion import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Diagnostico(Base):
    __tablename__ = "tb_diagnosticos"
    
    diagnostico_id = Column(Integer, primary_key = True, autoincrement = True)
    diagnostico = Column(String(30), nullable = False)
    
    info_clinica_alumno = relationship("InfoClinicaAlumno", back_populates = "diagnostico", cascade="save-update, merge")
    info_clinica_empleado = relationship("InfoClinicaEmpleado", back_populates = "diagnostico", cascade="save-update, merge")