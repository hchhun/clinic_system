import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QDialogButtonBox
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout, QGroupBox
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
        label_warning = QLabel("Do you really want to delete this patient?")
        button_box = QHBoxLayout()
        confirm_button = QPushButton("Confirm")
        cancel_button = QPushButton("Cancel")

        self.text_phn = self.parent.text_phn

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
        try: # deletes patient
            self.controller.delete_patient(int(self.text_phn.text()))
            self.hide()
            self.parent.clear_button_clicked()
            QMessageBox.information(self, "Success", "Patient has been successfully deleted")
        except:
            self.hide()
            QMessageBox.information(self, "Error", "Cannot delete current patient")

    def cancel_button_clicked(self):
        self.hide()

class DeletePatientGUI(QMainWindow):
    def __init__(self, controller, parent):
        super().__init__()
        self.controller = controller
        self.parent = parent
        self.resize(600, 400)
        self.setWindowTitle("Remove patient")

        # setting up layout
        layout = QVBoxLayout()
        outputLayout = QGridLayout()
        outputGroupBox = QGroupBox()
        searchLayout = QHBoxLayout()
        self.search_button = QPushButton("Search")
        spacer = QWidget()
        spacer.setFixedSize(50, 50)
        spacer2 = QWidget()
        spacer2.setFixedSize(10, 10)

        self.text_search_phn = QLineEdit()
        self.text_search_phn.setPlaceholderText("Enter PHN")

        # display fields for search patient
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

        self.patientInfo = ConfirmWarningGUI(self.controller, parent=self)

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

        # search layout
        label_info = QLabel("PHN of patient to be removed")
        searchLayout.addWidget(label_info)
        searchLayout.addWidget(self.text_search_phn)
        searchLayout.addWidget(spacer2)
        searchLayout.addWidget(self.search_button)

        # button box at bottom of window
        self.button_box = QDialogButtonBox()
        self.button_box.addButton("Back", QDialogButtonBox.ButtonRole.ResetRole)
        self.button_box.addButton("Clear", QDialogButtonBox.ButtonRole.AcceptRole)
        self.delete_button = self.button_box.addButton("Delete", QDialogButtonBox.ButtonRole.AcceptRole)
        self.delete_button.setEnabled(False)
        self.button_box.clicked.connect(self.handle_button_clicked)
        self.search_button.clicked.connect(self.search_button_clicked)

        searchWidget = QWidget()
        searchWidget.setLayout(searchLayout)
        layout.addWidget(searchWidget, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(outputGroupBox)
        layout.addWidget(spacer)
        layout.addWidget(self.button_box)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    # asks confirmation when delete is clicked
    def delete_confirm(self):
        self.patientInfo = ConfirmWarningGUI(self.controller, parent=self)
        self.patientInfo.show()

    # handles actions for which button is clicked
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

    # searches patient and displays info
    def search_button_clicked(self):
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
                    self.delete_button.setEnabled(True) # delete is enabled if patient is found
            else:
                QMessageBox.information(self, "Not found", "Patient not found")
                self.clear_button_clicked()
        except ValueError:
            QMessageBox.information(self, "Error", "Please enter a valid PHN format")
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
        self.text_phn.setEnabled(False)
        self.text_name.setEnabled(False)
        self.text_birth_date.setEnabled(False)
        self.text_phone.setEnabled(False)
        self.text_email.setEnabled(False)
        self.text_address.setEnabled(False)
        self.delete_button.setEnabled(False)