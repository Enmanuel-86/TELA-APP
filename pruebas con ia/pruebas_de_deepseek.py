from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit,
    QListWidget, QListWidgetItem, QPushButton, QLabel
)
from PyQt5.QtCore import Qt, QPoint
import sys

class BusquedaDinamica(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Buscar por cédula o nombre")
        self.resize(400, 300)

        # Lista de datos como tuplas: (id, cedula, nombre)
        self.datos = [
            (1, "12345678", "Juan Pérez"),
            (2, "23456789", "Ana Torres"),
            (3, "34567890", "Luis Gómez"),
            (4, "45678901", "María Fernández"),
            (5, "56789012", "Carlos Ramírez"),
            (6, "67890123", "Lucía Ortega"),
            (7, "78901234", "Pedro Martínez"),
            (8, "89012345", "Julia Sánchez"),
            (9, "90123456", "Rafael Peña"),
            (10, "01234567", "Andrea Blanco"),
        ]

        # Layout principal
        self.layout = QVBoxLayout(self)

        self.buscador = QLineEdit()
        self.buscador.setPlaceholderText("Buscar por cédula o nombre...")
        self.buscador.textChanged.connect(self.filtrar_resultados)

        self.boton_buscar = QPushButton("Buscar")
        self.boton_buscar.clicked.connect(self.buscar_persona)

        self.etiqueta_resultado = QLabel("")
        self.etiqueta_resultado.setStyleSheet("font-weight: bold; color: green")

        self.layout.addWidget(self.buscador)
        self.layout.addWidget(self.boton_buscar)
        self.layout.addWidget(self.etiqueta_resultado)

        # Lista de coincidencias
        self.resultados = QListWidget(self)
        self.resultados.setFocusPolicy(Qt.NoFocus)
        self.resultados.setMouseTracking(True)
        self.resultados.setStyleSheet("background-color: white; border: 1px solid gray;")
        self.resultados.itemClicked.connect(self.seleccionar_item)
        self.resultados.hide()

    def filtrar_resultados(self, texto):
        texto = texto.strip().lower()
        self.resultados.clear()

        if not texto:
            self.resultados.hide()
            return

        coincidencias = [
            persona for persona in self.datos
            if texto in persona[1] or texto in persona[2].lower()
        ]

        if not coincidencias:
            self.resultados.hide()
            return

        for persona in coincidencias:
            item = f'{persona[1]} - {persona[2]}'
            self.resultados.addItem(QListWidgetItem(item))

        # Ocultar si hay una coincidencia exacta por cédula
        if len(coincidencias) == 1 and coincidencias[0][1] == texto:
            self.resultados.hide()
        else:
            self.mostrar_lista()

    def mostrar_lista(self):
        pos = self.buscador.mapTo(self, QPoint(0, self.buscador.height()))
        self.resultados.move(pos)
        self.resultados.resize(self.buscador.width(), 100)
        self.resultados.show()

    def seleccionar_item(self, item):
        cedula = item.text().split(" - ")[0]
        self.buscador.setText(cedula)
        self.resultados.hide()

    def buscar_persona(self):
        texto = self.buscador.text().strip().lower()
        persona = next(
            (p for p in self.datos if texto == p[1] or texto == p[2].lower()),
            None
        )

        if persona:
            self.etiqueta_resultado.setText(f"Nombre: {persona[2]}")
        else:
            self.etiqueta_resultado.setText("Persona no encontrada")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = BusquedaDinamica()
    ventana.show()
    sys.exit(app.exec_())
