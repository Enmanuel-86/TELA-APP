from conexiones.conexion import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class Auditoria(Base):
    __tablename__ = "tb_auditorias"
    
    auditoria_id = Column(Integer, primary_key = True, autoincrement = True)
    usuario_id = Column(Integer, ForeignKey("tb_usuarios.usuario_id", ondelete = "CASCADE", onupdate = "CASCADE"))
    entidad_afectada = Column(String(30), nullable = False)
    accion = Column(String(250), nullable = False)
    fecha_accion = Column(DateTime, nullable = False)
    
    usuario = relationship("Usuario", back_populates = "auditoria")