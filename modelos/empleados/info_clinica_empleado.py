from conexiones.conexion import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship


class InfoClinicaEmpleado(Base):
    __tablename__ = "tb_info_clinica_empleados"
    
    info_clin_empleado_id = Column(Integer, primary_key = True, autoincrement = True)
    empleado_id = Column(Integer, ForeignKey("tb_empleados.empleado_id", ondelete = "CASCADE", onupdate = "CASCADE"))
    diagnostico_id = Column(Integer, ForeignKey("tb_diagnosticos.diagnostico_id", ondelete = "RESTRICT", onupdate = "CASCADE"), nullable = False)
    
    empleado = relationship("Empleado", back_populates = "info_clinica_empleado")
    diagnostico = relationship("Diagnostico", back_populates = "info_clinica_empleado")