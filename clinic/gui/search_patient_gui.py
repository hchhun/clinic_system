import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QDialogButtonBox
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QMessageBox, QGroupBox
from PyQt6.QtWidgets import QGridLayout, QVBoxLayout, QFormLayout

from clinic.exception.illegal_operation_exception import IllegalOperationException

from clinic.controller import Controller

class SearchPatientGUI(QMainWindow):
    def __init__(self, controller, parent):
        super().__init__()
        self.controller = controller
        self.parent = parent
        self.resize(600, 400)
        self.setWindowTitle("Search patient by PHN")

        # setting up layout
        layout = QVBoxLayout()
        outputLayout = QGridLayout()
        outputGroupBox = QGroupBox()
        searchLayout = QFormLayout()
        spacer = QWidget()
        spacer.setFixedSize(50, 50)

        self.text_search_phn = QLineEdit()
        self.text_search_phn.setPlaceholderText("Enter PHN")

        # output fields
        label_phn = QLabel("PHN: ")
        label_name = QLabel("Name: ")
        label_birth_date = QLabel("Birth date: ")
        label_phone = QLabel("Phone: ")
        label_email = QLabel("Email: ")
        label_address = QLabel("Address: ")
        self.text_phn = QLineEdit()
        self.text_name = QLineEdit()
        self.text_birth_date = QLineEdit()
        self.text_phone = QLineEdit()
        self.text_email = QLineEdit()
        self.text_address = QLineEdit()

        # read only
        self.text_phn.setEnabled(False)
        self.text_name.setEnabled(False)
        self.text_birth_date.setEnabled(False)
        self.text_phone.setEnabled(False)
        self.text_email.setEnabled(False)
        self.text_address.setEnabled(False)

        outputLayout.addWidget(label_phn, 0, 0)
        outputLayout.addWidget(self.text_phn, 0, 1)
        outputLayout.addWidget(label_name, 1, 0)
        outputLayout.addWidget(self.text_name, 1, 1)
        outputLayout.addWidget(label_birth_date, 2, 0)
        outputLayout.addWidget(self.text_birth_date, 2, 1)
        outputLayout.addWidget(label_phone, 3, 0)
        outputLayout.addWidget(self.text_phone, 3, 1)
        outputLayout.addWidget(label_email, 4, 0)
        outputLayout.addWidget(self.text_email, 4, 1)
        outputLayout.addWidget(label_address, 5, 0)
        outputLayout.addWidget(self.text_address, 5, 1)
        outputGroupBox.setLayout(outputLayout)

        searchLayout.addRow("Search by PHN", self.text_search_phn)

        # button box at bottom of window
        self.button_box = QDialogButtonBox()
        self.button_box.addButton("Back", QDialogButtonBox.ButtonRole.ResetRole)
        self.button_box.addButton("Clear", QDialogButtonBox.ButtonRole.AcceptRole)
        self.search_button = self.button_box.addButton("Search", QDialogButtonBox.ButtonRole.AcceptRole)
        self.button_box.clicked.connect(self.handle_button_clicked)

        searchWidget = QWidget()
        searchWidget.setLayout(searchLayout)
        layout.addWidget(searchWidget, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(outputGroupBox)
        layout.addWidget(spacer)
        layout.addWidget(self.button_box)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    # handles actions for which button is clicked
    def handle_button_clicked(self, button):
        clicked = button.text()
        if clicked == "Search": # searches the patient and displays info if found
            try:
                found = self.controller.search_patient(int(self.text_search_phn.text()))
                if found is not None:
                    self.text_phn.setText(f"{found.phn}")
                    self.text_name.setText(found.name)
                    self.text_birth_date.setText(found.birth_date)
                    self.text_phone.setText(found.phone)
                    self.text_email.setText(found.email)
                    self.text_address.setText(found.address)
                    self.text_search_phn.setEnabled(False)
                    self.search_button.setEnabled(False)
                else:
                    QMessageBox.information(self, "Not found", "Patient not found")
                    self.clear_button_clicked()
            except ValueError:
                QMessageBox.information(self, "Error", "Please enter a valid PHN format")
                self.clear_button_clicked()
        elif clicked == "Clear":
            self.clear_button_clicked()
        else:
            self.hide()
            self.parent.show()
            self.clear_button_clicked()

    # resetting the GUI
    def clear_button_clicked(self):
        self.text_search_phn.setText("")
        self.text_phn.setText("")
        self.text_name.setText("")
        self.text_birth_date.setText("")
        self.text_phone.setText("")
        self.text_email.setText("")
        self.text_address.setText("")
        self.text_search_phn.setEnabled(True)
        self.search_button.setEnabled(True)