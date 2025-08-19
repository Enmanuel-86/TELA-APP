from conexiones.conexion import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Usuario(Base):
    __tablename__ = "tb_usuarios"
    
    usuario_id = Column(Integer, primary_key = True, autoincrement = True)
    empleado_id = Column(Integer, ForeignKey("tb_empleados.empleado_id", ondelete = "RESTRICT", onupdate = "CASCADE"), nullable = True)
    rol_id = Column(Integer, ForeignKey("tb_roles.rol_id", ondelete = "RESTRICT", onupdate = "CASCADE"), nullable = False)
    nombre_usuario = Column(String(10), unique = True, nullable = False)
    clave_usuario = Column(String(12), nullable = False)
    
    empleado = relationship("Empleado", back_populates = "usuario")
    rol = relationship("Rol", back_populates = "usuario")
    auditoria = relationship("Auditoria", back_populates = "usuario", cascade="all, delete-orphan")