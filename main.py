import sys
import os
import random
from PyQt5.QtWidgets import (QApplication, QStackedWidget, QVBoxLayout,
                             QMainWindow, QWidget, QMessageBox, QLineEdit, QStatusBar)
from PyQt5.QtGui import QIcon, QPixmap

from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor


from PyQt5 import QtGui
from recursos_graficos_y_logicos.elementos_graficos_a_py import (Ui_Login, Ui_VentanaPrincipal)


from recursos_graficos_y_logicos.pantallas_de_la_aplicacion import (PantallaAdminCrearUsuario, PantallaAdminCrearRespaldo,
                                        PantallaControlDeLlegada, PantallaDeFormularioNuevoRegistroEmpleado, PantallaDeVistaGeneralDeAlumnos, PantallaDeVistaGeneralDelPersonal,
                                        PantallaPerfilEmpleado, PantallaDeFormularioNuevoRegistroAlumnos, PantallaPerfilAlumno, PantallaControlRepososPersonal, PantallaGenerarInformesReportesAlumnos,
                                        PantallaAsistenciaAlumnos, PantallaAdminInsertarCatalogo, PantallaBienvenidaUsuario)

from recursos_graficos_y_logicos.utilidades import FuncionSistema


##################################
# importaciones de base de datos #
##################################

from configuraciones.configuracion import app_configuracion
from excepciones.base_datos_error import BaseDatosError

# repositorios
from repositorios.usuarios.usuario_repositorio import UsuarioRepositorio
from repositorios.usuarios.permiso_repositorio import PermisoRepositorio

from repositorios.empleados.empleado_repositorio import EmpleadoRepositorio

# servicios
from servicios.usuarios.usuario_servicio import UsuarioServicio
from servicios.usuarios.permiso_servicio import PermisoServicio

from servicios.empleados.empleado_servicio import EmpleadoServicio



##################################
# importaciones de base de datos #
##################################


# instancias de los repositorios
usuario_repositorio = UsuarioRepositorio()
permisos_repositorio = PermisoRepositorio()
empleado_repositorio = EmpleadoRepositorio()



# instancia de los servicios
usuario_servicio = UsuarioServicio(usuario_repositorio)
permisos_servicio = PermisoServicio(permisos_repositorio)
empleado_servicio = EmpleadoServicio(empleado_repositorio)



ruta_del_icono = os.path.join(os.path.dirname(__file__), "recursos_graficos_y_logicos","recursos_de_imagenes", "Tela.ico")
icono_reloj_azul = os.path.join(os.path.dirname(__file__), "recursos_graficos_y_logicos","recursos_de_imagenes", "iconos_de_interfaz", "reloj_azul.png")
icono_reloj = os.path.join(os.path.dirname(__file__), "recursos_graficos_y_logicos","recursos_de_imagenes", "iconos_de_interfaz", "reloj.png")



mensajes_bienvenida = [
    "¡Bienvenido/a! Esperamos que tengas una excelente experiencia.",
    "Hola, nos alegra tenerte con nosotros. ¡Disfruta tu estancia!",
    "¡Hola! Qué gusto verte por aquí. ¿En qué podemos ayudarte hoy?",
    "Bienvenido/a a nuestra plataforma. Estamos aquí para servirte.",
    "¡Hola! Te damos la más cordial bienvenida. ¡Empecemos!",
    "Bienvenido/a de nuevo. Nos encanta verte por aquí.",
    "¡Hola! Qué bueno tenerte con nosotros. ¿Listo para comenzar?",
    "Bienvenido/a a la comunidad. Estamos felices de tenerte aquí.",
    "¡Hola! Tu aventura comienza ahora. ¡Bienvenido/a!",
    "Te damos la bienvenida. Esperamos que encuentres todo lo que necesitas.",
    "¡Hola! Gracias por unirte a nosotros. ¡Comencemos este viaje juntos!",
    "Bienvenido/a. Estamos aquí para hacer tu experiencia increíble.",
    "¡Hola! Nos alegra mucho verte. ¿En qué podemos asistirte hoy?",
    "Bienvenido/a a bordo. Prepárate para una experiencia única.",
    "¡Hola! Qué emoción tenerte aquí. ¡Bienvenido/a a la familia!",
    "Te damos la más cálida bienvenida. ¡Esperamos que disfrutes!",
    "¡Hola! Estamos encantados de tenerte con nosotros.",
    "Bienvenido/a. Tu viaje comienza ahora mismo. ¡Aprovecha al máximo!",
    "¡Hola! Nos llena de alegría recibirte. ¡Bienvenido/a!",
    "Bienvenido/a a tu nuevo espacio. Esperamos que te sientas como en casa."
]

