from PyQt5.QtWidgets import (QWidget, QMessageBox, QApplication, QListWidget, QListWidgetItem, 
                            QLabel, QHBoxLayout, QPushButton )
from PyQt5.QtCore import QSize, QPoint, Qt, QDate
from PyQt5.QtGui import QIcon
from PyQt5 import QtGui, QtCore
import os
from ..elementos_graficos_a_py import Ui_VistaGeneralAsistenciaAlumnos
from ..utilidades.funciones_sistema import FuncionSistema
from datetime import datetime, date


##################################
# importaciones de base de datos #
##################################

# Repositorios

from repositorios.especialidades.especialidad_repositorio import EspecialidadRepositorio
from repositorios.alumnos.alumno_repositorio import AlumnoRepositorio
from repositorios.alumnos.inscripcion_repositorio import InscripcionRepositorio
from repositorios.alumnos.asistencia_alumno_repositorio import AsistenciaAlumnoRepositorio

# Servicios

from servicios.especialidades.especialidad_servicio import EspecialidadServicio
from servicios.alumnos.alumno_servicio import AlumnoServicio
from servicios.alumnos.inscripcion_servicio import InscripcionServicio
from servicios.alumnos.asistencia_alumno_servicio import AsistenciaAlumnoServicio

# Instanacias Repositorios

especialidad_repositorio = EspecialidadRepositorio()

alumnos_repositorio = AlumnoRepositorio()

inscripcion_repositorio = InscripcionRepositorio()

asistencia_alumno_repositorio = AsistenciaAlumnoRepositorio()


# Instancia Servicios

especialidad_servicio = EspecialidadServicio(especialidad_repositorio)

alumnos_servicio = AlumnoServicio(alumnos_repositorio)

inscripcion_servicio = InscripcionServicio(inscripcion_repositorio)

asistencia_alumno_servicio = AsistenciaAlumnoServicio(asistencia_alumno_repositorio)



##################################
# importaciones de base de datos #
##################################


lista_especialidades = especialidad_servicio.obtener_todos_especialidades()



# Dia actual
today = datetime.now()
dia_de_hoy = today.strftime("%Y-%m-%d")


class PantallaVistaGeneralAsistenciaAlumnos(QWidget, Ui_VistaGeneralAsistenciaAlumnos):
    def __init__(self, stacked_widget):
        super().__init__()

        self.stacked_widget = stacked_widget
        self.setupUi(self)
        
        
    