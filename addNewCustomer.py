from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QRadioButton, QMessageBox
)
from dbClient import DbClient


class CustomerForm(QWidget):
    def __init__(self, selectedCustomerDetails, callback):
        super().__init__()

        self.selectedCustomerDetails = selectedCustomerDetails
        self.callback = callback

        self.setWindowTitle("Add Customer")
        self.setFixedWidth(400)

        # Parent background
        self.setStyleSheet("""
            background-color: #EBE8DB; 
            color: black;               
        """)

        layout = QVBoxLayout()
        layout.setSpacing(10)

        # Common input style
        inputStyle = """
            QLineEdit {
                background-color: #FFFFFF;
                color: black;
                border: 1px solid #ccc;
                border-radius: 6px;
                padding-left: 5px;
                height: 28px;
            }
        """

        # ------- Name (Required) -------
        layout.addWidget(QLabel("Customer Name *"))
        self.nameInput = QLineEdit()
        self.nameInput.setPlaceholderText("Enter name (required)")
        self.nameInput.setStyleSheet(inputStyle)
        layout.addWidget(self.nameInput)

        # ------- Customer Type -------
        layout.addWidget(QLabel("Customer Type"))
        typeLayout = QHBoxLayout()

        self.businessRadio = QRadioButton("Business")
        self.personalRadio = QRadioButton("Personal")
        self.personalRadio.setChecked(True)

        # Radio button style
        radioStyle = """
            QRadioButton {
                font-size: 14px;
                color: black;
            }
            QRadioButton::indicator {
                width: 18px;
                height: 18px;
                border-radius: 9px;
                background-color: #cccccc;  /* default grey */
                border: 1px solid #999999;
            }
            QRadioButton::indicator:checked {
                background-color: #3498DB;  /* blue when selected */
                border: 1px solid #2980B9;
            }
        """
        self.businessRadio.setStyleSheet(radioStyle)
        self.personalRadio.setStyleSheet(radioStyle)

        typeLayout.addWidget(self.businessRadio)
        typeLayout.addWidget(self.personalRadio)
        layout.addLayout(typeLayout)

        # ------- Email -------
        layout.addWidget(QLabel("Email"))
        self.emailInput = QLineEdit()
        self.emailInput.setPlaceholderText("Enter email")
        self.emailInput.setStyleSheet(inputStyle)
        layout.addWidget(self.emailInput)

        # ------- Phone -------
        layout.addWidget(QLabel("Phone"))
        self.phoneInput = QLineEdit()
        self.phoneInput.setPlaceholderText("Enter phone number")
        self.phoneInput.setStyleSheet(inputStyle)
        layout.addWidget(self.phoneInput)

        # ------- Address -------
        layout.addWidget(QLabel("Address"))
        self.addressInput = QLineEdit()
        self.addressInput.setPlaceholderText("Enter address")
        self.addressInput.setStyleSheet(inputStyle)
        layout.addWidget(self.addressInput)

        # ------- State -------
        layout.addWidget(QLabel("State"))
        self.stateInput = QLineEdit()
        self.stateInput.setPlaceholderText("Enter state")
        self.stateInput.setStyleSheet(inputStyle)
        layout.addWidget(self.stateInput)

        # ------- Postcode -------
        layout.addWidget(QLabel("Postcode"))
        self.postcodeInput = QLineEdit()
        self.postcodeInput.setPlaceholderText("Enter postcode")
        self.postcodeInput.setStyleSheet(inputStyle)
        layout.addWidget(self.postcodeInput)

        # ------- ABN -------
        layout.addWidget(QLabel("ABN"))
        self.abnInput = QLineEdit()
        self.abnInput.setPlaceholderText("Enter ABN")
        self.abnInput.setStyleSheet(inputStyle)
        layout.addWidget(self.abnInput)

        # ------- Save Button -------
        self.saveBtn = QPushButton("Save Customer")
        self.saveBtn.setStyleSheet("""
            QPushButton {
                background-color: #3498DB;
                color: white;
                padding: 8px 15px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2E86C1;
            }
        """)
        self.saveBtn.clicked.connect(self.saveCustomer)
        layout.addWidget(self.saveBtn)

        self.setLayout(layout)

    def saveCustomer(self):
        name = self.nameInput.text().strip()
        if not name:
            QMessageBox.warning(self, "Missing Name", "Customer name is required.")
            return

        customerType = "Business" if self.businessRadio.isChecked() else "Personal"

        customerData = {
            "name": name,
            "customerType": customerType,
            "email": self.emailInput.text().strip(),
            "phone": self.phoneInput.text().strip(),
            "address": self.addressInput.text().strip(),
            "state": self.stateInput.text().strip(),
            "postcode": self.postcodeInput.text().strip(),
            "ABN": self.abnInput.text().strip(),
        }

        db = DbClient()
        response = db.addCustomerData(customerData)

        if response["status"] != "Success":
            QMessageBox.critical(self, "Database Error", response["message"])
            return

        # Update selected customer
        self.selectedCustomerDetails.clear()
        self.selectedCustomerDetails.update({
            "name": name,
            "address": customerData["address"],
            "phone": customerData["phone"]
        })

        # Refresh main UI
        self.callback()
        self.close()
