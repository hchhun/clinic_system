import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QDialogButtonBox
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QMessageBox, QGroupBox
from PyQt6.QtWidgets import QGridLayout, QVBoxLayout

from clinic.exception.illegal_operation_exception import IllegalOperationException

from clinic.controller import Controller
class AddPatientGUI(QMainWindow):
    def __init__(self, controller, parent):
        super().__init__()
        self.controller = controller
        self.parent = parent
        self.resize(600, 400)
        self.setWindowTitle("Add new patient")

        # setting up layout
        layout = QVBoxLayout()
        inputLayout = QGridLayout()
        inputGroupBox = QGroupBox("Enter patient information below")

        # input fields
        label_phn = QLabel("PHN: ")
        label_name = QLabel("Name: ")
        label_birth_date = QLabel("Birth date: ")
        label_phone = QLabel("Phone: ")
        label_email = QLabel("Email: ")
        label_address = QLabel("Address: ")
        self.text_phn = QLineEdit()
        self.text_phn.setPlaceholderText("Enter a 10 digit PHN")
        self.text_name = QLineEdit()
        self.text_name.setPlaceholderText("Enter name")
        self.text_birth_date = QLineEdit()
        self.text_birth_date.setPlaceholderText("YYYY-MM-DD")
        self.text_phone = QLineEdit()
        self.text_phone.setPlaceholderText("Enter phone number")
        self.text_email = QLineEdit()
        self.text_email.setPlaceholderText("Enter preferred email")
        self.text_address = QLineEdit()
        self.text_address.setPlaceholderText("Enter current address")

        inputLayout.addWidget(label_phn, 0, 0)
        inputLayout.addWidget(self.text_phn, 0, 1)
        inputLayout.addWidget(label_name, 1, 0)
        inputLayout.addWidget(self.text_name, 1, 1)
        inputLayout.addWidget(label_birth_date, 2, 0)
        inputLayout.addWidget(self.text_birth_date, 2, 1)
        inputLayout.addWidget(label_phone, 3, 0)
        inputLayout.addWidget(self.text_phone, 3, 1)
        inputLayout.addWidget(label_email, 4, 0)
        inputLayout.addWidget(self.text_email, 4, 1)
        inputLayout.addWidget(label_address, 5, 0)
        inputLayout.addWidget(self.text_address, 5, 1)
        inputGroupBox.setLayout(inputLayout)

        # button box at bottom of window
        self.button_box = QDialogButtonBox()
        self.button_box.addButton("Back", QDialogButtonBox.ButtonRole.ResetRole)
        self.button_box.addButton("Clear", QDialogButtonBox.ButtonRole.AcceptRole)
        self.button_box.addButton("Create", QDialogButtonBox.ButtonRole.AcceptRole)
        self.button_box.clicked.connect(self.handle_button_clicked)

        layout.addWidget(inputGroupBox, alignment=Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(self.button_box)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    # handles actions for which button is clicked
    def handle_button_clicked(self, button):
        clicked = button.text()

        if clicked == "Create":
            try:
                self.controller.create_patient(int(self.text_phn.text()), self.text_name.text(), \
                self.text_birth_date.text(), self.text_phone.text(), self.text_email.text(), self.text_address.text())
                QMessageBox.information(self, "Success", "Patient has been successfully created")
                self.clear_button_clicked()
            except ValueError:
                QMessageBox.information(self, "Error", "Please enter a valid PHN format")
            except:
                QMessageBox.information(self, "Error", "Patient with this PHN already exists")
        elif clicked == "Clear":
            self.clear_button_clicked()
        else:
            self.clear_button_clicked()
            self.hide()
            self.parent.show()

    # resetting the GUI
    def clear_button_clicked(self):
        self.text_phn.setText("")
        self.text_name.setText("")
        self.text_birth_date.setText("")
        self.text_phone.setText("")
        self.text_email.setText("")
        self.text_address.setText("")