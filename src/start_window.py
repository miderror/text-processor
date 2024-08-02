from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QHBoxLayout, QToolButton


class StartWindow(QWidget):
    def __init__(self):
        super().__init__()
        button_layout = QHBoxLayout()

        self.new_file_button = QToolButton()
        self.new_file_button.setIcon(QIcon('../resources/new.png'))
        self.new_file_button.setIconSize(QSize(64, 64))
        self.new_file_button.setText('New')
        self.new_file_button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.new_file_button.setToolTip('New file')

        self.open_file_button = QToolButton()
        self.open_file_button.setIcon(QIcon('../resources/open.png'))
        self.open_file_button.setIconSize(QSize(64, 64))
        self.open_file_button.setText('Open')
        self.open_file_button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.open_file_button.setToolTip('Open file')

        button_layout.addWidget(self.new_file_button)
        button_layout.addWidget(self.open_file_button)
        self.setLayout(button_layout)

    def connect_signals(self, create_new_file_callback, open_existing_file_callback):
        self.new_file_button.clicked.connect(create_new_file_callback)
        self.open_file_button.clicked.connect(open_existing_file_callback)
