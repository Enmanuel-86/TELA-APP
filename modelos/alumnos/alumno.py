from conexiones.conexion import Base
from sqlalchemy import Column, Integer, String, Date, Boolean, LargeBinary, ForeignKey
from sqlalchemy.orm import relationship
from datetime import date


class Alumno(Base):
    __tablename__ = "tb_alumnos"
    
    alumno_id = Column(Integer, primary_key = True, autoincrement = True)
    representante_id = Column(Integer, ForeignKey("tb_representantes.representante_id", ondelete = "RESTRICT", onupdate = "CASCADE"), nullable = False)
    cedula = Column(String(10), unique = True)
    primer_nombre = Column(String(15), nullable = False)
    segundo_nombre = Column(String(15))
    tercer_nombre = Column(String(15))
    apellido_paterno = Column(String(15), nullable = False)
    apellido_materno = Column(String(15))
    fecha_nacimiento = Column(Date, nullable = False)
    lugar_nacimiento = Column(String(50), nullable = False)
    sexo = Column(String(1), default = "M")
    cma = Column(Boolean, default = 1)
    imt = Column(Boolean, default = 1)
    fecha_ingreso_institucion = Column(Date, default = date.today)
    relacion_con_rep = Column(String(15), nullable = False)
    escolaridad = Column(String(20), default = "No posee")
    procedencia = Column(String(35), default = "Foráneo/a")
    situacion = Column(String(10), default = "Ingresado")
    foto_perfil = Column(LargeBinary)
    
    representante = relationship("Representante", back_populates = "alumno")
    medidas_alumno = relationship("MedidasAlumno", back_populates = "alumno", cascade="all, delete-orphan")
    alumno_egresado = relationship("AlumnoEgresado", back_populates = "alumno", cascade="all, delete-orphan")
    info_clinica_alumno = relationship("InfoClinicaAlumno", back_populates = "alumno", cascade="all, delete-orphan")
    info_bancaria_alumno = relationship("InfoBancariaAlumno", back_populates = "alumno", cascade="all, delete-orphan")
    inscripcion = relationship("Inscripcion", back_populates = "alumno", cascade="all, delete-orphan")