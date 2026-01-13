from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import  QWidget, QMessageBox
from PyQt5.QtCore import QDate, QDateTime

import os
import platform
from ..elementos_graficos_a_py import Ui_PantallaGenerarInformesReportesAlumnos
from ..utilidades.funciones_sistema import FuncionSistema
from configuraciones.configuracion import app_configuracion

##################################
# Importaciones de base de datos #
##################################

from excepciones.base_datos_error import BaseDatosError


# Repositorios
from repositorios.alumnos.alumno_repositorio import AlumnoRepositorio
from repositorios.alumnos.medidas_alumno_repositorio import MedidasAlumnoRepositorio
from repositorios.alumnos.inscripcion_repositorio import InscripcionRepositorio
from repositorios.alumnos.info_clinica_alumno_repositorio import InfoClinicaAlumnoRepositorio
from repositorios.alumnos.asistencia_alumno_repositorio import AsistenciaAlumnoRepositorio
from repositorios.especialidades.especialidad_repositorio import EspecialidadRepositorio
from repositorios.empleados.detalle_cargo_repositorio import DetalleCargoRepositorio
from repositorios.empleados.empleado_repositorio import EmpleadoRepositorio
from repositorios.empleados.info_laboral_repositorio import InfoLaboralRepositorio
from repositorios.empleados.info_clinica_empleado_repositorio import InfoClinicaEmpleadoRepositorio

# Reportes
from reportes.alumnos.reporte_general_alumnos import ReporteGeneralAlumnos
from reportes.alumnos.reporte_asistencia_mensual_alumnos import ReporteAsistenciaMensualAlumnos
from reportes.alumnos.reporte_informe_educativo_alumnos import ReporteInformeEducativoAlumnos
from reportes.empleados.reporte_general_empleados import ReporteGeneralEmpleados


# Servicios
from servicios.especialidades.especialidad_servicio import EspecialidadServicio 


# Instancia de la base de datos

# Reportes
reporte_asistencia_mensual_alumnos = ReporteAsistenciaMensualAlumnos()

reporte_general_alumnos = ReporteGeneralAlumnos()

reporte_informe_educativo_integral_alumnos = ReporteInformeEducativoAlumnos()

reporte_general_empleados = ReporteGeneralEmpleados()

# Repositorios
asistencia_alumno_repositorio = AsistenciaAlumnoRepositorio()

especialidad_repositorio = EspecialidadRepositorio()

alumno_repositorio = AlumnoRepositorio()

medidas_alumno_repositorio = MedidasAlumnoRepositorio()

inscripcion_repositorio = InscripcionRepositorio()

info_clinica_alumno_repositorio = InfoClinicaAlumnoRepositorio()

especialidad_repositorio = EspecialidadRepositorio()

detalle_cargo_repositorio = DetalleCargoRepositorio()

empleado_repositorio = EmpleadoRepositorio()

info_laboral_repositorio = InfoLaboralRepositorio()

info_clinica_empleado_repositorio = InfoClinicaEmpleadoRepositorio()

# Servicios
especialidad_servicio = EspecialidadServicio(especialidad_repositorio)



