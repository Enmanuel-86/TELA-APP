from conexiones.conexion import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class DetalleCargo(Base):
    __tablename__ = "tb_detalles_cargo"
    
    detalle_cargo_id = Column(Integer, primary_key = True, autoincrement = True)
    empleado_id = Column(Integer, ForeignKey("tb_empleados.empleado_id", ondelete = "CASCADE", onupdate = "CASCADE"), unique = True, nullable = False)
    cargo_id = Column(Integer, ForeignKey("tb_cargos_empleados.cargo_id", ondelete = "RESTRICT", onupdate = "CASCADE"), nullable = False)
    funcion_cargo_id = Column(Integer, ForeignKey("tb_funciones_cargo.funcion_cargo_id", ondelete = "RESTRICT", onupdate = "CASCADE"), nullable = False)
    tipo_cargo_id = Column(Integer, ForeignKey("tb_tipos_cargo.tipo_cargo_id", ondelete = "RESTRICT", onupdate = "CASCADE"), nullable = False)
    especialidad_id = Column(Integer, ForeignKey("tb_especialidades.especialidad_id", ondelete = "RESTRICT", onupdate = "CASCADE"))
    titulo_cargo = Column(String(100), nullable = False)
    labores_cargo = Column(String(50))
    
    empleado = relationship("Empleado", back_populates = "detalle_cargo")
    cargo_empleado = relationship("CargoEmpleado", back_populates = "detalle_cargo")
    funcion_cargo = relationship("FuncionCargo", back_populates = "detalle_cargo")
    tipo_cargo = relationship("TipoCargo", back_populates = "detalle_cargo")
    especialidad = relationship("Especialidad", back_populates = "detalle_cargo")