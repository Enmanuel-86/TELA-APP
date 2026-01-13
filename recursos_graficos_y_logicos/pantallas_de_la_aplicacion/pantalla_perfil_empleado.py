from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import  QWidget, QLineEdit
from PyQt5 import QtGui
import os
from ..elementos_graficos_a_py import Ui_PantallaInfoCompletaDelEmpleado
from ..utilidades.funciones_sistema import FuncionSistema

# Repositorio
from repositorios.empleados.empleado_repositorio import EmpleadoRepositorio
from repositorios.empleados.info_laboral_repositorio import InfoLaboralRepositorio
from repositorios.empleados.cargo_empleado_repositorio import CargoEmpleadoRepositorio
from repositorios.empleados.detalle_cargo_repositorio import DetalleCargoRepositorio
from repositorios.empleados.tipo_cargo_repositorio import TipoCargoRepositorio
from repositorios.especialidades.especialidad_repositorio import EspecialidadRepositorio
from repositorios.empleados.historial_enferm_cronicas_repositorio import HistorialEnfermCronicasRepositorio
from repositorios.empleados.info_clinica_empleado_repositorio import InfoClinicaEmpleadoRepositorio



# servicios
from servicios.empleados.empleado_servicio import EmpleadoServicio
from servicios.empleados.info_laboral_servicio import InfoLaboralServicio
from servicios.empleados.detalle_cargo_servicio import DetalleCargoServicio
from servicios.empleados.cargo_empleado_servicio import CargoEmpleadoServicio
from servicios.empleados.tipo_cargo_servicio import TipoCargoServicio
from servicios.especialidades.especialidad_servicio import EspecialidadServicio
from servicios.empleados.historial_enferm_cronicas_servicio import HistorialEnfermCronicasServicio
from servicios.empleados.info_clinica_empleado_servicio import InfoClinicaEmpleadoServicio



##################################
# importaciones de base de datos #
##################################



# instancias de los repositorios

empleado_repositorio = EmpleadoRepositorio()

info_laboral_repositorio = InfoLaboralRepositorio()

cargo_empleado_repositorio = CargoEmpleadoRepositorio()

detalle_cargo_repositorio = DetalleCargoRepositorio()

tipo_cargo_repositorio = TipoCargoRepositorio()

especialidad_repositorio = EspecialidadRepositorio()

histotial_enferm_cronicas_repositorio = HistorialEnfermCronicasRepositorio()

info_clinica_empleado_repositorio = InfoClinicaEmpleadoRepositorio()


# instancia de los servicios

empleado_servicio = EmpleadoServicio(empleado_repositorio)

info_laboral_servicio = InfoLaboralServicio(info_laboral_repositorio)

cargo_empleado_servicio = CargoEmpleadoServicio(cargo_empleado_repositorio)

detalle_cargo_servicio = DetalleCargoServicio(detalle_cargo_repositorio)

tipo_cargo_servicio = TipoCargoServicio(tipo_cargo_repositorio)

especialidad_servicio = EspecialidadServicio(especialidad_repositorio)

histotial_enferm_cronicas_servicio = HistorialEnfermCronicasServicio(histotial_enferm_cronicas_repositorio)

info_clinica_empleado_servicio = InfoClinicaEmpleadoServicio(info_clinica_empleado_repositorio)



