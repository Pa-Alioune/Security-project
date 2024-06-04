from register import RegisterWindow
from dashboard import DashboardWindow
import json
import requests
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QMessageBox
import sys
import os
import json
import re  # Importer le module pour les expressions régulières

# Ajouter le chemin du dossier 'app' au sys.path
app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if app_path not in sys.path:
    sys.path.append(app_path)

# Maintenant, vous pouvez importer captcha_generator
from utils.captcha_generator import generate_captcha
from utils.token_utils import get_token, store_token

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SecurePwd - Connexion")
        self.setGeometry(100, 100, 800, 600)
        self.load_styles()
        self.showMaximized()

        # Layout principal
        main_layout = QHBoxLayout()

        # Section gauche (logo et texte)
        left_layout = QVBoxLayout()
        left_layout.setAlignment(Qt.AlignCenter)

        secure_pwd_label = QLabel("SecurePwd")
        secure_pwd_label.setObjectName("securePwdLabel")
        left_layout.addWidget(secure_pwd_label)

        description_label = QLabel(
            "Avec SecurePwd, vos mots de passe seront en toute sécurité.")
        description_label.setObjectName("descriptionLabel")
        description_label.setWordWrap(True)
        left_layout.addWidget(description_label)

        # Section droite (formulaire de connexion dans une card)
        right_frame = QFrame()
        right_frame.setObjectName("rightFrame")
        right_frame.setFrameShape(QFrame.StyledPanel)
        right_frame.setMaximumWidth(600)
        right_frame.setMaximumHeight(400)

        right_layout = QVBoxLayout(right_frame)
        right_layout.setAlignment(Qt.AlignCenter)
        right_layout.setContentsMargins(20, 20, 20, 20)
        right_layout.setSpacing(10)

        self.email_entry = QLineEdit()
        self.email_entry.setPlaceholderText("Adresse e-mail ou numéro de tél.")
        right_layout.addWidget(self.email_entry)

        self.password_entry = QLineEdit()
        self.password_entry.setPlaceholderText("Mot de passe")
        self.password_entry.setEchoMode(QLineEdit.Password)
        right_layout.addWidget(self.password_entry)

        # Ajout du captcha
        self.captcha_label = QLabel(self)
        self.captcha_label.setAlignment(Qt.AlignCenter)
        self.captcha_label.mousePressEvent = self.refresh_captcha  # Reload captcha on click
        self.captcha_image, self.captcha_text = generate_captcha()
        self.captcha_label.setPixmap(QPixmap.fromImage(self.captcha_image))
        right_layout.addWidget(self.captcha_label)

        self.captcha_entry = QLineEdit()
        self.captcha_entry.setPlaceholderText("Entrez le captcha")
        right_layout.addWidget(self.captcha_entry)

        validate_captcha_button = QPushButton("Valider Captcha")
        validate_captcha_button.clicked.connect(self.validate_captcha)
        right_layout.addWidget(validate_captcha_button)

        self.captcha_status_label = QLabel(self)
        self.captcha_status_label.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(self.captcha_status_label)

        login_button = QPushButton("Se connecter")
        login_button.setObjectName("loginButton")
        login_button.clicked.connect(self.handle_login)
        right_layout.addWidget(login_button)

        forgot_password_label = QLabel("Mot de passe oublié ?")
        forgot_password_label.setObjectName("forgotPasswordLabel")
        forgot_password_label.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(forgot_password_label)

        create_account_button = QPushButton("Créer nouveau compte")
        create_account_button.setObjectName("createAccountButton")
        create_account_button.clicked.connect(self.open_register_window)
        right_layout.addWidget(create_account_button)

        main_layout.addLayout(left_layout)
        main_layout.addWidget(right_frame)

        self.setLayout(main_layout)

        # Garder une référence à la fenêtre d'inscription
        self.register_window = None
        self.captcha_valid = False

    def load_styles(self):
        with open("styles/login.qss", "r") as file:
            self.setStyleSheet(file.read())

    def refresh_captcha(self, event):
        self.captcha_image, self.captcha_text = generate_captcha()
        self.captcha_label.setPixmap(QPixmap.fromImage(self.captcha_image))
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

    # def validate_password(self, password):
    #     # Exigences de mot de passe : au moins 8 caractères, comprenant des lettres majuscules et minuscules, des chiffres et des symboles
    #     if len(password) < 8:
    #         return False
    #     if not re.search(r'[A-Z]', password):
    #         return False
    #     if not re.search(r'[a-z]', password):
    #         return False
    #     if not re.search(r'[0-9]', password):
    #         return False
    #     # \W correspond aux caractères non-alphanumériques
    #     if not re.search(r'[\W_]', password):
    #         return False
    #     return True

    def handle_login(self):
        if not self.captcha_valid:
            QMessageBox.critical(self, "Erreur de connexion",
                                 "Veuillez valider le captcha.")
            return

        email = self.email_entry.text()
        password = self.password_entry.text()

        # if not self.validate_password(password):
        #     QMessageBox.critical(self, "Erreur de connexion",
        #                          "Le mot de passe doit contenir au moins 8 caractères, comprenant des lettres majuscules et minuscules, des chiffres et des symboles.")
        #     return

        # Exemple d'URL pour une API distante (à adapter selon votre API)
        api_url = "http://localhost/SecurePwd/Backend/login"

        # Exemple de payload pour l'authentification (à adapter selon votre API)
        payload = {
            "email": email,
            "password": password
        }

        try:
            response = requests.post(api_url, json=payload)
            response.raise_for_status()

            # Analyser la réponse JSON
            response_data = response.json()

            # Exemple : Vérification réussie
            if response_data.get("token"):
                token = response_data["token"]
                store_token(token)
                # Rediriger vers le dashboard
                self.redirect_to_dashboard()

            else:
                # Afficher un message d'erreur
                QMessageBox.critical(
                    self, "Erreur de connexion", "Adresse e-mail ou mot de passe incorrect.")

        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Erreur de connexion", f"Erreur : {e}")

    def redirect_to_dashboard(self):
        # Exemple de redirection vers le dashboard (à adapter selon votre application)
        # Ici, vous pouvez ouvrir une nouvelle fenêtre ou changer de page
        # Exemple simple : affichage d'un message
        QMessageBox.information(
            self, "Connexion réussie", "Vous êtes connecté ! Redirection vers le dashboard.")

        self.open_dashboard_window()

        self.close()

    def open_register_window(self):
        if self.register_window is None:
            self.register_window = RegisterWindow()
        self.register_window.show()
        self.close()

    def open_dashboard_window(self):
        self.dashboard_window = DashboardWindow()
        self.dashboard_window.show()
        self.close()
