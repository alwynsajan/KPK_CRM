from PySide6.QtWidgets import  QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QRadioButton, QWidget

# ------------------- Customer Form Window -------------------
class CustomerForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Customer")
        self.setFixedWidth(400)

        layout = QVBoxLayout()
        layout.setSpacing(10)

        # ------- Name (Required) -------
        layout.addWidget(QLabel("Customer Name *"))
        self.nameInput = QLineEdit()
        self.nameInput.setPlaceholderText("Enter name (required)")
        layout.addWidget(self.nameInput)

        # ------- Customer Type (Radio Buttons) -------
        layout.addWidget(QLabel("Customer Type"))
        typeLayout = QHBoxLayout()

        self.businessRadio = QRadioButton("Business")
        self.personalRadio = QRadioButton("Personal")
        self.personalRadio.setChecked(True)

        typeLayout.addWidget(self.businessRadio)
        typeLayout.addWidget(self.personalRadio)

        layout.addLayout(typeLayout)

        # ------- Email -------
        layout.addWidget(QLabel("Email"))
        self.emailInput = QLineEdit()
        self.emailInput.setPlaceholderText("Enter email")
        layout.addWidget(self.emailInput)

        # ------- Phone -------
        layout.addWidget(QLabel("Phone"))
        self.phoneInput = QLineEdit()
        self.phoneInput.setPlaceholderText("Enter phone number")
        layout.addWidget(self.phoneInput)

        # ------- Address -------
        layout.addWidget(QLabel("Address"))
        self.addressInput = QLineEdit()
        self.addressInput.setPlaceholderText("Enter address")
        layout.addWidget(self.addressInput)

        # ------- State -------
        layout.addWidget(QLabel("State"))
        self.stateInput = QLineEdit()
        self.stateInput.setPlaceholderText("Enter state")
        layout.addWidget(self.stateInput)

        # ------- Postcode -------
        layout.addWidget(QLabel("Postcode"))
        self.postcodeInput = QLineEdit()
        self.postcodeInput.setPlaceholderText("Enter postcode")
        layout.addWidget(self.postcodeInput)

        # ------- ABN -------
        layout.addWidget(QLabel("ABN"))
        self.abnInput = QLineEdit()
        self.abnInput.setPlaceholderText("Enter ABN")
        layout.addWidget(self.abnInput)

        # ------- Save Button -------
        self.saveBtn = QPushButton("Save Customer")
        self.saveBtn.setStyleSheet("""
            QPushButton {
                background-color: #3498DB;
                color: white;
                padding: 6px 15px;
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
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Missing Name", "Customer name is required.")
            return

        customerType = "Business" if self.businessRadio.isChecked() else "Personal"

        # Collect all data
        self.customerData = {
            "name": name,
            "type": customerType,
            "email": self.emailInput.text().strip(),
            "phone": self.phoneInput.text().strip(),
            "address": self.addressInput.text().strip(),
            "state": self.stateInput.text().strip(),
            "postcode": self.postcodeInput.text().strip(),
            "abn": self.abnInput.text().strip(),
        }

        print(self.customerData)  

        self.close()  # Close the form window
