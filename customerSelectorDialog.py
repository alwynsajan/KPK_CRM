from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QListWidget, QPushButton,
    QMessageBox, QLineEdit, QLabel, QFrame, QHBoxLayout,
    QListWidgetItem, QWidget
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon
from dbClient import DbClient

# ------------------- Modern Line Edit with Clear Button -------------------
class ModernSearchLineEdit(QLineEdit):
    def __init__(self, placeholder=""):
        super().__init__()
        self.setPlaceholderText(placeholder)
        self.setFixedHeight(42)
        
        # Create clear button widget
        self.clear_button = QPushButton("✕")
        self.clear_button.setCursor(Qt.PointingHandCursor)
        self.clear_button.setFixedSize(20, 20)
        self.clear_button.setStyleSheet("""
            QPushButton {
                background-color: #CBD5E0;
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #A0AEC0;
            }
            QPushButton:pressed {
                background-color: #718096;
            }
        """)
        
        self.clear_button.clicked.connect(self.clear)
        self.clear_button.hide()  # Initially hidden
        
        # Connect text changed to show/hide clear button
        self.textChanged.connect(self.onTextChanged)
        
        # Set base stylesheet
        self.setStyleSheet("""
            QLineEdit {
                background-color: #FFFFFF;
                color: #2D3748;
                border: 1px solid #E2E8F0;
                border-radius: 8px;
                padding: 10px 35px 10px 40px;
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
    
    def onTextChanged(self, text):
        # Show clear button when there's text, hide when empty
        self.clear_button.setVisible(bool(text))
    
    def setClearButtonWidget(self, button):
        """Set the clear button widget"""
        self.clear_button = button
    
    def getClearButton(self):
        """Get the clear button widget"""
        return self.clear_button

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
                }
                QPushButton:hover {
                    background-color: #3182CE;
                }
                QPushButton:pressed {
                    background-color: #2C5282;
                }
                QPushButton:disabled {
                    background-color: #E2E8F0;
                    color: #A0AEC0;
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
                }
                QPushButton:hover {
                    background-color: #E2E8F0;
                    border-color: #A0AEC0;
                }
            """
        }
        
        self.setStyleSheet(styles.get(style_type, styles["primary"]))

