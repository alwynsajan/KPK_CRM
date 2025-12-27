from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QRadioButton, QMessageBox,
    QFrame, QGroupBox, QGridLayout
)
from PySide6.QtCore import Signal, Qt
from dbClient import DbClient

# ------------------- Modern Line Edit -------------------
class ModernLineEdit(QLineEdit):
    def __init__(self, placeholder=""):
        super().__init__()
        self.setPlaceholderText(placeholder)
        self.setFixedHeight(40)
        self.setStyleSheet("""
            QLineEdit {
                background-color: #FFFFFF;
                color: #2D3748;
                border: 1px solid #E2E8F0;
                border-radius: 8px;
                padding: 10px 15px;
                font-size: 14px;
                font-weight: 400;
                selection-background-color: #4A90E2;
            }
            QLineEdit:focus {
                border: 2px solid #4A90E2;
                background-color: #F8FAFC;
                outline: none;
            }
            QLineEdit::placeholder {
                color: #A0AEC0;
            }
        """)

# ------------------- Modern Radio Button -------------------
class ModernRadioButton(QRadioButton):
    def __init__(self, text):
        super().__init__(text)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("""
            QRadioButton {
                font-size: 14px;
                font-weight: 500;
                color: #2D3748;
                background-color: transparent;
                padding: 8px 4px;
                spacing: 10px;
            }
            QRadioButton::indicator {
                width: 20px;
                height: 20px;
                border-radius: 10px;
                border: 2px solid #CBD5E0;
                background-color: white;
            }
            QRadioButton::indicator:checked {
                background-color: #4A90E2;
                border-color: #4A90E2;
            }
            QRadioButton::indicator:checked::after {
                width: 8px;
                height: 8px;
                border-radius: 4px;
                background-color: white;
                margin: 4px;
            }
            QRadioButton:hover::indicator {
                border-color: #A0AEC0;
            }
        """)

# ------------------- Modern Button -------------------
class ModernButton(QPushButton):
    def __init__(self, text, style_type="primary"):
        super().__init__(text)
        self.setFixedHeight(44)
        self.setCursor(Qt.PointingHandCursor)
        
        styles = {
            "primary": """
                QPushButton {
                    background-color: #4A90E2;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 12px 24px;
                    font-size: 14px;
                    font-weight: 600;
                    letter-spacing: 0.3px;
                }
                QPushButton:hover {
                    background-color: #3182CE;
                }
                QPushButton:pressed {
                    background-color: #2C5282;
                }
                QPushButton:disabled {
                    background-color: #CBD5E0;
                    color: #718096;
                }
            """,
            "secondary": """
                QPushButton {
                    background-color: #EDF2F7;
                    color: #4A5568;
                    border: 1px solid #CBD5E0;
                    border-radius: 8px;
                    padding: 12px 24px;
                    font-size: 14px;
                    font-weight: 600;
                }
                QPushButton:hover {
                    background-color: #E2E8F0;
                    border-color: #A0AEC0;
                }
            """
        }
        
        self.setStyleSheet(styles.get(style_type, styles["primary"]))

