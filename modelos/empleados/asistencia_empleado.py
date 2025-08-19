from conexiones.conexion import Base
from datetime import date
from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey
from sqlalchemy.orm import relationship


class AsistenciaEmpleado(Base):
    __tablename__ = "tb_asistencia_empleados"
    
    asist_empleado_id = Column(Integer, primary_key = True, autoincrement = True)
    empleado_id = Column(Integer, ForeignKey("tb_empleados.empleado_id", ondelete = "CASCADE", onupdate = "CASCADE"), nullable = False)
    fecha_asistencia = Column(Date, default = date.today)
    hora_entrada = Column(Time)
    hora_salida = Column(Time)
    estado_asistencia = Column(String(15), nullable = False)
    motivo_retraso = Column(String(100))
    motivo_inasistencia = Column(String(100))
    
    empleado = relationship("Empleado", back_populates = "asistencia_empleado")