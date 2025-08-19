from conexiones.conexion import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class FuncionCargo(Base):
    __tablename__ = "tb_funciones_cargo"
    
    funcion_cargo_id = Column(Integer, primary_key = True, autoincrement = True)
    funcion_cargo = Column(String(45), nullable = False)
    
    detalle_cargo = relationship("DetalleCargo", back_populates = "funcion_cargo", cascade="save-update, merge")