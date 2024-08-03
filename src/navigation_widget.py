from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QPushButton, QLabel


class NavigationWidget(QWidget):
    def __init__(self, editor_widget):
        super().__init__()
        self.editor_widget = editor_widget
        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)

        self.left_button = QPushButton()
        self.left_button.setIcon(QIcon("../resources/left_arrow.png"))
        self.left_button.setToolTip('Previous page')

        self.right_button = QPushButton()
        self.right_button.setIcon(QIcon("../resources/right_arrow.png"))
        self.right_button.setToolTip('Next page')

        self.page_number = QLabel('Page: 1')
        self.page_number.setAlignment(Qt.AlignCenter)

        self.left_button.clicked.connect(self.editor_widget.previous_page)
        self.right_button.clicked.connect(self.editor_widget.next_page)

        self.layout.addWidget(self.left_button, 0, 0, 1, 1)
        self.layout.addWidget(self.page_number, 0, 1, 1, 1)
        self.layout.addWidget(self.right_button, 0, 2, 1, 1)

    def update_page_number(self):
        self.page_number.setText(f'Page: {self.editor_widget.current_page + 1}')