class PantallaGenerarInformesReportesAlumnos(QWidget, Ui_PantallaGenerarInformesReportesAlumnos):
    def __init__(self, stacked_widget):
        super().__init__()
        
        self.stacked_widget = stacked_widget
        self.setupUi(self)

        # Cargar lista catalogos
        self.lista_especialidades = especialidad_servicio.obtener_todos_especialidades()
        
        # Cargar los elementos en el combobox
        FuncionSistema.cargar_elementos_para_el_combobox(self.lista_especialidades, self.boton_especialidades, 1, 1)
        
        # cargar rutas de las carpetas de los documentos
        self.carpeta_reportes_alumnos = str(app_configuracion.DIRECTORIO_REPORTES_ALUMNOS)
        self.carpeta_reportes_empleados = str(app_configuracion.DIRECTORIO_REPORTES_EMPLEADOS)
        
        # Establecer la fecha actual en el dateedit
        self.dateedit_fecha_reporte_asistencia.setDate(QDate.currentDate())
        
        
        # Conexiones a los botones
        self.boton_generar_reporte_asistencia.clicked.connect(self.generar_reporte_de_asistencia)
        self.boton_generar_informe_integral_2.clicked.connect(self.generar_caraterizacion_general_alumno)
        self.boton_generar_informe_integral.clicked.connect(self.generar_informe_educativo_integral_alumno)
        self.boton_generar_informe_general_empleados.clicked.connect(self.generar_informe_general_empleados)
        
        
    def generar_reporte_de_asistencia(self):
        
        """
            Este Metodo sirve para generar el reporte de asistencia que utilizan para calcular la estadistica de la asistencia de los alumnos segun su especialidad ocupacional
        """
        
        ESPECIALIDAD_ID = FuncionSistema.obtener_id_del_elemento_del_combobox(self.boton_especialidades, self.lista_especialidades, 1, 0, True)
        ANIO =  self.dateedit_fecha_reporte_asistencia.date().year()
        MES = self.dateedit_fecha_reporte_asistencia.date().month()

        
        if not self.boton_especialidades.currentIndex() == 0:
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
                
                
                QMessageBox.information(self, "AVISO", f"Generado con exito")
                self.boton_especialidades.setCurrentIndex(0)
                
                
                # 3. Verificar que existe
                FuncionSistema.abrir_carpeta_contenedora_de_archivos(self.carpeta_reportes_alumnos)
                

        else:
            
            QMessageBox.warning(self, "AVISO", f"Seleccione una especialidad")
            
            
    def generar_caraterizacion_general_alumno(self):
        """
        
            Este Metodo sirve para generar el informe general de los alumnos que contiene toda la informacion relevante de cada alumno
        
        """
        
        try:
            
            datos = reporte_general_alumnos.cargar_datos(
                inscripcion_repositorio, alumno_repositorio,
                medidas_alumno_repositorio, info_clinica_alumno_repositorio
            )
            
            reporte_general_alumnos.exportar(datos)
            
        except BaseDatosError as error:
            print(error)
            
        else:
            
            QMessageBox.information(self, "AVISO", f"Generado con exito")
            
            # Abrir carpeta contenedora de los archivos generados
            FuncionSistema.abrir_carpeta_contenedora_de_archivos(self.carpeta_reportes_alumnos) 
    
    def generar_informe_educativo_integral_alumno(self):
        """
        Este método es para generar el informe educativo integral de alumnos por especialidad
        
        :param self: No necesita parámetros (los obtenemos de la interfaz y los repositorios importados)
        """
        
        ESPECIALIDAD_ID = FuncionSistema.obtener_id_del_elemento_del_combobox(self.boton_especialidades, self.lista_especialidades, 1, 0, True)
        
        if not self.boton_especialidades.currentIndex() == 0:
            try:
                datos = reporte_informe_educativo_integral_alumnos.cargar_datos(
                    alumno_repositorio, inscripcion_repositorio,
                    info_clinica_alumno_repositorio, detalle_cargo_repositorio,
                    especialidad_repositorio, ESPECIALIDAD_ID,
                    self.input_director_actual.text()
                )
                
                reporte_informe_educativo_integral_alumnos.exportar(datos)
            except BaseDatosError as error:
                QMessageBox.warning(self, "AVISO", f"{error}")
            else:
                QMessageBox.information(self, "AVISO", f"Generado con exito")
                FuncionSistema.abrir_carpeta_contenedora_de_archivos(self.carpeta_reportes_alumnos)
        else:
            QMessageBox.warning(self, "AVISO", f"Seleccione una especialidad")
    
    def generar_informe_general_empleados(self):
        """
        Este método es para generar el informe general de los empleados
        
        :param self: No necesita parámetros (los obtenemos de la interfaz y los repositorios importados)
        """
        
        try:
            datos = reporte_general_empleados.cargar_datos(
                empleado_repositorio, info_laboral_repositorio,
                detalle_cargo_repositorio, info_clinica_empleado_repositorio
            )
            
            reporte_general_empleados.exportar(datos)
        except Exception as error:
            print(error)
        else:
            QMessageBox.information(self, "AVISO", f"Generado con exito")
            FuncionSistema.abrir_carpeta_contenedora_de_archivos(self.carpeta_reportes_empleados)