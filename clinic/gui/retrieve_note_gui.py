import sys
from PyQt6.QtCore import Qt
from PyQt6.QtCore import QAbstractTableModel, Qt, QModelIndex
from PyQt6.QtWidgets import QMainWindow, QDialogButtonBox, QPlainTextEdit
from PyQt6.QtWidgets import QWidget, QLineEdit, QMessageBox
from PyQt6.QtWidgets import QVBoxLayout, QComboBox, QFormLayout

from clinic.exception.illegal_operation_exception import IllegalOperationException

from clinic.controller import Controller

class RetrieveNoteGUI(QMainWindow):
    def __init__(self, controller, parent):
        super().__init__()
        self.controller = controller
        self.parent = parent
        self.resize(600, 400)
        self.setWindowTitle("Retrieve notes from patient record by text")
        self.retrieved_notes = []

        # setting up layout
        layout = QVBoxLayout()
        searchLayout = QFormLayout()
        self.text_search_text = QLineEdit()
        self.text_search_text.setPlaceholderText("Enter keyword")
        self.text_note = QPlainTextEdit()
        self.text_note.setReadOnly(True)
        spacer = QWidget()
        spacer.setFixedSize(10, 10)

        searchLayout.addRow("Search by text", self.text_search_text)
        
        # button box at bottom of window
        self.button_box = QDialogButtonBox()
        self.button_box.addButton("Back", QDialogButtonBox.ButtonRole.ResetRole)
        self.button_box.addButton("Clear", QDialogButtonBox.ButtonRole.AcceptRole)
        self.retrieve_button = self.button_box.addButton("Retrieve notes", QDialogButtonBox.ButtonRole.AcceptRole)
        self.button_box.clicked.connect(self.handle_button_clicked)

        layout.addWidget(spacer)
        layout.addLayout(searchLayout)
        layout.addWidget(spacer)
        layout.addWidget(self.text_note)
        layout.addWidget(self.button_box)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    # handles the actions for which button is clicked
    def handle_button_clicked(self, button):
        clicked = button.text()

        if clicked == "Retrieve notes": # retrieves notes based on text
            self.retrieved_notes = self.controller.retrieve_notes(self.text_search_text.text())
            self.text_note.clear()
            if self.retrieved_notes == []:
                QMessageBox.information(self, "Not found", "No matching notes found")
                self.clear_button_clicked()
            else:
                for note in self.retrieved_notes:
                    self.text_note.appendPlainText(str(note)+"\n")
                self.text_search_text.setEnabled(False)
                self.retrieve_button.setEnabled(False)
        elif clicked == "Clear":
            self.clear_button_clicked()
        else:
            self.clear_button_clicked()
            self.hide()
            self.parent.show()

    # resetting the GUI
    def clear_button_clicked(self):
        self.retrieved_notes = []
        self.text_search_text.clear()
        self.text_note.clear()
        self.text_search_text.setEnabled(True)
        self.retrieve_button.setEnabled(True)