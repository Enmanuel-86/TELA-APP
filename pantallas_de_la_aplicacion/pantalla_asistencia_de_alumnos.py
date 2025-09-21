from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import  QWidget, QDockWidget
from PyQt5 import QtGui, Qt
import os
from elementos_graficos_a_py import Ui_PantallaAsistenciaAlumnos




class PantallaAsistenciaAlumnos(QWidget, Ui_PantallaAsistenciaAlumnos):
    def __init__(self, stacked_widget):
        super().__init__()

        self.stacked_widget = stacked_widget
        self.setupUi(self)