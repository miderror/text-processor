import sys

from PySide6.QtWidgets import QApplication

from text_processor import TextProcessor

if __name__ == '__main__':
    app = QApplication(sys.argv)
    text_processor = TextProcessor()
    text_processor.show()
    sys.exit(app.exec())