def aplicar_sombra(widget, n_blurradio, n_opacidad):
        sombra = QGraphicsDropShadowEffect()
        sombra.setBlurRadius(n_blurradio)
        sombra.setOffset(2, 2)
        sombra.setColor(QColor(0, 0, 0, n_opacidad))
        widget.setGraphicsEffect(sombra) 

## Login del sistema
class Login(QWidget, Ui_Login):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Rutas de las imagenes
        self.logo_del_tela.setPixmap(QtGui.QPixmap(os.path.join(os.path.dirname(__file__), "recursos_graficos_y_logicos","recursos_de_imagenes", "Tela.png")))
        self.icono_usuario.setPixmap(QtGui.QPixmap(os.path.join(os.path.dirname(__file__), "recursos_graficos_y_logicos","recursos_de_imagenes", "iconos_de_interfaz", "icono_de_usuario.png")))
        self.icono_contrasena.setPixmap(QtGui.QPixmap(os.path.join(os.path.dirname(__file__), "recursos_graficos_y_logicos","recursos_de_imagenes", "iconos_de_interfaz", "icono_contraseña.png")))
        self.ojo_abierto = os.path.join(os.path.dirname(__file__), "recursos_graficos_y_logicos","recursos_de_imagenes", "iconos_de_interfaz","ver_contraseña.png")
        self.ojo_cerrado = os.path.join(os.path.dirname(__file__), "recursos_graficos_y_logicos","recursos_de_imagenes", "iconos_de_interfaz","no_ver_contraseña.png")

        aplicar_sombra(self.espacio_login, 50, 255)

        self.mensajes_usuario()
        
        self.input_usuario.setText("douglas345")
        self.input_contrasena.setText("1234")
        

        self.boton_ver_contrasena.clicked.connect(self.cambiar_ver_contrasena)

        # Estado inicial: contraseña oculta
        self.password_visible = False
        
    # metodo para cambiar el boton de ver contraseña
    def cambiar_ver_contrasena(self):
        if self.password_visible:
            # Ocultar la contraseña
            self.input_contrasena.setEchoMode(QLineEdit.Password)
            self.boton_ver_contrasena.setIcon(QIcon.fromTheme(self.ojo_cerrado))
            self.password_visible = False
        else:
            # Mostrar la contraseña
            self.input_contrasena.setEchoMode(QLineEdit.Normal)
            self.boton_ver_contrasena.setIcon(QIcon.fromTheme(self.ojo_abierto))
            self.password_visible = True
            
    def mensajes_usuario(self):
        self.label_mensaje_usuario.setText(random.choice(mensajes_bienvenida))
    

