from conexiones.conexion import Base
from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship


class AsistenciaAlumno(Base):
    __tablename__ = "tb_asistencia_alumnos"
    
    asist_alumno_id = Column(Integer, primary_key = True, autoincrement = True)
    inscripcion_id = Column(Integer, ForeignKey("tb_inscripciones.inscripcion_id", ondelete = "CASCADE", onupdate = "CASCADE"), nullable = False)
    fecha_asistencia = Column(Date, nullable = False)
    estado_asistencia = Column(Boolean, nullable = True)
    dia_no_laborable = Column(String(100))
    
    inscripcion = relationship("Inscripcion", back_populates = "asistencia_alumno")