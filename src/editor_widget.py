import webbrowser

from PySide6 import QtWidgets
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QTextEdit, QWidget, QApplication

from file_manager import FileManager
from navigation_widget import NavigationWidget


class CustomTextEdit(QTextEdit):
    def __init__(self):
        super().__init__()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and QApplication.keyboardModifiers() == Qt.ControlModifier:
            anchor = self.anchorAt(event.pos())
            if anchor:
                url = QUrl(anchor)
                if url.isValid() and url.scheme() in ['http', 'https']:
                    QDesktopServices.openUrl(url)
                    return
                webbrowser.open(f'https://www.google.com/search?q={anchor}')
                return
        super().mousePressEvent(event)


class EditorWidget(QWidget):
    def __init__(self, file_name=None):
        super().__init__()
        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)
        self.text_edit = CustomTextEdit()
        self.navigation_widget = NavigationWidget(self)
        self.navigation_widget.setFixedSize(200, 50)

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
        self.save_current_page_content()
        self.file_manager.save_file(file_name)

    def set_current_page(self, page_num):
        self.current_page = page_num
        self.navigation_widget.update_page_number()
        page_content = self.file_manager.get_page_content(self.current_page)
        self.text_edit.setHtml(page_content)

    def get_current_page_content(self):
        return self.text_edit.toHtml()

    def save_current_page_content(self):
        self.file_manager.set_page_content(self.current_page, self.get_current_page_content())

    def update_current_page(self):
        self.set_current_page(self.current_page)

    def next_page(self):
        self.save_current_page_content()
        self.current_page += 1
        if self.current_page >= self.file_manager.num_pages:
            self.file_manager.new_page()
        self.update_current_page()

    def previous_page(self):
        if self.current_page <= 0:
            return
        self.save_current_page_content()
        self.current_page -= 1
        self.update_current_page()
