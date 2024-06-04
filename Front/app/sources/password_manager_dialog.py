from PySide6.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PySide6.QtCore import Qt
import random
import string
import requests


class PasswordManagerDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestionnaire de mots de passe")
        self.setFixedSize(400, 300)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.account_label = QLabel("Compte")
        self.account_entry = QLineEdit()
        self.account_entry.setPlaceholderText("Nom du compte")
        layout.addWidget(self.account_label)
        layout.addWidget(self.account_entry)

        self.password_label = QLabel("Mot de passe")
        self.password_entry = QLineEdit()
        self.password_entry.setPlaceholderText("Mot de passe généré")
        self.password_entry.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_entry)

        self.generate_button = QPushButton("Générer")
        self.generate_button.clicked.connect(self.generate_password)
        layout.addWidget(self.generate_button)

        self.save_button = QPushButton("Enregistrer")
        self.save_button.clicked.connect(self.save_password)
        layout.addWidget(self.save_button)

        self.setLayout(layout)
        self.load_styles()

    def load_styles(self):
        try:
            with open("styles/password_manager.qss", "r") as file:
                self.setStyleSheet(file.read())
        except FileNotFoundError:
            print("Stylesheet file not found.")

    def generate_password(self):
        length = 12
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(length))
        self.password_entry.setText(password)

    def save_password(self):
        account = self.account_entry.text()
        password = self.password_entry.text()
        if not account or not password:
            QMessageBox.critical(
                self, "Erreur", "Veuillez remplir tous les champs.")
        else:
            api_url = "https://your-api-url.com/api/save_password"
            data = {
                "account": account,
                "password": password
            }
            try:
                response = requests.post(api_url, json=data)
                response.raise_for_status()
                if response.status_code == 200:
                    QMessageBox.information(
                        self, "Succès", "Mot de passe enregistré avec succès.")
                    self.accept()
                else:
                    QMessageBox.critical(
                        self, "Erreur", f"Échec de l'enregistrement du mot de passe. Code de statut: {response.status_code}")
            except requests.RequestException as e:
                QMessageBox.critical(
                    self, "Erreur", f"Une erreur est survenue : {e}")
