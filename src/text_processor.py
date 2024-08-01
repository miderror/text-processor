from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMainWindow, QStackedWidget

from commands import *
from src.editor_widget import EditorWidget
from src.start_window import StartWindow


class TextProcessor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.start_window = StartWindow()
        self.editor_widget = EditorWidget()

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.start_window)
        self.stacked_widget.addWidget(self.editor_widget)

        self.setCentralWidget(self.stacked_widget)

        self.start_window.connect_signals(self.create_new_file, self.open_existing_file)

        self.adjust_size_for_start_window()
        self.setWindowTitle('Text Processor')

    def create_new_file(self):
        self.stacked_widget.setCurrentWidget(self.editor_widget)
        self.adjust_size_for_editor()

    def open_existing_file(self):
        OpenFileCommand(self.editor_widget).execute()
        self.stacked_widget.setCurrentWidget(self.editor_widget)
        self.adjust_size_for_editor()

    def adjust_size_for_start_window(self):
        self.setGeometry(100, 100, 300, 200)

    def adjust_size_for_editor(self):
        self.setGeometry(100, 100, 800, 600)
        self.init_menubar()

    def init_menubar(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu('File')
        new_action = QAction('New', self)
        new_action.triggered.connect(lambda: NewFileCommand(self.editor_widget).execute())
        file_menu.addAction(new_action)

        open_action = QAction('Open', self)
        open_action.triggered.connect(lambda: OpenFileCommand(self.editor_widget).execute())
        file_menu.addAction(open_action)

        save_action = QAction('Save', self)
        save_action.triggered.connect(lambda: SaveFileCommand(self.editor_widget).execute())
        file_menu.addAction(save_action)
