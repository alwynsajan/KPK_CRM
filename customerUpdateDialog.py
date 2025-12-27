from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QHBoxLayout, QMessageBox, QFrame,
    QWidget, QRadioButton, QButtonGroup, QGridLayout
)
from PySide6.QtCore import Qt, Signal
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
                padding: 10px 16px;
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
                font-weight: 400;
            }
        """)

# ------------------- Modern Button -------------------
class ModernButton(QPushButton):
    def __init__(self, text, style_type="primary", width=None):
        super().__init__(text)
        self.setFixedHeight(40)
        if width:
            self.setFixedWidth(width)
        self.setCursor(Qt.PointingHandCursor)
        
        styles = {
            "primary": """
                QPushButton {
                    background-color: #4A90E2;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 0px 24px;
                    font-size: 14px;
                    font-weight: 600;
                    min-width: 120px;
                }
                QPushButton:hover {
                    background-color: #3182CE;
                }
                QPushButton:pressed {
                    background-color: #2C5282;
                }
            """,
            "danger": """
                QPushButton {
                    background-color: #E53E3E;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 0px 24px;
                    font-size: 14px;
                    font-weight: 600;
                    min-width: 140px;
                }
                QPushButton:hover {
                    background-color: #C53030;
                }
                QPushButton:pressed {
                    background-color: #9B2C2C;
                }
            """,
            "secondary": """
                QPushButton {
                    background-color: #EDF2F7;
                    color: #4A5568;
                    border: 1px solid #CBD5E0;
                    border-radius: 8px;
                    padding: 0px 24px;
                    font-size: 14px;
                    font-weight: 600;
                    min-width: 100px;
                }
                QPushButton:hover {
                    background-color: #E2E8F0;
                    border-color: #A0AEC0;
                }
            """
        }
        
        self.setStyleSheet(styles.get(style_type, styles["primary"]))

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
                width: 18px;
                height: 18px;
                border-radius: 9px;
                border: 2px solid #CBD5E0;
                background-color: white;
            }
            QRadioButton::indicator:checked {
                background-color: #4A90E2;
                border-color: #4A90E2;
            }
            QRadioButton:hover::indicator {
                border-color: #A0AEC0;
            }
        """)

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