class CustomerSelectorDialog(QDialog):
    def __init__(self, parent=None, customerInput=None, selectedCustomerDetails=None, refreshCustomerSidebar=None):
        super().__init__(parent)

        self.setWindowTitle("Select Customer")
        self.refreshCustomerSidebar = refreshCustomerSidebar

        # Set larger dialog size (40% width, 70% height of screen)
        screen = self.screen().availableGeometry()
        self.resize(
            min(int(screen.width() * 0.4), 600),
            min(int(screen.height() * 0.7), 800)
        )

        self.customerInput = customerInput
        self.selectedCustomerDetails = selectedCustomerDetails
        self.customerData = []

        # Modern dialog styling
        self.setStyleSheet("""
            QDialog {
                background-color: #F7FAFC;
                color: #2D3748;
                font-family: 'Segoe UI', 'Inter', -apple-system, sans-serif;
            }
        """)

        self.initUI()
        self.loadCustomers()

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # -------- Search Bar with Clear Button --------
        search_container = QWidget()
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(0, 0, 0, 0)
        search_layout.setSpacing(0)
        
        # Search container with custom styling
        search_wrapper = QWidget()
        search_wrapper.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 1px solid #E2E8F0;
                border-radius: 8px;
            }
            QWidget:focus-within {
                border: 2px solid #4A90E2;
            }
        """)
        
        search_inner_layout = QHBoxLayout(search_wrapper)
        search_inner_layout.setContentsMargins(5, 5, 5, 5)
        search_inner_layout.setSpacing(5)
        
        # Search icon label
        search_icon = QLabel("🔍")
        search_icon.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: #A0AEC0;
                padding-left: 5px;
            }
        """)
        search_icon.setFixedWidth(30)
        search_inner_layout.addWidget(search_icon)
        
        # Custom search line edit with clear button
        self.searchInput = ModernSearchLineEdit("Search customer by name...")
        self.searchInput.textChanged.connect(self.filterCustomers)
        search_inner_layout.addWidget(self.searchInput)
        
        # Add clear button to the line edit layout
        clear_button = self.searchInput.getClearButton()
        search_inner_layout.addWidget(clear_button)
        
        search_layout.addWidget(search_wrapper)
        layout.addWidget(search_container)

        # -------- Customer List (Takes most space) --------
        self.customerListWidget = QListWidget()
        self.customerListWidget.setSelectionMode(QListWidget.SingleSelection)
        self.customerListWidget.itemSelectionChanged.connect(
            self.updateSelectButtonState
        )

        # Set list to show more items - smaller font, more rows
        self.customerListWidget.setStyleSheet("""
            QListWidget {
                background-color: white;
                border: 1px solid #E2E8F0;
                border-radius: 8px;
                font-size: 13px;
                outline: none;
                padding: 2px;
            }
            
            QListWidget::item {
                padding: 10px 15px;
                border-bottom: 1px solid #F7FAFC;
                color: #2D3748;
                font-weight: 400;
                min-height: 20px;
            }
            
            QListWidget::item:hover {
                background-color: #F7FAFC;
            }
            
            QListWidget::item:selected {
                background-color: #EBF8FF;
                color: #2C5282;
                font-weight: 500;
                border-left: 4px solid #4A90E2;
            }
            
            /* Custom scrollbar styling */
            QScrollBar:vertical {
                background-color: transparent;
                width: 8px;
                border-radius: 4px;
                margin: 2px;
            }
            
            QScrollBar::handle:vertical {
                background-color: #CBD5E0;
                border-radius: 4px;
                min-height: 30px;
            }
            
            QScrollBar::handle:vertical:hover {
                background-color: #A0AEC0;
            }
            
            QScrollBar:horizontal {
                height: 8px;
                background: transparent;
            }
            
            QScrollBar::handle:horizontal {
                background-color: #CBD5E0;
                border-radius: 4px;
                min-width: 30px;
            }
        """)

        # Set the list widget to expand and take most space
        layout.addWidget(self.customerListWidget, 1)

        # -------- Selection Info (Small) --------
        self.selectionInfo = QLabel("")
        self.selectionInfo.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #718096;
                padding: 5px 0px;
            }
        """)
        self.selectionInfo.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.selectionInfo)

        # -------- Button Container --------
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(15)
        
        button_layout.addStretch()
        
        self.selectBtn = ModernButton("Select", "primary", width=120)
        self.selectBtn.setEnabled(False)
        self.selectBtn.clicked.connect(self.selectCustomer)
        button_layout.addWidget(self.selectBtn)
        
        layout.addWidget(button_container)

    def loadCustomers(self):
        db = DbClient()
        # Get all customers sorted by ID (assuming ID 1 is first)
        all_customers = db.getCustomerName()  # [(id, name), ...]
        
        if not all_customers:
            QMessageBox.information(
                self,
                "No Customers",
                "No customers found in the database.\n\nPlease add customers first."
            )
            self.reject()
            return

        # Sort by ID (assuming first element is ID)
        self.customerData = sorted(all_customers, key=lambda x: int(x[0]))
        self.populateCustomerList(self.customerData)
        self.updateSelectionInfo(len(self.customerData))

    def populateCustomerList(self, customers):
        self.customerListWidget.clear()
        
        # Add each customer with just the name (no ID)
        for custID, custName in customers:
            # Create simple text item with just the name
            item = QListWidgetItem(custName)
            
            # Store the raw data in custom role
            item.setData(Qt.UserRole, (custID, custName))
            
            # Set smaller font
            font = QFont()
            font.setPointSize(12)
            item.setFont(font)
            
            # Add to list
            self.customerListWidget.addItem(item)

        # Clear selection initially
        self.customerListWidget.clearSelection()
        self.selectBtn.setEnabled(False)
        
        # Select first item by default if available
        if self.customerListWidget.count() > 0:
            self.customerListWidget.setCurrentRow(0)

    def filterCustomers(self, text):
        if not self.customerData:
            return
            
        if text.strip() == "":
            # Show all sorted by ID when search is empty
            filtered = sorted(self.customerData, key=lambda x: int(x[0]))
        else:
            # Filter by name and sort by ID
            filtered = [
                (custID, custName) for custID, custName in self.customerData
                if text.lower() in custName.lower()
            ]
            filtered = sorted(filtered, key=lambda x: int(x[0]))
            
        self.populateCustomerList(filtered)
        self.updateSelectionInfo(len(filtered), text)

    def updateSelectionInfo(self, count, search_text=""):
        if search_text:
            if count == 0:
                self.selectionInfo.setText(f"No customers found matching '{search_text}'")
            else:
                self.selectionInfo.setText(f"Found {count} customer(s)")
        else:
            self.selectionInfo.setText(f"Showing {count} customer(s)")

    def updateSelectButtonState(self):
        selected = self.customerListWidget.currentItem()
        is_enabled = selected is not None
        self.selectBtn.setEnabled(is_enabled)
        
        if selected:
            custID, custName = selected.data(Qt.UserRole)
            self.selectionInfo.setText(f"Selected: {custName}")

    def selectCustomer(self):
        selected = self.customerListWidget.currentItem()
        if not selected:
            return

        # Get customer data from stored role
        custID, custName = selected.data(Qt.UserRole)

        # Get additional customer details
        db = DbClient()
        customerDetails = db.getCustomerDetails(custID, custName)

        customerAddress = customerDetails[3] if customerDetails else ""
        customerPhone = customerDetails[6] if customerDetails else ""

        # Update customer input field in parent
        if self.customerInput:
            self.customerInput.setText(custName)

        # Update selected customer details dictionary
        if self.selectedCustomerDetails is not None:
            self.selectedCustomerDetails.clear()
            self.selectedCustomerDetails.update({
                "customerID": custID,
                "name": custName,
                "address": customerAddress,
                "phone": customerPhone,
                "email": customerDetails[7] if customerDetails else "",
                "ABN": customerDetails[8] if customerDetails else "",
                "customerType": customerDetails[1] if customerDetails else "",
                "state": customerDetails[4] if customerDetails else "",
                "postcode": customerDetails[5] if customerDetails else ""
            })

        # Refresh SideBar in parent window
        if self.refreshCustomerSidebar:
            self.refreshCustomerSidebar()
            
        self.accept()

# Utility function to open the dialog
def openCustomerSelector(parent, customerInput, selectedCustomerDetails, refreshCustomerSidebar):
    """
    Called from MainArea.
    Checks DB first, opens dialog only if customers exist.
    """
    db = DbClient()
    customers = db.getCustomerName()

    if not customers:
        QMessageBox.information(
            parent,
            "No Customers",
            "No customers found in database.\n\nPlease add customers first."
        )
        return 

    dialog = CustomerSelectorDialog(
        parent=parent,
        customerInput=customerInput,
        selectedCustomerDetails=selectedCustomerDetails,
        refreshCustomerSidebar=refreshCustomerSidebar
    )
    dialog.exec()