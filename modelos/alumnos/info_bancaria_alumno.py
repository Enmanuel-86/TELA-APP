from conexiones.conexion import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class InfoBancariaAlumno(Base):
    __tablename__ = "tb_info_bancaria_alumnos"
    
    info_banc_alumno_id = Column(Integer, primary_key = True, autoincrement = True)
    alumno_id = Column(Integer, ForeignKey("tb_alumnos.alumno_id", ondelete = "CASCADE", onupdate = "CASCADE"), nullable = False)
    tipo_cuenta = Column(String(40), nullable = False)
    num_cuenta = Column(String(20), nullable = False)
    
    alumno = relationship("Alumno", back_populates = "info_bancaria_alumno")