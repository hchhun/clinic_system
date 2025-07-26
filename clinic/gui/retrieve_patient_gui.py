import sys
from PyQt6.QtCore import Qt
from PyQt6.QtCore import QAbstractTableModel, Qt, QModelIndex
from PyQt6.QtWidgets import QMainWindow, QDialogButtonBox, QTableView
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtWidgets import QGridLayout, QVBoxLayout, QFormLayout

from clinic.exception.illegal_operation_exception import IllegalOperationException

from clinic.controller import Controller
# GUI for displaying patient info when table is clicked
class PatientInfoGUI(QMainWindow):
    def __init__(self, controller, parent):
        super().__init__()
        self.controller = controller
        self.parent = parent
        self.resize(300, 200)
        self.setWindowTitle("Patient's information")

        layout = QVBoxLayout()
        outputLayout = QGridLayout()
        close_button = QPushButton("Close")

        # display fields
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

        # filling display fields
        self.text_phn.setText(f"{self.parent.current_phn}")
        self.text_name.setText(self.parent.current_name)
        self.text_birth_date.setText(self.parent.current_birth_date)
        self.text_phone.setText(self.parent.current_phone)
        self.text_email.setText(self.parent.current_email)
        self.text_address.setText(self.parent.current_address)

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
        close_button.clicked.connect(self.close_button_clicked)

        layout.addLayout(outputLayout)
        layout.addWidget(close_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def close_button_clicked(self):
        self.clear_button_clicked()
        self.hide()

    def clear_button_clicked(self):
        self.text_phn.setText("")
        self.text_name.setText("")
        self.text_birth_date.setText("")
        self.text_phone.setText("")
        self.text_email.setText("")
        self.text_address.setText("")

class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        if self._data:
            return len(self._data[0])
        else:
            return 0

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        headers = ["PHN", "Name", "Birth date", "Phone", "Email", "Address"]

        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return '%s' % headers[section]
        return super().headerData(section, orientation, role)

class RetrievePatientGUI(QMainWindow):
    def __init__(self, controller, parent):
        super().__init__()
        self.controller = controller
        self.parent = parent
        self.setWindowTitle("Retrieve patient by name")

        # storing for use in PatientInfoGUI
        self.current_phn = None
        self.current_name = None
        self.current_birth_date = None
        self.current_phone = None
        self.current_email = None
        self.current_address = None

        self.patientInfo = PatientInfoGUI(self.controller, parent=self)
        self.resize(600, 400)
        self.table = QTableView()
        self.data = []

        # setting up layout
        layout = QVBoxLayout()
        searchLayout = QFormLayout()
        self.text_search_name = QLineEdit()
        self.text_search_name.setPlaceholderText("Enter name")
        spacer = QWidget()
        spacer.setFixedSize(10, 10)

        searchLayout.addRow("Search by name", self.text_search_name)

        # button box at bottom of window
        self.button_box = QDialogButtonBox()
        self.button_box.addButton("Back", QDialogButtonBox.ButtonRole.ResetRole)
        self.button_box.addButton("Clear", QDialogButtonBox.ButtonRole.AcceptRole)
        self.retrieve_button = self.button_box.addButton("Retrieve patients", QDialogButtonBox.ButtonRole.AcceptRole)
        self.button_box.clicked.connect(self.handle_button_clicked)

        self.model = TableModel(self.data)
        self.table.setModel(self.model)

        layout.addWidget(spacer)
        layout.addLayout(searchLayout)
        layout.addWidget(spacer)
        layout.addWidget(self.table)
        layout.addWidget(self.button_box)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
    
    # refreshes table data
    def refresh_data(self):
        self.data = []
        found = self.controller.retrieve_patients(self.text_search_name.text()) # only stores matching patients
        if found != []:
            for person in found:
                temp = [person.phn, person.name, person.birth_date, person.phone, person.email, person.address]
                self.data.append(temp)
        else:
            QMessageBox.information(self, "Not found", "No patient found")
            self.clear_button_clicked()

    # storing the respective infos when table is clicked
    def list_patient_info(self, index:QModelIndex):
        row = index.row()
        self.current_phn = index.sibling(index.row(), 0).data()
        self.current_name = index.sibling(index.row(), 1).data()
        self.current_birth_date = index.sibling(index.row(), 2).data()
        self.current_phone = index.sibling(index.row(), 3).data()
        self.current_email = index.sibling(index.row(), 4).data()
        self.current_address = index.sibling(index.row(), 5).data()
        self.patientInfo = PatientInfoGUI(self.controller, parent=self)
        self.patientInfo.show()
    
    # handles actions for which button is clicked
    def handle_button_clicked(self, button):
        clicked = button.text()

        if clicked == "Retrieve patients": # refreshes the data and fills table
            self.refresh_data()
            self.model = TableModel(self.data)
            self.table.setModel(self.model)
            if self.data != []:
                self.table.doubleClicked.connect(self.list_patient_info)
                self.text_search_name.setEnabled(False)
                self.retrieve_button.setEnabled(False)

        elif clicked == "Clear":
            self.clear_button_clicked()
        else:
            self.hide()
            self.parent.show()
            self.clear_button_clicked()
            self.patientInfo.clear_button_clicked()
            self.patientInfo.hide()

    # resetting the GUI
    def clear_button_clicked(self):
        self.data = []
        self.model = TableModel(self.data)
        self.table.setModel(self.model)
        self.text_search_name.setText("")
        self.text_search_name.setEnabled(True)
        self.retrieve_button.setEnabled(True)