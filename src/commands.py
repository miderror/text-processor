from abc import ABC, abstractmethod

from PySide6.QtWidgets import QFileDialog

from src.editor_widget import EditorWidget


class Command(ABC):
    @abstractmethod
    def execute(self):
        pass


class NewFileCommand(Command):
    def __init__(self, editor_widget: EditorWidget):
        self.editor_widget = editor_widget

    def execute(self):
        self.editor_widget.new_file()


class OpenFileCommand(Command):
    def __init__(self, editor_widget: EditorWidget):
        self.editor_widget = editor_widget

    def execute(self):
        file_name, _ = QFileDialog.getOpenFileName(self.editor_widget, "Open File", "",
                                                   "Text Files (*.txt);;All Files (*)")
        if file_name:
            self.editor_widget.load_file(file_name)


class SaveFileCommand(Command):
    def __init__(self, editor_widget: EditorWidget):
        self.editor_widget = editor_widget

    def execute(self):
        file_name, _ = QFileDialog.getSaveFileName(self.editor_widget, "Save File", "",
                                                   "Text Files (*.txt);;All Files (*)")
        if file_name:
            self.editor_widget.save_file(file_name)
