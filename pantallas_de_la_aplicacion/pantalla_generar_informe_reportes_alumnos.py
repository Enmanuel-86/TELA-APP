from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import  QWidget, QDockWidget
from PyQt5 import QtGui, Qt
import os
from elementos_graficos_a_py import Ui_PantallaGenerarInformesReportesAlumnos




class PantallaGenerarInformesReportesAlumnos(QWidget, Ui_PantallaGenerarInformesReportesAlumnos):
    def __init__(self, stacked_widget):
        super().__init__()

        self.stacked_widget = stacked_widget
        self.setupUi(self)