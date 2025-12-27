from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout,
    QPushButton, QTableWidget, QHeaderView, QSizePolicy,
    QTableWidgetItem, QRadioButton, QButtonGroup, QMessageBox,
    QFrame, QFormLayout, QGroupBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor, QPalette
from dbClient import DbClient
from customerSelectorDialog import openCustomerSelector
from productSelectorDialog import openProductSelector
from generatePDF import generateInvoice
from datetime import date

# ------------------- Modern Line Edit -------------------
class ModernLineEdit(QLineEdit):
    def __init__(self, placeholder="", width=None):
        super().__init__()
        self.setPlaceholderText(placeholder)
        self.setFixedHeight(36)
        if width:
            self.setFixedWidth(width)
        self.setStyleSheet("""
            QLineEdit {
                background-color: #FFFFFF;
                color: #2D3748;
                border: 1px solid #CBD5E0;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 13px;
                font-weight: 400;
                selection-background-color: #4A90E2;
            }
            QLineEdit:focus {
                border: 2px solid #4A90E2;
                background-color: #F7FAFC;
            }
        """)

# ------------------- Modern Button -------------------
class ModernButton(QPushButton):
    def __init__(self, text, style_type="primary", width=None):
        super().__init__(text)
        self.setFixedHeight(34)
        if width:
            self.setFixedWidth(width)
        self.setCursor(Qt.PointingHandCursor)
        
        styles = {
            "primary": """
                QPushButton {
                    background-color: #4A90E2;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 8px 12px;
                    font-size: 12px;
                    font-weight: 600;
                }
                QPushButton:hover {
                    background-color: #3182CE;
                }
                QPushButton:pressed {
                    background-color: #2C5282;
                }
            """,
            "success": """
                QPushButton {
                    background-color: #38A169;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 8px 12px;
                    font-size: 12px;
                    font-weight: 600;
                }
                QPushButton:hover {
                    background-color: #2F855A;
                }
                QPushButton:pressed {
                    background-color: #276749;
                }
            """,
            "danger": """
                QPushButton {
                    background-color: #E53E3E;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 8px 12px;
                    font-size: 12px;
                    font-weight: 600;
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
                    background-color: #A0AEC0;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 8px 12px;
                    font-size: 12px;
                    font-weight: 600;
                }
                QPushButton:hover {
                    background-color: #718096;
                }
                QPushButton:pressed {
                    background-color: #4A5568;
                }
            """,
            "light": """
                QPushButton {
                    background-color: #EDF2F7;
                    color: #4A5568;
                    border: 1px solid #CBD5E0;
                    border-radius: 6px;
                    padding: 8px 12px;
                    font-size: 12px;
                    font-weight: 600;
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
        self.setStyleSheet("""
            QRadioButton {
                font-size: 13px;
                font-weight: 500;
                color: #2D3748;
                background-color: transparent;
                padding: 2px;
                spacing: 6px;
            }
            QRadioButton::indicator {
                width: 16px;
                height: 16px;
                border-radius: 8px;
                border: 2px solid #A0AEC0;
                background-color: white;
            }
            QRadioButton::indicator:checked {
                background-color: #4A90E2;
                border-color: #4A90E2;
            }
        """)
        self.setCursor(Qt.PointingHandCursor)

# ------------------- Card Frame -------------------
class CardFrame(QFrame):
    def __init__(self, title=None, height=None):
        super().__init__()
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
            }
        """)
        # Remove fixed height constraint
        if height:
            self.setMinimumHeight(height)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(16, 12, 16, 12)
        self.layout.setSpacing(10)

        if title:
            title_label = QLabel(title)
            title_label.setStyleSheet("""
                font-size: 14px;
                font-weight: 600;
                color: #2D3748;
            """)
            self.layout.addWidget(title_label)


