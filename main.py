import sys
import os
import random
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QFileDialog, QScrollArea, QFrame
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp')

def find_images(folder):
    image_paths = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.lower().endswith(IMAGE_EXTENSIONS):
                rel_path = os.path.relpath(os.path.join(root, file), folder)
                image_paths.append(rel_path)
    return image_paths

class ImageViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Перегляд картинок")
        self.resize(900, 600)

        main_layout = QHBoxLayout(self)

        # Ліва панель: кнопки
        left_panel = QVBoxLayout()
        self.open_folder_btn = QPushButton("Відкрити папку")
        self.open_folder_btn.clicked.connect(self.open_folder)
        left_panel.addWidget(self.open_folder_btn)

        # Додаємо кнопку "Випадкова картинка"
        self.random_btn = QPushButton("Випадкова картинка")
        self.random_btn.clicked.connect(self.show_random_image)
        self.random_btn.setEnabled(False)
        left_panel.addWidget(self.random_btn)

        # Список кнопок з прокруткою
        self.buttons_widget = QWidget()
        self.buttons_layout = QVBoxLayout(self.buttons_widget)
        self.buttons_layout.addStretch()
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.buttons_widget)
        left_panel.addWidget(self.scroll_area)

        # Права панель: картинка
        self.image_label = QLabel("Виберіть картинку")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFrameShape(QFrame.Box)
        self.image_label.setMinimumWidth(400)

        main_layout.addLayout(left_panel, 2)
        main_layout.addWidget(self.image_label, 5)

        self.current_image_path = None  # Додаємо змінну для збереження шляху

    def open_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Оберіть папку з картинками")
        if folder:
            self.show_image_buttons(folder)

    def show_image_buttons(self, folder):
        # Очистити старі кнопки
        for i in reversed(range(self.buttons_layout.count() - 1)):
            widget = self.buttons_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        self.folder = folder
        images = find_images(folder)
        for img_rel_path in images:
            btn = QPushButton(img_rel_path)
            btn.clicked.connect(lambda checked, p=img_rel_path: self.show_image(p))
            self.buttons_layout.insertWidget(self.buttons_layout.count() - 1, btn)

        self.images = images  # Зберігаємо список для випадкового вибору
        self.random_btn.setEnabled(bool(images))

    def show_image(self, rel_path):
        img_path = os.path.join(self.folder, rel_path)
        pixmap = QPixmap(img_path)
        if not pixmap.isNull():
            scaled = pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_label.setPixmap(scaled)
            self.current_image_path = rel_path  # Запам'ятовуємо шлях
        else:
            self.image_label.setText("Не вдалося завантажити картинку")
            self.current_image_path = None

    def show_random_image(self):
        if hasattr(self, 'images') and self.images:
            rel_path = random.choice(self.images)
            self.show_image(rel_path)

    def resizeEvent(self, event):
        # Оновити картинку при зміні розміру
        if self.current_image_path:
            self.show_image(self.current_image_path)
        super().resizeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = ImageViewer()
    viewer.show()
    sys.exit(app.exec_())