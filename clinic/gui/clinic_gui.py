import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialogButtonBox
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout, QGroupBox
from PyQt6.QtWidgets import QVBoxLayout, QListWidget, QFormLayout

from clinic.gui.add_patient_gui import AddPatientGUI
from clinic.gui.search_patient_gui import SearchPatientGUI
from clinic.gui.retrieve_patient_gui import RetrievePatientGUI
from clinic.gui.update_patient_gui import UpdatePatientGUI
from clinic.gui.delete_patient_gui import DeletePatientGUI
from clinic.gui.list_patient_gui import ListPatientGUI
from clinic.gui.appointment_gui import AppPatientGUI

from clinic.exception.illegal_operation_exception import IllegalOperationException

from clinic.controller import Controller

# main GUI after logging in
class ClinicGUI(QMainWindow):
    def __init__(self, controller, parent):
        super().__init__()
        self.controller = controller
        self.parent = parent

        # action GUIs
        self.add = AddPatientGUI(controller, parent=self)
        self.search = SearchPatientGUI(controller, parent=self)
        self.retrieve = RetrievePatientGUI(controller, parent=self)
        self.update = UpdatePatientGUI(controller, parent=self)
        self.delete = DeletePatientGUI(controller, parent=self)
        self.list = ListPatientGUI(controller, parent=self)
        self.app = AppPatientGUI(controller, parent=self)
        self.resize(600, 400)
        self.setWindowTitle("Medical Clinic System")
        
        self.action_list = (["Add new patient", "Search patient by PHN", "Retrieve patients by name", \
        "Change patient data", "Remove patient", "List all patients", "Start appointment with patient"])

        # setting up layout
        welcome = f"Welcome, {self.parent.text_username.text()}"
        welcome_label = QLabel(welcome)
        font = welcome_label.font()
        font.setPointSize(35)
        font.setBold(True)
        welcome_label.setFont(font) 
        spacer = QWidget()
        spacer.setFixedSize(10, 20)

        # button box at bottom of window
        self.button_box = QDialogButtonBox()
        self.button_box.addButton("Quit", QDialogButtonBox.ButtonRole.AcceptRole)
        self.button_box.addButton("Log out", QDialogButtonBox.ButtonRole.AcceptRole)

        userLayout = QVBoxLayout()
        actionGroupBox = QGroupBox("What would you like to do today?")
        selectLayout = QHBoxLayout()
        select = QListWidget()
        select.addItems(self.action_list)
        selectLayout.addWidget(select)
        actionGroupBox.setLayout(selectLayout)

        select.itemDoubleClicked.connect(self.select_clicked)
        self.button_box.clicked.connect(self.handle_button_clicked)

        userLayout.addWidget(welcome_label)
        userLayout.addWidget(spacer)
        userLayout.addWidget(actionGroupBox)
        userLayout.addWidget(self.button_box)

        widget = QWidget()
        widget.setLayout(userLayout)
        self.setCentralWidget(widget)

    # handles the actions to be performed
    def select_clicked(self, i):
        action = i.text()
        if action == self.action_list[0]:
            self.hide()
            self.add.show()
        elif action == self.action_list[1]:
            self.hide()
            self.search.show()
        elif action == self.action_list[2]:
            self.hide()
            self.retrieve.show()
        elif action == self.action_list[3]:
            self.hide()
            self.update.show()
        elif action == self.action_list[4]:
            self.hide()
            self.delete.show()
        elif action == self.action_list[5]:
            self.hide()
            self.list.refresh_data()
            self.list.show()
        elif action == self.action_list[6]:
            self.app.refresh_data()
            self.app.show()
        else:
            self.show()

    # handles the actions for which button is clicked
    def handle_button_clicked(self, button):
        clicked = button.text()

        if clicked == "Log out":
            self.controller.logout() # logs out
            self.hide()
            self.parent.show()
        elif clicked == "Quit":
            self.controller.logout() # logs out
            QApplication.quit()

class LoginGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.controller = Controller(autosave=True)
        self.setWindowTitle("Medical Clinic System")

        self.text_username = QLineEdit()
        self.text_password = QLineEdit()
        self.text_password.setEchoMode(QLineEdit.EchoMode.Password)
        login_button = QPushButton("Log in")
        quit_button = QPushButton("Quit")

        self.clinicWindow = ClinicGUI(self.controller, parent=self)

        # setting up layout
        outerLayout = QVBoxLayout()
        loginLayout = QFormLayout()
        buttonBox = QHBoxLayout()

        loginLayout.addRow("Username: ", self.text_username)
        loginLayout.addRow("Password: ", self.text_password)
        buttonBox.addWidget(login_button)
        buttonBox.addWidget(quit_button)
        
        outerLayout.addLayout(loginLayout)
        outerLayout.addLayout(buttonBox)

        widget = QWidget()
        widget.setLayout(outerLayout)
        self.setCentralWidget(widget)

        login_button.clicked.connect(self.login_button_clicked)
        quit_button.clicked.connect(self.quit_button_clicked)

    def login_button_clicked(self):
        try:
            self.controller.login(self.text_username.text(), self.text_password.text()) # logs in
            QMessageBox.information(self, "Log in Status", "Logged in successfully!")
            self.clinicWindow = ClinicGUI(self.controller, parent=self)
            self.hide()
            self.clinicWindow.show()
        except:
            QMessageBox.information(self, "Log in Status", "Incorrect username or password")
        
        self.text_username.setText("")
        self.text_password.setText("")

    def quit_button_clicked(self):
        QApplication.quit()

def main():
    app = QApplication(sys.argv)
    window = LoginGUI()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()
