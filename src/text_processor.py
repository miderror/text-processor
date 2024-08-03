from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow, QStackedWidget, QTabWidget

from commands import *
from editor_widget import EditorWidget
from start_window import StartWindow
from tab_widgets import FileTab, MainTab, InsertTab, StylesTab, FindReplaceTab


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
        self.setWindowIcon(QIcon('../resources/logo.png'))

    def create_new_file(self) -> None:
        self.stacked_widget.setCurrentWidget(self.editor_widget)
        self.adjust_size_for_editor()

    def open_existing_file(self) -> None:
        OpenFileCommand(self.editor_widget).execute()
        self.stacked_widget.setCurrentWidget(self.editor_widget)
        self.adjust_size_for_editor()

    def adjust_size_for_start_window(self) -> None:
        self.setGeometry(100, 100, 300, 200)

    def adjust_size_for_editor(self) -> None:
        self.setGeometry(100, 100, 800, 600)
        self.init_tabs()

    def init_tabs(self) -> None:
        self.tab_widget = QTabWidget(self)
        self.tab_widget.setMaximumHeight(100)
        self.editor_widget.layout.addWidget(self.tab_widget, 0, 0, 1, 3)

        file_tab = FileTab(self.editor_widget)
        main_tab = MainTab(self.editor_widget)
        insert_tab = InsertTab(self.editor_widget)
        styles_tab = StylesTab(self.editor_widget)
        replace_search_tab = FindReplaceTab(self.editor_widget)

        self.tab_widget.addTab(file_tab, "File")
        self.tab_widget.addTab(main_tab, "Home")
        self.tab_widget.addTab(insert_tab, "Insert")
        self.tab_widget.addTab(styles_tab, "Styles")
        self.tab_widget.addTab(replace_search_tab, "Find and Replace")
