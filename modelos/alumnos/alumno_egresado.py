from conexiones.conexion import Base
from datetime import date
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship


class AlumnoEgresado(Base):
    __tablename__ = "tb_alumnos_egresados"
    
    alumno_egresado_id = Column(Integer, primary_key = True, autoincrement = True)
    alumno_id = Column(Integer, ForeignKey("tb_alumnos.alumno_id", ondelete = "CASCADE", onupdate = "CASCADE"), nullable = False)
    fecha_emision = Column(Date, default = date.today)
    razon_egreso = Column(String(50), nullable = False)
    
    alumno = relationship("Alumno", back_populates = "alumno_egresado")