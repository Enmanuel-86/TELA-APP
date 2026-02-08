"""
    Este archivo contiene todas las importaciones necesarias para utilizar la base de datos, y funciona asi:
    
    - La base de datos diseñada para este sistema funciona a partir de un repositorio y un servicio
    - Se importan primero los repositorios y luego los servicios
    - Se le da instacia a los repositorios y a los servicios
    - Despues se pueden utilizar la base de datos solamente llamando el servicio correspondiente
    
    **Ejemplo:**
    
    si quiere obtener los cargos de los empleados use el servicio correspondiente
    
    from ..utilidades.base_de_datos import cargos_empleado_servicio
    
    cargo_empleado_servicio.obtener_todos_cargos_empleados() retorna una lista con todos los cargos registrados en la base de datos


"""


##################################
# importaciones de base de datos #
##################################


# Repositorios

# EMPLEADOS
from repositorios.empleados.empleado_repositorio import EmpleadoRepositorio
from repositorios.empleados.info_laboral_repositorio import InfoLaboralRepositorio
from repositorios.empleados.cargo_empleado_repositorio import CargoEmpleadoRepositorio
from repositorios.empleados.detalle_cargo_repositorio import DetalleCargoRepositorio
from repositorios.empleados.tipo_cargo_repositorio import TipoCargoRepositorio
from repositorios.empleados.historial_enferm_cronicas_repositorio import HistorialEnfermCronicasRepositorio
from repositorios.empleados.info_clinica_empleado_repositorio import InfoClinicaEmpleadoRepositorio
from repositorios.empleados.asistencia_empleado_repositorio import AsistenciaEmpleadoRepositorio

# especialidades
from repositorios.especialidades.especialidad_repositorio import EspecialidadRepositorio

# Diagnosticos
from repositorios.diagnosticos.diagnostico_repositorio import DiagnosticoRepositorio 


# Alumnos
from repositorios.alumnos.alumno_repositorio import AlumnoRepositorio
from repositorios.alumnos.inscripcion_repositorio import InscripcionRepositorio
from repositorios.alumnos.info_bancaria_alumno_repositorio import InfoBancarioAlumnoRepositorio
from repositorios.alumnos.info_clinica_alumno_repositorio import InfoClinicaAlumnoRepositorio
from repositorios.alumnos.inscripcion_repositorio import InscripcionRepositorio
from repositorios.alumnos.medidas_alumno_repositorio import MedidasAlumnoRepositorio
from repositorios.alumnos.representante_repositorio import RepresentanteRepositorio



# USUARIOS
from repositorios.usuarios.usuario_repositorio import UsuarioRepositorio
from repositorios.usuarios.rol_repositorio import RolRepositorio
from repositorios.usuarios.auditoria_repositorio import AuditoriaRepositorio
from repositorios.usuarios.permiso_repositorio import PermisoRepositorio


# EMPLEADOS
from servicios.empleados.empleado_servicio import EmpleadoServicio
from servicios.empleados.info_laboral_servicio import InfoLaboralServicio
from servicios.empleados.detalle_cargo_servicio import DetalleCargoServicio
from servicios.empleados.cargo_empleado_servicio import CargoEmpleadoServicio
from servicios.empleados.tipo_cargo_servicio import TipoCargoServicio
from servicios.empleados.historial_enferm_cronicas_servicio import HistorialEnfermCronicasServicio
from servicios.empleados.info_clinica_empleado_servicio import InfoClinicaEmpleadoServicio
from servicios.empleados.asistencia_empleado_servicio import AsistenciaEmpleadoServicio

#################
### Servicios ###
################

# Especialidades
from servicios.especialidades.especialidad_servicio import EspecialidadServicio

# Diagnostico
from servicios.diagnosticos.diagnostico_servicio import DiagnosticoServicio

# 

# Alumnos
from servicios.alumnos.alumno_servicio import AlumnoServicio
from servicios.alumnos.inscripcion_servicio import InscripcionServicio
from servicios.alumnos.info_bancaria_alumno_servicio import InfoBancariaAlumnoServicio
from servicios.alumnos.info_clinica_alumno_servicio import InfoClinicaAlumnoServicio
from servicios.alumnos.inscripcion_servicio import InscripcionServicio
from servicios.alumnos.medidas_alumno_servicio import MedidasAlumnoServicio
from servicios.alumnos.representante_servicio import RepresentanteServicio