class PantallaPerfilEmpleado(QWidget, Ui_PantallaInfoCompletaDelEmpleado):
    def __init__(self, stacked_widget):
        super().__init__()

        self.stacked_widget = stacked_widget
        self.setupUi(self)
        
        # Ruta relativa de las imagenes ##
        self.boton_de_regreso.setIcon(QIcon.fromTheme(os.path.join(os.path.dirname(__file__), "..","recursos_de_imagenes", "iconos_de_interfaz","flecha_izquierda_2.png")))
        self.label_imagen_del_personal.setPixmap(QtGui.QPixmap(os.path.join(os.path.dirname(__file__), "..","recursos_de_imagenes", "imagen_personal_m.png")))

        self.imagen_personal_f = os.path.join(os.path.dirname(__file__), "..","recursos_de_imagenes", "imagen_personal_f.png")
        
        
        self.lista_qlineedits = (
                
                    self.input_mostrar_primer_nombre,
                    self.input_mostrar_segundo_nombre,
                    self.input_mostrar_apellido_paterno,
                    self.input_mostrar_apellido_materno,
                    self.input_mostrar_cedula,
                    self.input_mostrar_fecha_nacimiento,
                    self.input_mostrar_edad,
                    
                    self.input_mostrar_numero_telefono,
                    self.input_mostrar_correo,
                    
                    self.input_mostrar_estado_residente,
                    self.input_mostrar_municipio,
                    self.input_mostrar_direccion_residente,
                    
                    self.input_mostrar_talla_camisa,
                    self.input_mostrar_talla_pantalon,
                    self.input_mostrar_talla_zapatos,
                    
                    self.input_mostrar_codigo_cargo,
                    self.input_mostrar_cargo,
                    self.input_mostrar_funcion_cargo,
                    self.input_mostrar_tipo_cargo,
                    self.input_mostrar_titulo_cargo,
                    self.input_mostrar_labores_que_realiza,
                    self.input_mostrar_fecha_del_tela,
                    self.input_mostrar_fecha_ministerio,
                    self.input_mostrar_tiempo_servicio,
                    self.input_mostrar_especialidad,
            )
            
        self.lista_radiobuttons = (self.input_sexo_femenino, self.input_sexo_masculino, self.input_si, self.input_no)
        
        self.espacio_scroll_mostrar_datos_obtenidos.setWidgetResizable(True)
        
        self.boton_de_regreso.clicked.connect(self.volver_vista_general_empleados)
        
    
    
        
    
        
    def mostra_info_empleado(self, empleado_id):
        
        
        ## info basica del empleado
        
        try:
            
            info_basica = empleado_servicio.obtener_empleado_por_id(empleado_id)
        
            
            
        
            self.input_mostrar_primer_nombre.setText(info_basica[1])
            
            segundo_nombre = FuncionSistema.comprobar_si_hay_valor(info_basica[2])
            self.input_mostrar_segundo_nombre.setText(segundo_nombre)
            
            tercer_nombre = FuncionSistema.comprobar_si_hay_valor(info_basica[3])
            self.input_mostrar_tercer_nombre.setText(tercer_nombre)
            
            self.input_mostrar_apellido_paterno.setText(info_basica[4])
            
            apellido_materno = FuncionSistema.comprobar_si_hay_valor(info_basica[5])
            self.input_mostrar_apellido_materno.setText(apellido_materno)
            
            self.input_mostrar_cedula.setText(info_basica[6])
            self.input_mostrar_fecha_nacimiento.setText(info_basica[7])
            
            self.input_mostrar_edad.setText(str(info_basica[8]))
            
            self.label_mostrar_estado.setText(str(info_basica[9]))
            
                        
            
            if info_basica[10] == 'M' or info_basica[10] == 'm':
                
                self.label_imagen_del_personal.setPixmap(QtGui.QPixmap(os.path.join(os.path.dirname(__file__), "..", "recursos_de_imagenes", "imagen_personal_m.png")))
                self.input_sexo_masculino.setChecked(True)
                self.input_sexo_femenino.setChecked(False)
                
            if info_basica[10] == 'F' or info_basica[10] == 'f':
                
                self.label_imagen_del_personal.setPixmap(QtGui.QPixmap(os.path.join(os.path.dirname(__file__), "..", "recursos_de_imagenes", "imagen_personal_f.png")))
                self.input_sexo_masculino.setChecked(False)
                self.input_sexo_femenino.setChecked(True)
        
            FuncionSistema.cargar_foto_perfil_en_la_interfaz(info_basica[12] ,self.label_imagen_del_personal)

        
            
            if info_basica[11] == 1:
                
                self.input_si.setChecked(True)
                self.input_no.setChecked(False)
                
                
            else:
                
                self.input_si.setChecked(False)
                self.input_no.setChecked(True)
                
            
        except Exception as e:
            print(f"Algo paso en info basica: {e}")
            
       
       
        try:
            
            ## info de contacto del empleado
            info_contacto = empleado_servicio.obtener_info_contacto_empleado(empleado_id)
            
            print(info_contacto)
            self.input_mostrar_numero_telefono.setText(info_contacto[1])
            
            num_telefono_adicional = FuncionSistema.comprobar_si_hay_valor(info_contacto[2])
            self.input_mostrar_numero_telefono_adicional.setText(num_telefono_adicional)
            
            self.input_mostrar_correo.setText(info_contacto[3])
            
            correo_adicional = FuncionSistema.comprobar_si_hay_valor(info_contacto[4])
            self.input_mostrar_correo_adicional.setText(correo_adicional)


            
        except Exception as e:
            print(f"Algo paso en info contacto: {e}")
            
            
        
        ## info medidas 
        
        try:
            
            info_medidas = empleado_servicio.obtener_medidas_empleado(empleado_id)


            self.input_mostrar_talla_camisa.setText(info_medidas[1])
            self.input_mostrar_talla_pantalon.setText(str(info_medidas[2]))
            self.input_mostrar_talla_zapatos.setText(str(info_medidas[3]))
                
        except Exception as e:
            print(f"Algo paso en info medica: {e}")
            
        
        
        
        ## info geografica
        
        
        try:
            
            info_geografica = empleado_servicio.obtener_info_geografica_empleado(empleado_id)
        
        
            self.input_mostrar_estado_residente.setText(str(info_geografica[1]))
            self.input_mostrar_municipio.setText(str(info_geografica[2]))
            self.input_mostrar_direccion_residente.setText(str(info_geografica[3]))
            
            
            
            
        except Exception as e:
            print(f"Algo paso info geografica: {e}")
            
        
        
        ## info detalles del cargo
        
        
        try:
            
            info_detalles_cargos = detalle_cargo_servicio.obtener_detalles_cargo(empleado_id)
        
        
            self.input_mostrar_codigo_cargo.setText(info_detalles_cargos[1])
            self.input_mostrar_cargo.setText(info_detalles_cargos[2])
            self.input_mostrar_funcion_cargo.setText(info_detalles_cargos[3])
            self.input_mostrar_tipo_cargo.setText(info_detalles_cargos[4])
            self.input_mostrar_titulo_cargo.setText(info_detalles_cargos[5])
            
            labores = FuncionSistema.comprobar_si_hay_valor(info_detalles_cargos[6])
            self.input_mostrar_labores_que_realiza.setText(labores)
            self.input_mostrar_fecha_del_tela.setText(info_detalles_cargos[7])
            self.input_mostrar_fecha_ministerio.setText(info_detalles_cargos[8])
            self.input_mostrar_tiempo_servicio.setText(str(info_detalles_cargos[9]) + " años")
            self.input_mostrar_especialidad.setText(info_detalles_cargos[10])

            

            
            
            if not self.input_mostrar_tipo_cargo.text() == "DOCENTE" and not self.input_mostrar_tipo_cargo.text() == "Docente":
                
                self.label_especialidad.hide()
                self.input_mostrar_especialidad.hide()
            
            else:
                self.label_especialidad.show()
                self.input_mostrar_especialidad.show()
            
            
            
            #self.ver_cursor_posicion_cero(self.lista_qlineedits)
        
        
        except Exception as e:
            print(f"Algo paso detalles del cargo: {e}")
            
        
        
        
        
        ### info medica
    
        try:
            
            lista_historial_enferm = histotial_enferm_cronicas_servicio.obtener_historial_enferm_cronica_por_empleado_id(empleado_id)
            print(lista_historial_enferm)
            
            for enfermedad in lista_historial_enferm:
                
                self.mostrar_enfermedades.addItem(enfermedad[2])
                
        except Exception as e:
            print(f"Algo paso info medica: {e}")
            
        
        
        # info diagnostico
        try:
            lista_info_clinica = info_clinica_empleado_servicio.obtener_info_clinica_por_empleado_id(empleado_id)

            

            for diagnostico in lista_info_clinica:
            
                self.mostrar_diagnosticos.addItem(diagnostico[2])

        
            
        except Exception as e:
            print(f"Algo paso info diagnostico: {e}")
            
                
    
    
    
    
        
        
    def volver_vista_general_empleados(self):
        
        self.stacked_widget.setCurrentIndex(7)
        
        self.espacio_scroll_mostrar_datos_obtenidos.verticalScrollBar().setValue(0)

        self.mostrar_enfermedades.clear()
        self.mostrar_diagnosticos.clear()
        
        self.deshabilitar_inputs()
        
        
    def deshabilitar_inputs(self):
        
        for child in self.findChildren(QLineEdit):
            if not child.isReadOnly():
                child.setReadOnly(True)