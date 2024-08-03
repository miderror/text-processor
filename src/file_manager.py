import gzip
import json

from PySide6.QtWidgets import QMessageBox, QWidget


class FileManager:
    def __init__(self):
        self.file_name = None
        self.data = {"pages": []}

    def new_file(self):
        self.file_name = None
        self.data = {"pages": [""]}

    def save_file(self, file_name):
        compressed_data = gzip.compress(json.dumps(self.data).encode('utf-8'))
        with open(file_name, 'wb') as file:
            file.write(compressed_data)
        self.file_name = file_name

    def load_file(self, file_name):
        try:
            with gzip.open(file_name, 'rb') as file:
                json_data = file.read()
            self.data = json.loads(json_data)
        except (OSError, json.JSONDecodeError):
            QMessageBox.critical(
                QWidget(), "Error loading file", "Failed to load file: invalid format"
            )
            return
        self.file_name = file_name

    def get_page_content(self, page_num):
        try:
            return self.data["pages"][page_num]
        except IndexError:
            return ""

    def set_page_content(self, page_num, content):
        if page_num < len(self.data["pages"]):
            self.data["pages"][page_num] = content
        else:
            self.data["pages"].append(content)

    def new_page(self):
        self.data["pages"].append("")

    @property
    def num_pages(self):
        return len(self.data["pages"])
