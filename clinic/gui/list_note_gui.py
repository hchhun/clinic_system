import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QDialogButtonBox, QPlainTextEdit
from PyQt6.QtWidgets import QVBoxLayout, QWidget

from clinic.exception.illegal_operation_exception import IllegalOperationException

from clinic.controller import Controller

class ListNoteGUI(QMainWindow):
    def __init__(self, controller, parent):
        super().__init__()
        self.controller = controller
        self.parent = parent
        self.resize(600, 400)
        self.setWindowTitle("List full patient record")

        # setting up layout
        layout = QVBoxLayout()
        self.text_note = QPlainTextEdit()
        self.text_note.setReadOnly(True)

        # button box at bottom of window
        self.button_box = QDialogButtonBox()
        self.button_box.addButton("Back", QDialogButtonBox.ButtonRole.ResetRole)
        self.button_box.clicked.connect(self.handle_button_clicked)

        layout.addWidget(self.text_note)
        layout.addWidget(self.button_box)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    # refreshes note list
    def refresh_data(self):
        self.text_note.clear()
        found = self.controller.list_notes()
        for note in found: # appends to display
            self.text_note.appendPlainText(str(note)+"\n")

    # back button
    def handle_button_clicked(self, button):
        self.hide()
        self.parent.show()