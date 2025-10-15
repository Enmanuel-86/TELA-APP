import sys
from PySide2.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QComboBox, QLabel, QPushButton
)
from crear_grafico_estadistico import GraficoEstadistico


class VentanaPrincipal(QMainWindow):
    
    """
        Este archivo no se usa para nada, solo para recordar la sintaxis de como usar las funciones del grafico
    
    
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gráfico Estadístico Interactivo")
        self.setGeometry(200, 200, 700, 500)

        contenedor = QWidget()
        layout = QVBoxLayout(contenedor)
        self.setCentralWidget(contenedor)

        # ====== SELECTOR DE GRÁFICO ======
        self.selector_tipo = QComboBox()
        self.selector_tipo.addItems(["Torta", "Torres", "Líneas"])
        layout.addWidget(QLabel("Selecciona el tipo de gráfico:"))
        layout.addWidget(self.selector_tipo)

        # ====== GRÁFICO ======
        self.grafico = GraficoEstadistico()
        layout.addWidget(self.grafico)

        # ====== BOTONES ======
        btn_agregar = QPushButton("Agregar datos")
        btn_limpiar = QPushButton("Limpiar gráfico")
        layout.addWidget(btn_agregar)
        layout.addWidget(btn_limpiar)

        # ====== DATOS BASE ======
        self.contenido = [
            ("Alumnos", "#12f234", 20),
            ("Alumnas", "#276389", 30),
            ("Profesores", "#f2b134", 15),
        ]
        self.grafico.crear_grafico(self.contenido, tipo_grafico="torta")

        # ====== CONEXIONES ======
        self.selector_tipo.currentIndexChanged.connect(self.actualizar_tipo)
        btn_agregar.clicked.connect(self.agregar_datos)
        btn_limpiar.clicked.connect(self.grafico.limpiar_grafico)

    # ====== MÉTODOS ======
    def actualizar_tipo(self):
        tipo = self.selector_tipo.currentText().lower()
        self.grafico.crear_grafico(self.contenido, tipo_grafico=tipo)

    def agregar_datos(self):
        """Ejemplo de datos nuevos"""
        nuevos = [
            ("Personal", "#d9534f", 8),
            ("Visitantes", "#5bc0de", 5)
        ]
        tipo = self.selector_tipo.currentText().lower()
        self.grafico.agregar_datos(nuevos, tipo_grafico=tipo)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())
