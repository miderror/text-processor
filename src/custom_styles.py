import json
import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor, QIcon
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QComboBox, QPushButton, QLineEdit, QColorDialog, QLabel,
    QFontComboBox, QToolBar, QToolButton
)


class StyleManager:
    def __init__(self, filepath=os.path.join('..', 'config', 'styles.json')):
        self.filepath = filepath
        self.styles = self.load_styles()

    def load_styles(self):
        try:
            with open(self.filepath, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.styles = {}

    def save_styles(self):
        with open(self.filepath, 'w') as file:
            json.dump(self.styles, file)

    def add_style(self, name, font: QFont, color: QColor, size: int):
        self.styles[name] = {
            'font': font.toString(),
            'color': color.name(),
            'size': size,
            'bold': font.bold(),
            'italic': font.italic(),
            'underline': font.underline()
        }
        self.save_styles()

    def delete_style(self, name):
        if name in self.styles:
            del self.styles[name]
            self.save_styles()

    def get_style(self, name):
        style = self.styles.get(name)
        if style:
            font = QFont()
            font.fromString(style['font'])
            color = QColor(style['color'])
            size = style['size']
            font.setBold(style.get('bold', False))
            font.setItalic(style.get('italic', False))
            font.setUnderline(style.get('underline', False))
            return font, color, size
        return None, None, None


class StyleDialog(QDialog):
    def __init__(self, style_manager, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Manage Styles")
        self.style_manager = style_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.style_combo = QComboBox()
        self.update_style_combo()
        self.style_combo.currentTextChanged.connect(self.load_style)
        layout.addWidget(self.style_combo)

        toolbar = QToolBar()

        select_button = QToolButton()
        select_button.setText("select")
        select_button.setIcon(QIcon('../resources/select.png'))
        select_button.setToolTip('Select style')
        select_button.clicked.connect(self.select_style)
        toolbar.addWidget(select_button)

        toolbar.addSeparator()

        add_button = QToolButton()
        add_button.setText("add")
        add_button.setIcon(QIcon('../resources/add.png'))
        add_button.setToolTip('Add style')
        add_button.clicked.connect(self.create_style)
        toolbar.addWidget(add_button)

        edit_button = QToolButton()
        edit_button.setText("edit")
        edit_button.setIcon(QIcon('../resources/edit.png'))
        edit_button.setToolTip('Edit style')
        edit_button.clicked.connect(self.edit_style)
        toolbar.addWidget(edit_button)

        delete_button = QToolButton()
        delete_button.setText("delete")
        delete_button.setIcon(QIcon('../resources/delete.png'))
        delete_button.setToolTip('Delete style')
        delete_button.clicked.connect(self.delete_style)
        toolbar.addWidget(delete_button)

        layout.addWidget(toolbar)

        self.example_text = QLabel("Example")
        layout.addWidget(self.example_text)

        self.setLayout(layout)
        self.load_style(self.parent().style_button.text())

    def update_style_combo(self):
        self.style_combo.clear()
        keys = self.style_manager.styles.keys()
        if not keys:
            self.parent().update_style("None", self)
            self.close()
        self.style_combo.addItems(keys)

    def load_style(self, name):
        self.style_combo.setCurrentText(name)
        font, color, size = self.style_manager.get_style(name)
        if font and color and size:
            self.example_text.setFont(font)
            self.example_text.setStyleSheet(f"color: {color.name()}; font-size: {size}px;")

    def create_style(self):
        style_editor = StyleEditor(self.style_manager, self, new_style=True)
        style_editor.exec()

    def edit_style(self):
        name = self.style_combo.currentText()
        font, color, size = self.style_manager.get_style(name)
        style_editor = StyleEditor(self.style_manager, self, new_style=False, style_name=name, font=font, color=color,
                                   size=size)
        style_editor.exec()

    def delete_style(self):
        name = self.style_combo.currentText()
        self.style_manager.delete_style(name)
        self.update_style_combo()

    def select_style(self):
        style_name = self.style_combo.currentText()
        self.parent().update_style(style_name, self)
        self.close()


class StyleEditor(QDialog):
    def __init__(self, style_manager, parent=None, new_style=True, style_name='', font=None, color=None, size=12):
        super().__init__(parent)
        self.setWindowTitle("Manage Styles")
        self.style_manager = style_manager
        self.new_style = new_style
        self.style_name = style_name
        self.init_ui(font, color, size)

    def init_ui(self, font, color, size):
        layout = QVBoxLayout()

        self.name_edit = QLineEdit()
        if self.new_style:
            layout.addWidget(QLabel("Style Name:"))
            layout.addWidget(self.name_edit)
        else:
            self.name_edit.setText(self.style_name)
            self.name_edit.setReadOnly(True)
            layout.addWidget(QLabel(f"Style Name: {self.style_name}"))

        self.font_combo = QFontComboBox()
        self.font_combo.setCurrentFont(font if font else QFont())
        self.font_combo.setEditable(False)
        self.font_combo.currentFontChanged.connect(self.update_example)
        layout.addWidget(QLabel("Font:"))
        layout.addWidget(self.font_combo)

        self.size_combo = QComboBox()
        self.size_combo.addItems([str(size) for size in range(8, 48, 1)])
        self.size_combo.setCurrentText(str(size))
        self.size_combo.currentTextChanged.connect(self.update_example)
        layout.addWidget(QLabel("Size:"))
        layout.addWidget(self.size_combo)

        self.color_button = QPushButton("Select Color")
        self.color_button.clicked.connect(self.select_color)
        self.color_button.setStyleSheet(f"background-color: {color.name() if color else 'gray'}")
        layout.addWidget(self.color_button)

        self.bold_button = QPushButton("Bold")
        self.bold_button.setCheckable(True)
        self.bold_button.setChecked(font.bold() if font else False)
        self.bold_button.setFocusPolicy(Qt.NoFocus)
        self.bold_button.clicked.connect(self.update_example)
        layout.addWidget(self.bold_button)

        self.italic_button = QPushButton("Italic")
        self.italic_button.setCheckable(True)
        self.italic_button.setChecked(font.italic() if font else False)
        self.italic_button.setFocusPolicy(Qt.NoFocus)
        self.italic_button.clicked.connect(self.update_example)
        layout.addWidget(self.italic_button)

        self.underline_button = QPushButton("Underline")
        self.underline_button.setCheckable(True)
        self.underline_button.setChecked(font.underline() if font else False)
        self.underline_button.setFocusPolicy(Qt.NoFocus)
        self.underline_button.clicked.connect(self.update_example)
        layout.addWidget(self.underline_button)

        self.example_text = QLabel("Example")
        layout.addWidget(self.example_text)

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_style)
        layout.addWidget(save_button)

        self.setLayout(layout)
        self.update_example()

    def select_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color_button.setStyleSheet(f"background-color: {color.name()}")
            self.update_example()

    def update_example(self):
        font = self.font_combo.currentFont()
        font.setPointSize(int(self.size_combo.currentText()))
        font.setBold(self.bold_button.isChecked())
        font.setItalic(self.italic_button.isChecked())
        font.setUnderline(self.underline_button.isChecked())
        self.example_text.setFont(font)
        background_color = self.color_button.palette().button().color()
        self.example_text.setStyleSheet(f"color: {background_color.name()}")

    def save_style(self):
        name = self.name_edit.text() if self.new_style else self.style_name
        font = self.font_combo.currentFont()
        font.setPointSize(int(self.size_combo.currentText()))
        font.setBold(self.bold_button.isChecked())
        font.setItalic(self.italic_button.isChecked())
        font.setUnderline(self.underline_button.isChecked())
        color = self.color_button.palette().button().color()
        size = int(self.size_combo.currentText())
        self.style_manager.add_style(name, font, color, size)
        parent = self.parent()
        parent.update_style_combo()
        parent.load_style(name)
        self.close()
