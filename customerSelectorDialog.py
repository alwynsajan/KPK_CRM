from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QListWidget, QPushButton,
    QMessageBox, QLineEdit, QLabel
)
from PySide6.QtCore import Qt
from dbClient import DbClient


class CustomerSelectorDialog(QDialog):
    def __init__(self, parent=None, customerInput=None, selectedCustomerDetails=None):
        super().__init__(parent)

        self.setWindowTitle("Select Customer")

        # Set dialog size (25% width, 50% height of screen)
        screen = self.screen().availableGeometry()
        self.resize(
            int(screen.width() * 0.25),
            int(screen.height() * 0.5)
        )

        self.customerInput = customerInput
        self.selectedCustomerDetails = selectedCustomerDetails
        self.customerData = []

        self.initUI()
        self.loadCustomers()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)

        # -------- Search Bar --------
        searchLabel = QLabel("Search Customer Name:")
        self.searchInput = QLineEdit()
        self.searchInput.setPlaceholderText("Type customer name...")
        self.searchInput.textChanged.connect(self.filterCustomers)
        self.searchInput.setClearButtonEnabled(True)
        self.searchInput.setStyleSheet("""
                                        background-color: #FFFFFF;
                                        color: black;               
                                        border: 1px solid #ccc; 
                                        border-radius: 6px;    
                                        padding-left: 5px;          
                                    """)

        layout.addWidget(searchLabel)
        layout.addWidget(self.searchInput)

        # -------- Customer List --------
        self.customerListWidget = QListWidget()
        self.customerListWidget.setSelectionMode(QListWidget.SingleSelection)
        self.customerListWidget.setFocusPolicy(Qt.NoFocus)

        self.customerListWidget.setStyleSheet("""
            QListWidget::item {
                padding: 8px;
                border: none;
            }
            QListWidget::item:selected {
                background-color: #3498DB;
                color: white;
            }
        """)

        self.customerListWidget.itemSelectionChanged.connect(
            self.updateSelectButtonState
        )

        layout.addWidget(self.customerListWidget)

        # -------- Select Button --------
        self.selectBtn = QPushButton("Select")
        self.selectBtn.setCursor(Qt.PointingHandCursor)
        self.selectBtn.setEnabled(False)
        self.selectBtn.clicked.connect(self.selectCustomer)

        self.selectBtn.setStyleSheet("""
            QPushButton {
                background-color: #B0B0B0;
                color: white;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:enabled {
                background-color: #3498DB;
            }
            QPushButton:hover:enabled {
                background-color: #2E86C1;
            }
        """)

        layout.addWidget(self.selectBtn)

        self.setLayout(layout)

    def loadCustomers(self):
        db = DbClient()
        self.customerData = db.getCustomerName()  # [(id, name), ...]

        if not self.customerData:
            QMessageBox.warning(self, "No Customers", "No customers found in database.")
            return

        self.populateCustomerList(self.customerData)

    def populateCustomerList(self, customers):
        self.customerListWidget.clear()
        for custID, custName in customers:
            self.customerListWidget.addItem(f"{custID}: {custName}")

        self.customerListWidget.clearSelection()
        self.selectBtn.setEnabled(False)

    def filterCustomers(self, text):
        filtered = [
            (cid, name) for cid, name in self.customerData
            if text.lower() in name.lower()
        ]
        self.populateCustomerList(filtered)

    def updateSelectButtonState(self):
        self.selectBtn.setEnabled(
            self.customerListWidget.currentItem() is not None
        )

    def selectCustomer(self):
        selected = self.customerListWidget.currentItem()
        if not selected:
            QMessageBox.warning(self, "No Selection", "Please select a customer.")
            return

        custID, custName = selected.text().split(":", 1)
        custID = custID.strip()
        custName = custName.strip()

        db = DbClient()
        customerDetails = db.getCustomerDetails(custID, custName)

        customerAddress = customerDetails[3] if customerDetails else ""
        customerPhone = customerDetails[6] if customerDetails else ""

        if self.customerInput:
            self.customerInput.setText(custName)

        if self.selectedCustomerDetails is not None:
            self.selectedCustomerDetails.clear()
            self.selectedCustomerDetails.update({
                "customerID": custID,
                "name": custName,
                "address": customerAddress,
                "phone": customerPhone
            })

        self.accept()
