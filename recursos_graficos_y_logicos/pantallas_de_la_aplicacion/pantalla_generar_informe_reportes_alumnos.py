from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import  QWidget, QMessageBox
from PyQt5.QtCore import QDate, QDateTime

import os
from ..elementos_graficos_a_py import Ui_PantallaGenerarInformesReportesAlumnos


"""##################################
# Importaciones de base de datos #
##################################

from repositorios.alumnos.asistencia_alumno_repositorio import AsistenciaAlumnoRepositorio
from repositorios.especialidades.especialidad_repositorio import EspecialidadRepositorio
from reportes.alumnos.reporte_asistencia_mensual_alumnos import ReporteAsistenciaMensualAlumnos
from excepciones.base_datos_error import BaseDatosError

# Instancia de la base de datos

reporte_asistencia_mensual_alumnos = ReporteAsistenciaMensualAlumnos()
asistencia_alumno_repositorio = AsistenciaAlumnoRepositorio()
especialidad_repositorio = EspecialidadRepositorio()
"""


class PantallaGenerarInformesReportesAlumnos(QWidget, Ui_PantallaGenerarInformesReportesAlumnos):
    def __init__(self, stacked_widget):
        super().__init__()
        
        self.stacked_widget = stacked_widget
        self.setupUi(self)
    """   
        self.boton_generar_reporte_asistencia.clicked.connect(self.generar_reporte_de_asistencia)
        
        
    def generar_reporte_de_asistencia(self):
        
        
        
        ESPECIALIDAD_ID = 1
        ANIO =  self.dateedit_fecha_reporte_asistencia.date().year()
        MES = self.dateedit_fecha_reporte_asistencia.date().month()

        # Se envuelve la carga de datos junto con la exportación para recibir cualquier error y que se muestre en pantalla en caso
        # de que no se pueda exportar dicho reporte de asistencia
        try:
            # Acá se cargan los datos para que internamente se transporte hacia el siguiente método (exportar)
            datos = reporte_asistencia_mensual_alumnos.cargar_datos(asistencia_alumno_repositorio, especialidad_repositorio, ESPECIALIDAD_ID, ANIO, MES)
            
            # Y por último exportamos los datos cargados
            reporte_asistencia_mensual_alumnos.exportar(datos)
        except BaseDatosError as error:
            
            QMessageBox.warning(self, "AVISO", f"{error}")
            
            
        else:
            
            
            QMessageBox.information(self, "AVISO", f"Generado con exito")"""