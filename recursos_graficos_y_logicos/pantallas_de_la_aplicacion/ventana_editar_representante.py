from PyQt5.QtWidgets import (QWidget, QMessageBox, QApplication, QListWidget, QListWidgetItem, 
                            QLabel, QHBoxLayout, QPushButton, QHeaderView )
from PyQt5.QtCore import (QTime, QPoint, Qt, QDate, QSize)
from PyQt5 import QtGui, QtCore
import os
from ..elementos_graficos_a_py import  Ui_VentanaEditarRepresentante
from ..utilidades.funciones_sistema import FuncionSistema


class VentanaEditarRepresentante(QWidget, Ui_VentanaEditarRepresentante):
    def __init__(self):
        super().__init__()
        
        self.setupUi(self)
        