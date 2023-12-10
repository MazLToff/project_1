import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFileDialog,
                             QAction, QTextEdit, QVBoxLayout,
                             QHBoxLayout, QPushButton, QSlider, QLabel,
                             QWidget, QSizePolicy, QStyle, QColorDialog)
from PyQt5.QtCore import Qt


class TextEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Простой текстовый редактор')

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        self.textEdit = QTextEdit(self)
        self.textEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        font = self.textEdit.font()
        self.textEdit.setFont(font)

        toolbar = self.create_toolbar()

        main_layout = QVBoxLayout(central_widget)
        toolbar_layout = QHBoxLayout()

        main_layout.addWidget(self.textEdit)

        self.size_slider = QSlider(self)
        self.size_slider.setOrientation(Qt.Horizontal)
        self.size_slider.setMinimum(1)
        self.size_slider.setMaximum(50)
        size_label = QLabel('Размер шрифта:', self)
        toolbar_layout.addWidget(size_label)
        toolbar_layout.addWidget(self.size_slider)
        main_layout.addLayout(toolbar_layout)

        self.size_slider.valueChanged.connect(self.set_font_size)

        self.normal_button = QPushButton('Обычный стиль', self)
        self.bold_button = QPushButton('Жирный', self)
        self.cursive_button = QPushButton('Курсив', self)
        self.color_button = QPushButton('Выбрать цвет', self)

        toolbar_layout.addWidget(self.normal_button)
        toolbar_layout.addWidget(self.bold_button)
        toolbar_layout.addWidget(self.cursive_button)
        toolbar_layout.addWidget(self.color_button)
        main_layout.addLayout(toolbar_layout)

        self.normal_button.clicked.connect(self.set_font_normal)
        self.bold_button.clicked.connect(self.set_font_bold)
        self.cursive_button.clicked.connect(self.set_font_cursive)
        self.color_button.clicked.connect(self.choose_text_color)

        undo_action = QAction('Отменить', self)
        undo_action.triggered.connect(self.textEdit.undo)

        redo_action = QAction('Повторить', self)
        redo_action.triggered.connect(self.textEdit.redo)

        toolbar.addAction(undo_action)
        toolbar.addAction(redo_action)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
                color: #333333;
            }
            QTextEdit {
                font-family: Arial;
                font-size: 14px;
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 5px;
            }
            QSlider::handle:horizontal {
                background: #0077ff;
                border: 1px solid #0077ff;
                width: 12px;
                margin: -5px 0;
                border-radius: 6px;
            }
            QPushButton {
                background-color: #0077ff;
                color: #ffffff;
                border: 1px solid #0077ff;
                border-radius: 4px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #0055cc;
                border: 1px solid #0055cc;
            }
        """)

    def set_font_size(self, value):
        font = self.textEdit.font()
        font.setPointSize(int(value))
        self.textEdit.setFont(font)

    def update_status_bar(self):
        text = self.textEdit.toPlainText()
        word_count = len(text.split())
        line_count = self.textEdit.document().blockCount()
        self.statusBar.showMessage(f"Слов: {word_count}, Строк: {line_count}")

    def set_font_normal(self):
        font = self.textEdit.font()
        font.setBold(False)
        font.setItalic(False)
        self.textEdit.setFont(font)

    def set_font_bold(self):
        font = self.textEdit.font()
        font.setBold(True)
        font.setItalic(False)
        self.textEdit.setFont(font)

    def set_font_cursive(self):
        font = self.textEdit.font()
        font.setBold(False)
        font.setItalic(True)
        self.textEdit.setFont(font)

    def choose_text_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.textEdit.setTextColor(color)

    def toggle_underline(self):
        cursor = self.textEdit.textCursor()
        format = cursor.charFormat()
        format.setFontUnderline(not format.fontUnderline())
        cursor.setCharFormat(format)

    def toggle_strikeout(self):
        cursor = self.textEdit.textCursor()
        format = cursor.charFormat()
        format.setFontStrikeOut(not format.fontStrikeOut())
        cursor.setCharFormat(format)

    def create_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu('Файл')

        open_action = QAction('Открыть', self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction('Сохранить', self)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        exit_action = QAction('Выход', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def create_toolbar(self):
        toolbar = self.addToolBar('Инструменты')

        open_action = QAction(self)
        open_action.setIcon(self.style().standardIcon(QStyle.SP_DialogOpenButton))
        open_action.setText('')
        open_action.triggered.connect(self.open_file)
        toolbar.addAction(open_action)
        open_action.setShortcut('Ctrl+O')

        save_action = QAction(self)
        save_action.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
        save_action.setText('')
        save_action.triggered.connect(self.save_file)
        toolbar.addAction(save_action)
        save_action.setShortcut('Ctrl+S')

        undo_action = QAction(self)
        undo_action.setIcon(self.style().standardIcon(QStyle.SP_ArrowBack))
        undo_action.setText('')
        undo_action.triggered.connect(self.textEdit.undo)
        toolbar.addAction(undo_action)
        undo_action.setShortcut('Ctrl+Z')

        redo_action = QAction(self)
        redo_action.setIcon(self.style().standardIcon(QStyle.SP_ArrowForward))
        redo_action.setText('')
        redo_action.triggered.connect(self.textEdit.redo)
        toolbar.addAction(redo_action)
        redo_action.setShortcut('Ctrl+Y')

        return toolbar

    def open_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Открыть файл", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'r') as file:
                self.textEdit.setPlainText(file.read())

    def save_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'w') as file:
                file.write(self.textEdit.toPlainText())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = TextEditor()
    editor.show()
    sys.exit(app.exec_())