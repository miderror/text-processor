from PySide6.QtWidgets import QDialog, QLabel, QLineEdit, QCheckBox, QPushButton, QVBoxLayout

from src.commands import FindReplaceRegExpDocumentCommand, FindReplaceStringDocumentCommand


class FindReplaceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Find and Replace")

        self.findLabel = QLabel("Find what:")
        self.findLineEdit = QLineEdit()
        self.replaceLabel = QLabel("Replace with:")
        self.replaceLineEdit = QLineEdit()
        self.regexpCheckbox = QCheckBox("Regular expressions")
        self.replaceAllButton = QPushButton("Replace All")

        self.replaceAllButton.clicked.connect(self.replace)

        layout = QVBoxLayout()
        layout.addWidget(self.findLabel)
        layout.addWidget(self.findLineEdit)
        layout.addWidget(self.replaceLabel)
        layout.addWidget(self.replaceLineEdit)
        layout.addWidget(self.regexpCheckbox)
        layout.addWidget(self.replaceAllButton)

        self.setLayout(layout)

    def replace(self):
        find_text = self.findLineEdit.text()
        replace_text = self.replaceLineEdit.text()
        use_regexp = self.regexpCheckbox.isChecked()

        if find_text and replace_text and use_regexp:
            FindReplaceRegExpDocumentCommand(self.parent().editor_widget, find_text, replace_text).execute()
        else:
            FindReplaceStringDocumentCommand(self.parent().editor_widget, find_text, replace_text).execute()

        self.close()
