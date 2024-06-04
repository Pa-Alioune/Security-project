# app/sources/pin_entry_window.py
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QMessageBox, QSpacerItem, QSizePolicy
from PySide6.QtCore import Qt
import requests


class PinEntryWindow(QWidget):
    def __init__(self, token):
        super().__init__()
        self.token = token
        self.setWindowTitle("Saisie du code PIN - SecurePwd")
        self.setGeometry(100, 100, 800, 600)
        self.load_styles()
        self.showMaximized()

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        # Spacer item en haut pour centrer verticalement
        top_spacer = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        main_layout.addItem(top_spacer)

        # Création de la carte
        card_frame = QFrame()
        card_frame.setObjectName("cardFrame")
        card_frame.setMaximumWidth(600)
        card_frame.setMaximumHeight(400)
        card_layout = QVBoxLayout(card_frame)
        card_layout.setAlignment(Qt.AlignCenter)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(20)

        self.title_label = QLabel(
            "Veuillez saisir le code envoyé à votre e-mail")
        self.title_label.setObjectName("pinTitleLabel")
        self.title_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.title_label)

        self.pin_entry = QLineEdit()
        self.pin_entry.setPlaceholderText("Code PIN")
        self.pin_entry.setMaxLength(6)
        self.pin_entry.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.pin_entry)

        self.submit_button = QPushButton("Valider")
        self.submit_button.setObjectName("pinSubmitButton")
        self.submit_button.clicked.connect(self.handle_pin_submission)
        card_layout.addWidget(self.submit_button)

        main_layout.addWidget(card_frame)

        # Spacer item en bas pour centrer verticalement
        bottom_spacer = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        main_layout.addItem(bottom_spacer)

        self.setLayout(main_layout)

    def load_styles(self):
        with open("styles/pin_entry.qss", "r") as file:
            self.setStyleSheet(file.read())

    def handle_pin_submission(self):
        pin = self.pin_entry.text()
        if not pin:
            QMessageBox.critical(
                self, "Erreur", "Veuillez saisir le code PIN.")
            return

        payload = {"otp": pin}
        api_url = "http://localhost/SecurePwd/Backend/valide-otp"
        # Inclure le token dans les en-têtes
        headers = {"Authorization": f"Bearer {self.token}"}

        try:
            response = requests.post(api_url, json=payload, headers=headers)
            status_code = response.status_code
            response.raise_for_status()

            if status_code == 200:
                QMessageBox.information(
                    self, "Validation réussie", "Code PIN validé avec succès. Vous allez être rediriger vers la page de connexion")
                self.open_login_window()
            else:
                QMessageBox.critical(
                    self, "Erreur", "Erreur lors de la validation du pin")

        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Erreur", f"Erreur : {e}")

    def open_login_window(self):
        from login import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()
