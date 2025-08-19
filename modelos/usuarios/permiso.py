from conexiones.conexion import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Permiso(Base):
    __tablename__ = "tb_permisos"
    
    permiso_id = Column(Integer, primary_key = True, autoincrement = True)
    tipo_permiso = Column(String(70), nullable = False)
    
    permiso_x_rol = relationship("PermisoXRol", back_populates = "permiso", cascade="all, delete-orphan")