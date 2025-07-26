import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QDialogButtonBox
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QGroupBox
from PyQt6.QtWidgets import QVBoxLayout, QComboBox, QListWidget, QMessageBox

from clinic.gui.add_note_gui import AddNoteGUI
from clinic.gui.retrieve_note_gui import RetrieveNoteGUI
from clinic.gui.update_note_gui import UpdateNoteGUI
from clinic.gui.delete_note_gui import DeleteNoteGUI
from clinic.gui.list_note_gui import ListNoteGUI

from clinic.exception.illegal_operation_exception import IllegalOperationException

from clinic.controller import Controller
# GUI for selected patient's appointment
class CurrPatientGUI(QMainWindow):
    def __init__(self, controller, parent):
        super().__init__()
        self.controller = controller
        self.parent = parent
        self.resize(600, 400)
        self.setWindowTitle("Current appointment")

        # action GUIs
        self.add_note = AddNoteGUI(controller, parent=self)
        self.retrieve_note = RetrieveNoteGUI(controller, parent=self)
        self.update_note = UpdateNoteGUI(controller, parent=self)
        self.delete_note = DeleteNoteGUI(controller, parent=self)
        self.list_note = ListNoteGUI(controller, parent=self)
        
        self.action_list = (["Add note to patient record", "Retrieve notes from patient record by text", "Change note from patient record", \
        "Remove note from patient record", "List full patient record"])

        userLayout = QVBoxLayout()
        if self.parent.setted is not None:
            # setting up layout
            welcome = f"Patient: {self.parent.setted.name}"
            welcome_label = QLabel(welcome)
            font = welcome_label.font()
            font.setPointSize(35)
            font.setBold(True)
            welcome_label.setFont(font) 
            spacer = QWidget()
            spacer.setFixedSize(10, 20)

            # patient info display
            text_patient = \
            f"PHN:\t\t{self.parent.setted.phn}\nBirth date:\t{self.parent.setted.birth_date}\nPhone:\t\t{self.parent.setted.phone}\nEmail:\t\t{self.parent.setted.email}\nAddress:\t\t{self.parent.setted.address}"
            label_patient = QLabel(text_patient)

            self.button_box = QDialogButtonBox()
            self.button_box.addButton("End appointment", QDialogButtonBox.ButtonRole.AcceptRole)

            # setting up layout
            userLayout = QVBoxLayout()
            actionGroupBox = QGroupBox("Select an action to perform with the patient's record")
            selectLayout = QHBoxLayout()
            select = QListWidget()
            select.addItems(self.action_list)
            selectLayout.addWidget(select)
            actionGroupBox.setLayout(selectLayout)

            select.itemDoubleClicked.connect(self.select_clicked)
            self.button_box.clicked.connect(self.handle_button_clicked)

            userLayout.addWidget(welcome_label)
            userLayout.addWidget(label_patient)
            userLayout.addWidget(spacer)
            userLayout.addWidget(actionGroupBox)
            userLayout.addWidget(self.button_box)

        widget = QWidget()
        widget.setLayout(userLayout)
        self.setCentralWidget(widget)

    # handles the actions to be performed
    def select_clicked(self, i):
        self.hide()
        action = i.text()
        if action == self.action_list[0]:
            self.add_note.show()
        elif action == self.action_list[1]:
            self.retrieve_note.show()
        elif action == self.action_list[2]:
            self.update_note.show()
        elif action == self.action_list[3]:
            self.delete_note.show()
        elif action == self.action_list[4]:
            self.list_note.refresh_data()
            self.list_note.show()

    # end appointment button
    def handle_button_clicked(self):
        self.controller.unset_current_patient()
        self.hide()
        self.parent.parent.show()

# GUI for selecting which patient to start an appointment with
class AppPatientGUI(QMainWindow):
    def __init__(self, controller, parent):
        super().__init__()
        self.controller = controller
        self.parent = parent
        self.resize(300, 100)
        self.setWindowTitle("Start appointment with patient")

        self.data = []
        self.setted = None

        self.curr = CurrPatientGUI(self.controller, parent=self)

        # setting up layout
        layout = QVBoxLayout()
        button_box = QHBoxLayout()
        ok_button = QPushButton("Ok")
        cancel_button = QPushButton("Cancel")

        ok_button.clicked.connect(self.ok_button_clicked)
        cancel_button.clicked.connect(self.cancel_button_clicked)

        label_info = QLabel("Enter the patient's PHN")
        self.select_phn = QComboBox()
        self.select_phn.setEditable(True)

        layout.addWidget(label_info)
        layout.addWidget(self.select_phn)
        button_box.addWidget(ok_button)
        button_box.addWidget(cancel_button)
        layout.addLayout(button_box)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    # refreshes phn selection
    def refresh_data(self):
        self.select_phn.clear()
        self.data = []
        found = self.controller.list_patients()
        for person in found:
            self.data.append(f"{person.phn}")
        
        self.select_phn.addItems(self.data)

    # sets current patient and starts appointment
    def ok_button_clicked(self):
        try:
            self.controller.set_current_patient(int(self.select_phn.currentText()))
            self.setted = self.controller.get_current_patient()
            self.curr = CurrPatientGUI(self.controller, parent=self)
            self.parent.hide()
            self.hide()
            self.curr.show()
        except ValueError:
            QMessageBox.information(self, "Error", "Please enter a valid PHN format")
        except:
            QMessageBox.information(self, "Error", "Patient not found")

    def cancel_button_clicked(self):
        self.hide()