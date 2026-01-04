from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QWidget, QPushButton , QHBoxLayout, QListWidgetItem, QLabel)
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QSize
import os
from ..elementos_graficos_a_py import Ui_PantallaInfoCompletaDelAlumno
from ..utilidades.funciones_sistema import FuncionSistema

##################################
# importaciones de base de datos #
##################################

# Repositorios

from repositorios.alumnos.alumno_repositorio import AlumnoRepositorio
from repositorios.alumnos.inscripcion_repositorio import InscripcionRepositorio
from repositorios.alumnos.info_bancaria_alumno_repositorio import InfoBancarioAlumnoRepositorio
from repositorios.alumnos.info_clinica_alumno_repositorio import InfoClinicaAlumnoRepositorio
from repositorios.alumnos.inscripcion_repositorio import InscripcionRepositorio

# Servicios

from servicios.alumnos.alumno_servicio import AlumnoServicio
from servicios.alumnos.inscripcion_servicio import InscripcionServicio
from servicios.alumnos.info_bancaria_alumno_servicio import InfoBancariaAlumnoServicio
from servicios.alumnos.info_clinica_alumno_servicio import InfoClinicaAlumnoServicio
from servicios.alumnos.inscripcion_servicio import InscripcionServicio



# Instanacias Repositorios


alumnos_repositorio = AlumnoRepositorio()

inscripcion_repositorio = InscripcionRepositorio()

info_bancaria_alumno_repositorio = InfoBancarioAlumnoRepositorio()

info_clinica_alumno_repositorio = InfoClinicaAlumnoRepositorio()



# Instancia Servicios


alumno_servicio = AlumnoServicio(alumnos_repositorio)

inscripcion_servicio = InscripcionServicio(inscripcion_repositorio)

info_bancaria_alumno_servicio = InfoBancariaAlumnoServicio(info_bancaria_alumno_repositorio)

info_clinica_alumno_servicio = InfoClinicaAlumnoServicio(info_clinica_alumno_repositorio)



