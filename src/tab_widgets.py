from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout, QToolBar, QFontComboBox, QComboBox, QColorDialog, QToolButton, QMenu

from commands import *


class FileTab(QWidget):
    def __init__(self, editor_widget):
        super().__init__()
        self.editor_widget = editor_widget
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        toolbar = QToolBar()
        toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        new_action = QAction(QIcon('../resources/new.png'), 'New', self)
        new_action.triggered.connect(lambda: NewFileCommand(self.editor_widget).execute())
        toolbar.addAction(new_action)

        toolbar.addSeparator()

        open_action = QAction(QIcon('../resources/open.png'), 'Open', self)
        open_action.triggered.connect(lambda: OpenFileCommand(self.editor_widget).execute())
        toolbar.addAction(open_action)

        toolbar.addSeparator()

        save_action = QAction(QIcon('../resources/save.png'), 'Save', self)
        save_action.triggered.connect(lambda: SaveFileCommand(self.editor_widget).execute())
        toolbar.addAction(save_action)

        layout.addWidget(toolbar)
        self.setLayout(layout)


class MainTab(QWidget):
    def __init__(self, editor_widget):
        super().__init__()
        self.editor_widget = editor_widget
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        toolbar = QToolBar()

        bold_action = QAction(QIcon('../resources/bold.png'), 'Bold', self)
        bold_action.triggered.connect(lambda: ToggleBoldCommand(self.editor_widget).execute())
        toolbar.addAction(bold_action)

        italic_action = QAction(QIcon('../resources/italic.png'), 'Italic', self)
        italic_action.triggered.connect(lambda: ToggleItalicCommand(self.editor_widget).execute())
        toolbar.addAction(italic_action)

        underline_action = QAction(QIcon('../resources/underline.png'), 'Underline', self)
        underline_action.triggered.connect(lambda: ToggleUnderlineCommand(self.editor_widget).execute())
        toolbar.addAction(underline_action)

        toolbar.addSeparator()

        font_box = QFontComboBox()
        font_box.setEditable(False)
        font_box.currentFontChanged.connect(lambda font: SetFontCommand(self.editor_widget, font).execute())
        toolbar.addWidget(font_box)

        font_size_box = QComboBox()
        font_size_box.addItems([str(size) for size in range(8, 48, 2)])
        font_size_box.currentTextChanged.connect(
            lambda size: SetFontSizeCommand(self.editor_widget, int(size)).execute())
        toolbar.addWidget(font_size_box)

        color_action = QAction(QIcon('../resources/color.png'), "Color", self)
        color_action.triggered.connect(self.change_text_color)
        toolbar.addAction(color_action)

        toolbar.addSeparator()

        outdent_action = QAction(QIcon('../resources/outdent.png'), 'Outdent', self)
        outdent_action.triggered.connect(self.decrease_indent)
        toolbar.addAction(outdent_action)

        indent_action = QAction(QIcon('../resources/indent.png'), 'Indent', self)
        indent_action.triggered.connect(self.increase_indent)
        toolbar.addAction(indent_action)

        line_spacing_button = QToolButton(self)
        line_spacing_button.setIcon(QIcon('../resources/line_spacing.png'))
        line_spacing_menu = QMenu(self)
        for spacing in ['1.0', '1.15', '1.5', '2.0', '2.5', '3.0']:
            action = QAction(spacing, self)
            action.triggered.connect(
                lambda checked, s=spacing: SetLineSpacingCommand(self.editor_widget, float(s)).execute())
            line_spacing_menu.addAction(action)
        line_spacing_button.setMenu(line_spacing_menu)
        line_spacing_button.setPopupMode(QToolButton.InstantPopup)
        toolbar.addWidget(line_spacing_button)

        layout.addWidget(toolbar)
        self.setLayout(layout)

    def change_text_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            SetFontColorCommand(self.editor_widget, color).execute()

    def increase_indent(self):
        cursor = self.editor_widget.text_edit.textCursor()
        block_format = cursor.blockFormat()
        block_format.setIndent(block_format.indent() + 1)
        cursor.setBlockFormat(block_format)

    def decrease_indent(self):
        cursor = self.editor_widget.text_edit.textCursor()
        block_format = cursor.blockFormat()
        if block_format.indent() > 0:
            block_format.setIndent(block_format.indent() - 1)
        cursor.setBlockFormat(block_format)


class InsertTab(QWidget):
    def __init__(self, editor_widget):
        super().__init__()
        self.editor_widget = editor_widget
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        toolbar = QToolBar()
        toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        insert_image_action = QAction(QIcon('../resources/insert_image.png'), 'Insert Image', self)
        insert_image_action.triggered.connect(lambda: InsertImageCommand(self.editor_widget).execute())
        toolbar.addAction(insert_image_action)

        toolbar.addSeparator()

        insert_link_action = QAction(QIcon('../resources/insert_link.png'), 'Insert Link', self)
        insert_link_action.triggered.connect(lambda: InsertLinkCommand(self.editor_widget).execute())
        toolbar.addAction(insert_link_action)

        layout.addWidget(toolbar)
        self.setLayout(layout)
