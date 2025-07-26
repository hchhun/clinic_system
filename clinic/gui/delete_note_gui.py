import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QDialogButtonBox, QPlainTextEdit
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout
from PyQt6.QtWidgets import QGridLayout, QVBoxLayout

from clinic.exception.illegal_operation_exception import IllegalOperationException

from clinic.controller import Controller
# delete confirmation window
class ConfirmWarningGUI(QMainWindow):
    def __init__(self, controller, parent):
        super().__init__()
        self.controller = controller
        self.parent = parent
        self.resize(300, 100)
        self.setWindowTitle("Confirm removal?")

        layout = QVBoxLayout()
        label_warning = QLabel("Do you really want to delete this note?")
        button_box = QHBoxLayout()
        confirm_button = QPushButton("Confirm")
        cancel_button = QPushButton("Cancel")

        self.text_code = self.parent.text_search_code

        confirm_button.clicked.connect(self.confirm_button_clicked)
        cancel_button.clicked.connect(self.cancel_button_clicked)

        layout.addWidget(label_warning, alignment=Qt.AlignmentFlag.AlignCenter)
        button_box.addWidget(confirm_button)
        button_box.addWidget(cancel_button)
        layout.addLayout(button_box)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def confirm_button_clicked(self):
        code = self.text_code.text()
        self.controller.delete_note(int(code)) # deletes note
        self.parent.clear_button_clicked()
        self.hide()
        QMessageBox.information(self, "Success", f"Note #{code} has been successfully deleted")
        self.parent.clear_button_clicked()

    def cancel_button_clicked(self):
        self.hide()

class DeleteNoteGUI(QMainWindow):
    def __init__(self, controller, parent):
        super().__init__()
        self.controller = controller
        self.parent = parent
        self.resize(600, 400)
        self.setWindowTitle("Remove note from patient record")

        # setting up layout
        layout = QVBoxLayout()
        searchLayout = QGridLayout()
        self.search_button = QPushButton("Search")
        self.text_note = QPlainTextEdit()
        self.text_note.setReadOnly(True)
        self.text_note.textChanged.connect(self.text_changed)
        self.text_note.setReadOnly(True)
        spacer = QWidget()
        spacer.setFixedSize(10, 3)
        spacer2 = QWidget()
        spacer2.setFixedSize(85, 0)

        self.text_search_code = QLineEdit()
        self.text_search_code.setPlaceholderText("Enter note code")
        
        # search layout
        label_info = QLabel("Code of note to be deleted")
        searchLayout.addWidget(spacer2, 0, 0)
        searchLayout.addWidget(label_info, 0, 1)
        searchLayout.addWidget(self.text_search_code, 0, 2)
        searchLayout.addWidget(spacer, 0, 3)
        searchLayout.addWidget(self.search_button, 0, 4)
        searchLayout.addWidget(spacer2, 0, 5)

        # button box at bottom of window
        self.button_box = QDialogButtonBox()
        self.button_box.addButton("Back", QDialogButtonBox.ButtonRole.ResetRole)
        self.button_box.addButton("Clear", QDialogButtonBox.ButtonRole.AcceptRole)
        self.delete_button = self.button_box.addButton("Delete", QDialogButtonBox.ButtonRole.AcceptRole)
        self.delete_button.setEnabled(False)
        self.button_box.clicked.connect(self.handle_button_clicked)
        self.search_button.clicked.connect(self.search_button_clicked)

        layout.addWidget(spacer)
        layout.addLayout(searchLayout)
        layout.addWidget(spacer)
        layout.addWidget(self.text_note)
        layout.addWidget(self.button_box)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    # asks for confirmation when delete is clicked
    def delete_confirm(self):
        self.confirm_warning = ConfirmWarningGUI(self.controller, parent=self)
        self.confirm_warning.show()

    # enables delete only if note is found
    def text_changed(self):
        self.text_search_code.setEnabled(False)
        self.search_button.setEnabled(False)
        self.delete_button.setEnabled(True)
    
    # searches note and displays info
    def search_button_clicked(self):
        try:
            note = self.controller.search_note(int(self.text_search_code.text()))
            if note is not None:
                self.text_note.insertPlainText(str(note))
            else:
                QMessageBox.information(self, "Not found", "Note not found")
                self.clear_button_clicked()
        except ValueError:
            QMessageBox.information(self, "Not found", "Please enter a number")
            self.clear_button_clicked()

    # handles the actions for which button is clicked
    def handle_button_clicked(self, button):
        clicked = button.text()

        if clicked == "Delete":
            self.delete_confirm() # asks for confirmation
        elif clicked == "Clear":
            self.clear_button_clicked()
        else:
            self.hide()
            self.parent.show()
            self.clear_button_clicked()

    # resetting the GUI
    def clear_button_clicked(self):
        self.text_search_code.clear()
        self.text_note.clear()
        self.text_search_code.setEnabled(True)
        self.search_button.setEnabled(True)
        self.delete_button.setEnabled(False)