class MainArea(QWidget):
    def __init__(self, selectedCustomerDetails=None, finalProductList=None, sidebar=None):
        super().__init__()
        
        self.dbClent = DbClient()
        
        if selectedCustomerDetails is None:
            self.selectedCustomerDetails = {}
        else:
            self.selectedCustomerDetails = selectedCustomerDetails
        self.finalProductList = finalProductList or []
        self.sideBar = sidebar

        # Main layout with stretch factors
        mainAreaLayout = QVBoxLayout(self)
        mainAreaLayout.setContentsMargins(20, 15, 20, 15)
        mainAreaLayout.setSpacing(15)
        
        # Remove stretch from main layout to let rows control height
        mainAreaLayout.setStretch(0, 0)

        # ------------------- Top Row: Customer & Product (20%) -------------------
        topRow = QHBoxLayout()
        topRow.setSpacing(15)
        
        # Create container widget for top row with stretch factor
        topRowWidget = QWidget()
        topRowWidget.setLayout(topRow)

        # Card 1: Customer Section (30% width of top row)
        customerCard = CardFrame("Customer")  
        customerCard.layout.setContentsMargins(12, 10, 12, 10)
        
        # Customer input with label removed 
        self.customerInput = ModernLineEdit("Search or enter customer name")
        customerCard.layout.addWidget(self.customerInput)
        
        # Customer buttons
        customerBtnLayout = QHBoxLayout()
        customerBtnLayout.setSpacing(8)
        
        self.selectCustomerBtn = ModernButton("Select Customer", "primary")
        self.clearCustomerBtn = ModernButton("Clear", "secondary", width=80)
        
        self.selectCustomerBtn.clicked.connect(
            lambda: openCustomerSelector(
                parent=self,
                customerInput=self.customerInput,
                selectedCustomerDetails=self.selectedCustomerDetails,
                refreshCustomerSidebar=self.refreshCustomerSidebar
            )
        )
        self.clearCustomerBtn.clicked.connect(self.clearCustomerData)
        
        customerBtnLayout.addWidget(self.selectCustomerBtn)
        customerBtnLayout.addWidget(self.clearCustomerBtn)
        customerBtnLayout.addStretch()
        
        customerCard.layout.addLayout(customerBtnLayout)
        
        topRow.addWidget(customerCard, 3)  # 30% width

        # Card 2: Product Section (70% width of top row)
        productCard = CardFrame("Add Products")  
        productCard.layout.setContentsMargins(12, 10, 12, 10)
        
        # Product form layout - single row
        productFormLayout = QHBoxLayout()
        productFormLayout.setSpacing(10)
        
        # Product name with reduced width
        self.productNameInput = ModernLineEdit("Product name")
        self.productNameInput.setMinimumWidth(180)  
        productFormLayout.addWidget(self.productNameInput, 4)  # 40% of product card
        
        # Quantity with reduced width
        self.qtyInput = ModernLineEdit("Qty")
        self.qtyInput.setFixedWidth(70)  
        productFormLayout.addWidget(self.qtyInput, 1)  # 10% of product card
        
        # Price with reduced width
        self.priceInput = ModernLineEdit("Price")
        self.priceInput.setFixedWidth(90) 
        productFormLayout.addWidget(self.priceInput, 2)  # 20% of product card
        
        # Add button with reduced width
        self.checkoutBtn = ModernButton("Add", "success", width=80)
        productFormLayout.addWidget(self.checkoutBtn, 1)  # 10% of product card
        
        productCard.layout.addLayout(productFormLayout)
        
        # Product action buttons - second row
        productBtnLayout = QHBoxLayout()
        productBtnLayout.setSpacing(8)
        
        self.selectProductBtn = ModernButton("Browse Products", "light")
        self.clearProductBtn = ModernButton("Clear Fields", "light")
        
        self.selectProductBtn.clicked.connect(
            lambda: openProductSelector(
                parent=self,
                addProductRow=self.addProductRow
            )
        )
        self.clearProductBtn.clicked.connect(self.clearProductFields)
        
        productBtnLayout.addWidget(self.selectProductBtn)
        productBtnLayout.addWidget(self.clearProductBtn)
        productBtnLayout.addStretch()
        
        productCard.layout.addLayout(productBtnLayout)
        
        topRow.addWidget(productCard, 7)  # 70% width

        # Add top row widget to main layout with 20% stretch
        mainAreaLayout.addWidget(topRowWidget, 2)  

        # ------------------- Cart Items Table (40%) -------------------
        tableCard = CardFrame("Cart Items")  
        tableCard.layout.setContentsMargins(2, 2, 2, 2)

        # Product table
        self.productTable = QTableWidget()
        self.productTable.setColumnCount(6)
        self.productTable.setHorizontalHeaderLabels(
            ["Product", "Qty", "Price", "Discount %", "Total", "Remove"]
        )
        self.productTable.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Header styling
        header = self.productTable.horizontalHeader()
        header.setStyleSheet("""
            QHeaderView::section {
                background-color: #EDF2F7;
                color: #2D3748;
                font-weight: 600;
                font-size: 12px;
                padding: 10px 6px;
                border: none;
                border-right: 1px solid #E2E8F0;
            }
            QHeaderView::section:last {
                border-right: none;
            }
        """)

        header.setSectionResizeMode(QHeaderView.Fixed)
        header.setStretchLastSection(False)

        # ---- COLUMN WIDTH LOGIC ----
        def adjustColumnWidths():
            total = tableCard.contentsRect().width()
            if total <= 0:
                return

            self.productTable.setColumnWidth(0, int(total * 0.49))  # Product 50%
            for col in range(1, 6):
                self.productTable.setColumnWidth(col, int(total * 0.10))  # Others 10%

        # Apply once and on resize
        adjustColumnWidths()
        tableCard.resizeEvent = lambda e: adjustColumnWidths()

        # Table styling 
        self.productTable.setStyleSheet("""
            QTableWidget {
                background-color: white;
                gridline-color: #E2E8F0;
                border: none;
                font-size: 12px;
                selection-background-color: #EBF8FF;
                selection-color: #2D3748;
                alternate-background-color: white;
            }
            QTableWidget::item {
                padding: 8px 6px;
                border-bottom: 1px solid #F7FAFC;
                color: #2D3748;
            }
            QTableWidget::item:selected {
                background-color: #EBF8FF;
            }

            QScrollBar:vertical {
                background: #F7FAFC;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #CBD5E0;
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #A0AEC0;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar:horizontal {
                height: 8px;
                background: #F7FAFC;
            }
            QScrollBar::handle:horizontal {
                background: #CBD5E0;
                min-width: 20px;
            }
        """)

        self.productTable.verticalHeader().setVisible(False)
        self.productTable.setAlternatingRowColors(False)
        self.productTable.cellChanged.connect(self.updateTotalPrice)

        tableCard.layout.addWidget(self.productTable)
        # Add table card to main layout with 40% stretch
        mainAreaLayout.addWidget(tableCard, 4)  # 40% of available space

        # ------------------- Bottom Row: Notes, Payment, Total (15%) -------------------
        bottomRow = QHBoxLayout()
        bottomRow.setSpacing(15)
        
        # Create container widget for bottom row
        bottomRowWidget = QWidget()
        bottomRowWidget.setLayout(bottomRow)

        # Notes Card
        notesCard = CardFrame("Notes")
        
        self.notesInput = ModernLineEdit("Enter any notes...")
        notesCard.layout.addWidget(self.notesInput)
        bottomRow.addWidget(notesCard, 1)

        # Payment Card
        paymentCard = CardFrame("Payment Method")
        
        paymentOptionsLayout = QHBoxLayout()
        paymentOptionsLayout.setSpacing(12)
        
        self.efposRadio = ModernRadioButton("EFTPOS")
        self.cashRadio = ModernRadioButton("Cash")
        self.bankRadio = ModernRadioButton("Bank")
        self.creditRadio = ModernRadioButton("Credit")
        
        self.paymentGroup = QButtonGroup(self)
        self.paymentGroup.addButton(self.efposRadio)
        self.paymentGroup.addButton(self.cashRadio)
        self.paymentGroup.addButton(self.bankRadio)
        self.paymentGroup.addButton(self.creditRadio)
        self.paymentGroup.setExclusive(True)
        
        paymentOptionsLayout.addWidget(self.efposRadio)
        paymentOptionsLayout.addWidget(self.cashRadio)
        paymentOptionsLayout.addWidget(self.bankRadio)
        paymentOptionsLayout.addWidget(self.creditRadio)
        paymentOptionsLayout.addStretch()
        
        paymentCard.layout.addLayout(paymentOptionsLayout)
        bottomRow.addWidget(paymentCard, 1)

        # Total Card 
        totalCard = CardFrame("Grand Total")
        totalCard.layout.setAlignment(Qt.AlignCenter)
        
        self.totalAmountValue = QLabel("$0.00")
        self.totalAmountValue.setStyleSheet("""
            font-size: 24px;
            font-weight: 700;
            color: #2F855A;
            text-align: center;
            padding: 15px;
            background-color: #F0FFF4;
            border-radius: 6px;
            border: 1px solid #C6F6D5;
            min-width: 150px;
            max-width: 180px;
        """)
        self.totalAmountValue.setAlignment(Qt.AlignCenter)
        self.totalAmountValue.setWordWrap(True)
        
        totalCard.layout.addWidget(self.totalAmountValue)
        bottomRow.addWidget(totalCard, 1)

        # Add bottom row widget to main layout with 15% stretch
        mainAreaLayout.addWidget(bottomRowWidget, 1.5)  # 15% of available space

        # ------------------- Action Buttons (Fixed Height) -------------------
        actionLayout = QHBoxLayout()
        actionLayout.setSpacing(15)
        
        self.saveSalesBtn = ModernButton("Save Sale", "success", 120)
        self.printInvoiceBtn = ModernButton("Print Invoice", "primary", 120)
        self.voidSaleBtn = ModernButton("Void Sale", "danger", 120)
        
        self.saveSalesBtn.clicked.connect(self.handleSaveSales)
        self.printInvoiceBtn.clicked.connect(self.handlePrintInvoice)
        self.voidSaleBtn.clicked.connect(self.handleVoidSale)
        
        actionLayout.addStretch()
        actionLayout.addWidget(self.saveSalesBtn)
        actionLayout.addWidget(self.printInvoiceBtn)
        actionLayout.addWidget(self.voidSaleBtn)
        actionLayout.addStretch()
        
        # Create container for action buttons with fixed height
        actionWidget = QWidget()
        actionWidget.setFixedHeight(60)
        actionWidget.setLayout(actionLayout)
        
        mainAreaLayout.addWidget(actionWidget)

        # Connect Add Product Button
        self.checkoutBtn.clicked.connect(
            lambda: self.addProductRow({
                "name": self.productNameInput.text().strip(),
                "price": float(self.priceInput.text().strip() or 0),
                "qty": float(self.qtyInput.text().strip() or 1)
            })
        )

    # ------------------- Clear Customer Data -------------------
    def clearCustomerData(self):
        if self.selectedCustomerDetails:
            self.selectedCustomerDetails.clear()
            self.customerInput.clear()
            self.sideBar.updateCustomerInfo()
        else:
            self.selectedCustomerDetails.clear()
            self.customerInput.clear()

    # ------------------- Clear Product Fields -------------------
    def clearProductFields(self):
        self.productNameInput.clear()
        self.qtyInput.clear()
        self.priceInput.clear()

    # ------------------- Add Product Logic -------------------
    def addProductRow(self, productData):
        name = productData.get("name", "").strip()
        priceValue = productData.get("price", 0)
        qtyValue = productData.get("qty", 1)

        if not name or not priceValue:
            QMessageBox.warning(self, "Missing Information", "Please enter product name and price.")
            return

        try:
            qtyValue = float(qtyValue)
            priceValue = float(priceValue)
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Quantity and price must be valid numbers.")
            return

        total = qtyValue * priceValue

        row = self.productTable.rowCount()
        self.productTable.insertRow(row)

        # Product Name
        name_item = QTableWidgetItem(name)
        self.productTable.setItem(row, 0, name_item)

        # Qty
        qty_item = QTableWidgetItem(str(int(qtyValue)) if qtyValue.is_integer() else str(qtyValue))
        qty_item.setTextAlignment(Qt.AlignCenter)
        self.productTable.setItem(row, 1, qty_item)

        # Unit Price
        price_item = QTableWidgetItem(f"${priceValue:.2f}")
        price_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.productTable.setItem(row, 2, price_item)

        # Discount
        discount_item = QTableWidgetItem("0.0%")
        discount_item.setTextAlignment(Qt.AlignCenter)
        self.productTable.setItem(row, 3, discount_item)

        # Total Price
        totalItem = QTableWidgetItem(f"${total:.2f}")
        totalItem.setFlags(totalItem.flags() & ~Qt.ItemIsEditable)
        totalItem.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.productTable.setItem(row, 4, totalItem)

        # Using QLabel which has alignment property
        deleteLabel = QLabel("X")
        deleteLabel.setAlignment(Qt.AlignCenter)
        deleteLabel.setFixedHeight(20)
        deleteLabel.setStyleSheet("""
            QLabel {
                background-color: #E53E3E;
                color: white;
                border-radius: 4px;
                padding: 3px 0px;
                font-weight: bold;
                font-size: 12px;
                margin: 2px 10px;
            }
            QLabel:hover {
                background-color: #C53030;
            }
        """)
        deleteLabel.setCursor(Qt.PointingHandCursor)

        # Make it clickable
        deleteLabel.mousePressEvent = lambda event, r=row: self.deleteRow(r)

        self.productTable.setCellWidget(row, 5, deleteLabel)

        # Clear input fields after adding
        self.clearProductFields()
        self.updateGrandTotal()

    # ------------------- Delete Row -------------------
    def deleteRow(self, row):
        self.productTable.removeRow(row)
        self.updateGrandTotal()

    # ------------------- Update Customer Input -------------------
    def updateCustomerInput(self):
        if "name" in self.selectedCustomerDetails:
            self.customerInput.setText(self.selectedCustomerDetails["name"])

    # ------------------- Update Total Price on Cell Change -------------------
    def updateTotalPrice(self, row, column):
        if column not in [1, 2, 3]:
            return

        try:
            qty_item = self.productTable.item(row, 1)
            price_item = self.productTable.item(row, 2)
            discount_item = self.productTable.item(row, 3)

            if not discount_item:
                discount_item = QTableWidgetItem("0.0%")
                self.productTable.setItem(row, 3, discount_item)

            qty = float(qty_item.text()) if qty_item and qty_item.text() else 0
            price = float(price_item.text().replace("$", "")) if price_item else 0
            discount = float(discount_item.text().replace("%", "")) if discount_item.text() else 0

            total = (price * qty) * (1 - discount / 100)

            total_item = self.productTable.item(row, 4)
            if not total_item:
                total_item = QTableWidgetItem()
                self.productTable.setItem(row, 4, total_item)

            self.productTable.blockSignals(True)
            total_item.setText(f"${total:.2f}")
            discount_item.setText(f"{discount:.1f}%")
            self.productTable.blockSignals(False)

            self.updateGrandTotal()

        except Exception:
            pass

    def updateGrandTotal(self):
        total = 0.0
        for row in range(self.productTable.rowCount()):
            item = self.productTable.item(row, 4)
            if item and item.text():
                total += float(item.text().replace("$", ""))

        self.totalAmountValue.setText(f"${total:.2f}")

    # ------------------- Handle Void Sale -------------------
    def handleVoidSale(self):
        # reply = QMessageBox.question(
        #     self, 
        #     "Confirm Void Sale",
        #     "Are you sure you want to void this sale? All entered data will be cleared.",
        #     QMessageBox.Yes | QMessageBox.No,
        #     QMessageBox.No
        # )
        
        # if reply == QMessageBox.No:
        #     return

        # Clear Product Inputs
        self.productNameInput.clear()
        self.qtyInput.clear()
        self.priceInput.clear()

        # Clear Product Table
        self.productTable.blockSignals(True)
        self.productTable.setRowCount(0)
        self.productTable.blockSignals(False)

        # Reset Total
        self.totalAmountValue.setText("$0.00")

        # Clear Notes
        self.notesInput.clear()

        # Reset Payment Type
        self.paymentGroup.setExclusive(False)
        for btn in self.paymentGroup.buttons():
            btn.setChecked(False)
        self.paymentGroup.setExclusive(True)

        # Clear Internal Product List
        self.finalProductList = []

        if self.selectedCustomerDetails:
            # Clear Customer
            self.customerInput.clear()
            self.selectedCustomerDetails.clear()
            self.sideBar.updateCustomerInfo()
        else:
            # Clear Customer
            self.customerInput.clear()
            self.selectedCustomerDetails.clear()

    # ------------------- Handle Save Sales -------------------
    def handleSaveSales(self, type=None):
        # Customer Check
        customerName = self.customerInput.text().strip()

        # If no selected customer details, try using input field
        if not self.selectedCustomerDetails:
            if customerName:
                self.selectedCustomerDetails = {
                    "name": customerName
                }
            else:
                self.selectedCustomerDetails = {}

        # Collect Product Table Data
        self.finalProductList = []
        for row in range(self.productTable.rowCount()):
            nameItem = self.productTable.item(row, 0)
            qtyItem = self.productTable.item(row, 1)
            priceItem = self.productTable.item(row, 2)
            discountItem = self.productTable.item(row, 3)

            # Validate Quantity
            try:
                quantity = int(float(qtyItem.text().replace('%', ''))) if qtyItem and qtyItem.text() else 0
            except ValueError:
                QMessageBox.warning(
                    self,
                    "Invalid Quantity",
                    f"Invalid quantity on row {row+1}. Please enter a valid number."
                )
                return -1

            # Validate Price
            try:
                price_text = priceItem.text().replace('$', '').replace('%', '') if priceItem and priceItem.text() else "0"
                price = float(price_text)
            except ValueError:
                QMessageBox.warning(
                    self,
                    "Invalid Price",
                    f"Invalid unit price on row {row+1}. Please enter a valid number."
                )
                return -1

            # Validate Discount
            try:
                discount_text = discountItem.text().replace('$', '').replace('%', '') if discountItem and discountItem.text() else "0"
                discount = float(discount_text)
            except ValueError:
                QMessageBox.warning(
                    self,
                    "Invalid Discount",
                    f"Invalid discount on row {row+1}. Please enter a valid number."
                )
                return -1

            productData = {
                "name": nameItem.text().strip(),
                "quantity": quantity,
                "price": price,
                "discount": discount
            }

            self.finalProductList.append(productData)

        # Validate Products
        if not self.finalProductList:
            QMessageBox.warning(self, "No Products", "Please add at least one product before proceeding.")
            return -1

        # Validate Payment
        checkedButton = self.paymentGroup.checkedButton()
        if not checkedButton:
            QMessageBox.warning(self, "Payment Type Required", "Please select a payment type before proceeding.")
            return -1

        saleData = {
            "saleDate": date.today(),
            "customerID": self.selectedCustomerDetails.get("customerID"),
            "paymentType": checkedButton.text(),
            "note": self.notesInput.text().strip(),
            "items": self.finalProductList
        }

        response = self.dbClent.addSaleWithItems(saleData)

        # Popup Result
        if response.get("status") == "Success":
            if type != "invoice":
                QMessageBox.information(
                    self,
                    "Success",
                    "Sale saved successfully!"
                )

            # Clear UI after save
            if type != "invoice":
                self.handleVoidSale()
            return 1

        else:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to save sale.\n\n{response.get('error')}"
            )
            return -1

    # ------------------- Handle Print Invoice -------------------
    def handlePrintInvoice(self):
        # Save Sale First
        status = self.handleSaveSales("invoice")

        if status != 1:
            self.finalProductList = []
            return

        customerData = {
            "Name": self.selectedCustomerDetails.get("name", ""),
            "Address": self.selectedCustomerDetails.get("address", ""),
            "State": self.selectedCustomerDetails.get("state", ""),
            "Postcode": self.selectedCustomerDetails.get("postcode", ""),
            "Phone": self.selectedCustomerDetails.get("phone", "")
        }

        # Convert Product Data
        productDataForPDF = []

        for item in self.finalProductList:
            price = float(item.get("price", 0))
            discount = float(item.get("discount", 0))
            quantity = int(item.get("quantity", 0))

            # Apply discount here
            discountedPrice = round(
                price - (price * discount / 100), 2
            )

            productDataForPDF.append({
                "Name": item.get("name", ""),
                "Quantity": quantity,
                "Price": discountedPrice
            })

        # Generate Invoice
        pdfPath = generateInvoice(
            customerData=customerData,
            productData=productDataForPDF
        )

        QMessageBox.information(
            self,
            "Invoice Generated",
            "Invoice generated successfully!"
        )

        # Clear Internal Product List
        self.handleVoidSale()

    # ------------------- Refresh Customer Sidebar -------------------
    def refreshCustomerSidebar(self):
        self.sideBar.updateCustomerInfo()

    # ------------------- Resize Event for Responsive Columns -------------------
    # def resizeEvent(self, event):
    #     super().resizeEvent(event)
    #     totalWidth = self.productTable.viewport().width()
    #     self.productTable.setColumnWidth(0, int(totalWidth * 0.5))

    #     remaining = totalWidth - self.productTable.columnWidth(0)
    #     perCol = remaining // 5
    #     for col in range(1, 6):
    #         self.productTable.setColumnWidth(col, perCol)