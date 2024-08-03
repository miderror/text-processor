import re
from abc import ABC, abstractmethod

from PySide6 import QtGui, QtCore
from PySide6.QtGui import QFont, QImage, QTextImageFormat, QTextCursor, QTextCharFormat, QColor
from PySide6.QtWidgets import QFileDialog, QInputDialog, QMessageBox
from bs4 import BeautifulSoup

from custom_styles import StyleManager
from editor_widget import EditorWidget


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
        cursor = self.editor_widget.text_edit.textCursor()
        current_format = cursor.charFormat()
        current_size = current_format.fontPointSize()
        self.editor_widget.text_edit.setCurrentFont(self.font)
        self.editor_widget.text_edit.setFontPointSize(current_size)


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
            state = cursor.charFormat().fontWeight() != QFont.Weight.Bold
        weight = QFont.Weight.Bold if state else QFont.Weight.Normal
        text_edit.setFontWeight(weight)
        cursor.setCharFormat(text_edit.currentCharFormat())


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


class ApplyStyleCommand(Command):
    def __init__(self, editor_widget: EditorWidget, style_name: str, style_manager: StyleManager):
        self.editor_widget = editor_widget
        self.style_name = style_name
        self.style_manager = style_manager

    def execute(self):
        font, color, size = self.style_manager.get_style(self.style_name)
        if font and color and size:
            cursor = self.editor_widget.text_edit.textCursor()
            text_format = QTextCharFormat()
            text_format.setFont(font)
            text_format.setForeground(color)
            text_format.setFontPointSize(size)
            cursor.mergeCharFormat(text_format)
            self.editor_widget.text_edit.setTextCursor(cursor)


class DocumentCommand(Command):
    def __init__(self, editor_widget: EditorWidget):
        self.editor_widget = editor_widget

    def execute(self):
        self.editor_widget.save_current_page_content()
        for page_num in range(self.editor_widget.file_manager.num_pages):
            page_content = self.editor_widget.file_manager.get_page_content(page_num)
            updated_content = self.apply_to_string(page_content)
            self.editor_widget.file_manager.data["pages"][page_num] = updated_content
        self.editor_widget.update_current_page()

    @abstractmethod
    def apply_to_string(self, content: str) -> str:
        pass


class ToggleBoldDocumentCommand(DocumentCommand):

    def apply_to_string(self, content: str) -> str:
        soup = BeautifulSoup(content, 'html.parser')
        for text in soup.find_all(text=True):
            if text.parent.name != 'b':
                text.wrap(soup.new_tag("b"))
        return str(soup)


class ToggleItalicDocumentCommand(DocumentCommand):

    def apply_to_string(self, content: str) -> str:
        soup = BeautifulSoup(content, 'html.parser')
        for text in soup.find_all(text=True):
            if text.parent.name != 'i':
                text.wrap(soup.new_tag("i"))
        return str(soup)


class ToggleUnderlineDocumentCommand(DocumentCommand):

    def apply_to_string(self, content: str) -> str:
        soup = BeautifulSoup(content, 'html.parser')
        for text in soup.find_all(text=True):
            if text.parent.name != 'u':
                text.wrap(soup.new_tag("u"))
        return str(soup)


class SetFontDocumentCommand(DocumentCommand):

    def __init__(self, editor_widget, font: QFont):
        super().__init__(editor_widget)
        self.font = font

    def apply_to_string(self, content: str) -> str:
        soup = BeautifulSoup(content, 'html.parser')
        for text in soup.find_all(text=True):
            text.wrap(soup.new_tag("span", style=f"font-family: '{self.font.family()}';"))
        return str(soup)


class SetFontSizeDocumentCommand(DocumentCommand):

    def __init__(self, editor_widget, size: int):
        super().__init__(editor_widget)
        self.size = size

    def apply_to_string(self, content: str) -> str:
        soup = BeautifulSoup(content, 'html.parser')
        for text in soup.find_all(text=True):
            text.wrap(soup.new_tag("span", style=f"font-size: {self.size}px;"))
        return str(soup)


class SetFontColorDocumentCommand(DocumentCommand):

    def __init__(self, editor_widget, color: QColor):
        super().__init__(editor_widget)
        self.color = color

    def apply_to_string(self, content: str) -> str:
        soup = BeautifulSoup(content, 'html.parser')
        for text in soup.find_all(text=True):
            text.wrap(soup.new_tag("span", style=f"color: {self.color.name()};"))
        return str(soup)