# USUARIOS
from servicios.usuarios.usuario_servicio import UsuarioServicio
from servicios.usuarios.rol_servicio import RolServicio
from servicios.usuarios.auditoria_servicio import AuditoriaServicio
from servicios.usuarios.permiso_servicio import PermisoServicio


# EMPLEADOS
from servicios.empleados.empleado_servicio import EmpleadoServicio
from servicios.empleados.asistencia_empleado_servicio import AsistenciaEmpleadoServicio


# Instanacias Repositorios

# especialidades
especialidad_repositorio = EspecialidadRepositorio()


# Diagnosticos
diagnostico_repositorio = DiagnosticoRepositorio()



# Alumnos:

alumno_repositorio = AlumnoRepositorio()
inscripcion_repositorio = InscripcionRepositorio()
info_bancaria_alumno_repositorio = InfoBancarioAlumnoRepositorio()
info_clinica_alumno_repositorio = InfoClinicaAlumnoRepositorio()
medidas_alumno_repositorio = MedidasAlumnoRepositorio()
representante_repositorio = RepresentanteRepositorio()


# USUARIOS
usuario_repositorio = UsuarioRepositorio()
rol_repositorio = RolRepositorio()
auditoria_repositorio = AuditoriaRepositorio()
permiso_repositorio = PermisoRepositorio()


# EMPLEADOS
empleado_repositorio = EmpleadoRepositorio()
asistencia_empleado_repositorio = AsistenciaEmpleadoRepositorio()
empleado_repositorio = EmpleadoRepositorio()
info_laboral_repositorio = InfoLaboralRepositorio()
cargo_empleado_repositorio = CargoEmpleadoRepositorio()
detalle_cargo_repositorio = DetalleCargoRepositorio()
tipo_cargo_repositorio = TipoCargoRepositorio()
especialidad_repositorio = EspecialidadRepositorio()
histotial_enferm_cronicas_repositorio = HistorialEnfermCronicasRepositorio()
info_clinica_empleado_repositorio = InfoClinicaEmpleadoRepositorio()



###########################
### Instancia Servicios ###
###########################

# EMPLEADOS
asistencia_empleado_servicio = AsistenciaEmpleadoServicio(asistencia_empleado_repositorio)

# especialidades
especialidad_servicio = EspecialidadServicio(especialidad_repositorio)

# Diagnostico
diagnostico_servicio = DiagnosticoServicio(diagnostico_repositorio)

# Alumnos
alumno_servicio = AlumnoServicio(alumno_repositorio)
inscripcion_servicio = InscripcionServicio(inscripcion_repositorio)
info_bancaria_alumno_servicio = InfoBancariaAlumnoServicio(info_bancaria_alumno_repositorio)
info_clinica_alumno_servicio = InfoClinicaAlumnoServicio(info_clinica_alumno_repositorio)
medidas_alumno_servicio = MedidasAlumnoServicio(medidas_alumno_repositorio)
representante_servicio = RepresentanteServicio(representante_repositorio)

# USUARIOS
usuario_servicio = UsuarioServicio(usuario_repositorio)
rol_servicio = RolServicio(rol_repositorio)
auditoria_servicio = AuditoriaServicio(auditoria_repositorio)
permiso_servicio = PermisoServicio(permiso_repositorio)


# EMPLEADOS
empleado_servicio = EmpleadoServicio(empleado_repositorio)
info_laboral_servicio = InfoLaboralServicio(info_laboral_repositorio)
cargo_empleado_servicio = CargoEmpleadoServicio(cargo_empleado_repositorio)
detalle_cargo_servicio = DetalleCargoServicio(detalle_cargo_repositorio)
tipo_cargo_servicio = TipoCargoServicio(tipo_cargo_repositorio)
especialidad_servicio = EspecialidadServicio(especialidad_repositorio)
histotial_enferm_cronicas_servicio = HistorialEnfermCronicasServicio(histotial_enferm_cronicas_repositorio)
info_clinica_empleado_servicio = InfoClinicaEmpleadoServicio(info_clinica_empleado_repositorio)