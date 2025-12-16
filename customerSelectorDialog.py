# customerSelectorDialog.py
from PySide6.QtWidgets import QDialog, QVBoxLayout, QListWidget, QPushButton, QMessageBox
from PySide6.QtCore import Qt
from dbClient import DbClient

class CustomerSelectorDialog(QDialog):
    def __init__(self, parent=None, customerInput=None, selectedCustomerDetails=None):
        super().__init__(parent)
        self.setWindowTitle("Select Customer")
        self.setMinimumWidth(600)   
        self.setMinimumHeight(600)  

        self.customerInput = customerInput
        self.selectedCustomerDetails = selectedCustomerDetails

        self.initUI()
        self.loadCustomers()

    def initUI(self):
        layout = QVBoxLayout()

        self.customerListWidget = QListWidget()
        layout.addWidget(self.customerListWidget)

        self.selectBtn = QPushButton("Select")
        layout.addWidget(self.selectBtn)
        self.selectBtn.clicked.connect(self.selectCustomer)

        self.setLayout(layout)

    def loadCustomers(self):
        db = DbClient()
        customerData = db.getCustomerName()  # returns [(id1, name1), (id2, name2), ...]

        if not customerData:
            QMessageBox.warning(self, "No Customers", "No customers found in database.")
            return

        for custID, custName in customerData:
            self.customerListWidget.addItem(f"{custID}: {custName}")

    def selectCustomer(self):
        selected = self.customerListWidget.currentItem()
        if selected:
            custID, custName = selected.text().split(":", 1)
            custName = custName.strip()
            custID = custID.strip()

            db = DbClient()
            # Fetch full details for selected customer
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
        else:
            QMessageBox.warning(self, "No Selection", "Please select a customer.")
