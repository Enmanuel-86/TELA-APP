import os
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QLineEdit, QPushButton,
                             QFileDialog, QMessageBox, QProgressBar)
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.uic import compileUi


class UiConverterThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(bool, str)

    def __init__(self, input_file, output_file):
        super().__init__()
        self.input_file = input_file
        self.output_file = output_file

    def run(self):
        try:
            with open(self.output_file, 'w', encoding='utf-8') as f:
                compileUi(self.input_file, f)
            self.progress.emit(100)
            self.finished.emit(True, "Conversión completada con éxito!")
        except Exception as e:
            self.finished.emit(False, f"Error: {str(e)}")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Conversor UI a PY - Qt Designer")
        self.setGeometry(100, 100, 500, 200)

        self.init_ui()
        self.converter_thread = None

    def init_ui(self):
        # Widget principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Sección de archivo de entrada (.ui)
        input_layout = QHBoxLayout()
        self.input_label = QLabel("Archivo UI:")
        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText("Selecciona un archivo .ui")
        self.input_btn = QPushButton("Examinar...")
        self.input_btn.clicked.connect(self.browse_ui_file)

        input_layout.addWidget(self.input_label)
        input_layout.addWidget(self.input_line)
        input_layout.addWidget(self.input_btn)

        # Sección de archivo de salida (.py)
        output_layout = QHBoxLayout()
        self.output_label = QLabel("Archivo PY:")
        self.output_line = QLineEdit()
        self.output_line.setPlaceholderText("Selecciona destino para el archivo .py")
        self.output_btn = QPushButton("Examinar...")
        self.output_btn.clicked.connect(self.browse_py_file)

        output_layout.addWidget(self.output_label)
        output_layout.addWidget(self.output_line)
        output_layout.addWidget(self.output_btn)

        # Barra de progreso
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)

        # Botón de conversión
        self.convert_btn = QPushButton("Convertir")
        self.convert_btn.clicked.connect(self.convert_ui)

        # Agregar widgets al layout principal
        main_layout.addLayout(input_layout)
        main_layout.addLayout(output_layout)
        main_layout.addWidget(self.progress_bar)
        main_layout.addWidget(self.convert_btn)

    def browse_ui_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar archivo UI", "", "Qt Designer Files (*.ui)"
        )
        if file_path:
            self.input_line.setText(file_path)
            # Sugerir nombre para el archivo .py
            py_file = os.path.splitext(file_path)[0] + ".py"
            self.output_line.setText(py_file)

    def browse_py_file(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Guardar archivo PY", "", "Python Files (*.py)"
        )
        if file_path:
            self.output_line.setText(file_path)

    def convert_ui(self):
        input_file = self.input_line.text()
        output_file = self.output_line.text()

        if not input_file or not output_file:
            QMessageBox.warning(self, "Advertencia", "Debes seleccionar ambos archivos!")
            return

        if not input_file.endswith('.ui'):
            QMessageBox.warning(self, "Advertencia", "El archivo de entrada debe ser .ui!")
            return

        if not output_file.endswith('.py'):
            QMessageBox.warning(self, "Advertencia", "El archivo de salida debe ser .py!")
            return

        # Deshabilitar botones durante la conversión
        self.input_btn.setEnabled(False)
        self.output_btn.setEnabled(False)
        self.convert_btn.setEnabled(False)
        self.progress_bar.setValue(0)

        # Crear y ejecutar hilo de conversión
        self.converter_thread = UiConverterThread(input_file, output_file)
        self.converter_thread.progress.connect(self.update_progress)
        self.converter_thread.finished.connect(self.conversion_finished)
        self.converter_thread.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def conversion_finished(self, success, message):
        # Habilitar botones nuevamente
        self.input_btn.setEnabled(True)
        self.output_btn.setEnabled(True)
        self.convert_btn.setEnabled(True)

        # Mostrar mensaje
        if success:
            QMessageBox.information(self, "Éxito", message)
        else:
            QMessageBox.critical(self, "Error", message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())