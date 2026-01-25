##################################
# importaciones de base de datos #
##################################


# Repositorios

# especialidades
from repositorios.especialidades.especialidad_repositorio import EspecialidadRepositorio


# Alumnos
from repositorios.alumnos.alumno_repositorio import AlumnoRepositorio
from repositorios.alumnos.inscripcion_repositorio import InscripcionRepositorio
from repositorios.alumnos.info_bancaria_alumno_repositorio import InfoBancarioAlumnoRepositorio
from repositorios.alumnos.info_clinica_alumno_repositorio import InfoClinicaAlumnoRepositorio
from repositorios.alumnos.inscripcion_repositorio import InscripcionRepositorio

# USUARIOS
from repositorios.usuarios.usuario_repositorio import UsuarioRepositorio
from repositorios.usuarios.rol_repositorio import RolRepositorio
from repositorios.usuarios.auditoria_repositorio import AuditoriaRepositorio
from repositorios.usuarios.permiso_repositorio import PermisoRepositorio


# EMPLEADOS
from repositorios.empleados.empleado_repositorio import EmpleadoRepositorio


# Servicios

# especialidades
from servicios.especialidades.especialidad_servicio import EspecialidadServicio


# alumnos
from servicios.alumnos.alumno_servicio import AlumnoServicio
from servicios.alumnos.inscripcion_servicio import InscripcionServicio
from servicios.alumnos.info_bancaria_alumno_servicio import InfoBancariaAlumnoServicio
from servicios.alumnos.info_clinica_alumno_servicio import InfoClinicaAlumnoServicio
from servicios.alumnos.inscripcion_servicio import InscripcionServicio


# USUARIOS
from servicios.usuarios.usuario_servicio import UsuarioServicio
from servicios.usuarios.rol_servicio import RolServicio
from servicios.usuarios.auditoria_servicio import AuditoriaServicio
from servicios.usuarios.permiso_servicio import PermisoServicio


# EMPLEADOS
from servicios.empleados.empleado_servicio import EmpleadoServicio


# Instanacias Repositorios

# especialidades
especialidad_repositorio = EspecialidadRepositorio()

# Alumnos:

alumnos_repositorio = AlumnoRepositorio()

inscripcion_repositorio = InscripcionRepositorio()

info_bancaria_alumno_repositorio = InfoBancarioAlumnoRepositorio()

info_clinica_alumno_repositorio = InfoClinicaAlumnoRepositorio()


# USUARIOS
usuario_repositorio = UsuarioRepositorio()
rol_repositorio = RolRepositorio()
auditoria_repositorio = AuditoriaRepositorio()
permiso_repositorio = PermisoRepositorio()


# EMPLEADOS
empleado_repositorio = EmpleadoRepositorio()


# Instancia Servicios

# especialidades
especialidad_servicio = EspecialidadServicio(especialidad_repositorio)


# Alumnos

alumnos_servicio = AlumnoServicio(alumnos_repositorio)

inscripcion_servicio = InscripcionServicio(inscripcion_repositorio)

info_bancaria_alumno_servicio = InfoBancariaAlumnoServicio(info_bancaria_alumno_repositorio)

info_clinica_alumno_servicio = InfoClinicaAlumnoServicio(info_clinica_alumno_repositorio)


# USUARIOS
usuario_servicio = UsuarioServicio(usuario_repositorio)
rol_servicio = RolServicio(rol_repositorio)
auditoria_servicio = AuditoriaServicio(auditoria_repositorio)
permiso_servicio = PermisoServicio(permiso_repositorio)


# EMPLEADOS
empleado_servicio = EmpleadoServicio(empleado_repositorio)