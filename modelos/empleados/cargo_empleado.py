from conexiones.conexion import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class CargoEmpleado(Base):
    __tablename__ = "tb_cargos_empleados"
    
    cargo_id = Column(Integer, primary_key = True, autoincrement = True)
    codigo_cargo = Column(String(15), unique = True, nullable = False)
    cargo = Column(String(35), nullable = False)
    
    detalle_cargo = relationship("DetalleCargo", back_populates = "cargo_empleado", cascade="save-update, merge")