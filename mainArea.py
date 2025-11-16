# mainArea.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout,
    QPushButton, QTableWidget, QHeaderView, QSizePolicy
)
from PySide6.QtCore import Qt

class MainArea(QWidget):
    def __init__(self):
        super().__init__()

        mainAreaLayout = QVBoxLayout()
        mainAreaLayout.setAlignment(Qt.AlignTop)
        mainAreaLayout.setSpacing(15)

        # ------------------- Customer Section -------------------
        mainAreaLayout.addWidget(QLabel("Customer Name:"))
        self.customerInput = QLineEdit()
        self.customerInput.setFixedHeight(30)
        self.customerInput.setPlaceholderText("Enter customer name")
        mainAreaLayout.addWidget(self.customerInput)

        # Customer Buttons
        customerBtnLayout = QHBoxLayout()
        self.selectCustomerBtn = QPushButton("Select Customer")
        self.addCustomerBtn = QPushButton("Add Customer")
        self.clearCustomerBtn = QPushButton("Clear")
        customerBtnLayout.setAlignment(Qt.AlignLeft)

        # Button styles
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

        # Apply styles
        self.selectCustomerBtn.setStyleSheet(primaryBtnStyle)
        self.addCustomerBtn.setStyleSheet(primaryBtnStyle)
        self.clearCustomerBtn.setStyleSheet(failureBtnStyle)

        # Set fixed height
        for btn in [self.selectCustomerBtn, self.addCustomerBtn, self.clearCustomerBtn]:
            btn.setFixedHeight(28)
            btn.setFixedWidth(140) 

        customerBtnLayout.addWidget(self.selectCustomerBtn)
        customerBtnLayout.addWidget(self.addCustomerBtn)
        customerBtnLayout.addWidget(self.clearCustomerBtn)
        mainAreaLayout.addLayout(customerBtnLayout)

        mainAreaLayout.addSpacing(20)

        # ------------------- Product Section -------------------
        mainAreaLayout.addWidget(QLabel("Product Name:"))

        # Product Input Form
        productFormLayout = QHBoxLayout()
        self.productNameInput = QLineEdit()
        self.productNameInput.setFixedHeight(30)
        self.productNameInput.setPlaceholderText("Enter product name")
        self.qtyInput = QLineEdit()
        self.qtyInput.setFixedHeight(30)
        self.qtyInput.setPlaceholderText("Enter quantity")
        self.priceInput = QLineEdit()
        self.priceInput.setFixedHeight(30)
        self.priceInput.setPlaceholderText("Enter Unit price")
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
        self.selectProductBtn = QPushButton("Select Product")
        self.clearProductBtn = QPushButton("Clear")
        productBtnLayout.setAlignment(Qt.AlignLeft)

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
        self.productTable.setColumnCount(5)
        self.productTable.setHorizontalHeaderLabels(["Product Name", "Qty", "Price", "Discount", "Total"])
        self.productTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.productTable.setMaximumHeight(200)
        self.productTable.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        mainAreaLayout.addWidget(self.productTable)

        self.setLayout(mainAreaLayout)
