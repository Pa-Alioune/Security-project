# app/sources/dashboard_window.py
import requests
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QMessageBox, QDialog, QLineEdit
from PySide6.QtCore import Qt
from password_manager_dialog import PasswordManagerDialog
import random
import string

API_URL = "https://your-api-url.com"  # Remplacez par l'URL de votre API


class DashboardWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dashboard - SecurePwd")
        self.setGeometry(100, 100, 800, 600)
        self.load_styles()
        self.showMaximized()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        self.title_label = QLabel("Bienvenue sur SecurePwd")
        self.title_label.setObjectName("dashboardTitleLabel")
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)

        self.generate_password_button = QPushButton("Générer un mot de passe")
        self.generate_password_button.setObjectName("generatePasswordButton")
        self.generate_password_button.clicked.connect(
            self.open_password_manager)
        layout.addWidget(self.generate_password_button,
                         alignment=Qt.AlignCenter)

        self.account_list = QListWidget()
        self.load_account_list()
        layout.addWidget(self.account_list)

        self.setLayout(layout)

    def load_styles(self):
        with open("styles/dashboard.qss", "r") as file:
            self.setStyleSheet(file.read())

    def open_password_manager(self):
        dialog = PasswordManagerDialog()
        if dialog.exec():
            # Logique de mise à jour de la liste des comptes
            self.load_account_list()

    def load_account_list(self):
        self.account_list.clear()
        try:
            response = requests.get(f"{API_URL}/accounts")
            response.raise_for_status()
            accounts = response.json()
        except requests.RequestException as e:
            QMessageBox.critical(
                self, "Erreur", f"Erreur de chargement des comptes : {e}")
            return

        for account in accounts:
            item_widget = QWidget()
            item_layout = QHBoxLayout()
            item_layout.setContentsMargins(10, 10, 10, 10)
            item_label = QLabel(account['name'])
            item_label.setObjectName("accountLabel")
            view_button = QPushButton("Visualiser")
            view_button.setObjectName("viewButton")
            view_button.clicked.connect(
                lambda _, pwd=account['password']: self.view_password(pwd))
            edit_button = QPushButton("Modifier")
            edit_button.setObjectName("editButton")
            edit_button.clicked.connect(
                lambda _, acct=account: self.open_edit_dialog(acct))
            delete_button = QPushButton("Supprimer")
            delete_button.setObjectName("deleteButton")
            delete_button.clicked.connect(
                lambda _, acct=account: self.delete_account(acct))

            item_layout.addWidget(item_label)
            item_layout.addWidget(view_button)
            item_layout.addWidget(edit_button)
            item_layout.addWidget(delete_button)
            item_widget.setLayout(item_layout)

            list_item = QListWidgetItem()
            list_item.setSizeHint(item_widget.sizeHint())
            self.account_list.addItem(list_item)
            self.account_list.setItemWidget(list_item, item_widget)

    def view_password(self, password):
        QMessageBox.information(self, "Mot de passe",
                                f"Le mot de passe est : {password}")

    def open_edit_dialog(self, account):
        dialog = EditPasswordDialog(account)
        if dialog.exec():
            new_password = dialog.get_password()
            try:
                response = requests.put(
                    f"{API_URL}/accounts/{account['id']}", json={"password": new_password})
                response.raise_for_status()
                QMessageBox.information(self, "Succès",
                                        f"Le mot de passe pour {account['name']} a été modifié.")
                self.load_account_list()
            except requests.RequestException as e:
                QMessageBox.critical(
                    self, "Erreur", f"Erreur de mise à jour du compte : {e}")

    def delete_account(self, account):
        reply = QMessageBox.question(self, "Confirmation",
                                     f"Voulez-vous vraiment supprimer le compte {account['name']}?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                response = requests.delete(
                    f"{API_URL}/accounts/{account['id']}")
                response.raise_for_status()
                QMessageBox.information(self, "Succès",
                                        f"Le compte {account['name']} a été supprimé.")
                self.load_account_list()
            except requests.RequestException as e:
                QMessageBox.critical(
                    self, "Erreur", f"Erreur de suppression du compte : {e}")


class EditPasswordDialog(QDialog):
    def __init__(self, account):
        super().__init__()
        self.setWindowTitle("Modifier le mot de passe")
        self.setFixedSize(400, 200)
        self.account = account
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.password_label = QLabel(
            f"Modifier le mot de passe pour {self.account['name']}")
        layout.addWidget(self.password_label)

        self.password_entry = QLineEdit()
        layout.addWidget(self.password_entry)

        self.generate_button = QPushButton("Générer")
        self.generate_button.clicked.connect(self.generate_password)
        layout.addWidget(self.generate_button)

        self.save_button = QPushButton("Enregistrer")
        self.save_button.clicked.connect(self.accept)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def generate_password(self):
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(12))
        self.password_entry.setText(password)

    def get_password(self):
        return self.password_entry.text()