# ------------------- Card Frame -------------------
class CardFrame(QFrame):
    def __init__(self, title=None):
        super().__init__()
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #E2E8F0;
            }
        """)
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(16)

# ------------------- Modern Label -------------------
class ModernLabel(QLabel):
    def __init__(self, text, required=False):
        super().__init__(text)
        if required:
            text = f"{text} <span style='color: #E53E3E'>*</span>"
        self.setText(text)
        self.setStyleSheet("""
            QLabel {
                font-size: 13px;
                font-weight: 600;
                color: #2D3748;
                margin-bottom: 4px;
            }
        """)

class CustomerForm(QWidget):
    # ------------------- Signal -------------------
    customerAdded = Signal(dict)   # Emits newly added customer details

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Add New Customer")
        
        # Set window flags for modern look
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)
        
        # Modern window styling
        self.setStyleSheet("""
            QWidget {
                background-color: #F7FAFC;
                color: #2D3748;
                font-family: 'Segoe UI', 'Inter', -apple-system, sans-serif;
            }
        """)

        # --- Window Size ---
        screen = self.screen().availableGeometry()
        self.resize(
            min(int(screen.width() * 0.4), 600),
            min(int(screen.height() * 0.7), 800)
        )

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(20)

        # Title
        title_label = QLabel("Add New Customer")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 22px;
                font-weight: 700;
                color: #2D3748;
                padding: 0px;
                margin-bottom: 8px;
            }
        """)
        main_layout.addWidget(title_label)

        # Description
        description_label = QLabel("Fill in the customer details below. Fields marked with * are required.")
        description_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #718096;
                margin-bottom: 24px;
            }
        """)
        description_label.setWordWrap(True)
        main_layout.addWidget(description_label)

        # Create main card
        card = CardFrame()
        
        # Use grid layout for better alignment
        grid_layout = QGridLayout()
        grid_layout.setVerticalSpacing(16)
        grid_layout.setHorizontalSpacing(24)

        # ------- Name (Required) -------
        grid_layout.addWidget(ModernLabel("Customer Name", required=True), 0, 0)
        self.nameInput = ModernLineEdit("Enter customer name")
        grid_layout.addWidget(self.nameInput, 0, 1)

        # ------- Customer Type -------
        grid_layout.addWidget(ModernLabel("Customer Type"), 1, 0)
        
        type_widget = QWidget()
        type_layout = QHBoxLayout(type_widget)
        type_layout.setContentsMargins(0, 0, 0, 0)
        type_layout.setSpacing(24)
        
        self.personalRadio = ModernRadioButton("Personal")
        self.businessRadio = ModernRadioButton("Business")
        self.personalRadio.setChecked(True)
        
        type_layout.addWidget(self.personalRadio)
        type_layout.addWidget(self.businessRadio)
        type_layout.addStretch()
        
        grid_layout.addWidget(type_widget, 1, 1)

        # ------- Email -------
        grid_layout.addWidget(ModernLabel("Email"), 2, 0)
        self.emailInput = ModernLineEdit("email@gmail.com")
        grid_layout.addWidget(self.emailInput, 2, 1)

        # ------- Phone -------
        grid_layout.addWidget(ModernLabel("Phone"), 3, 0)
        self.phoneInput = ModernLineEdit("04567-89012")
        grid_layout.addWidget(self.phoneInput, 3, 1)

        # ------- Address -------
        grid_layout.addWidget(ModernLabel("Address"), 4, 0)
        self.addressInput = ModernLineEdit("Street address")
        grid_layout.addWidget(self.addressInput, 4, 1)

        # ------- State & Postcode (same row) -------
        grid_layout.addWidget(ModernLabel("State"), 5, 0)
        grid_layout.addWidget(ModernLabel("Postcode"), 5, 1)
        
        state_postcode_widget = QWidget()
        state_postcode_layout = QHBoxLayout(state_postcode_widget)
        state_postcode_layout.setContentsMargins(0, 0, 0, 0)
        state_postcode_layout.setSpacing(16)
        
        self.stateInput = ModernLineEdit("State")
        self.postcodeInput = ModernLineEdit("Postcode")
        
        state_postcode_layout.addWidget(self.stateInput)
        state_postcode_layout.addWidget(self.postcodeInput)
        
        grid_layout.addWidget(state_postcode_widget, 6, 0, 1, 2)

        # ------- ABN -------
        grid_layout.addWidget(ModernLabel("ABN"), 7, 0)
        self.abnInput = ModernLineEdit("11 222 333 444")
        grid_layout.addWidget(self.abnInput, 7, 1)

        # Add grid layout to card
        card.layout.addLayout(grid_layout)
        
        # Add spacer
        card.layout.addStretch()

        main_layout.addWidget(card)

        # ------- Save Button -------
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(12)
        
        # Add stretch to push button to right
        button_layout.addStretch()
        
        self.saveBtn = ModernButton("Save Customer", "primary")
        self.saveBtn.setFixedWidth(180)
        self.saveBtn.clicked.connect(self.saveCustomer)
        button_layout.addWidget(self.saveBtn)
        
        main_layout.addWidget(button_container)

    # ------------------- Save Customer -------------------
    def saveCustomer(self):
        name = self.nameInput.text().strip()
        if not name:
            QMessageBox.warning(self, "Missing Information", 
                              "Customer name is required. Please enter a name.")
            self.nameInput.setStyleSheet("""
                QLineEdit {
                    background-color: #FFFFFF;
                    color: #2D3748;
                    border: 2px solid #E53E3E;
                    border-radius: 8px;
                    padding: 10px 15px;
                    font-size: 14px;
                }
                QLineEdit:focus {
                    border: 2px solid #E53E3E;
                }
            """)
            self.nameInput.setFocus()
            return

        db = DbClient()

        # ---- Duplicate name check ----
        existingCustomers = db.getCustomerName()
        existingNames = [custName.lower() for _, custName in existingCustomers]

        if name.lower() in existingNames:
            QMessageBox.critical(
                self,
                "Duplicate Customer",
                f"A customer with the name '{name}' already exists.\n\nPlease use a different name."
            )
            self.nameInput.setStyleSheet("""
                QLineEdit {
                    background-color: #FFFFFF;
                    color: #2D3748;
                    border: 2px solid #E53E3E;
                    border-radius: 8px;
                    padding: 10px 15px;
                    font-size: 14px;
                }
            """)
            self.nameInput.setFocus()
            self.nameInput.selectAll()
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

        # ---- Insert into DB ----
        response = db.addCustomerData(customerData)

        if response["status"] != "Success":
            QMessageBox.critical(
                self,
                "Database Error",
                "Failed to save customer.\n\nPlease try again or check your connection."
            )
            return

        # Attach generated customerID
        customerData["customerID"] = response["customerID"]

        # Success message
        QMessageBox.information(
            self,
            "Success",
            f"Customer '{name}' has been successfully added!"
        )

        # Emit signal with FULL customer data (including ID)
        self.customerAdded.emit(customerData)

        self.close()