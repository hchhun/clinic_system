import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QDialogButtonBox, QPlainTextEdit
from PyQt6.QtWidgets import QWidget, QMessageBox, QGroupBox
from PyQt6.QtWidgets import QVBoxLayout

from clinic.exception.illegal_operation_exception import IllegalOperationException

from clinic.controller import Controller

class AddNoteGUI(QMainWindow):
    def __init__(self, controller, parent):
        super().__init__()
        self.controller = controller
        self.parent = parent
        self.resize(600, 400)
        self.setWindowTitle("Add note to patient record")
        
        # setting up layout
        layout = QVBoxLayout()
        self.text_note = QPlainTextEdit()
        inputLayout = QVBoxLayout()
        inputGroupBox = QGroupBox("Add new note's contents below")

        # button box at bottom of window
        self.button_box = QDialogButtonBox()
        self.button_box.addButton("Back", QDialogButtonBox.ButtonRole.ResetRole)
        self.button_box.addButton("Clear", QDialogButtonBox.ButtonRole.AcceptRole)
        self.button_box.addButton("Create", QDialogButtonBox.ButtonRole.AcceptRole)
        self.button_box.clicked.connect(self.handle_button_clicked)

        inputLayout.addWidget(self.text_note)
        inputGroupBox.setLayout(inputLayout)
        layout.addWidget(inputGroupBox, alignment=Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(self.button_box)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    # handles the actions for which button is clicked
    def handle_button_clicked(self, button):
        clicked = button.text()

        if clicked == "Create": # creates note in patient's record
            self.controller.create_note(self.text_note.toPlainText())
            QMessageBox.information(self, "Success", "Note has been successfully added")
        elif clicked == "Clear":
            self.text_note.clear()
        else:
            self.hide()
            self.parent.show()

        self.text_note.clear()