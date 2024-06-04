from PySide6.QtGui import QImage, QPainter, QColor, QFont, QPen
from PySide6.QtCore import Qt
import random
import string


def generate_captcha():
    # Générer un texte aléatoire pour le captcha
    captcha_text = ''.join(random.choices(
        string.ascii_uppercase + string.digits, k=6))

    # Créer une image pour le captcha
    width, height = 200, 50
    image = QImage(width, height, QImage.Format_ARGB32)
    image.fill(QColor('white'))

    # Dessiner le texte du captcha sur l'image
    painter = QPainter(image)
    font = QFont()
    font.setPointSize(20)
    painter.setFont(font)

    # Dessiner du bruit (lignes) sur l'image pour rendre le captcha plus difficile à lire par une machine
    pen = QPen()
    pen.setColor(QColor('gray'))
    painter.setPen(pen)
    for _ in range(10):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        painter.drawLine(x1, y1, x2, y2)

    painter.setPen(QColor('black'))
    painter.drawText(image.rect(), Qt.AlignCenter, captcha_text)
    painter.end()

    return image, captcha_text
