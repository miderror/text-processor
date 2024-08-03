from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout, QToolBar, QFontComboBox, QComboBox, QToolButton, QMenu, QCheckBox, \
    QDialog, QColorDialog, QSizePolicy

from commands import *
from src.custom_styles import StyleManager, StyleDialog
from src.find_replace_dialog import FindReplaceDialog


def get_checkbox_stylesheet():
    stylesheet = """
        QCheckBox {
            spacing: 5px;
            outline: none;
            color: #333;
            font-size: 14px;
        }

        QCheckBox::indicator {
            width: 16px;
            height: 16px;
            border: 1px solid #888;
            border-radius: 3px;
            background-color: #f5f5f5;
        }

        QCheckBox::indicator:checked {
            image: url(../resources/check.png);
        }

        QCheckBox::indicator:unchecked {
            background-color: #f5f5f5;
        }
    """
    return stylesheet


class FileTab(QWidget):
    def __init__(self, editor_widget):
        super().__init__()
        self.editor_widget = editor_widget
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        toolbar = self.create_toolbar()
        layout.addWidget(toolbar)
        self.setLayout(layout)

    def create_toolbar(self):
        toolbar = QToolBar()
        toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        # New action
        new_action = QAction(QIcon('../resources/new.png'), 'New', self)
        new_action.triggered.connect(self.new_file_action)
        toolbar.addAction(new_action)
        toolbar.addSeparator()

        # Open action
        open_action = QAction(QIcon('../resources/open.png'), 'Open', self)
        open_action.triggered.connect(self.open_file_action)
        toolbar.addAction(open_action)
        toolbar.addSeparator()

        # Save action
        save_action = QAction(QIcon('../resources/save.png'), 'Save', self)
        save_action.triggered.connect(self.save_file_action)
        toolbar.addAction(save_action)

        return toolbar

    def new_file_action(self):
        NewFileCommand(self.editor_widget).execute()

    def open_file_action(self):
        OpenFileCommand(self.editor_widget).execute()

    def save_file_action(self):
        SaveFileCommand(self.editor_widget).execute()


