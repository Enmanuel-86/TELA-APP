from PyQt5.QtCore import Qt,QPoint, QSortFilterProxyModel
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import (QWidget, QHeaderView,  QVBoxLayout, 
                             QPushButton , QHBoxLayout,QMessageBox, QListWidget, QListWidgetItem, QLabel, QApplication)
from PyQt5 import QtGui, QtCore
from configuraciones.configuracion import app_configuracion
from ..elementos_graficos_a_py import Ui_VistaGeneralAuditorias
from ..utilidades.base_de_datos import especialidad_servicio
from ..utilidades.funciones_sistema import FuncionSistema

class PantallaDeVistaGeneralAuditorias(QWidget, Ui_VistaGeneralAuditorias):
    def __init__(self, stacked_widget):
        super().__init__()

        self.stacked_widget = stacked_widget
        self.setupUi(self)
        
        self.boton_de_regreso.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(12))
        