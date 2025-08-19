from conexiones.conexion import Base
from datetime import date
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship


class Inscripcion(Base):
    __tablename__ = "tb_inscripciones"
    
    inscripcion_id = Column(Integer, primary_key = True, autoincrement = True)
    alumno_id = Column(Integer, ForeignKey("tb_alumnos.alumno_id", ondelete = "CASCADE", onupdate = "CASCADE"), nullable = False)
    num_matricula = Column(String(5), nullable = False)
    especialidad_id = Column(Integer, ForeignKey("tb_especialidades.especialidad_id", ondelete = "RESTRICT", onupdate = "CASCADE"), nullable = False)
    fecha_inscripcion = Column(Date, default = date.today)
    periodo_escolar = Column(String(9), nullable = False)
    
    alumno = relationship("Alumno", back_populates = "inscripcion")
    especialidad = relationship("Especialidad", back_populates = "inscripcion")
    asistencia_alumno = relationship("AsistenciaAlumno", back_populates = "inscripcion", cascade="all, delete-orphan")