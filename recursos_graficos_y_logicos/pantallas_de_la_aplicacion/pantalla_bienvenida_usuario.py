from PyQt5.QtWidgets import (QWidget, QPushButton, 
                             QVBoxLayout, QMessageBox)
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices
import os
from ..elementos_graficos_a_py import  Ui_PantallaBienvenidaUsuario
from datetime import datetime, time

class PantallaBienvenidaUsuario(QWidget, Ui_PantallaBienvenidaUsuario):
    def __init__(self, stacked_widget):
        super().__init__()

        self.stacked_widget = stacked_widget
        self.setupUi(self)
        
        self.pushButton.clicked.connect(self.abrir_manual_de_usuario)
        
    def abrir_manual_de_usuario(self):
        """
            Este metodo sirve para abrir el manual de usuario
        """
        
        pdf_path = r'recursos_graficos_y_logicos/utilidades/MANUAL DE USUARIO PARA EL USO DEL TELA-APP.pdf'  # Cambia esta ruta
        
        if os.path.exists(pdf_path):
            # Abre el PDF con la aplicación predeterminada del sistema
            QDesktopServices.openUrl(QUrl.fromLocalFile(pdf_path))
        else:
            QMessageBox.warning(self, 'Error', 
                              f'No se encontró el archivo:\n{pdf_path}')
        
        
    