from PySide6 import QtWidgets
from PySide6.QtWidgets import QTextEdit, QLabel, QWidget
from src.file_manager import FileManager
from src.navigation_widget import NavigationWidget


class EditorWidget(QWidget):
    def __init__(self, file_name=None):
        super().__init__()
        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)
        self.text_edit = QTextEdit()
        self.page_number_label = QLabel("Page: 1")
        self.navigation_widget = NavigationWidget(self)

        self.layout.addWidget(self.page_number_label, 0, 0, 1, 1)
        self.layout.addWidget(self.text_edit, 1, 0, 1, 3)
        self.layout.addWidget(self.navigation_widget, 2, 1, 1, 1)

        self.file_manager = FileManager()
        self.current_page = 0

        if file_name:
            self.load_file(file_name)

    def new_file(self):
        self.file_manager.new_file()
        self.set_current_page(0)

    def load_file(self, file_name):
        self.file_manager.load_file(file_name)
        self.set_current_page(0)

    def save_file(self, file_name):
        self.file_manager.save_file(file_name)

    def set_current_page(self, page_num):
        self.current_page = page_num
        self.page_number_label.setText(f"Page: {self.current_page + 1}")
        self.navigation_widget.update_page_number()
        page_content = self.file_manager.get_page_content(self.current_page)
        self.text_edit.setHtml(page_content)

    def get_current_page_content(self):
        return self.text_edit.toHtml()

    def next_page(self):
        self.file_manager.set_page_content(self.current_page, self.get_current_page_content())
        self.current_page += 1
        if self.current_page >= self.file_manager.num_pages:
            self.file_manager.new_page()
        self.set_current_page(self.current_page)

    def previous_page(self):
        if self.current_page > 0:
            self.file_manager.set_page_content(self.current_page, self.get_current_page_content())
            self.current_page -= 1
            self.set_current_page(self.current_page)
