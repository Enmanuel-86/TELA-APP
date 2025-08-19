from conexiones.conexion import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship


class HistorialEnfermCronicas(Base):
    __tablename__ = "tb_historial_enferm_cronicas"
    
    hist_enferm_cronica_id = Column(Integer, primary_key = True, autoincrement = True)
    empleado_id = Column(Integer, ForeignKey("tb_empleados.empleado_id", ondelete = "CASCADE", onupdate = "CASCADE"))
    enferm_cronica_id = Column(Integer, ForeignKey("tb_enfermedades_cronicas.enferm_cronica_id", ondelete = "RESTRICT", onupdate = "CASCADE"), nullable = False)
    
    empleado = relationship("Empleado", back_populates = "historial_enfermedades")
    enfermedad_cronica = relationship("EnfermedadCronica", back_populates = "historial_enfermedades")