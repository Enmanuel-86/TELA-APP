from conexiones.conexion import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship


class PermisoXRol(Base):
    __tablename__ = "tb_permisos_x_rol"
    
    perm_x_rol_id = Column(Integer, primary_key = True, autoincrement = True)
    rol_id = Column(Integer, ForeignKey("tb_roles.rol_id", ondelete = "CASCADE", onupdate = "CASCADE"))
    permiso_id = Column(Integer, ForeignKey("tb_permisos.permiso_id", ondelete = "CASCADE", onupdate = "CASCADE"))
    
    rol = relationship("Rol", back_populates = "permiso_x_rol")
    permiso = relationship("Permiso", back_populates = "permiso_x_rol")