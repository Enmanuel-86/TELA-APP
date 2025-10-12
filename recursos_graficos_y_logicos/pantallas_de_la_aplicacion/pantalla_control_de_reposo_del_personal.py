from PySide2.QtGui import QIcon
from PySide2 import QtGui
import os
from datetime import datetime
from PySide2.QtWidgets import (QWidget, QCalendarWidget, QMessageBox,
                            QApplication)

from ..elementos_graficos_a_py import Ui_PantallaControlReposoPersonal, Ui_VentanaAnadirReposo




class PantallaControlRepososPersonal(QWidget, Ui_PantallaControlReposoPersonal):
    def __init__(self, stacked_widget):
        super().__init__()


        self.stacked_widget = stacked_widget
        
        self.setupUi(self)
        
        
        # Rutas relativas de las imagenes
        self.boton_de_regreso.setIcon(QIcon.fromTheme(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "iconos_de_interfaz", "flecha_izquierda_2.png")))
        self.boton_buscar.setIcon(QIcon.fromTheme(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "iconos_de_interfaz","lupa_blanca.png")))
        self.boton_anadir_reposo.setIcon(QIcon.fromTheme(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "iconos_de_interfaz", "control_de_reposos.png")))


        self.ventana_anadir_reposo = VentanaAnadirRepososPersonal()
        
        
        self.boton_de_regreso.clicked.connect(self.volver_vista_general_personal)
        self.boton_anadir_reposo.clicked.connect(self.anadir_reposo)
    
    
    
    def anadir_reposo(self):
        
        self.ventana_anadir_reposo.show()
        
    
    
    
    # Metodo para regresar a la pantalla anterior
    def volver_vista_general_personal(self):
        
        self.stacked_widget.setCurrentIndex(2)
        
        
        
        
        
        
        
        
class VentanaAnadirRepososPersonal(QWidget, Ui_VentanaAnadirReposo):
    def __init__(self):
        super().__init__()
        
        self.setupUi(self)
        
        
        self.setWindowTitle("Añada el reposo del empleado")
        
        
        # Inicialización de variables 
        self.calendario = None  # Usa 'calendario' en todo el código
        self.current_label = None

        
        
        # Rutas relativas de las imagenes
        self.boton_para_agregar_fecha.setIcon(QIcon.fromTheme(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "iconos_de_interfaz", "calendario.png")))
        self.boton_para_agregar_fecha_2.setIcon(QIcon.fromTheme(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "iconos_de_interfaz", "calendario.png")))

        
        
        self.boton_para_agregar_fecha.clicked.connect(lambda: self.mostrar_calendario(self.label_mostrar_fecha_solicitud))
        self.boton_para_agregar_fecha_2.clicked.connect(lambda: self.mostrar_calendario(self.label_mostrar_fecha_reingreso))
        self.boton_anadir_reposo.clicked.connect(self.anadir_reposo)
        
        
        
    def anadir_reposo(self):
        
        QMessageBox.information(self, "Aviso", "El reposo del empleado se a añadido correctamente") 
        
    
    # Metodo que se ejecuta cuando le das a la X de la ventana
    def closeEvent(self, event):
        
        
        event.accept()  # Aceptamos el evento de cierre
        
        
    ## Metodo para mostrar el calendario ##
    def mostrar_calendario(self, label_destino):
        
        ## Metodo para colocar la fecha a un label  ##
        def seleccionar_fecha(date):
            """Actualiza el label con la fecha seleccionada y cierra el calendario."""
            if self.current_label:
                fecha_formateada = date.toString("yyyy-MM-dd")
                fecha_date = datetime.strptime(fecha_formateada, "%Y-%m-%d").date()
                self.current_label.setText(f"{fecha_date}")
                #print(type(fecha_date))
                self.calendario.close()  # Cerrar el calendario 


        
        """Muestra el calendario y asigna el label objetivo."""
        if not self.calendario:
            # Crear el calendario solo una vez
            self.calendario = QCalendarWidget(self)
            self.calendario.setGridVisible(True)
            self.calendario.clicked.connect(seleccionar_fecha)
            self.calendario.setWindowTitle("Seleccione una fecha")
            self.calendario.setFixedSize(400, 300)

        self.current_label = label_destino  # Guardar el label a actualizar
        self.calendario.move(
            (self.width() - self.calendario.width()) // 2,
            (self.height() - self.calendario.height()) // 2
        )
        self.calendario.show()
