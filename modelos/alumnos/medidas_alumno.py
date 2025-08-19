from conexiones.conexion import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship


class MedidasAlumno(Base):
    __tablename__ = "tb_medidas_alumnos"
    
    medid_alumno_id = Column(Integer, primary_key = True, autoincrement = True)
    alumno_id = Column(Integer, ForeignKey("tb_alumnos.alumno_id", ondelete = "CASCADE", onupdate = "CASCADE"), nullable = False)
    estatura = Column(Float, nullable = False)
    peso = Column(Float, nullable = False)
    talla_camisa = Column(String(3), nullable = False)
    talla_pantalon = Column(Integer, nullable = False)
    talla_zapatos = Column(Integer, nullable = False)
    
    alumno = relationship("Alumno", back_populates = "medidas_alumno")