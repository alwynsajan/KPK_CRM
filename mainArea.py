from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout,
    QPushButton, QTableWidget, QHeaderView, QSizePolicy,
    QTableWidgetItem, QRadioButton, QButtonGroup, QMessageBox,
    QFrame, QFormLayout, QGroupBox, QApplication
)
from PySide6.QtCore import Qt, QTimer, QEvent
from PySide6.QtGui import QIntValidator, QDoubleValidator
from dbClient import DbClient
from customerSelectorDialog import openCustomerSelector
from productSelectorDialog import openProductSelector
from generatePDF import generateInvoice
from generatePDF import printPDF
from datetime import datetime
import time

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

        self.barcode_buffer = ""
        self.barcode_timer = QTimer()
        self.barcode_timer.setSingleShot(True)
        self.barcode_timer.timeout.connect(self.processBarcode)

        # Global barcode scan (works without focusing the product name field)
        self._scan_buffer = ""
        self._last_scan_time = 0.0
        app = QApplication.instance()
        if app:
            app.installEventFilter(self)

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
        self.productNameInput.textChanged.connect(self.onProductNameTextChanged)
        
        # Quantity (integers only)
        self.qtyInput = ModernLineEdit("Qty")
        self.qtyInput.setFixedWidth(70)
        self.qtyInput.setValidator(QIntValidator(1, 99999, self))  # only positive integers
        productFormLayout.addWidget(self.qtyInput, 1)

        # Price (decimal numbers only)
        self.priceInput = ModernLineEdit("Price")
        self.priceInput.setFixedWidth(90)

        priceValidator = QDoubleValidator(0.0, 999999.99, 2, self)
        priceValidator.setNotation(QDoubleValidator.StandardNotation)
        self.priceInput.setValidator(priceValidator)

        productFormLayout.addWidget(self.priceInput, 2)
        
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
        self.productTable.setColumnCount(8)
        self.productTable.setHorizontalHeaderLabels(
            ["S/N", "Barcode", "Product", "Qty", "Price", "Discount %", "Total", "Remove"]
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

            self.productTable.setColumnWidth(0, int(total * 0.06))  # S/N
            self.productTable.setColumnWidth(1, int(total * 0.14))  # Barcode
            self.productTable.setColumnWidth(2, int(total * 0.30))  # Product
            self.productTable.setColumnWidth(3, int(total * 0.10))  # Qty
            self.productTable.setColumnWidth(4, int(total * 0.12))  # Price
            self.productTable.setColumnWidth(5, int(total * 0.10))  # Discount
            self.productTable.setColumnWidth(6, int(total * 0.12))  # Total
            self.productTable.setColumnWidth(7, int(total * 0.06))  # Remove

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

        # ------------------- Official Card -------------------
        officialCard = CardFrame("Sale Type")

        officialLayout = QHBoxLayout()
        officialLayout.setSpacing(12)

        self.officialToggle = ModernRadioButton("Official")
        self.notOfficialToggle = ModernRadioButton("Not Official")

        # Default selection
        self.notOfficialToggle.setChecked(True)

        self.officialGroup = QButtonGroup(self)
        self.officialGroup.setExclusive(True)
        self.officialGroup.addButton(self.officialToggle)
        self.officialGroup.addButton(self.notOfficialToggle)

        officialLayout.addWidget(self.officialToggle)
        officialLayout.addWidget(self.notOfficialToggle)
        officialLayout.addStretch()

        officialCard.layout.addLayout(officialLayout)
        bottomRow.addWidget(officialCard, 1)

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

        self.checkoutBtn.clicked.connect(self.onAddProductClicked)

    # ------------------- Add Product Clicked Handler -------------------
    def onAddProductClicked(self):
        try:
            self.addProductRow({
                "name": self.productNameInput.text().strip(),
                "price": float(self.priceInput.text().strip() or 0),
                "qty": float(self.qtyInput.text().strip() or 1)
            })
        except Exception as e:
            QMessageBox.warning(self, "Invalid Information", "Please check the product details entered.")
            return

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

    def _shouldHandleGlobalScan(self):
        """Only capture scans on the main sales screen (not inside dialogs)."""
        if not self.isVisible():
            return False
        if QApplication.activeModalWidget() is not None:
            return False
        if QApplication.activeWindow() is not self.window():
            return False
        return True

    def _resetScanBuffer(self):
        self._scan_buffer = ""
        self._last_scan_time = 0.0

    def _stripBarcodeFromFocus(self, barcode):
        """Remove scanned digits that landed in the focused line edit."""
        focus = QApplication.focusWidget()
        if not isinstance(focus, QLineEdit) or not barcode:
            return
        text = focus.text()
        if text == barcode:
            focus.clear()
        elif text.endswith(barcode):
            focus.setText(text[: -len(barcode)])

    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress and self._shouldHandleGlobalScan():
            key = event.key()
            text = event.text()
            now = time.monotonic()

            if key in (Qt.Key_Return, Qt.Key_Enter):
                # Scanner finished: rapid digit burst ending with Enter
                if (
                    self._scan_buffer
                    and len(self._scan_buffer) >= 6
                    and (now - self._last_scan_time) < 0.15
                ):
                    barcode = self._scan_buffer
                    self._resetScanBuffer()
                    self.barcode_timer.stop()
                    self._stripBarcodeFromFocus(barcode)
                    self.barcode_buffer = barcode
                    self.processBarcode()
                    return True
                self._resetScanBuffer()
                return False

            if text and text.isdigit():
                # New burst if typing paused (human) vs continuous (scanner)
                if self._last_scan_time and (now - self._last_scan_time) > 0.12:
                    self._scan_buffer = ""
                self._scan_buffer += text
                self._last_scan_time = now
                self.barcode_buffer = self._scan_buffer
                # Fallback for scanners that do not send Enter
                self.barcode_timer.start(120)
                return False

            if text:
                self._resetScanBuffer()

        return super().eventFilter(obj, event)

    def onProductNameTextChanged(self, text):
        """Handle text changes in product name input for barcode detection"""
        # If text is empty, reset barcode buffer
        if not text:
            self.barcode_buffer = ""
            return
        
        # If text is numeric, add to buffer and start timer
        if text.isdigit():
            self.barcode_buffer = text
            # Restart timer - when timer completes, we'll check if it's a barcode
            self.barcode_timer.start(200)  # 200ms delay
        else:
            # If non-numeric input, it's manual typing, clear buffer
            self.barcode_buffer = ""

    def processBarcode(self):
        """Process the barcode after typing delay or global scan"""
        barcode = (self.barcode_buffer or self._scan_buffer or "").strip()
        self.barcode_timer.stop()
        self.barcode_buffer = ""
        self._resetScanBuffer()

        if not barcode or len(barcode) < 6:
            return

        try:
            db = DbClient()
            product_data = db.getProductByBarcode(barcode)

            if product_data:
                qty_text = self.qtyInput.text().strip()
                if not qty_text:
                    qty = 1.0
                    self.qtyInput.setText("1")
                else:
                    qty = float(qty_text)

                self.addProductRow({
                    "name": product_data.get("name", "Unknown Product"),
                    "price": float(product_data.get("price", 0)),
                    "productBarCode": barcode,
                    "qty": qty
                })

                self.productNameInput.clear()
                self.qtyInput.clear()
                self.priceInput.clear()
            else:
                QMessageBox.warning(
                    self,
                    "Product Not Found",
                    f"No product found with barcode: {barcode}\n\nPlease enter product details manually."
                )
                self.productNameInput.setFocus()
                self.productNameInput.clear()

        except Exception as e:
            print(f"Error processing barcode: {e}")

    # ------------------- Add Product Logic -------------------
    def addProductRow(self, productData):

        name = productData.get("name", "").strip()
        priceValue = productData.get("price", 0)
        qtyValue = productData.get("qty", 1)
        barcode = productData.get("productBarCode", "").strip()

        if not name or not priceValue:
            QMessageBox.warning(self, "Missing Information", "Please enter product name and price.")
            return

        try:
            qtyValue = float(qtyValue)
            priceValue = float(priceValue)
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Quantity and price must be valid numbers.")
            return

        # =========================================================
        # CHECK IF PRODUCT ALREADY EXISTS (BY BARCODE)
        # =========================================================
        for row in range(self.productTable.rowCount()):
            existingBarcodeItem = self.productTable.item(row, 1)

            if existingBarcodeItem and existingBarcodeItem.text().strip() == barcode:

                qty_item = self.productTable.item(row, 3)
                price_item = self.productTable.item(row, 4)
                discount_item = self.productTable.item(row, 5)

                try:
                    existingQty = float(qty_item.text())
                    unitPrice = float(price_item.text().replace("$", ""))
                    discount = float(discount_item.text().replace("%", "")) if discount_item else 0
                except ValueError:
                    QMessageBox.warning(self, "Invalid Data", "Existing product data is invalid.")
                    return

                newQty = existingQty + qtyValue
                qty_item.setText(str(int(newQty)) if newQty.is_integer() else str(newQty))

                total = (unitPrice * newQty) * (1 - discount / 100)
                self.productTable.item(row, 6).setText(f"${total:.2f}")

                self.updateGrandTotal()
                self.clearProductFields()
                return

        # =========================================================
        # ADD NEW ROW (IF PRODUCT DOES NOT EXIST)
        # =========================================================
        total = qtyValue * priceValue
        row = self.productTable.rowCount()
        self.productTable.insertRow(row)

        serialNumber = row + 1

        # ---------------- Serial Number (0) ----------------
        sn_item = QTableWidgetItem(str(serialNumber))
        sn_item.setFlags(sn_item.flags() & ~Qt.ItemIsEditable)
        sn_item.setTextAlignment(Qt.AlignCenter)
        self.productTable.setItem(row, 0, sn_item)

        # ---------------- Barcode (1) ----------------
        barcode_item = QTableWidgetItem(barcode)
        barcode_item.setTextAlignment(Qt.AlignCenter)
        self.productTable.setItem(row, 1, barcode_item)

        # ---------------- Product Name (2) ----------------
        name_item = QTableWidgetItem(name)
        self.productTable.setItem(row, 2, name_item)

        # ---------------- Qty (3) ----------------
        qty_item = QTableWidgetItem(str(int(qtyValue)) if qtyValue.is_integer() else str(qtyValue))
        qty_item.setTextAlignment(Qt.AlignCenter)
        self.productTable.setItem(row, 3, qty_item)

        # ---------------- Price (4) ----------------
        price_item = QTableWidgetItem(f"${priceValue:.2f}")
        price_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.productTable.setItem(row, 4, price_item)

        # ---------------- Discount (5) ----------------
        discount_item = QTableWidgetItem("0.0%")
        discount_item.setTextAlignment(Qt.AlignCenter)
        self.productTable.setItem(row, 5, discount_item)

        # ---------------- Total (6) ----------------
        totalItem = QTableWidgetItem(f"${total:.2f}")
        totalItem.setFlags(totalItem.flags() & ~Qt.ItemIsEditable)
        totalItem.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.productTable.setItem(row, 6, totalItem)

        # ---------------- Delete Button (7) ----------------
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
        deleteLabel.mousePressEvent = lambda event, r=row: self.deleteRow(r)

        self.productTable.setCellWidget(row, 7, deleteLabel)

        self.clearProductFields()
        self.updateGrandTotal()

    #-------------------- Refresh S/N ------------------------------
    def refreshSerialNumbers(self):
        for row in range(self.productTable.rowCount()):
            self.productTable.item(row, 0).setText(str(row + 1))

    #-------------------- Delete Row ------------------------------
    def deleteRow(self, row):
        self.productTable.removeRow(row)
        self.refreshSerialNumbers()
        self.updateGrandTotal()

    # ------------------- Update Customer Input -------------------
    def updateCustomerInput(self):
        if "name" in self.selectedCustomerDetails:
            self.customerInput.setText(self.selectedCustomerDetails["name"])

    # ------------------- Update Total Price on Cell Change -------------------
    def updateTotalPrice(self, row, column):
        if column not in [3, 4, 5]:
            return

        try:
            qty_item = self.productTable.item(row, 3)
            price_item = self.productTable.item(row, 4)
            discount_item = self.productTable.item(row, 5)

            if not discount_item:
                discount_item = QTableWidgetItem("0.0%")
                self.productTable.setItem(row, 5, discount_item)

            # -------- Validate Quantity --------
            try:
                qty = float(qty_item.text()) if qty_item and qty_item.text() else 0
            except ValueError:
                QMessageBox.warning(
                    self,
                    "Invalid Quantity",
                    "Please enter a valid number for quantity."
                )
                return

            # -------- Validate Price --------
            try:
                price = float(price_item.text().replace("$", "")) if price_item and price_item.text() else 0
            except ValueError:
                QMessageBox.warning(
                    self,
                    "Invalid Price",
                    "Please enter a valid number for price."
                )
                return

            # -------- Validate Discount --------
            try:
                discount = float(discount_item.text().replace("%", "")) if discount_item.text() else 0
            except ValueError:
                QMessageBox.warning(
                    self,
                    "Invalid Discount",
                    "Please enter a valid number for discount."
                )
                return

            total = (price * qty) * (1 - discount / 100)

            total_item = self.productTable.item(row, 6)
            if not total_item:
                total_item = QTableWidgetItem()
                self.productTable.setItem(row, 6, total_item)

            self.productTable.blockSignals(True)
            total_item.setText(f"${total:.2f}")
            discount_item.setText(f"{discount:.1f}%")
            self.productTable.blockSignals(False)

            self.updateGrandTotal()

        except Exception:
            QMessageBox.warning(
                self,
                "Invalid Input",
                "Please enter valid numeric values."
            )

    # ------------------- Update Grand Total -------------------
    def updateGrandTotal(self):
        total = 0.0
        for row in range(self.productTable.rowCount()):
            total_item = self.productTable.item(row, 6)  # Updated to Total column
            if total_item and total_item.text():
                try:
                    total += float(total_item.text().replace("$", ""))
                except ValueError:
                    continue

        self.totalAmountValue.setText(f"${total:.2f}")

    # ------------------- Handle Void Sale -------------------
    def handleVoidSale(self):

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

        # ------------------ Customer Check ------------------
        customerName = self.customerInput.text().strip()

        if not self.selectedCustomerDetails:
            if customerName:
                self.selectedCustomerDetails = {
                    "name": customerName,
                    "customerID": None
                }
            else:
                self.selectedCustomerDetails = {}

        # ------------------ Collect Product Table Data ------------------
        self.finalProductList = []

        for row in range(self.productTable.rowCount()):

            # UPDATED COLUMN INDEXES
            nameItem = self.productTable.item(row, 2)
            barcodeItem = self.productTable.item(row, 1)
            qtyItem = self.productTable.item(row, 3)
            priceItem = self.productTable.item(row, 4)
            discountItem = self.productTable.item(row, 5)

            # ---- Validate Product Name ----
            if not nameItem or not nameItem.text().strip():
                QMessageBox.warning(
                    self,
                    "Invalid Product",
                    f"Missing product name for product {row + 1}."
                )
                return {"status": "Failed", "saleID": None}

            # ---- Validate Quantity ----
            try:
                quantity = int(float(qtyItem.text())) if qtyItem and qtyItem.text() else 0
                if quantity <= 0:
                    raise ValueError
            except ValueError:
                QMessageBox.warning(
                    self,
                    "Invalid Quantity",
                    f"Invalid quantity for product {row + 1}."
                )
                return {"status": "Failed", "saleID": None}

            # ---- Validate Price ----
            try:
                price = float(priceItem.text().replace("$", "")) if priceItem and priceItem.text() else 0
                if price < 0:
                    raise ValueError
            except ValueError:
                QMessageBox.warning(
                    self,
                    "Invalid Price",
                    f"Invalid price for product {row + 1}."
                )
                return {"status": "Failed", "saleID": None}

            # ---- Validate Discount ----
            try:
                discount = float(discountItem.text().replace("%", "")) if discountItem and discountItem.text() else 0
                if discount < 0 or discount > 100:
                    raise ValueError
            except ValueError:
                QMessageBox.warning(
                    self,
                    "Invalid Discount",
                    f"Invalid discount for product {row + 1}."
                )
                return {"status": "Failed", "saleID": None}

            self.finalProductList.append({
                "name": nameItem.text().strip(),
                "barcode": barcodeItem.text().strip() if barcodeItem else "",
                "quantity": quantity,
                "price": price,
                "discount": discount
            })

        # ------------------ Validate Products ------------------
        if not self.finalProductList:
            QMessageBox.warning(
                self,
                "No Products",
                "Please add at least one product before proceeding."
            )
            return {"status": "Failed", "saleID": None}

        # ------------------ Validate Payment ------------------
        checkedButton = self.paymentGroup.checkedButton()
        if not checkedButton:
            QMessageBox.warning(
                self,
                "Payment Type Required",
                "Please select a payment type before proceeding."
            )
            return {"status": "Failed", "saleID": None}

        # ------------------ Prepare Sale Data ------------------
        isOfficial = 1 if self.officialToggle.isChecked() else 0

        saleData = {
            "saleDateTime": datetime.now(),
            "customerID": self.selectedCustomerDetails.get("customerID"),
            "paymentType": checkedButton.text(),
            "note": self.notesInput.text().strip(),
            "official": isOfficial,
            "items": self.finalProductList
        }

        # ------------------ Save to Database ------------------
        response = self.dbClent.addSaleWithItems(saleData)

        if response.get("status") == "Success":
            if type != "invoice":
                QMessageBox.information(self, "Success", "Sale saved successfully!")
                self.handleVoidSale()

            return {"status": "Success", "saleID": response.get("saleID")}

        else:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to save sale.\n\n{response.get('message')}"
            )
            return {"status": "Failed", "saleID": None}

    # ------------------- Handle Print Invoice -------------------
    def handlePrintInvoice(self):
        # Save Sale First
        status = self.handleSaveSales("invoice")

        if status["status"] != "Success":
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
        buffer = generateInvoice(
            customerData=customerData,
            productData=productDataForPDF,
            saleID=status["saleID"],
            date=datetime.now(),
            saveToFile=False
        )
        status=  printPDF(buffer)
        # Show message
        if status["status"] == "Success":
            QMessageBox.information(self, "Print Status", status["message"])

            # Clear sale ONLY if print succeeded
            self.handleVoidSale()
        else:
            QMessageBox.critical(self, "Print Failed", status["message"])

    # ------------------- Refresh Customer Sidebar -------------------
    def refreshCustomerSidebar(self):
        self.sideBar.updateCustomerInfo()
