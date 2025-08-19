from conexiones.conexion import Base
from datetime import date
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship


class ReposoEmpleado(Base):
    __tablename__ = "tb_reposos_empleados"
    
    reposo_empleado_id = Column(Integer, primary_key = True, autoincrement = True)
    empleado_id = Column(Integer, ForeignKey("tb_empleados.empleado_id", ondelete = "CASCADE", onupdate = "CASCADE"))
    motivo_reposo = Column(String(100), nullable = False)
    fecha_emision = Column(Date, default = date.today)
    fecha_reingreso = Column(Date, nullable = False)
    
    empleado = relationship("Empleado", back_populates = "reposo_empleado")