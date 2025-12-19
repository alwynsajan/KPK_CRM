from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QHBoxLayout, QMessageBox
)
from PySide6.QtCore import Qt
from dbClient import DbClient


class ProductForm(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Add Product")
        screen = self.screen().availableGeometry()
        self.resize(
            int(screen.width() * 0.5),
            int(screen.height() * 0.25)
        )

        self.setStyleSheet("""
            background-color: #EBE8DB;
            color: black;
        """)

        layout = QVBoxLayout()
        layout.setSpacing(10)

        inputStyle = """
            QLineEdit {
                background-color: #FFFFFF;
                color: black;
                border: 1px solid #ccc;
                border-radius: 6px;
                padding-left: 5px;
                height: 28px;
            }
        """

        # --- Product Bar Code ---
        layout.addWidget(QLabel("Product Bar Code"))
        self.barcodeInput = QLineEdit()
        self.barcodeInput.setPlaceholderText("Enter bar code")
        self.barcodeInput.setStyleSheet(inputStyle)
        layout.addWidget(self.barcodeInput)

        # --- Product Name ---
        layout.addWidget(QLabel("Product Name"))
        self.nameInput = QLineEdit()
        self.nameInput.setPlaceholderText("Enter product name")
        self.nameInput.setStyleSheet(inputStyle)
        layout.addWidget(self.nameInput)

        # --- Price ---
        layout.addWidget(QLabel("Price"))
        self.priceInput = QLineEdit()
        self.priceInput.setPlaceholderText("Enter price")
        self.priceInput.setStyleSheet(inputStyle)
        layout.addWidget(self.priceInput)

        # --- Buttons ---
        btnLayout = QHBoxLayout()

        self.clearBtn = QPushButton("Clear")
        self.clearBtn.setStyleSheet("""
            QPushButton {
                background-color: #E74C3C;
                color: white;
                padding: 8px 15px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
        """)
        self.clearBtn.clicked.connect(self.clearFields)

        self.addBtn = QPushButton("Add Product")
        self.addBtn.setStyleSheet("""
            QPushButton {
                background-color: #3498DB;
                color: white;
                padding: 8px 15px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2E86C1;
            }
        """)
        self.addBtn.clicked.connect(self.addProduct)
        btnLayout.addWidget(self.addBtn)
        btnLayout.addWidget(self.clearBtn)
        

        layout.addLayout(btnLayout)
        self.setLayout(layout)

    def clearFields(self):
        self.barcodeInput.clear()
        self.nameInput.clear()
        self.priceInput.clear()

    def addProduct(self):
        barcode = self.barcodeInput.text().strip()
        name = self.nameInput.text().strip()
        price = self.priceInput.text().strip()

        if not name or not price:
            QMessageBox.warning(self, "Missing Data", "Product name and price are required.")
            return

        try:
            price = float(price)
        except ValueError:
            QMessageBox.warning(self, "Invalid Price", "Price must be a number.")
            return
        
        if not barcode:
            barcode = 0
        else:
            try:
                barcode = int(barcode)
            except ValueError:
                QMessageBox.warning(self, "Invalid Barcode", "Barcode must be a number.")
                return

        db = DbClient()
        response = db.addProductData({
            "productBarCode": barcode,
            "name": name,
            "price": price
        })

        if response["status"] != "Success":
            QMessageBox.critical(self, "Database Error", response["message"])
            return

        QMessageBox.information(self, "Success", "Product added successfully.")
        # self.clearFields()