class IncreaseIndentDocumentCommand(DocumentCommand):

    def apply_to_string(self, content: str) -> str:
        soup = BeautifulSoup(content, 'html.parser')
        indent_increment = 20

        for element in soup.find_all():
            current_style = element.get('style', '')
            current_indent = self.extract_indent(current_style)
            new_indent = current_indent + indent_increment

            new_style = re.sub(r'margin-left:\s*\d+px;', f'margin-left: {new_indent}px;', current_style)
            if 'margin-left' not in new_style:
                new_style = f'margin-left: {new_indent}px; ' + new_style
            element['style'] = new_style

        return str(soup)

    @staticmethod
    def extract_indent(style: str) -> int:
        match = re.search(r'margin-left:\s*(\d+)px;', style)
        if match:
            return int(match.group(1))
        return 0


class DecreaseIndentDocumentCommand(DocumentCommand):
    def apply_to_string(self, content: str) -> str:
        soup = BeautifulSoup(content, 'html.parser')
        indent_decrement = 40

        for element in soup.find_all():
            current_style = element.get('style', '')
            current_indent = self.extract_indent(current_style)
            new_indent = max(current_indent - indent_decrement, 0)

            if new_indent != current_indent:
                new_style = re.sub(r'margin-left:\s*\d+px;', f'margin-left: {new_indent}px;', current_style)
                if 'margin-left' not in new_style:
                    new_style = f'margin-left: {new_indent}px; ' + new_style
                element['style'] = new_style

        return str(soup)

    @staticmethod
    def extract_indent(style: str) -> int:
        match = re.search(r'margin-left:\s*(\d+)px;', style)
        if match:
            return int(match.group(1))
        return 0


class SetLineSpacingDocumentCommand(DocumentCommand):

    def __init__(self, editor_widget, spacing: float):
        super().__init__(editor_widget)
        self.spacing = spacing

    def apply_to_string(self, content: str) -> str:
        soup = BeautifulSoup(content, 'html.parser')
        line_height_regex = re.compile(r'line-height:\s*[\d.]+(?:px|em|%)?;?')

        for element in soup.find_all(['p', 'div', 'span']):
            current_style = element.get('style', '')
            new_style = line_height_regex.sub(f'line-height: {self.spacing};', current_style)
            if new_style == current_style:
                new_style = f'line-height: {self.spacing}; ' + current_style

            element['style'] = new_style.strip()

        return str(soup)


class ApplyStyleDocumentCommand(DocumentCommand):

    def __init__(self, editor_widget, style_name, style_manager):
        super().__init__(editor_widget)
        self.style_name = style_name
        self.style_manager = style_manager

    def apply_to_string(self, content):
        font, color, size = self.style_manager.get_style(self.style_name)

        soup = BeautifulSoup(content, 'html.parser')

        for text in soup.find_all(text=True):
            parent_span = text.find_parent("span")
            if parent_span is None:
                parent_span = soup.new_tag("span")
                text.wrap(parent_span)

            if not font.bold():
                for bold in parent_span.find_all("b"):
                    bold.unwrap()

            if not font.italic():
                for italic in parent_span.find_all("i"):
                    italic.unwrap()

            if not font.underline():
                for underline in parent_span.find_all("u"):
                    underline.unwrap()

            style = f"font-family: '{font.family()}'; font-size: {size}px; color: {color.name()};"
            parent_span["style"] = style

            if font.bold():
                text.wrap(soup.new_tag("b"))

            if font.italic():
                text.wrap(soup.new_tag("i"))

            if font.underline():
                text.wrap(soup.new_tag("u"))

        return str(soup)


class FindReplaceRegExpDocumentCommand(DocumentCommand):
    def __init__(self, editor_widget, find_text, replace_text):
        super().__init__(editor_widget)
        self.findText = find_text
        self.replaceText = replace_text

    def apply_to_string(self, content):
        try:
            pattern = re.compile(self.findText)
            return pattern.sub(self.replaceText, content)
        except re.error as e:
            QMessageBox.critical(
                self.editor_widget,
                "Ошибка",
                f"Некорректное регулярное выражение: {e}"
            )
            return content


class FindReplaceStringDocumentCommand(DocumentCommand):
    def __init__(self, editor_widget, find_text, replace_text, use_regexp=False):
        super().__init__(editor_widget)
        self.findText = find_text
        self.replaceText = replace_text
        self.useRegexp = use_regexp

    def apply_to_string(self, content):
        return content.replace(self.findText, self.replaceText)
