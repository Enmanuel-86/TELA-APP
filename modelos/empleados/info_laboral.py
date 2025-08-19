from conexiones.conexion import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class InfoLaboral(Base):
    __tablename__ = "tb_info_laboral"
    
    info_lab_id = Column(Integer, primary_key = True, autoincrement = True)
    empleado_id = Column(Integer, ForeignKey("tb_empleados.empleado_id", ondelete = "CASCADE", onupdate = "CASCADE"), unique = True, nullable = False)
    cod_depend_cobra = Column(String(9), nullable = False)
    institucion_labora = Column(String(25), nullable = False)
    
    empleado = relationship("Empleado", back_populates = "info_laboral")