from conexiones.conexion import Base
from sqlalchemy import Column, Integer, String, Time
from sqlalchemy.orm import relationship


class TipoCargo(Base):
    __tablename__ = "tb_tipos_cargo"
    
    tipo_cargo_id = Column(Integer, primary_key = True, autoincrement = True)
    tipo_cargo = Column(String(25), nullable = False)
    horario_llegada = Column(Time, nullable = False)
    
    detalle_cargo = relationship("DetalleCargo", back_populates = "tipo_cargo", cascade="save-update, merge")