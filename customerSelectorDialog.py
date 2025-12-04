# customerSelectorDialog.py
from PySide6.QtWidgets import QDialog, QVBoxLayout, QListWidget, QPushButton, QMessageBox
from dbClient import DbServer

class CustomerSelectorDialog(QDialog):
    def __init__(self, parent=None, customerInput=None, selectedCustomerDetails=None):
        super().__init__(parent)
        self.setWindowTitle("Select Customer")
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
        db = DbServer()
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

            if self.customerInput:
                self.customerInput.setText(custName)

            if self.selectedCustomerDetails is not None:
                self.selectedCustomerDetails.clear()
                self.selectedCustomerDetails.update({
                    "customerID": custID,
                    "name": custName
                })

            self.accept()
        else:
            QMessageBox.warning(self, "No Selection", "Please select a customer.")
