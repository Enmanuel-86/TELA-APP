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
            # Primero compila el .ui en memoria
            from io import StringIO
            buffer = StringIO()
            compileUi(self.input_file, buffer)
            content = buffer.getvalue()

            # Quitar la línea con la ruta absoluta
            lines = content.splitlines()
            cleaned_lines = []
            for line in lines:
                if "reading ui file" in line:  # detecta la línea con la ruta
                    continue
                cleaned_lines.append(line)

            # Guardar el resultado sin la ruta
            with open(self.output_file, "w", encoding="utf-8") as f:
                f.write("\n".join(cleaned_lines))

            self.progress.emit(100)
            self.finished.emit(True, "Conversión completada con éxito!")
        except Exception as e:
            self.finished.emit(False, f"Error: {str(e)}")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Conversor UI a PY - Qt Designer")
        self.setGeometry(100, 100, 500, 220)  # Aumenté la altura para el nuevo label

        self.init_ui()
        self.converter_thread = None
        self.output_folder = ""

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

        # Sección de carpeta de salida
        output_layout = QHBoxLayout()
        self.output_label = QLabel("Carpeta PY:")
        self.output_line = QLineEdit()
        self.output_line.setPlaceholderText("Selecciona carpeta para guardar .py")
        self.output_btn = QPushButton("Examinar...")
        self.output_btn.clicked.connect(self.browse_output_folder)

        output_layout.addWidget(self.output_label)
        output_layout.addWidget(self.output_line)
        output_layout.addWidget(self.output_btn)

        # Label para mostrar el nombre del archivo de salida
        self.filename_label = QLabel("Nombre del archivo: ")
        self.filename_label.setStyleSheet("font-weight: bold; color: #2c3e50;")

        # Barra de progreso
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)

        # Botón de conversión
        self.convert_btn = QPushButton("Convertir")
        self.convert_btn.clicked.connect(self.convert_ui)

        # Agregar widgets al layout principal
        main_layout.addLayout(input_layout)
        main_layout.addLayout(output_layout)
        main_layout.addWidget(self.filename_label)
        main_layout.addWidget(self.progress_bar)
        main_layout.addWidget(self.convert_btn)

    def browse_ui_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar archivo UI", "", "Qt Designer Files (*.ui)"
        )
        if file_path:
            self.input_line.setText(file_path)
            self.update_filename_display()

    def browse_output_folder(self):
        folder_path = QFileDialog.getExistingDirectory(
            self, "Seleccionar carpeta de destino"
        )
        if folder_path:
            self.output_folder = folder_path
            self.output_line.setText(folder_path)
            self.update_filename_display()

    def update_filename_display(self):
        """Actualiza el label con el nombre del archivo de salida que se generará"""
        input_file = self.input_line.text()
        output_folder = self.output_line.text()

        if input_file and output_folder:
            base_name = os.path.splitext(os.path.basename(input_file))[0]
            output_filename = f"{base_name}_gui.py"
            self.filename_label.setText(f"Nombre del archivo: {output_filename}")
        else:
            self.filename_label.setText("Nombre del archivo: ")

    def convert_ui(self):
        input_file = self.input_line.text()
        output_folder = self.output_line.text()

        if not input_file:
            QMessageBox.warning(self, "Advertencia", "Debes seleccionar un archivo .ui!")
            return

        if not output_folder:
            QMessageBox.warning(self, "Advertencia", "Debes seleccionar una carpeta de destino!")
            return

        if not input_file.endswith('.ui'):
            QMessageBox.warning(self, "Advertencia", "El archivo de entrada debe ser .ui!")
            return

        # Generar nombre del archivo de salida
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        output_file = os.path.join(output_folder, f"{base_name}_gui.py")

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