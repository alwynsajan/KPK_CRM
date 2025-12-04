# mainArea.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout,
    QPushButton, QTableWidget, QHeaderView, QSizePolicy,
    QTableWidgetItem, QCheckBox, QTextEdit,QRadioButton,QButtonGroup
)
from PySide6.QtCore import Qt
from dbClient import DbServer
from addNewCustomer import CustomerForm

class MainArea(QWidget):
    def __init__(self):
        super().__init__()

        mainAreaLayout = QVBoxLayout()
        mainAreaLayout.setAlignment(Qt.AlignTop)
        mainAreaLayout.setSpacing(15)

        # ------------------- Internal State Variables -------------------
        self.selectedCustomerDetails = {} 
        self.finalProductList = [] 

        # ------------------- Button Styles -------------------
        primaryBtnStyle = """
            QPushButton {
                background-color: #3498DB;
                color: white;
                padding: 5px 15px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2E86C1;
            }
        """

        failureBtnStyle = """
            QPushButton {
                background-color: #E74C3C;
                color: white;
                padding: 5px 15px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
        """

        # ------------------- Customer Section -------------------
        mainAreaLayout.addWidget(QLabel("Customer Name:"))
        self.customerInput = QLineEdit()
        self.customerInput.setFixedHeight(30)
        self.customerInput.setPlaceholderText("Enter customer name")
        mainAreaLayout.addWidget(self.customerInput)

        # Customer Buttons
        customerBtnLayout = QHBoxLayout()
        customerBtnLayout.setAlignment(Qt.AlignLeft)

        self.selectCustomerBtn = QPushButton("Select Customer")
        self.addCustomerBtn = QPushButton("Add Customer")
        self.clearCustomerBtn = QPushButton("Clear")

        self.selectCustomerBtn.setStyleSheet(primaryBtnStyle)
        self.addCustomerBtn.setStyleSheet(primaryBtnStyle)
        self.clearCustomerBtn.setStyleSheet(failureBtnStyle)

        for btn in [self.selectCustomerBtn, self.addCustomerBtn, self.clearCustomerBtn]:
            btn.setFixedHeight(28)
            btn.setFixedWidth(140)

        customerBtnLayout.addWidget(self.selectCustomerBtn)
        customerBtnLayout.addWidget(self.addCustomerBtn)
        customerBtnLayout.addWidget(self.clearCustomerBtn)
        mainAreaLayout.addLayout(customerBtnLayout)

        self.addCustomerBtn.clicked.connect(self.openCustomerForm)

        mainAreaLayout.addSpacing(20)

        # ------------------- Product Section -------------------
        mainAreaLayout.addWidget(QLabel("Product Name:"))

        productFormLayout = QHBoxLayout()

        self.productNameInput = QLineEdit()
        self.productNameInput.setFixedHeight(30)
        self.productNameInput.setPlaceholderText("Enter product name")

        self.qtyInput = QLineEdit()
        self.qtyInput.setFixedHeight(30)
        self.qtyInput.setPlaceholderText("Enter quantity")

        self.priceInput = QLineEdit()
        self.priceInput.setFixedHeight(30)
        self.priceInput.setPlaceholderText("Enter unit price")

        self.addProductBtn = QPushButton("Add Product")
        self.addProductBtn.setStyleSheet(primaryBtnStyle)
        self.addProductBtn.setFixedHeight(30)

        productFormLayout.addWidget(self.productNameInput)
        productFormLayout.addWidget(self.qtyInput)
        productFormLayout.addWidget(self.priceInput)
        productFormLayout.addWidget(self.addProductBtn)

        mainAreaLayout.addLayout(productFormLayout)

        # Product Buttons
        productBtnLayout = QHBoxLayout()
        productBtnLayout.setAlignment(Qt.AlignLeft)

        self.selectProductBtn = QPushButton("Select Product")
        self.clearProductBtn = QPushButton("Clear")

        self.selectProductBtn.setStyleSheet(primaryBtnStyle)
        self.clearProductBtn.setStyleSheet(failureBtnStyle)

        for btn in [self.selectProductBtn, self.clearProductBtn]:
            btn.setFixedHeight(28)
            btn.setFixedWidth(140)

        productBtnLayout.addWidget(self.selectProductBtn)
        productBtnLayout.addWidget(self.clearProductBtn)
        mainAreaLayout.addLayout(productBtnLayout)

        mainAreaLayout.addSpacing(20)

        # ------------------- Product Table -------------------
        self.productTable = QTableWidget()
        self.productTable.setColumnCount(6)
        self.productTable.setHorizontalHeaderLabels(
            ["Product Name", "Qty", "Price", "Discount", "Total", "Delete"]
        )

        self.productTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # reduce table height
        self.productTable.setFixedHeight(180)
        self.productTable.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.productTable.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        mainAreaLayout.addWidget(self.productTable)

        # Connect Add Product Button
        self.addProductBtn.clicked.connect(self.addProductRow)

        # ------------------- Notes Section -------------------
        self.notesInput = QLineEdit()
        self.notesInput.setPlaceholderText("Enter note")
        self.notesInput.setFixedHeight(30)
        mainAreaLayout.addWidget(self.notesInput)

        # ------------------- Payment Options -------------------
        paymentLayout = QHBoxLayout()
        paymentLayout.setAlignment(Qt.AlignLeft)

        self.efposRadio = QRadioButton("EFTPOS")
        self.cashRadio = QRadioButton("Cash")
        self.bankRadio = QRadioButton("Bank Transfer")
        self.creditRadio = QRadioButton("Credit")

        # Set font size
        for radio in [self.efposRadio, self.cashRadio, self.bankRadio, self.creditRadio]:
            radio.setStyleSheet("font-size: 14px;")

        # Group them to allow only one selection
        self.paymentGroup = QButtonGroup(self)
        self.paymentGroup.addButton(self.efposRadio)
        self.paymentGroup.addButton(self.cashRadio)
        self.paymentGroup.addButton(self.bankRadio)
        self.paymentGroup.addButton(self.creditRadio)
        self.paymentGroup.setExclusive(True)

        paymentLayout.addWidget(self.efposRadio)
        paymentLayout.addWidget(self.cashRadio)
        paymentLayout.addWidget(self.bankRadio)
        paymentLayout.addWidget(self.creditRadio)

        mainAreaLayout.addLayout(paymentLayout)

        # ------------------- Save & Print Buttons -------------------
        actionBtnLayout = QHBoxLayout()
        actionBtnLayout.setAlignment(Qt.AlignLeft)

        self.saveSalesBtn = QPushButton("Save Sales")
        self.printSalesBtn = QPushButton("Print Sales")

        self.saveSalesBtn.setStyleSheet(primaryBtnStyle)
        self.printSalesBtn.setStyleSheet(primaryBtnStyle)

        for btn in [self.saveSalesBtn, self.printSalesBtn]:
            btn.setFixedHeight(30)
            btn.setFixedWidth(150)

        actionBtnLayout.addWidget(self.saveSalesBtn)
        actionBtnLayout.addWidget(self.printSalesBtn)

        mainAreaLayout.addLayout(actionBtnLayout)

        self.setLayout(mainAreaLayout)

    # ------------------- Add Product Logic -------------------
    def addProductRow(self):
        product = self.productNameInput.text().strip()
        qty = self.qtyInput.text().strip()
        price = self.priceInput.text().strip()

        if not product or not qty or not price:
            return

        try:
            qtyValue = float(qty)
            priceValue = float(price)
        except ValueError:
            return

        total = qtyValue * priceValue

        row = self.productTable.rowCount()
        self.productTable.insertRow(row)

        self.productTable.setItem(row, 0, QTableWidgetItem(product))
        self.productTable.setItem(row, 1, QTableWidgetItem(qty))
        self.productTable.setItem(row, 2, QTableWidgetItem(price))
        self.productTable.setItem(row, 3, QTableWidgetItem("0"))
        self.productTable.setItem(row, 4, QTableWidgetItem(str(total)))

        deleteBtn = QPushButton("Delete")
        deleteBtn.setStyleSheet("""
            QPushButton {
                background-color: #E74C3C;
                color: white;
                padding: 5px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
        """)
        deleteBtn.clicked.connect(lambda _, r=row: self.deleteRow(r))
        self.productTable.setCellWidget(row, 5, deleteBtn)

    # ------------------- Delete Row -------------------
    def deleteRow(self, row):
        self.productTable.removeRow(row)

        # re-bind buttons due to index shift
        for i in range(self.productTable.rowCount()):
            btn = self.productTable.cellWidget(i, 5)
            if btn:
                btn.clicked.disconnect()
                btn.clicked.connect(lambda _, r=i: self.deleteRow(r))

    # ------------------- Open Customer Form -------------------
    def openCustomerForm(self):
         # Pass the dictionary and a callback to update the input
        self.customerForm = CustomerForm(self.selectedCustomerDetails,self.updateCustomerInput)
        self.customerForm.show()

    # ------------------- Update Customer Input -------------------
    def updateCustomerInput(self):
        # Update the input field with saved customer name
        if "name" in self.selectedCustomerDetails:
            self.customerInput.setText(self.selectedCustomerDetails["name"])



