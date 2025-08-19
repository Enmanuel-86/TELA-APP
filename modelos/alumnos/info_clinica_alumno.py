from conexiones.conexion import Base
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship


class InfoClinicaAlumno(Base):
    __tablename__ = "tb_info_clinica_alumnos"
    
    info_clin_alumno_id = Column(Integer, primary_key = True, autoincrement = True)
    alumno_id = Column(Integer, ForeignKey("tb_alumnos.alumno_id", ondelete = "CASCADE", onupdate = "CASCADE"), nullable = False)
    diagnostico_id = Column(Integer, ForeignKey("tb_diagnosticos.diagnostico_id", ondelete = "RESTRICT", onupdate = "CASCADE"), nullable = False)
    fecha_diagnostico = Column(Date, nullable = False)
    medico_tratante = Column(String(35), nullable = False)
    certificacion_discap = Column(String(15), nullable = False)
    fecha_vencimiento_certif = Column(Date, nullable = False)
    medicacion = Column(String(30), default = "No tiene")
    observacion_adicional = Column(String(150))
    
    alumno = relationship("Alumno", back_populates = "info_clinica_alumno")
    diagnostico = relationship("Diagnostico", back_populates = "info_clinica_alumno")