class PantallaPerfilAlumno(QWidget, Ui_PantallaInfoCompletaDelAlumno):
    def __init__(self, stacked_widget):
        super().__init__()

        self.stacked_widget = stacked_widget
        self.setupUi(self)
        
    
        # Ruta relativa de las imagenes ##
        self.label_imagen_del_alumno.setPixmap(QtGui.QPixmap(os.path.join(os.path.dirname(__file__), "..","recursos_de_imagenes", "estudiante_m.png")))
        
        self.dockWidget_diagnostico.hide()
        
        
        self.lista_qlineedit = (self.input_mostrar_cedula_representante, self.input_mostrar_cedula_representante, self.input_mostrar_apellido, self.input_mostrar_nombre, self.input_mostrar_carga_familiar,
                                self.input_mostrar_direccion_residencial, self.input_mostrar_cedula, self.input_mostrar_escolaridad, self.input_mostrar_especialidad, self.input_mostrar_procedencia,
                                self.input_mostrar_primer_nombre, self.input_mostrar_segundo_nombre, self.input_mostrar_apellido_materno, self.input_mostrar_apellido_paterno, self.input_mostrar_estado_civil,
                                self.label_mostrar_estado, self.input_mostrar_tiempo, self.input_mostrar_fecha_ingreso, self.input_mostrar_edad, self.input_mostrar_fecha_nacimiento, self.input_mostrar_lugar_nacimiento, 
                                self.input_mostrar_numero_telefono,  self.input_mostrar_relacion_alumno, self.lista_cuentas_alumno, self.lista_diagnostico_alumno
                                
                                )
        
        
     
        
        self.boton_de_regreso.clicked.connect(self.volver_vista_general_alumnos)
        
        
    
    # Metodo para acceder a la informacion del alumno
    def mostrar_la_info_alumno(self, alumno_id: int):
        
        """
        
            Este metodo sirve para ver toda la informacion del alumno en su correspondiente pantalla, esto funciona asi:
            
            1. en una variable accedemos a la pantalla de ver_perfil_alumno
            2. usamos todos los metodos de la base de datos para acceder a la informacion del alumno con el id que pedimos en la barra de busqueda o en la tabla de la vista previa
            3. se cargan los datos a cada QLineEdit, QRadioButton, QListWidget, QLabel, etc, de cada segmento
        
        
        """
        

    
        if self.lista_cuentas_alumno.count() == 0:
            
            self.lista_cuentas_alumno.addItem("No tiene cuentas bancarias registradas")
            
        
        
        # cargamos todos la infomacion del alumno
        info_basica = alumno_servicio.obtener_alumno_por_id(alumno_id)
        
        datos_representante = alumno_servicio.obtener_datos_representante(alumno_id)
        
        
        info_academica = alumno_servicio.obtener_info_academica_alumno(alumno_id)
        
        info_clinica = info_clinica_alumno_servicio.obtener_info_clinica_por_alumno_id(alumno_id)
        
        info_inscripcion = inscripcion_servicio.obtener_inscripcion_por_id(alumno_id)
        
        
        try:
            
            
            # info basica
            self.input_mostrar_cedula.setText(info_basica[1])
            self.input_mostrar_primer_nombre.setText(info_basica[2])
            
            segundo_nombre = FuncionSistema.comprobar_si_hay_valor(info_basica[3])
            self.input_mostrar_segundo_nombre.setText(segundo_nombre)
            
            
            tercer_nombre = FuncionSistema.comprobar_si_hay_valor(info_basica[4])
            self.input_mostrar_tercer_nombre.setText(tercer_nombre)
            
            
            self.input_mostrar_apellido_paterno.setText(info_basica[5])
            
            apellido_materno = FuncionSistema.comprobar_si_hay_valor(info_basica[6])
            self.input_mostrar_apellido_materno.setText(apellido_materno)
            self.input_mostrar_fecha_nacimiento.setText(info_basica[7])
            self.input_mostrar_edad.setText(str(info_basica[8]))
            self.input_mostrar_lugar_nacimiento.setText(info_basica[9])
            
            self.label_mostrar_estado.setText(info_basica[14])
            
            
            if info_basica[10] == 'F':
                    
                self.label_imagen_del_alumno.setPixmap(QtGui.QPixmap(os.path.join(os.path.dirname(__file__), "..", "recursos_de_imagenes", "estudiante_f.png")))
                
                self.input_sexo_femenino.setChecked(True)
                self.input_sexo_masculino.setChecked(False)
                
                
            elif info_basica[10] == 'M':
                
                
                self.label_imagen_del_alumno.setPixmap(QtGui.QPixmap(os.path.join(os.path.dirname(__file__), "..", "recursos_de_imagenes", "estudiante_m.png")))
                self.input_sexo_masculino.setChecked(True)
                self.input_sexo_femenino.setChecked(False)
        
        
        
            if info_basica[11] == 1:
                
                self.input_si_cma.setChecked(True)
                self.input_no_cma.setChecked(False)
                
            elif info_basica[11] == 0:
                
                self.input_no_cma.setChecked(True)
                self.input_si_cma.setChecked(False)
                
                
                
            if info_basica[12] == 1:
                
                self.input_si_imt.setChecked(True)
                self.input_no_imt.setChecked(False)
                
            elif info_basica[12] == 0:
                
                self.input_no_imt.setChecked(True)
                self.input_si_imt.setChecked(False)
                
        except Exception as e:
            
            print(f"Algo malo paso en la info basica: {e}")  
            
            
        
        try:    
            # Datos del representante
                
            
            
            self.input_mostrar_nombre.setText(datos_representante[3])
            self.input_mostrar_apellido.setText(datos_representante[4])   
            self.input_mostrar_relacion_alumno.setText(info_inscripcion[10])
            self.input_mostrar_cedula_representante.setText(datos_representante[2])
            
            self.input_mostrar_direccion_residencial.setText(datos_representante[5])
            self.input_mostrar_numero_telefono.setText(datos_representante[6])
            
            if datos_representante[7] == None:
                self.input_mostrar_numero_telefono_adicional.setText("No tiene")
            
            else:
                self.input_mostrar_numero_telefono_adicional.setText(datos_representante[7])
            
            self.input_mostrar_carga_familiar.setText(str(datos_representante[8]))   
            self.input_mostrar_estado_civil.setText(datos_representante[9])
            
        except Exception as e:
            print(f"Algo paso en datos del representante: {e}")
            
            
        
        
        try: 
        
            # Info bancaria del alumno
            info_bancaria = info_bancaria_alumno_servicio.obtener_info_bancaria_por_alumno_id(alumno_id)
            
            if info_bancaria:
                
                print("tiene cuenta en el banco")
                print(info_bancaria)
                self.lista_cuentas_alumno.clear()
                self.agregar_elementos_a_la_vista_previa_cuentas_alumno(self.lista_cuentas_alumno, info_bancaria)
                
                
            
        except Exception as e:
            
            print(f"Algo paso en info bancaria: {e}")
    
            
            
        
        
        
        
        try:
            
            
            # info escolaridad
            
            self.input_mostrar_escolaridad.setText(info_academica[1])
            self.input_mostrar_procedencia.setText(info_academica[2])
            
            
        except Exception as e:
            print(f"Algo paso en escolaridad: {e}")
            
            
            
        try:
            
            
            # info clinica
            self.agregar_elementos_a_la_vista_previa_diagnostico_alumno(self.lista_diagnostico_alumno, info_clinica)
            
        except Exception as e:
            print(f"Algo paso en info clinia: {e}")
            
            
        try:
            
            
            # info inscripcion
            self.input_mostrar_especialidad.setText(info_inscripcion[4])
            self.input_mostrar_matricula.setText(info_inscripcion[5])
            self.input_mostrar_fecha_ingreso.setText(str(info_inscripcion[6]))
            self.input_mostrar_tiempo.setText("1 año")
            
            
            
        except Exception as e:
            print(f"Algo paso en info inscripcion: {e}")
            
            
    # Metodo para agregar diagnostico a la vista previa
    def agregar_elementos_a_la_vista_previa_diagnostico_alumno(self, nombre_qlistwidget, nombre_lista):
        
        i = 1
        for diagnostico in nombre_lista:
            
            
            
            texto_a_mostrar = f"{i}) " + diagnostico[2]
            
            i += 1
            
            # Crear un QListWidgetItem
            item = QListWidgetItem()
            nombre_qlistwidget.addItem(item)
            
            

            # Crear un widget personalizado para la fila
            widget = QWidget()
            row_layout = QHBoxLayout()
            widget.setLayout(row_layout)

            # Label para el texto
            label = QLabel(texto_a_mostrar if texto_a_mostrar else f"Elemento {self.list_widget.count() + 1}")
            label.setStyleSheet("""
                                
                                QLabel{
                                    
                                    background:none;
                                    font-family: 'Arial';
                                    font-size: 14pt;
                                    
                                    
                                }
                                
                                """)
            row_layout.addWidget(label)

            # Botón para eliminar
            boton_ver = QPushButton()
            boton_ver.setIcon(QIcon.fromTheme(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "iconos_de_interfaz", "ver_contraseña.png")))
            boton_ver.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            boton_ver.setFixedSize(60,40)
            boton_ver.setIconSize(QSize(30, 30))
            boton_ver.setProperty("tipo", "boton_ver")
            
            
            row_layout.addWidget(boton_ver)
            
            boton_ver.clicked.connect(
            lambda  _, item=item, lista=nombre_lista: self.ver_diagnostico_seleccionado(nombre_qlistwidget, lista, item)
        )
        
            # Asignar el widget al QListWidgetItem
            item.setSizeHint(widget.sizeHint())
            nombre_qlistwidget.setItemWidget(item, widget)


    # Metodo para agregar diagnostico a la vista previa
    def agregar_elementos_a_la_vista_previa_cuentas_alumno(self, nombre_qlistwidget, nombre_lista):
        
        
        for cuenta in nombre_lista:
            
            texto_a_mostrar = cuenta[2] + " " + cuenta[3] 
    
            # Crear un QListWidgetItem
            item = QListWidgetItem()
            nombre_qlistwidget.addItem(item)
            
            

            # Crear un widget personalizado para la fila
            widget = QWidget()
            row_layout = QHBoxLayout()
            widget.setLayout(row_layout)

            # Label para el texto
            label = QLabel(texto_a_mostrar if texto_a_mostrar else f"Elemento {self.list_widget.count() + 1}")
            label.setStyleSheet("""
                                
                                QLabel{
                                    
                                    background:none;
                                    font-family: 'Arial';
                                    font-size: 14pt;
                                    
                                    
                                }
                                
                                """)
            row_layout.addWidget(label)

            # Asignar el widget al QListWidgetItem
            item.setSizeHint(widget.sizeHint())
            nombre_qlistwidget.setItemWidget(item, widget)
            
            
        
    

    
    def ver_diagnostico_seleccionado(self, nombre_qlistwidget, nombre_lista,  item):
        
        """
            Metodo para mostrar el dockwidget que se encargar de mostrar el diagnostico seleccionado del alumno
        
        
        """
        
        indice_vista_previa = nombre_qlistwidget.row(item)
        
        info_clinica_id = nombre_lista[indice_vista_previa][0]
        
        print(f"Indice del diagnostico: {info_clinica_id}")
        
        
        try:
            
            diagnostico = info_clinica_alumno_servicio.obtener_info_clinica_alumno_por_id(info_clinica_id)
        
            if self.dockWidget_diagnostico.show():
                
                self.dockWidget_diagnostico.hide()
                
            elif self.dockWidget_diagnostico.hide():
                
                self.dockWidget_diagnostico.show()
                
                
                
        
        except Exception as e:
            
            FuncionSistema.mostrar_errores_por_excepcion(e, "mostrar_diagnostico")    
            
            
        else:
            titulo= f"Diagnóstico N° {indice_vista_previa + 1}"
            nombre_diag= diagnostico[2]
            fecha_diag= str(diagnostico[3])
            medico = diagnostico[4]
            medicacion=diagnostico[5]
            certificado=str(diagnostico[6])
            fecha_venc= diagnostico[7]
            
            self.dockWidget_diagnostico.setWindowTitle(f"{titulo}: {nombre_diag}")
            self.titulo.setText(titulo)
            self.input_mostrar_diagnostico.setText(nombre_diag)
            self.input_mostrar_fecha_diagnostico.setText(fecha_diag)
            self.input_mostrar_medico_tratante.setText(medico)
            self.input_mostrar_certificado_discap.setText(certificado)
            self.input_mostrar_fecha_venc_certificado.setText(fecha_venc)
            self.input_mostrar_medicacion.setText(medicacion)
            
            self.dockWidget_diagnostico.show()
            self.dockWidget_diagnostico.setFloating(True)
    
        

            
            
        # Metodo para volver a la pantalla anterior
    
    
    def volver_vista_general_alumnos(self):
        
        self.stacked_widget.setCurrentIndex(2)
        self.dockWidget_diagnostico.hide()

        
        FuncionSistema.limpiar_inputs_de_qt(self.lista_qlineedit)
    
    