## Clase principal donde esta toda la apliacion ##
class MainWindow(QMainWindow, Ui_VentanaPrincipal):
    def __init__(self):
        super().__init__()
        
        self.setupUi(self)
        
        ## Colocamos el icono a la aplicacion ##
        self.setWindowTitle("T.E.L.A APP")
        self.setWindowIcon(QIcon(ruta_del_icono))
        
        #Eliminar las 2 primeras páginas
        self.remove_default_pages()
        
        self.setGeometry(0,0,700,650)
        # Establecer tamaño mínimo y máximo
        self.setMinimumSize(700, 650)  # Mínimo: 300x300 px
        #self.setMaximumSize(1080, 800)  # Máximo: 600x600 px

        ## Mostrar ventana emergente a traves de esta funcion ##
        ## Procurar activarlo al final ##
        #self.mostrar_advertencia()
        
        
        
        # Rutas relativas de la imagenes
        
        ## cintillo ##
        ## Rutas relativas de la imagenes ##
        self.logo_zona_educativa.setPixmap(QtGui.QPixmap(os.path.join(os.path.dirname(__file__), "recursos_graficos_y_logicos","recursos_de_imagenes", "logo_zona_educativa.png")))
        self.membrete.setPixmap(QtGui.QPixmap(os.path.join(os.path.dirname(__file__), "recursos_graficos_y_logicos","recursos_de_imagenes", "membrete.png")))
        self.logo_tela.setPixmap(QtGui.QPixmap(os.path.join(os.path.dirname(__file__), "recursos_graficos_y_logicos","recursos_de_imagenes", "Tela.png")))
        self.logo_juventud.setPixmap(QtGui.QPixmap(os.path.join(os.path.dirname(__file__), "recursos_graficos_y_logicos","recursos_de_imagenes", "logo_juventud.png")))

        
        self.botones_sidebar = (self.boton_principal, self.boton_estudiante, self.boton_personal, 
                                self.boton_cargar_catologo, self.boton_respaldo, self.boton_salir)
        
        self.pantallas_importantes = (3,8)
        
        
        

        # instancia del login y el cintillo
        #self.stacked_widget = QStackedWidget()
        self.login = Login()

        self.login.boton_ver_contrasena.setIcon(QIcon.fromTheme(self.login.ojo_cerrado))



        ## Instanacias de las primeras pantallas ##
        self.pantalla_bienvenida = PantallaBienvenidaUsuario(self.stacked_widget) # pantalla bienvenida al usuario / dashboard
        
        self.pantalla_vista_general_de_alumnos = PantallaDeVistaGeneralDeAlumnos(self.stacked_widget) # pantalla vista general de los alumnos
        self.pantalla_formulario_nuevo_registro_de_alumnos = PantallaDeFormularioNuevoRegistroAlumnos(self.stacked_widget) # pantalla del formulario para el nuevo registro de los alumnos
        self.pantalla_asistencia_alumnos = PantallaAsistenciaAlumnos(self.stacked_widget) # pantalla de asistencias de los alumnos
        self.pantalla_generar_informes_reportes_alumno = PantallaGenerarInformesReportesAlumnos(self.stacked_widget) # pantalla para generar los reportes de los alumnos
        self.pantalla_perfil_alumno = PantallaPerfilAlumno(self.stacked_widget) # pantalla para ver el perfil del alumno
        
        
        self.pantalla_vista_general_del_personal = PantallaDeVistaGeneralDelPersonal(self.stacked_widget) # pantalla vista general del personal
        self.pantalla_formulario_nuevo_registro_empleado = PantallaDeFormularioNuevoRegistroEmpleado(self.stacked_widget) # pantalla del formulario para el nuevo registro del personal
        self.pantalla_control_de_llegada = PantallaControlDeLlegada(self.stacked_widget) # pantalla de control de llegada del personal
        self.pantalla_control_de_reposos = PantallaControlRepososPersonal(self.stacked_widget) # pantalla para ver y registrar los reposos del personal/empleados
        self.pantalla_perfil_empleado = PantallaPerfilEmpleado(self.stacked_widget) # pantalla para ver el perfil del empleado

        
        self.pantalla_admin_crear_usuario = PantallaAdminCrearUsuario(self.stacked_widget) # pantalla del admin para crear usuario 
        self.pantalla_admin_crear_respaldo = PantallaAdminCrearRespaldo(self.stacked_widget) # pantalla del admin para crear respaldo
        self.pantalla_admin_insertar_catalogo = PantallaAdminInsertarCatalogo(self.stacked_widget)
        
        
        

        # Añadiendo las pantalla en el stackedwidget
        self.stacked_widget.addWidget(self.login) # indice 0
        
        self.stacked_widget.addWidget(self.pantalla_bienvenida)  # indice 1
        
        self.stacked_widget.addWidget(self.pantalla_vista_general_de_alumnos)  # indice 2
        self.stacked_widget.addWidget(self.pantalla_formulario_nuevo_registro_de_alumnos)  # indice 3
        self.stacked_widget.addWidget(self.pantalla_asistencia_alumnos) # indice 4
        self.stacked_widget.addWidget(self.pantalla_generar_informes_reportes_alumno) # indice 5
        self.stacked_widget.addWidget(self.pantalla_perfil_alumno) # indice 6
        
        self.stacked_widget.addWidget(self.pantalla_vista_general_del_personal)  # indice 7
        self.stacked_widget.addWidget(self.pantalla_formulario_nuevo_registro_empleado)  # indice 8
        self.stacked_widget.addWidget(self.pantalla_control_de_llegada)  # indice 9
        self.stacked_widget.addWidget(self.pantalla_control_de_reposos) # indice 10
        self.stacked_widget.addWidget(self.pantalla_perfil_empleado) # indice 11
        
        self.stacked_widget.addWidget(self.pantalla_admin_crear_usuario) # indice 12
        self.stacked_widget.addWidget(self.pantalla_admin_crear_respaldo) #indice 13
        self.stacked_widget.addWidget(self.pantalla_admin_insertar_catalogo) # indice 14
        
        # Los indices, al final hay que acomodarlos para que sean mas entendibles
        
        
        self.stacked_widget.setCurrentIndex(0)
    
        self.area_scroll_side_bar.hide()
        
        self.stacked_widget.currentChanged.connect(lambda indice_stackedwidget: FuncionSistema.bloquear_botones_sidebar(indice_stackedwidget, self.pantallas_importantes, self.botones_sidebar) if indice_stackedwidget > 0 else self.area_scroll_side_bar.hide())
        self.stacked_widget.currentChanged.connect(lambda indice_stackedwidget:  self.boton_principal.setChecked(True) if indice_stackedwidget == 1 else None)
        
        # Funciones para los botones del sidebar
        self.boton_menu.clicked.connect(lambda: FuncionSistema.cambiar_tamano_side_bar(self.area_scroll_side_bar))
        self.boton_principal.toggled.connect(lambda : FuncionSistema.moverse_de_pantalla(self.stacked_widget,1 ))
        self.boton_estudiante.toggled.connect(lambda : FuncionSistema.moverse_de_pantalla(self.stacked_widget,2 ))
        self.boton_personal.toggled.connect(lambda : FuncionSistema.moverse_de_pantalla(self.stacked_widget, 7 ))
        self.boton_respaldo.toggled.connect(lambda : FuncionSistema.moverse_de_pantalla(self.stacked_widget, 13) )
        self.boton_cargar_catologo.toggled.connect(lambda : FuncionSistema.moverse_de_pantalla(self.stacked_widget, 14) )
        self.boton_salir.clicked.connect(lambda : FuncionSistema.salir_al_login_con_sidebar(self.stacked_widget, self.area_scroll_side_bar))
        
        
        
        
        
        self.msg = QMessageBox()
        self.msg.setWindowTitle("Error de inicio de sesión")
        self.msg.setText("")
        # Usar un icono del sistema 
        self.msg.setIcon(QMessageBox.Warning)
        self.msg.setWindowIcon(QIcon(ruta_del_icono))

        # self.msg.exec_()

        self.login.boton_ingresar.clicked.connect(self.validar_credenciales)
        
        

   
    
      

    def validar_credenciales(self):
        nombre_usuario = self.login.input_usuario.text()
        contrasena_usuario = self.login.input_contrasena.text()

        try:
            
            global usuario_id_autenticado
            usuario_id_autenticado = usuario_servicio.autenticar_usuario(nombre_usuario, contrasena_usuario)


        except BaseDatosError as error:

            self.msg.setWindowTitle("Error de inicio de sesión")
            self.msg.setText(f"{error}")
            # Usar un icono del sistema (predeterminado de PyQt5)
            self.msg.setIcon(QMessageBox.Warning)

            self.msg.exec_()

            self.login.input_contrasena.clear()

        else:
            
            print("Usuario ID: ",usuario_id_autenticado)
            self.setMinimumSize(1200, 650)
            #self.showMaximized()

            if (usuario_id_autenticado):

                usuario = usuario_servicio.obtener_usuario_por_id(usuario_id_autenticado)
                
                app_configuracion.actualizar_usuario_id(usuario_id_autenticado)
                
                
            

                if usuario[5] == "DIRECTOR":
                    self.login.input_usuario.clear()
                    self.login.input_contrasena.clear()
                    self.stacked_widget.setCurrentIndex(1)
                    self.area_scroll_side_bar.show()
                    self.pantalla_bienvenida.label_titulo_del_segemeto_bienvenido.setText(f"Bienvenido {nombre_usuario} al sistema de información TELA-APP")


                elif usuario[5] == "SUB-DIRECTOR":

                    # eventos
                    
                    pass

                elif usuario[5] == "SECRETARIO":

                    self.login.input_usuario.clear() #limpia el input de nombre de usuario
                    self.login.input_contrasena.clear() #limpia el input de contraseña de usuario
                    self.stacked_widget.setCurrentIndex(1) # cambia de pantalla
                    self.area_scroll_side_bar.show()
                    
                    self.boton_cargar_catologo.hide()
                    
                    self.pantalla_bienvenida.label_titulo_del_segemeto_bienvenido.setText(f"Bienvenido {nombre_usuario}")
                    
                    


            crear_nuevo_empleado = permisos_servicio.verificar_permiso_usuario(usuario_id_autenticado,"CREAR EMPLEADOS")

            if not(crear_nuevo_empleado):
                self.pantalla_vista_general_del_personal.boton_crear_nuevo_registro.setDisabled(True)







        
    def remove_default_pages(self):
        """Elimina las 2 primeras páginas por defecto de Qt Designer"""
        # Verificar que existen al menos 2 páginas
        if self.stacked_widget.count() >= 2:
            # Eliminar página 1 (índice 0)
            page1 = self.stacked_widget.widget(0)
            self.stacked_widget.removeWidget(page1)
            if page1:
                page1.deleteLater()
            
            # Eliminar página 2 (índice 0 ahora, porque ya eliminamos la primera)
            page2 = self.stacked_widget.widget(0)
            self.stacked_widget.removeWidget(page2)
            if page2:
                page2.deleteLater()







    ## Metodo para mostrar advertencia de actualizar la fecha y hora ##
    def mostrar_advertencia(self):
        # Crear el QMessageBox

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)

        msg.setWindowTitle("Verificación de hora del sistema")
        msg.setText("Bienvenido al TELA-APP, esta es una versión de prueba, pueden haber errores, por favor tenga la hora de su dispositivo (su computadora) actualizada para que los registros no tengan errores")


        
        msg.setIconPixmap(QPixmap(icono_reloj))
        msg.setWindowIcon(QIcon(icono_reloj))



        # Añadir botón OK
        msg.setStandardButtons(QMessageBox.Ok)

        # Mostrar el messagebox
        msg.exec_()





# Ejecutar la aplicación
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.showMaximized()

    sys.exit(app.exec_())
