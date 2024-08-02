from abc import ABC, abstractmethod

from PySide6 import QtGui, QtCore
from PySide6.QtGui import QFont, QImage, QTextImageFormat, QTextCursor, QTextCharFormat
from PySide6.QtWidgets import QFileDialog, QInputDialog, QMessageBox

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


class SetFontCommand(Command):
    def __init__(self, editor_widget: EditorWidget, font: QFont):
        self.editor_widget = editor_widget
        self.font = font

    def execute(self):
        self.editor_widget.text_edit.setCurrentFont(self.font)


class SetFontSizeCommand(Command):
    def __init__(self, editor_widget: EditorWidget, size: int):
        self.editor_widget = editor_widget
        self.size = size

    def execute(self):
        self.editor_widget.text_edit.setFontPointSize(self.size)


class SetFontColorCommand(Command):
    def __init__(self, editor_widget: EditorWidget, color: QtGui.QColor):
        self.editor_widget = editor_widget
        self.color = color

    def execute(self):
        self.editor_widget.text_edit.setTextColor(self.color)


class SetLineSpacingCommand(Command):
    def __init__(self, editor_widget: EditorWidget, spacing: float):
        self.editor_widget = editor_widget
        self.spacing = spacing

    def execute(self):
        cursor = self.editor_widget.text_edit.textCursor()
        block_fmt = QtGui.QTextBlockFormat()
        block_fmt.setLineHeight(float(self.spacing * 100), 1)
        cursor.mergeBlockFormat(block_fmt)


class ToggleBoldCommand(Command):
    def __init__(self, editor_widget: EditorWidget):
        self.editor_widget = editor_widget

    def execute(self):
        text_edit = self.editor_widget.text_edit
        cursor = text_edit.textCursor()

        if cursor.hasSelection():
            state = any(
                cursor.charFormat().fontWeight() != QFont.Weight.Bold
                for i in range(cursor.selectionStart() + 1, cursor.selectionEnd() + 1)
                if cursor.setPosition(i) or True
            )
        else:
            state = text_edit.fontWeight != QFont.Weight.Bold
        weight = QFont.Weight.Bold if state else QFont.Weight.Normal
        text_edit.setFontWeight(weight)


class ToggleItalicCommand(Command):
    def __init__(self, editor_widget: EditorWidget):
        self.editor_widget = editor_widget

    def execute(self):
        text_edit = self.editor_widget.text_edit
        cursor = text_edit.textCursor()

        if cursor.hasSelection():
            state = any(
                not cursor.charFormat().fontItalic()
                for i in range(cursor.selectionStart() + 1, cursor.selectionEnd() + 1)
                if cursor.setPosition(i) or True
            )
        else:
            state = not text_edit.fontItalic()
        text_edit.setFontItalic(state)


class ToggleUnderlineCommand(Command):
    def __init__(self, editor_widget: EditorWidget):
        self.editor_widget = editor_widget

    def execute(self):
        text_edit = self.editor_widget.text_edit
        cursor = text_edit.textCursor()

        if cursor.hasSelection():
            state = any(
                not cursor.charFormat().fontUnderline()
                for i in range(cursor.selectionStart() + 1, cursor.selectionEnd() + 1)
                if cursor.setPosition(i) or True
            )
        else:
            state = not text_edit.fontUnderline()
        text_edit.setFontUnderline(state)


class InsertImageCommand(Command):
    def __init__(self, editor_widget: EditorWidget):
        self.editor_widget = editor_widget

    def execute(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(None, "Insert Image", "",
                                                   "Images (*.png *.xpm *.jpg *.jpeg *.bmp *.gif)")

        if not file_path:
            return

        image = QImage(file_path)
        if image.isNull():
            return

        width, ok_width = QInputDialog.getInt(
            self.editor_widget, "Image Width", "Enter width:", image.width(), 1, 3000
        )
        height, ok_height = QInputDialog.getInt(
            self.editor_widget, "Image Height", "Enter height:", image.height(), 1, 3000
        )

        if not ok_width or not ok_height:
            QMessageBox.critical(self.editor_widget, "Error", "Invalid width or height")
            return

        image = image.scaled(width, height, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        text_cursor = self.editor_widget.text_edit.textCursor()
        document = self.editor_widget.text_edit.document()

        document.addResource(
            QtGui.QTextDocument.ImageResource,
            QtCore.QUrl(file_path), image
        )

        image_format = QTextImageFormat()
        image_format.setWidth(width)
        image_format.setHeight(height)
        image_format.setName(file_path)

        text_cursor.insertImage(image_format)


class InsertLinkCommand(Command):
    def __init__(self, editor_widget: EditorWidget):
        self.editor_widget = editor_widget

    def execute(self):
        text_edit = self.editor_widget.text_edit
        cursor = text_edit.textCursor()

        current_format = cursor.charFormat()

        text, ok_text = QInputDialog.getText(self.editor_widget, 'Insert Link', 'Enter text:')
        if not ok_text:
            return
        url, ok_url = QInputDialog.getText(self.editor_widget, 'Insert Link', 'Enter URL:')
        if not ok_url:
            return

        cursor.insertText(" ")
        cursor.insertHtml(f'<a href="{url}">{text}</a>')
        end = cursor.position()
        cursor.setPosition(end, QTextCursor.MoveAnchor)

        cursor.setCharFormat(current_format)
        cursor.insertText(" ")
        text_edit.setTextCursor(cursor)
