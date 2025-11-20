from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QLineEdit,
    QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView
)
from PySide6.QtCore import Qt
import sys

class CRMApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("K.P.K Associates CRM")
        self.showMaximized()

        # List to store data
        self.customers = []
        self.products = []

        # MAIN LAYOUT
        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)

        # ====== TOP HEADER ======
        headerLayout = QHBoxLayout()
        headerLayout.setContentsMargins(10,10,10,10)

        title = QLabel("K.P.K Associates")
        title.setStyleSheet("font-size: 30px; font-weight: bold;")
        title.setAlignment(Qt.AlignLeft)

        btnSelectCustomer = QPushButton("Select Customer")
        btnSelectProduct = QPushButton("Select Product")
        btnVoidSale = QPushButton("Void Sale")

        buttonStyle = """
            QPushButton {
                background-color: #3498DB;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2E86C1;
            }
        """
        btnSelectCustomer.setStyleSheet(buttonStyle)
        btnSelectProduct.setStyleSheet(buttonStyle)
        btnVoidSale.setStyleSheet(buttonStyle)

        headerLayout.addWidget(title)
        headerLayout.addStretch()
        headerLayout.addWidget(btnSelectCustomer)
        headerLayout.addWidget(btnSelectProduct)
        headerLayout.addWidget(btnVoidSale)

        mainLayout.addLayout(headerLayout)
        mainLayout.addSpacing(20)

        # ====== MAIN HORIZONTAL AREA ======
        contentLayout = QHBoxLayout()

        # ---- SIDEBAR ----
        sideBar = QWidget()
        sideBar.setFixedWidth(200)
        sideBarLayout = QVBoxLayout()
        sideBarLayout.setAlignment(Qt.AlignTop)

        sidebarButtons = ["Sales", "Credits", "Misc", "Upload Pdt Details"]
        self.sidebarBtns = []
        for btnName in sidebarButtons:
            btn = QPushButton(btnName)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #E6E6E6;
                    color: #333;
                    padding: 10px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #D9D9D9;
                }
            """)
            sideBarLayout.addWidget(btn)
            self.sidebarBtns.append(btn)

        sideBar.setLayout(sideBarLayout)

        # ---- MAIN CONTENT ----
        mainArea = QWidget()
        mainAreaLayout = QVBoxLayout()
        mainAreaLayout.setAlignment(Qt.AlignTop)

        # Customer Name
        self.customerInput = QLineEdit()
        self.customerInput.setPlaceholderText("Customer Name")
        self.customerInput.setFixedWidth(300)

        mainAreaLayout.addWidget(QLabel("Customer Name:"))
        mainAreaLayout.addWidget(self.customerInput)
        mainAreaLayout.addSpacing(20)

        # Product Input Form
        formLayout = QHBoxLayout()
        self.productNameInput = QLineEdit()
        self.productNameInput.setPlaceholderText("Product Name")
        self.productNameInput.setFixedWidth(200)

        self.qtyInput = QLineEdit()
        self.qtyInput.setPlaceholderText("Qty")
        self.qtyInput.setFixedWidth(100)

        self.priceInput = QLineEdit()
        self.priceInput.setPlaceholderText("Price")
        self.priceInput.setFixedWidth(100)

        addProductBtn = QPushButton("Add Product")
        addProductBtn.setStyleSheet(buttonStyle)
        addProductBtn.clicked.connect(self.addProduct)

        self.productNameInput.textChanged.connect(self.onProductNameChange)

        formLayout.addWidget(self.productNameInput)
        formLayout.addWidget(self.qtyInput)
        formLayout.addWidget(self.priceInput)
        formLayout.addWidget(addProductBtn)

        mainAreaLayout.addLayout(formLayout)
        mainAreaLayout.addSpacing(20)

        # Product Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Product Name", "Qty", "Price", "Discount", "Total"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        mainAreaLayout.addWidget(self.table)

        mainArea.setLayout(mainAreaLayout)

        # ADD SIDEBAR + MAIN AREA TO CONTENT
        contentLayout.addWidget(sideBar)
        contentLayout.addWidget(mainArea, stretch=1)

        mainLayout.addLayout(contentLayout)

    def onProductNameChange(self, text):
        print("Product Name changed:", text)


    def addProduct(self):
        product = self.productNameInput.text().strip()
        qty = self.qtyInput.text().strip()
        price = self.priceInput.text().strip()
        customer = self.customerInput.text().strip()

        if not product or not qty or not price:
            return  # skip empty input

        # Save customer if not already saved
        if customer not in self.customers:
            self.customers.append(customer)

        # Convert to numbers
        try:
            qty_val = float(qty)
            price_val = float(price)
        except ValueError:
            return  # invalid number

        discount = 0
        total = qty_val * price_val - discount

        # Add to products list
        self.products.append({
            "customer": customer,
            "product": product,
            "qty": qty_val,
            "price": price_val,
            "discount": discount,
            "total": total
        })

        # Add row to table
        rowPos = self.table.rowCount()
        self.table.insertRow(rowPos)
        self.table.setItem(rowPos, 0, QTableWidgetItem(product))
        self.table.setItem(rowPos, 1, QTableWidgetItem(str(qty_val)))
        self.table.setItem(rowPos, 2, QTableWidgetItem(str(price_val)))
        self.table.setItem(rowPos, 3, QTableWidgetItem(str(discount)))
        self.table.setItem(rowPos, 4, QTableWidgetItem(str(total)))

        # Clear product inputs
        self.productNameInput.clear()
        self.qtyInput.clear()
        self.priceInput.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CRMApp()
    window.show()
    sys.exit(app.exec())