class MainTab(QWidget):
    def __init__(self, editor_widget):
        super().__init__()
        self.editor_widget = editor_widget
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        toolbar = self.create_toolbar()
        layout.addWidget(toolbar)
        self.setLayout(layout)

    def create_toolbar(self):
        toolbar = QToolBar()

        # Formatting actions
        self.add_formatting_actions(toolbar)

        toolbar.addSeparator()

        # Font settings button
        self.add_font_settings(toolbar)

        toolbar.addSeparator()

        # Font size selection
        self.add_font_size_selection(toolbar)

        # Text color action
        color_action = QAction(QIcon('../resources/color.png'), "Color", self)
        color_action.triggered.connect(self.change_text_color)
        toolbar.addAction(color_action)

        toolbar.addSeparator()

        # Indent/Outdent actions
        self.add_indent_actions(toolbar)

        # Line spacing button
        self.add_line_spacing_button(toolbar)

        toolbar.addSeparator()

        # Spacer
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        toolbar.addWidget(spacer)

        # Whole document checkbox
        self.apply_to_whole_doc = QCheckBox("Whole Doc")
        self.apply_to_whole_doc.setToolTip("Apply formatting to the entire document")
        self.apply_to_whole_doc.setStyleSheet(get_checkbox_stylesheet())
        toolbar.addWidget(self.apply_to_whole_doc)

        return toolbar

    def add_formatting_actions(self, toolbar):
        bold_action = QAction(QIcon('../resources/bold.png'), 'Bold', self)
        bold_action.triggered.connect(self.toggle_bold)
        toolbar.addAction(bold_action)

        italic_action = QAction(QIcon('../resources/italic.png'), 'Italic', self)
        italic_action.triggered.connect(self.toggle_italic)
        toolbar.addAction(italic_action)

        underline_action = QAction(QIcon('../resources/underline.png'), 'Underline', self)
        underline_action.triggered.connect(self.toggle_underline)
        toolbar.addAction(underline_action)

    def add_font_settings(self, toolbar):
        self.font_button = QToolButton()
        self.font_button.setText('Arial')
        self.font_button.setToolTip('Apply font')
        self.font_button.clicked.connect(self.set_font)
        toolbar.addWidget(self.font_button)

        font_settings_button = QToolButton()
        font_settings_button.setIcon(QIcon('../resources/settings.png'))
        font_settings_button.setToolTip('Select font')
        font_settings_button.clicked.connect(self.open_font_selection_dialog)
        toolbar.addWidget(font_settings_button)

    def add_font_size_selection(self, toolbar):
        font_size_box = QComboBox()
        font_size_box.addItems([str(size) for size in range(8, 48, 1)])
        font_size_box.currentTextChanged.connect(self.set_font_size)
        toolbar.addWidget(font_size_box)

    def add_indent_actions(self, toolbar):
        outdent_action = QAction(QIcon('../resources/outdent.png'), 'Outdent', self)
        outdent_action.triggered.connect(self.decrease_indent)
        toolbar.addAction(outdent_action)

        indent_action = QAction(QIcon('../resources/indent.png'), 'Indent', self)
        indent_action.triggered.connect(self.increase_indent)
        toolbar.addAction(indent_action)

    def add_line_spacing_button(self, toolbar):
        line_spacing_button = QToolButton()
        line_spacing_button.setIcon(QIcon('../resources/line_spacing.png'))
        line_spacing_button.setToolTip('Line spacing')
        line_spacing_menu = QMenu(self)
        for spacing in ['1.0', '1.15', '1.5', '2.0', '2.5', '3.0']:
            action = QAction(spacing, self)
            action.triggered.connect(lambda _, s=spacing: self.set_line_spacing(s))
            line_spacing_menu.addAction(action)
        line_spacing_button.setMenu(line_spacing_menu)
        line_spacing_button.setPopupMode(QToolButton.InstantPopup)
        toolbar.addWidget(line_spacing_button)

    def toggle_bold(self):
        if self.apply_to_whole_doc.isChecked():
            ToggleBoldDocumentCommand(self.editor_widget).execute()
            return
        ToggleBoldCommand(self.editor_widget).execute()

    def toggle_italic(self):
        if self.apply_to_whole_doc.isChecked():
            ToggleItalicDocumentCommand(self.editor_widget).execute()
            return
        ToggleItalicCommand(self.editor_widget).execute()

    def toggle_underline(self):
        if self.apply_to_whole_doc.isChecked():
            ToggleUnderlineDocumentCommand(self.editor_widget).execute()
            return
        ToggleUnderlineCommand(self.editor_widget).execute()

    def set_font(self):
        if self.apply_to_whole_doc.isChecked():
            SetFontDocumentCommand(self.editor_widget, QFont(self.font_button.text())).execute()
            return
        SetFontCommand(self.editor_widget, QFont(self.font_button.text())).execute()

    def open_font_selection_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Select font")

        font_box = QFontComboBox(dialog)
        font_box.setEditable(False)
        font_box.setCurrentText(self.font_button.text())
        font_box.currentFontChanged.connect(lambda font: self.update_font(font, dialog))

        dialog_layout = QVBoxLayout(dialog)
        dialog_layout.addWidget(font_box)
        dialog.setLayout(dialog_layout)
        dialog.exec()

    def update_font(self, font, dialog):
        self.font_button.setText(font.family())
        SetFontCommand(self.editor_widget, font).execute()
        dialog.close()

    def set_font_size(self, size):
        if self.apply_to_whole_doc.isChecked():
            SetFontSizeDocumentCommand(self.editor_widget, int(size)).execute()
            return
        SetFontSizeCommand(self.editor_widget, int(size)).execute()

    def change_text_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            if self.apply_to_whole_doc.isChecked():
                SetFontColorDocumentCommand(self.editor_widget, color).execute()
                return
            SetFontColorCommand(self.editor_widget, color).execute()

    def increase_indent(self):
        if self.apply_to_whole_doc.isChecked():
            IncreaseIndentDocumentCommand(self.editor_widget).execute()
            return
        cursor = self.editor_widget.text_edit.textCursor()
        block_format = cursor.blockFormat()
        block_format.setIndent(block_format.indent() + 1)
        cursor.setBlockFormat(block_format)

    def decrease_indent(self):
        if self.apply_to_whole_doc.isChecked():
            DecreaseIndentDocumentCommand(self.editor_widget).execute()
            return
        cursor = self.editor_widget.text_edit.textCursor()
        block_format = cursor.blockFormat()

        if block_format.indent() > 0:
            block_format.setIndent(block_format.indent() - 1)
            cursor.setBlockFormat(block_format)
            return

        current_margin = block_format.leftMargin()
        new_margin = max(0, current_margin - 40)
        block_format.setLeftMargin(new_margin)
        cursor.setBlockFormat(block_format)

    def set_line_spacing(self, spacing):
        if self.apply_to_whole_doc.isChecked():
            SetLineSpacingDocumentCommand(self.editor_widget, float(spacing)).execute()
            return
        SetLineSpacingCommand(self.editor_widget, float(spacing)).execute()


