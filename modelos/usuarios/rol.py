from conexiones.conexion import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Rol(Base):
    __tablename__ = "tb_roles"
    
    rol_id = Column(Integer, primary_key = True, autoincrement = True)
    tipo_rol = Column(String(25), nullable = False)
    
    usuario = relationship("Usuario", back_populates = "rol", cascade="save-update, merge")
    permiso_x_rol = relationship("PermisoXRol", back_populates = "rol", cascade="all, delete-orphan")