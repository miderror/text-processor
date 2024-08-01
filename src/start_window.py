from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout


class StartWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.new_file_button = QPushButton('Create New File')
        self.open_file_button = QPushButton('Open Existing File')

        layout.addWidget(self.new_file_button)
        layout.addWidget(self.open_file_button)

        self.setLayout(layout)

    def connect_signals(self, create_new_file_callback, open_existing_file_callback):
        self.new_file_button.clicked.connect(create_new_file_callback)
        self.open_file_button.clicked.connect(open_existing_file_callback)