# ------------------- Card Frame -------------------
class CardFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #E2E8F0;
            }
        """)

class CustomerUpdateDialog(QDialog):
    # Signal to emit when customer is updated
    customerUpdated = Signal(dict)
    
    def __init__(self, parent=None, customerData=None):
        super().__init__(parent)
        
        self.parent = parent  # Store parent reference for signal
        self.customerData = customerData or {}
        self.customerID = customerData.get("customerID", "") if customerData else ""
        self.originalName = customerData.get("name", "") if customerData else ""
        self.db = DbClient()
        
        self.setWindowTitle(f"Update Customer: {customerData.get('name', '')}")
        
        # Set window size - wider but shorter
        screen = self.screen().availableGeometry()
        width = min(int(screen.width() * 0.5), 600)  # Wider
        height = min(int(screen.height() * 0.55), 600)  # Slightly taller for buttons
        self.resize(width, height)
        
        # Center the window
        self.move(
            screen.left() + (screen.width() - width) // 2,
            screen.top() + (screen.height() - height) // 5
        )
        
        # Modern window styling
        self.setStyleSheet("""
            QDialog {
                background-color: #F7FAFC;
                color: #2D3748;
                font-family: 'Segoe UI', 'Inter', -apple-system, sans-serif;
            }
        """)
        
        self.initUI()
        self.populateFields()

    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(16)

        # Create main card with grid layout
        card = CardFrame()
        grid_layout = QGridLayout(card)
        grid_layout.setContentsMargins(20, 20, 20, 20)
        grid_layout.setVerticalSpacing(16)
        grid_layout.setHorizontalSpacing(20)
        
        # Row 0: Name (Full width)
        grid_layout.addWidget(ModernLabel("Customer Name", required=True), 0, 0, 1, 2)
        self.nameInput = ModernLineEdit("Enter customer name")
        grid_layout.addWidget(self.nameInput, 1, 0, 1, 2)
        
        # Row 1: Customer Type (Full width)
        grid_layout.addWidget(ModernLabel("Customer Type"), 2, 0, 1, 2)
        
        type_widget = QWidget()
        type_layout = QHBoxLayout(type_widget)
        type_layout.setContentsMargins(0, 0, 0, 0)
        type_layout.setSpacing(24)
        
        self.personalRadio = ModernRadioButton("Personal")
        self.businessRadio = ModernRadioButton("Business")
        
        self.typeGroup = QButtonGroup(self)
        self.typeGroup.addButton(self.personalRadio)
        self.typeGroup.addButton(self.businessRadio)
        self.typeGroup.setExclusive(True)
        
        type_layout.addWidget(self.personalRadio)
        type_layout.addWidget(self.businessRadio)
        type_layout.addStretch()
        
        grid_layout.addWidget(type_widget, 3, 0, 1, 2)
        
        # Row 2: Email and Phone
        grid_layout.addWidget(ModernLabel("Email"), 4, 0)
        grid_layout.addWidget(ModernLabel("Phone"), 4, 1)
        
        self.emailInput = ModernLineEdit("email@example.com")
        self.phoneInput = ModernLineEdit("(123) 456-7890")
        
        grid_layout.addWidget(self.emailInput, 5, 0)
        grid_layout.addWidget(self.phoneInput, 5, 1)
        
        # Row 3: Address (Full width)
        grid_layout.addWidget(ModernLabel("Address"), 6, 0, 1, 2)
        self.addressInput = ModernLineEdit("Street address")
        grid_layout.addWidget(self.addressInput, 7, 0, 1, 2)
        
        # Row 4: State and Postcode
        grid_layout.addWidget(ModernLabel("State"), 8, 0)
        grid_layout.addWidget(ModernLabel("Postcode"), 8, 1)
        
        self.stateInput = ModernLineEdit("State")
        self.postcodeInput = ModernLineEdit("Postcode")
        
        grid_layout.addWidget(self.stateInput, 9, 0)
        grid_layout.addWidget(self.postcodeInput, 9, 1)
        
        # Row 5: ABN (Full width)
        grid_layout.addWidget(ModernLabel("ABN"), 10, 0, 1, 2)
        self.abnInput = ModernLineEdit("11 222 333 444")
        grid_layout.addWidget(self.abnInput, 11, 0, 1, 2)
        
        # Add card to main layout
        main_layout.addWidget(card)

        # --- Button Container ---
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(12)
        
        # Add stretch on left
        button_layout.addStretch()
        
        # Delete button in middle
        self.deleteBtn = ModernButton("Delete Customer", "danger", width=150)
        self.deleteBtn.clicked.connect(self.deleteCustomer)
        button_layout.addWidget(self.deleteBtn)
        
        button_layout.addStretch()
        
        # Cancel button
        self.cancelBtn = ModernButton("Cancel", "secondary", width=100)
        self.cancelBtn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancelBtn)
        
        # Save button
        self.saveBtn = ModernButton("Save Changes", "primary", width=140)
        self.saveBtn.clicked.connect(self.saveCustomer)
        button_layout.addWidget(self.saveBtn)
        
        button_layout.addStretch()
        
        main_layout.addWidget(button_container)

    def populateFields(self):
        """Populate form fields with existing customer data"""
        if not self.customerData:
            return
        
        # Name
        self.nameInput.setText(self.customerData.get("name", ""))
        
        # Customer Type
        customer_type = self.customerData.get("customerType", "Personal")
        if customer_type.lower() == "business":
            self.businessRadio.setChecked(True)
        else:
            self.personalRadio.setChecked(True)
        
        # Email
        self.emailInput.setText(self.customerData.get("email", ""))
        
        # Phone
        self.phoneInput.setText(self.customerData.get("phone", ""))
        
        # Address
        self.addressInput.setText(self.customerData.get("address", ""))
        
        # State
        self.stateInput.setText(self.customerData.get("state", ""))
        
        # Postcode
        self.postcodeInput.setText(self.customerData.get("postcode", ""))
        
        # ABN
        self.abnInput.setText(self.customerData.get("ABN", ""))

    def validateForm(self):
        """Validate form inputs"""
        errors = []
        
        # Name validation
        name = self.nameInput.text().strip()
        if not name:
            errors.append("Customer name is required")
            self.nameInput.setStyleSheet("""
                QLineEdit {
                    background-color: #FFFFFF;
                    color: #2D3748;
                    border: 2px solid #E53E3E;
                    border-radius: 8px;
                    padding: 10px 16px;
                    font-size: 14px;
                }
                QLineEdit:focus {
                    border: 2px solid #E53E3E;
                }
            """)
            self.nameInput.setFocus()
        else:
            self.nameInput.setStyleSheet(ModernLineEdit().styleSheet())
            
            # Check for duplicate name (only if name changed)
            if name.lower() != self.originalName.lower():
    
                existingCustomers = self.db.getCustomerName()  # [(id, name), ...]
                existingNames = [custName.lower() for _, custName in existingCustomers]
                
                if name.lower() in existingNames:
                    errors.append(f"A customer with the name '{name}' already exists")
                    self.nameInput.setStyleSheet("""
                        QLineEdit {
                            background-color: #FFFFFF;
                            color: #2D3748;
                            border: 2px solid #E53E3E;
                            border-radius: 8px;
                            padding: 10px 16px;
                            font-size: 14px;
                        }
                        QLineEdit:focus {
                            border: 2px solid #E53E3E;
                        }
                    """)
                    self.nameInput.setFocus()
                    self.nameInput.selectAll()
        
        return errors

    def saveCustomer(self):
        """Save updated customer details"""
        # Validate form
        errors = self.validateForm()
        if errors:
            QMessageBox.warning(
                self,
                "Validation Error",
                "Please fix the following errors:\n\n• " + "\n• ".join(errors)
            )
            return
        
        # Collect form data
        customer_type = "Business" if self.businessRadio.isChecked() else "Personal"
        new_name = self.nameInput.text().strip()
        
        # Final duplicate check (just in case)
        if new_name.lower() != self.originalName.lower():
            existingCustomers = self.db.getCustomerName()
            existingNames = [custName.lower() for _, custName in existingCustomers]
            
            if new_name.lower() in existingNames:
                QMessageBox.critical(
                    self,
                    "Duplicate Customer",
                    f"A customer with the name '{new_name}' already exists.\n\nPlease use a different name."
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
        
        updated_data = {
            "customerID": self.customerID,
            "name": new_name,
            "customerType": customer_type,
            "email": self.emailInput.text().strip(),
            "phone": self.phoneInput.text().strip(),
            "address": self.addressInput.text().strip(),
            "state": self.stateInput.text().strip(),
            "postcode": self.postcodeInput.text().strip(),
            "ABN": self.abnInput.text().strip()
        }
        
        # Update database
        response = self.db.updateCustomerData(self.customerID, updated_data)
        
        if response["status"] == "Success":
            # Check if name was changed
            if new_name != self.originalName:
                # Emit signal to parent with updated data
                if self.parent and hasattr(self.parent, 'customerAdded'):
                    self.parent.customerAdded.emit(updated_data)
            
            # Update the customer data dictionary with new values
            self.customerData.update(updated_data)
            
            # Close dialog
            self.accept()
        else:
            QMessageBox.critical(
                self,
                "Database Error",
                f"Failed to update customer.\n\nError: {response.get('message', 'Unknown error')}"
            )

    def deleteCustomer(self):
        """Delete the customer from database"""
        # Check if customer has any sales first
        sales_check = self.db.getCustomerSalesHistory(self.customerData.get('customerID', ''))
        
        if sales_check:
            QMessageBox.warning(
                self,
                "Cannot Delete",
                f"Cannot delete customer '{self.customerData.get('name', '')}' because they have existing sales records."
            )
            return
        
        reply = QMessageBox.question(
            self,
            "Delete Customer",
            f"Are you sure you want to delete customer '{self.customerData.get('name', '')}'?\n\nThis action cannot be undone.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.No:
            return
        
        
        
        # Delete customer from database
        response = self.db.deleteCustomerData(self.customerID)
        
        if response["status"] == "Success":

            # Clear customer data
            self.customerData.clear()
            
            # Close dialog
            self.accept()
        else:
            QMessageBox.critical(
                self,
                "Delete Failed",
                f"Failed to delete customer.\n\nError: {response.get('message', 'Unknown error')}"
            )

# Utility function to open the dialog
def openCustomerUpdateDialog(parent, customerData):
    """Open customer update dialog"""
    if not customerData:
        QMessageBox.warning(
            parent,
            "No Customer Selected",
            "Please select a customer first."
        )
        return
    
    dialog = CustomerUpdateDialog(parent, customerData)
    dialog.exec()