from PyQt5.QtGui import QIcon
from PyQt5 import QtGui
import os
from datetime import datetime
from PyQt5.QtWidgets import (QWidget, QCalendarWidget, QMessageBox,
                            QApplication)

from ..elementos_graficos_a_py import Ui_VistaGeneralReposoEmpleados, Ui_VentanaAnadirReposo




class PantallaControlRepososPersonal(QWidget, Ui_VistaGeneralReposoEmpleados):
    def __init__(self, stacked_widget):
        super().__init__()


        self.stacked_widget = stacked_widget
        
        self.setupUi(self)
        
        