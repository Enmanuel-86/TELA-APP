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

# Servicios
# especialidades
from servicios.especialidades.especialidad_servicio import EspecialidadServicio


# alumnos
from servicios.alumnos.alumno_servicio import AlumnoServicio
from servicios.alumnos.inscripcion_servicio import InscripcionServicio
from servicios.alumnos.info_bancaria_alumno_servicio import InfoBancariaAlumnoServicio
from servicios.alumnos.info_clinica_alumno_servicio import InfoClinicaAlumnoServicio
from servicios.alumnos.inscripcion_servicio import InscripcionServicio



# Instanacias Repositorios
# especialidades
especialidad_repositorio = EspecialidadRepositorio()

# Alumnos:

alumnos_repositorio = AlumnoRepositorio()

inscripcion_repositorio = InscripcionRepositorio()

info_bancaria_alumno_repositorio = InfoBancarioAlumnoRepositorio()

info_clinica_alumno_repositorio = InfoClinicaAlumnoRepositorio()



# Instancia Servicios

# especialidades
especialidad_servicio = EspecialidadServicio(especialidad_repositorio)


# Alumnos

alumnos_servicio = AlumnoServicio(alumnos_repositorio)

inscripcion_servicio = InscripcionServicio(inscripcion_repositorio)

info_bancaria_alumno_servicio = InfoBancariaAlumnoServicio(info_bancaria_alumno_repositorio)

info_clinica_alumno_servicio = InfoClinicaAlumnoServicio(info_clinica_alumno_repositorio)