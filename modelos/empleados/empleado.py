from conexiones.conexion import Base
from datetime import date
from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.orm import relationship


class Empleado(Base):
    __tablename__ = "tb_empleados"
    
    empleado_id = Column(Integer, primary_key = True, autoincrement = True)
    cedula = Column(String(10), unique = True, nullable = False)
    primer_nombre = Column(String(15), nullable = False)
    segundo_nombre = Column(String(15))
    apellido_paterno = Column(String(15), nullable = False)
    apellido_materno = Column(String(15))
    fecha_nacimiento = Column(Date, nullable = False)
    sexo = Column(String(1), default = "M")
    tiene_hijos_menores = Column(Boolean, default = 0)
    fecha_ingreso_institucion = Column(Date, default = date.today)
    fecha_ingreso_ministerio = Column(Date, nullable = False)
    talla_camisa = Column(String(3), nullable = False)
    talla_pantalon = Column(Integer, nullable = False)
    talla_zapatos = Column(Integer, nullable = False)
    num_telefono = Column(String(15), default = "No tiene")
    correo_electronico = Column(String(50), unique = True, nullable = False)
    estado_reside = Column(String(20), nullable = False)
    municipio = Column(String(20), nullable = False)
    direccion_residencia = Column(String(100), nullable = False)
    situacion = Column(String(10), default = "Activo")
    
    usuario = relationship("Usuario", back_populates = "empleado", cascade="save-update, merge")
    info_laboral = relationship("InfoLaboral", back_populates = "empleado", cascade="all, delete-orphan")
    info_clinica_empleado = relationship("InfoClinicaEmpleado", back_populates = "empleado", cascade="all, delete-orphan")
    historial_enfermedades = relationship("HistorialEnfermCronicas", back_populates = "empleado", cascade="all, delete-orphan")
    detalle_cargo = relationship("DetalleCargo", back_populates = "empleado", cascade="all, delete-orphan")
    asistencia_empleado = relationship("AsistenciaEmpleado", back_populates = "empleado", cascade="all, delete-orphan")
    reposo_empleado = relationship("ReposoEmpleado", back_populates = "empleado", cascade = "all, delete-orphan")