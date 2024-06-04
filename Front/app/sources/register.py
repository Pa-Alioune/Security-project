import re
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
import requests
import os
import sys

token = ""

# Ajouter le chemin du dossier 'app' au sys.path
app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if app_path not in sys.path:
    sys.path.append(app_path)

# Importer la fonction generate_captcha
from utils.captcha_generator import generate_captcha

class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Inscription - SecurePwd")
        self.setGeometry(100, 100, 800, 600)
        self.load_styles()
        self.showMaximized()

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        # Création de la card pour le formulaire
        form_frame = QFrame()
        form_frame.setObjectName("formFrame")
        form_layout = QVBoxLayout(form_frame)
        form_layout.setAlignment(Qt.AlignCenter)
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setSpacing(10)

        title_label = QLabel("Inscription")
        title_label.setObjectName("registerTitleLabel")
        title_label.setAlignment(Qt.AlignCenter)
        form_layout.addWidget(title_label)

        self.first_name_entry = QLineEdit()
        self.first_name_entry.setPlaceholderText("Prénom")
        form_layout.addWidget(self.first_name_entry)

        self.last_name_entry = QLineEdit()
        self.last_name_entry.setPlaceholderText("Nom")
        form_layout.addWidget(self.last_name_entry)

        self.email_entry = QLineEdit()
        self.email_entry.setPlaceholderText("Adresse e-mail")
        form_layout.addWidget(self.email_entry)

        self.password_entry = QLineEdit()
        self.password_entry.setPlaceholderText("Mot de passe")
        self.password_entry.setEchoMode(QLineEdit.Password)
        form_layout.addWidget(self.password_entry)

        self.confirm_password_entry = QLineEdit()
        self.confirm_password_entry.setPlaceholderText(
            "Confirmer le mot de passe")
        self.confirm_password_entry.setEchoMode(QLineEdit.Password)
        form_layout.addWidget(self.confirm_password_entry)

        # Ajouter le captcha
        captcha_layout = QHBoxLayout()
        captcha_layout.setAlignment(Qt.AlignCenter)
        captcha_layout.setSpacing(10)

        self.captcha_label = QLabel(self)
        self.captcha_label.setAlignment(Qt.AlignCenter)
        # Réduire la taille du captcha
        self.captcha_label.setFixedSize(150, 50)
        self.captcha_label.mousePressEvent = self.refresh_captcha  # Reload captcha on click
        self.captcha_image, self.captcha_text = generate_captcha()
        self.captcha_label.setPixmap(QPixmap.fromImage(
            self.captcha_image).scaled(150, 50, Qt.KeepAspectRatio))
        captcha_layout.addWidget(self.captcha_label)

        self.captcha_entry = QLineEdit()
        self.captcha_entry.setPlaceholderText("Entrez le captcha")
        # Fixer la largeur du champ de texte pour qu'il corresponde à l'image du captcha
        self.captcha_entry.setFixedWidth(150)
        captcha_layout.addWidget(self.captcha_entry)

        form_layout.addLayout(captcha_layout)

        validate_captcha_button = QPushButton("Valider Captcha")
        validate_captcha_button.clicked.connect(self.validate_captcha)
        form_layout.addWidget(validate_captcha_button)

        self.captcha_status_label = QLabel(self)
        self.captcha_status_label.setAlignment(Qt.AlignCenter)
        form_layout.addWidget(self.captcha_status_label)

        register_button = QPushButton("S'inscrire")
        register_button.setObjectName("registerButton")
        register_button.clicked.connect(self.handle_register)
        form_layout.addWidget(register_button)

        login_button = QPushButton("Connexion")
        login_button.setObjectName("loginButton")
        login_button.clicked.connect(self.open_login_window)
        form_layout.addWidget(login_button)

        main_layout.addWidget(form_frame)
        self.setLayout(main_layout)

        self.captcha_valid = False

    def load_styles(self):
        with open("styles/register.qss", "r") as file:
            self.setStyleSheet(file.read())

    def refresh_captcha(self, event):
        self.captcha_image, self.captcha_text = generate_captcha()
        self.captcha_label.setPixmap(QPixmap.fromImage(
            self.captcha_image).scaled(150, 50, Qt.KeepAspectRatio))
        self.captcha_entry.clear()
        self.captcha_status_label.clear()
        self.captcha_valid = False

    def validate_captcha(self):
        captcha_input = self.captcha_entry.text()
        if captcha_input == self.captcha_text:
            self.captcha_status_label.setText("Captcha validé.")
            self.captcha_valid = True
        else:
            self.captcha_status_label.setText("Captcha incorrect.")
            self.captcha_valid = False

    def handle_register(self):
        first_name = self.first_name_entry.text()
        last_name = self.last_name_entry.text()
        email = self.email_entry.text()
        password = self.password_entry.text()
        confirm_password = self.confirm_password_entry.text()

        if not all([first_name, last_name, email, password, confirm_password]):
            QMessageBox.critical(
                self, "Erreur", "Tous les champs doivent être remplis.")
            return

        if not self.is_valid_email(email):
            QMessageBox.critical(self, "Erreur", "Adresse e-mail invalide.")
            return

        if password != confirm_password:
            QMessageBox.critical(
                self, "Erreur", "Les mots de passe ne correspondent pas.")
            return

        if not self.captcha_valid:
            QMessageBox.critical(
                self, "Erreur", "Veuillez valider le captcha.")
            return

        if not self.is_valid_password(password):
            QMessageBox.critical(
                self, "Erreur", "Le mot de passe doit contenir au moins 8 caractères, comprenant des lettres majuscules et minuscules, des chiffres et des symboles.")
            return

        payload = {
            "firstname": first_name,
            "lastname": last_name,
            "email": email,
            "password": password
        }

        api_url = "http://localhost/SecurePwd/Backend/register"

        try:
            response = requests.post(api_url, json=payload)
            response.raise_for_status()

            response_data = response.json()
            if response_data.get("token"):
                QMessageBox.information(
                    self, "Inscription réussie", "Un code vous a été envoyé dans votre boite mail.")
                token = response_data.get("token")
                self.open_pin_entry_window(token)
            else:
                QMessageBox.critical(self, "Erreur", response_data.get(
                    "message", "Erreur lors de l'inscription."))

        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Erreur", f"Erreur : {e}")

    def open_pin_entry_window(self, token):
        from pin_entry import PinEntryWindow
        self.pin_entry_window = PinEntryWindow(token)
        self.pin_entry_window.show()
        self.close()

    def is_valid_email(self, email):
        regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.match(regex, email)

    def is_valid_password(self, password):
        # Vérifie si le mot de passe contient au moins 8 caractères, des lettres majuscules et minuscules, des chiffres et des symboles
        regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        return re.match(regex, password)

    def open_login_window(self):
        from login import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()
