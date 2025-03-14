import sys
import mysql.connector
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox


class AuthApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Авторизация")
        self.setGeometry(100, 100, 300, 200)

        self.db = self.connect_db()
        self.create_tables()
        self.init_ui()

    def connect_db(self):
        try:
            return mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="kuzn",
                port=3306
            )
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Ошибка БД", f"Ошибка подключения: {e}")
            sys.exit()

    def create_tables(self):
        cursor = self.db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL
            )
        """)
        self.db.commit()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel("Логин:")
        self.username_input = QLineEdit()
        self.password_label = QLabel("Пароль:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_button = QPushButton("Войти")
        self.login_button.clicked.connect(self.login)

        self.register_button = QPushButton("Регистрация")
        self.register_button.clicked.connect(self.register)

        layout.addWidget(self.label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()

        if user:
            QMessageBox.information(self, "Успех", "Вы успешно вошли!")
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()

        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))

        if cursor.fetchone():
            QMessageBox.warning(self, "Ошибка", "Пользователь уже существует")
            return

        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        self.db.commit()
        QMessageBox.information(self, "Успех", "Вы успешно зарегистрировались!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AuthApp()
    window.show()
    sys.exit(app.exec())
