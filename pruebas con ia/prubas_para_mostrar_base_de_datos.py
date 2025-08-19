import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QVBoxLayout, QWidget, QPushButton, QLineEdit, QLabel, \
    QHBoxLayout
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtCore import Qt


class VentanaPersonal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lista de Personal")
        self.setGeometry(100, 100, 600, 400)

        # Crear la base de datos y agregar datos
        self.crear_base_datos()

        # Conectar la base de datos
        self.conectar_base_datos()

        # Crear y configurar la tabla
        self.tabla = QTableView(self)
        self.modelo = QSqlTableModel()
        self.modelo.setTable("personal")  # Nombre de la tabla en la BD
        self.modelo.select()  # Cargar los datos
        self.tabla.setModel(self.modelo)

        # Ocultar la columna ID
        self.tabla.setColumnHidden(0, True)

        # Crear widgets para agregar y eliminar personas
        self.nombre_input = QLineEdit(self)
        self.apellido_input = QLineEdit(self)
        self.cedula_input = QLineEdit(self)
        self.cargo_input = QLineEdit(self)
        self.agregar_button = QPushButton("Agregar Persona", self)
        self.borrar_button = QPushButton("Borrar Persona", self)
        self.id_borrar_input = QLineEdit(self)
        self.id_borrar_input.setPlaceholderText("ID de la persona a borrar")

        # Conectar botones a funciones
        self.agregar_button.clicked.connect(self.agregar_persona)
        self.borrar_button.clicked.connect(self.borrar_persona)

        # Layout para los inputs
        form_layout = QVBoxLayout()
        form_layout.addWidget(QLabel("Nombre"))
        form_layout.addWidget(self.nombre_input)
        form_layout.addWidget(QLabel("Apellido"))
        form_layout.addWidget(self.apellido_input)
        form_layout.addWidget(QLabel("Cédula"))
        form_layout.addWidget(self.cedula_input)
        form_layout.addWidget(QLabel("Cargo"))
        form_layout.addWidget(self.cargo_input)
        form_layout.addWidget(self.agregar_button)

        # Layout para el botón de borrar
        borrar_layout = QHBoxLayout()
        borrar_layout.addWidget(self.id_borrar_input)
        borrar_layout.addWidget(self.borrar_button)

        # Layout general
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabla)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(borrar_layout)

        # Configurar el contenedor central
        contenedor = QWidget()
        contenedor.setLayout(main_layout)
        self.setCentralWidget(contenedor)

    def crear_base_datos(self):
        """Crea la base de datos SQLite y agrega datos de ejemplo si no existen"""
        conexion = sqlite3.connect("empresa.db")
        cursor = conexion.cursor()

        # Crear la tabla si no existe
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS personal (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                cedula TEXT NOT NULL,
                cargo TEXT NOT NULL
            )
        """)

        # Verificar si la tabla ya tiene datos
        cursor.execute("SELECT COUNT(*) FROM personal")
        if cursor.fetchone()[0] == 0:
            # Insertar datos de ejemplo
            cursor.executemany("""
                INSERT INTO personal (nombre, apellido, cedula, cargo) VALUES (?, ?, ?, ?)
            """, [
                ("Juan", "Pérez", "12345678", "Gerente"),
                ("Ana", "Gómez", "87654321", "Secretaria"),
                ("Carlos", "López", "56781234", "Ingeniero"),
                ("Marta", "Fernández", "23456789", "Contadora"),
                ("Luis", "Ramírez", "34567890", "Supervisor")
            ])
            conexion.commit()

        conexion.close()

    def conectar_base_datos(self):
        """Conectar SQLite con PyQt5"""
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("empresa.db")
        if not db.open():
            print("Error: No se pudo conectar a la base de datos")

    def agregar_persona(self):
        """Agregar persona a la base de datos"""
        nombre = self.nombre_input.text()
        apellido = self.apellido_input.text()
        cedula = self.cedula_input.text()
        cargo = self.cargo_input.text()

        if nombre and apellido and cedula and cargo:
            conexion = sqlite3.connect("empresa.db")
            cursor = conexion.cursor()
            cursor.execute("""
                INSERT INTO personal (nombre, apellido, cedula, cargo) 
                VALUES (?, ?, ?, ?)
            """, (nombre, apellido, cedula, cargo))
            conexion.commit()
            conexion.close()

            # Actualizar la tabla
            self.modelo.select()

            # Limpiar los campos de entrada
            self.nombre_input.clear()
            self.apellido_input.clear()
            self.cedula_input.clear()
            self.cargo_input.clear()
        else:
            print("Por favor, complete todos los campos.")

    def borrar_persona(self):
        """Eliminar persona de la base de datos por ID"""
        id_borrar = self.id_borrar_input.text()

        if id_borrar:
            conexion = sqlite3.connect("empresa.db")
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM personal WHERE id = ?", (id_borrar,))
            conexion.commit()
            conexion.close()

            # Actualizar la tabla
            self.modelo.select()

            # Limpiar el campo de ID de borrar
            self.id_borrar_input.clear()
        else:
            print("Por favor, ingrese un ID válido.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPersonal()
    ventana.show()
    sys.exit(app.exec_())