class InsertTab(QWidget):
    def __init__(self, editor_widget):
        super().__init__()
        self.editor_widget = editor_widget
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        toolbar = self.create_toolbar()
        layout.addWidget(toolbar)
        self.setLayout(layout)

    def create_toolbar(self):
        toolbar = QToolBar()
        toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        insert_image_action = QAction(QIcon('../resources/insert_image.png'), 'Insert Image', self)
        insert_image_action.triggered.connect(self.insert_image)
        toolbar.addAction(insert_image_action)
        toolbar.addSeparator()

        insert_link_action = QAction(QIcon('../resources/insert_link.png'), 'Insert Link', self)
        insert_link_action.setToolTip('Insert Link (Ctrl + Left Click to follow)')
        insert_link_action.triggered.connect(self.insert_link)
        toolbar.addAction(insert_link_action)

        return toolbar

    def insert_image(self):
        InsertImageCommand(self.editor_widget).execute()

    def insert_link(self):
        InsertLinkCommand(self.editor_widget).execute()


class StylesTab(QWidget):
    def __init__(self, editor_widget):
        super().__init__()
        self.editor_widget = editor_widget
        self.style_manager = StyleManager()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        toolbar = self.create_toolbar()
        layout.addWidget(toolbar)
        self.setLayout(layout)

    def create_toolbar(self):
        toolbar = QToolBar()
        toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        style_name = str(next(iter(self.style_manager.styles), None))
        self.style_button = QAction(QIcon('../resources/style.png'), style_name, self)
        self.style_button.setToolTip('Your Style')
        self.style_button.triggered.connect(self.apply_selected_style)
        toolbar.addAction(self.style_button)

        style_settings_button = QToolButton()
        style_settings_button.setIcon(QIcon('../resources/settings.png'))
        style_settings_button.setToolTip('Manage Style')
        style_settings_button.clicked.connect(self.open_style_settings_dialog)
        toolbar.addWidget(style_settings_button)

        # Spacer
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        toolbar.addWidget(spacer)

        # Whole document checkbox
        self.apply_to_whole_doc = QCheckBox("Whole Doc")
        self.apply_to_whole_doc.setToolTip("Apply style to the entire document")
        self.apply_to_whole_doc.setStyleSheet(get_checkbox_stylesheet())
        toolbar.addWidget(self.apply_to_whole_doc)

        return toolbar

    def apply_selected_style(self):
        if self.apply_to_whole_doc.isChecked():
            ApplyStyleDocumentCommand(self.editor_widget, self.style_button.text(), self.style_manager).execute()
            return
        ApplyStyleCommand(self.editor_widget, self.style_button.text(), self.style_manager).execute()
        ApplyStyleCommand(self.editor_widget, self.style_button.text(), self.style_manager).execute()

    def open_style_settings_dialog(self):
        dialog = StyleDialog(self.style_manager, self)
        dialog.exec()

    def update_style(self, style_name, dialog):
        self.style_button.setText(style_name)
        ApplyStyleCommand(self.editor_widget, style_name, self.style_manager).execute()
        dialog.close()


class FindReplaceTab(QWidget):
    def __init__(self, editor_widget):
        super().__init__()
        self.editor_widget = editor_widget
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        toolbar = self.create_toolbar()
        layout.addWidget(toolbar)
        self.setLayout(layout)

    def create_toolbar(self):
        toolbar = QToolBar()
        toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.style_button = QAction(QIcon('../resources/find_and_replace.png'), "Find and Replace", self)
        self.style_button.triggered.connect(self.open_search_dialog)
        toolbar.addAction(self.style_button)

        return toolbar

    def open_search_dialog(self):
        dialog = FindReplaceDialog(self)
        dialog.exec()
