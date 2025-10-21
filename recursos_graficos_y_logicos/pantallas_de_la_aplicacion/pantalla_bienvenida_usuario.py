from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton)

from ..elementos_graficos_a_py import  Ui_PantallaBienvenidaUsuario
from datetime import datetime, time

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

class PantallaBienvenidaUsuario(QWidget, Ui_PantallaBienvenidaUsuario):
    def __init__(self, stacked_widget):
        super().__init__()

        self.stacked_widget = stacked_widget
        self.setupUi(self)
        
    