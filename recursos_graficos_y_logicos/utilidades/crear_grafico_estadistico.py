# crear_grafico_estadistico.py
from PySide2.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class GraficoEstadistico(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.figure = Figure(figsize=(5, 3))
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)
        self.contenido_actual = []  # guarda los datos actuales

    def crear_grafico(self, contenido_grafico, tipo_grafico="torta"):
        """Crea el gráfico según el tipo."""
        self.contenido_actual = contenido_grafico  # guarda los datos

        self.figure.clear()
        ax = self.figure.add_subplot(111)

        etiquetas = [item[0] for item in contenido_grafico]
        colores = [item[1] for item in contenido_grafico]
        valores = [item[2] for item in contenido_grafico]

        if tipo_grafico == "torta":
            ax.pie(valores, labels=etiquetas, colors=colores,
                   autopct=lambda p: f'{int(p * sum(valores) / 100)}', startangle=90)
            ax.set_title("Gráfico tipo torta")

        elif tipo_grafico == "torres":
            ax.bar(etiquetas, valores, color=colores)
            ax.set_title("Gráfico de barras")

        elif tipo_grafico == "líneas" or tipo_grafico == "linhas":
            ax.plot(etiquetas, valores, marker="o", color="blue")
            ax.set_title("Gráfico de líneas")

        self.canvas.draw()

    def limpiar_grafico(self):
        """Limpia el gráfico actual."""
        self.figure.clear()
        self.canvas.draw()
        self.contenido_actual = []

    def agregar_datos(self, nuevos_datos, tipo_grafico="torta"):
        """Agrega más datos al gráfico actual."""
        self.contenido_actual.extend(nuevos_datos)
        self.crear_grafico(self.contenido_actual, tipo_grafico)
