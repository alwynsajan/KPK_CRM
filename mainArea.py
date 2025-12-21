# mainArea.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout,
    QPushButton, QTableWidget, QHeaderView, QSizePolicy,
    QTableWidgetItem, QCheckBox, QTextEdit,QRadioButton,QButtonGroup,QMessageBox
)
from PySide6.QtCore import Qt
from dbClient import DbClient
from customerSelectorDialog import openCustomerSelector
from productSelectorDialog import openProductSelector
from datetime import date

class MainArea(QWidget):
    def __init__(self, selectedCustomerDetails=None, finalProductList=None, sidebar=None):
        super().__init__()

        self.dbClent= DbClient()

        self.selectedCustomerDetails = selectedCustomerDetails or {}
        self.finalProductList = finalProductList or []
        self.sidebar = sidebar  # reference to sidebar to update it dynamically

        mainAreaLayout = QVBoxLayout()
        mainAreaLayout.setAlignment(Qt.AlignTop)
        mainAreaLayout.setSpacing(15)


        # ------------------- Button Styles -------------------
        primaryBtnStyle = """
            QPushButton {
                background-color: #3498DB;
                color: white;
                padding: 5px 15px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2E86C1;
            }
        """
        successBtnStyle = """
                            QPushButton {
                                background-color: #2ECC71;   /* green */
                                color: white;
                                padding: 5px 15px;
                                border-radius: 5px;
                                font-size: 14px;
                                font-weight: bold;
                            }
                            QPushButton:hover {
                                background-color: #27AE60;
                            }
                        """

        failureBtnStyle = """
            QPushButton {
                background-color: #E74C3C;
                color: white;
                padding: 5px 15px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
        """

        # ------------------- Customer Section -------------------
        mainAreaLayout.addWidget(QLabel("Customer Name:"))
        mainAreaLayout.itemAt(mainAreaLayout.count() - 1).widget().setStyleSheet("font-size:16px; font-weight:bold; color:black;")

        self.customerInput = QLineEdit()
        self.customerInput.setFixedHeight(30)
        self.customerInput.setPlaceholderText("Enter customer name")
        self.customerInput.setStyleSheet("""
                                        background-color: #FFFFFF;
                                        color: black;               
                                        border: 1px solid #ccc; 
                                        border-radius: 6px;    
                                        padding-left: 5px;          
                                    """)
        mainAreaLayout.addWidget(self.customerInput)

        # Customer Buttons
        customerBtnLayout = QHBoxLayout()
        customerBtnLayout.setAlignment(Qt.AlignLeft)

        self.selectCustomerBtn = QPushButton("Select Customer")
        self.clearCustomerBtn = QPushButton("Clear")

        self.selectCustomerBtn.setStyleSheet(primaryBtnStyle)
        self.clearCustomerBtn.setStyleSheet(failureBtnStyle)

        for btn in [self.selectCustomerBtn, self.clearCustomerBtn]:
            btn.setFixedHeight(28)
            btn.setFixedWidth(140)
            btn.setCursor(Qt.PointingHandCursor)

        customerBtnLayout.addWidget(self.selectCustomerBtn)
        customerBtnLayout.addWidget(self.clearCustomerBtn)
        mainAreaLayout.addLayout(customerBtnLayout)

        self.selectCustomerBtn.clicked.connect(
                                lambda: openCustomerSelector(
                                    parent=self,
                                    customerInput=self.customerInput,
                                    selectedCustomerDetails=self.selectedCustomerDetails
                                )
                            )


        self.clearCustomerBtn.clicked.connect(self.clearCustomerData)

        mainAreaLayout.addSpacing(20)

        # ------------------- Product Section -------------------
        mainAreaLayout.addWidget(QLabel("Product Name:"))
        mainAreaLayout.itemAt(mainAreaLayout.count() - 1).widget().setStyleSheet("font-size:16px; font-weight:bold; color:black;")

        productFormLayout = QHBoxLayout()

        self.productNameInput = QLineEdit()
        self.productNameInput.setFixedHeight(30)
        self.productNameInput.setPlaceholderText("Enter product name")
        self.productNameInput.setStyleSheet("""
                                        background-color: #FFFFFF;
                                        color: black;               
                                        border: 1px solid #ccc; 
                                        border-radius: 6px;    
                                        padding-left: 5px;          
                                    """)

        self.qtyInput = QLineEdit()
        self.qtyInput.setFixedHeight(30)
        self.qtyInput.setPlaceholderText("Enter quantity")
        self.qtyInput.setStyleSheet("""
                                        background-color: #FFFFFF;
                                        color: black;               
                                        border: 1px solid #ccc; 
                                        border-radius: 6px;    
                                        padding-left: 5px;          
                                    """)

        self.priceInput = QLineEdit()
        self.priceInput.setFixedHeight(30)
        self.priceInput.setPlaceholderText("Enter unit price")
        self.priceInput.setStyleSheet("""
                                        background-color: #FFFFFF;
                                        color: black;               
                                        border: 1px solid #ccc; 
                                        border-radius: 6px;    
                                        padding-left: 5px;          
                                    """)

        self.checkoutBtn = QPushButton("Checkout")
        self.checkoutBtn.setStyleSheet(successBtnStyle)
        self.checkoutBtn.setFixedHeight(30)
        self.checkoutBtn.setCursor(Qt.PointingHandCursor)

        productFormLayout.addWidget(self.productNameInput)
        productFormLayout.addWidget(self.qtyInput)
        productFormLayout.addWidget(self.priceInput)
        productFormLayout.addWidget(self.checkoutBtn)

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
            btn.setCursor(Qt.PointingHandCursor)

        productBtnLayout.addWidget(self.selectProductBtn)
        productBtnLayout.addWidget(self.clearProductBtn)
        mainAreaLayout.addLayout(productBtnLayout)

        # Connect the Clear button
        self.clearProductBtn.clicked.connect(self.clearProductFields)

        # Connect the Select Product button
        self.selectProductBtn.clicked.connect(
                                    lambda: openProductSelector(
                                        parent=self,
                                        addProductRow=self.addProductRow
                                    )
                                )
        mainAreaLayout.addSpacing(20)

        # ------------------- Product Table -------------------
        self.productTable = QTableWidget()
        self.productTable.setColumnCount(6)
        self.productTable.setHorizontalHeaderLabels(
            ["Product Name", "Qty", "Unit Price", "Discount", "Total Price", "Delete"]
        )

        self.productTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # reduce table height
        self.productTable.setFixedHeight(180)
        self.productTable.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.productTable.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.productTable.setStyleSheet("""
                                            QTableWidget {
                                                background-color: white;
                                                gridline-color: #cccccc;
                                            }
                                            QHeaderView::section {
                                                background-color: #f0f0f0;
                                                font-weight: bold;
                                            }
                                        /* --- Vertical Scrollbar --- */
                                            QScrollBar:vertical {
                                                background: transparent;
                                                width: 10px;
                                                margin: 0px;
                                            }

                                            QScrollBar::handle:vertical {
                                                background: lightblue;
                                                border-radius: 5px;
                                                min-height: 30px;
                                            }

                                            QScrollBar::handle:vertical:hover {
                                                background: #2E86C1;
                                            }

                                            QScrollBar::add-line:vertical,
                                            QScrollBar::sub-line:vertical {
                                                height: 0px;
                                                background: none;
                                            }

                                            QScrollBar::add-page:vertical,
                                            QScrollBar::sub-page:vertical {
                                                background: none;
                                            }
                                        """)
        self.productTable.cellChanged.connect(self.updateTotalPrice)
        mainAreaLayout.addWidget(self.productTable)

        # Connect Add Product Button
        self.checkoutBtn.clicked.connect(lambda: self.addProductRow({
                                                        "name": self.productNameInput.text().strip(),
                                                        "price": float(self.priceInput.text().strip() or 0),
                                                        "qty": float(self.qtyInput.text().strip() or 1)
                                                    }))
        # ------------------- Total Amount Section -------------------
        totalLayout = QHBoxLayout()

        totalLayout.addStretch()  # push content to the right

        self.totalAmountLabel = QLabel("Total Amount:")
        self.totalAmountLabel.setStyleSheet(
            "font-size:16px; font-weight:bold; color:black;"
        )

        self.totalAmountValue = QLabel("0.00")
        self.totalAmountValue.setStyleSheet(
            "font-size:18px; font-weight:bold; color:#2E86C1;"
        )
        self.totalAmountValue.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        totalLayout.addWidget(self.totalAmountLabel)
        totalLayout.addSpacing(10)
        totalLayout.addWidget(self.totalAmountValue)

        mainAreaLayout.addLayout(totalLayout)


        # ------------------- Notes Section -------------------
        self.notesInput = QLineEdit()
        self.notesInput.setPlaceholderText("Enter note")
        self.notesInput.setFixedHeight(30)
        self.notesInput.setStyleSheet("""
                                        background-color: #FFFFFF;
                                        color: black;               
                                        border: 1px solid #ccc; 
                                        border-radius: 6px;    
                                        padding-left: 5px;          
                                    """)
        mainAreaLayout.addWidget(self.notesInput)

        # ------------------- Payment Options -------------------
        paymentLayout = QHBoxLayout()
        paymentLayout.setAlignment(Qt.AlignLeft)

        self.efposRadio = QRadioButton("EFTPOS")
        self.cashRadio = QRadioButton("Cash")
        self.bankRadio = QRadioButton("Bank Transfer")
        self.creditRadio = QRadioButton("Credit")

        # Set font size and cursor
        for radio in [self.efposRadio, self.cashRadio, self.bankRadio, self.creditRadio]:
            radio.setStyleSheet("""
                QRadioButton {
                    font-size: 14px;
                    color: black;
                    font-weight: bold;
                }
                QRadioButton::indicator {
                    width: 18px;
                    height: 18px;
                    border-radius: 9px;
                    background-color: #cccccc;  /* default grey */
                    border: 1px solid #999999;
                }
                QRadioButton::indicator:checked {
                    background-color: #3498DB;  /* blue when selected */
                    border: 1px solid #2980B9;
                }
            """)
            radio.setCursor(Qt.PointingHandCursor)

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
        self.printInvoiceBtn = QPushButton("Print Invoive")

        self.saveSalesBtn.setStyleSheet(successBtnStyle)
        self.printInvoiceBtn.setStyleSheet(primaryBtnStyle)

        for btn in [self.saveSalesBtn, self.printInvoiceBtn]:
            btn.setFixedHeight(30)
            btn.setFixedWidth(150)

        self.saveSalesBtn.clicked.connect(self.handleSaveSales)


        actionBtnLayout.addWidget(self.saveSalesBtn)
        actionBtnLayout.addWidget(self.printInvoiceBtn)

        mainAreaLayout.addLayout(actionBtnLayout)
        self.saveSalesBtn.setCursor(Qt.PointingHandCursor)
        self.printInvoiceBtn.setCursor(Qt.PointingHandCursor)

        self.setLayout(mainAreaLayout)

    # ------------------- Clear Customer Data -------------------
    def clearCustomerData(self):
        self.selectedCustomerDetails = {}
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
        qtyValue = productData.get("qty", 1)  # default 1 if not provided

        if not name or not priceValue:
            return

        try:
            qtyValue = float(qtyValue)
            priceValue = float(priceValue)
        except ValueError:
            return

        total = qtyValue * priceValue

        row = self.productTable.rowCount()
        self.productTable.insertRow(row)

        self.productTable.setItem(row, 0, QTableWidgetItem(name))
        self.productTable.setItem(row, 1, QTableWidgetItem(str(qtyValue)))
        self.productTable.setItem(row, 2, QTableWidgetItem(str(priceValue)))
        self.productTable.setItem(row, 3, QTableWidgetItem("0"))  # discount or other field
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

        self.updateGrandTotal()

    # ------------------- Update Customer Input -------------------
    def updateCustomerInput(self):
        # Update the input field with saved customer name
        if "name" in self.selectedCustomerDetails:
            self.customerInput.setText(self.selectedCustomerDetails["name"])

    # ------------------- Update Total Price on Cell Change -------------------
    def updateTotalPrice(self, row, column):
        # Only update if Qty, Unit Price, or Discount columns are changed
        if column not in [1, 2, 3]:  # Qty=1, Unit Price=2, Discount=3
            return

        try:
            qty_item = self.productTable.item(row, 1)
            price_item = self.productTable.item(row, 2)
            discount_item = self.productTable.item(row, 3)

            qty = float(qty_item.text()) if qty_item and qty_item.text() else 0
            price = float(price_item.text()) if price_item and price_item.text() else 0
            discount_percent = float(discount_item.text()) if discount_item and discount_item.text() else 0

            total = (price * qty) * (1 - discount_percent / 100)

            # Update the Total Price cell safely
            total_item = self.productTable.item(row, 4)
            if not total_item:
                total_item = QTableWidgetItem()
                self.productTable.setItem(row, 4, total_item)

            # Block signals to avoid infinite recursion
            self.productTable.blockSignals(True)
            total_item.setText(f"{total:.2f}")
            self.productTable.blockSignals(False)

            self.updateGrandTotal()

        except ValueError:
            pass  # Ignore invalid inputs

    def updateGrandTotal(self):
        total = 0.0
        for row in range(self.productTable.rowCount()):
            item = self.productTable.item(row, 4)  # Total Price column
            if item and item.text():
                try:
                    total += float(item.text())
                except ValueError:
                    pass

        self.totalAmountValue.setText(f"{total:.2f}")


    # ------------------- Handle Save Sales -------------------
    def handleSaveSales(self):
        # ------------------ Customer Check ------------------
        customerName = self.customerInput.text().strip()

        # If no selected customer details, try using input field
        if not self.selectedCustomerDetails:
            if customerName:
                self.selectedCustomerDetails = {
                    "name": customerName
                }
            else:
                self.selectedCustomerDetails = {}

        print("Customer Details:", self.selectedCustomerDetails)

        # ------------------ Product Table Data ------------------
        finalProductList = []

        for row in range(self.productTable.rowCount()):
            nameItem = self.productTable.item(row, 0)
            qtyItem = self.productTable.item(row, 1)
            priceItem = self.productTable.item(row, 2)
            discountItem = self.productTable.item(row, 3)

            # ---------------- Validate Quantity ----------------
            try:
                quantity = int(float(qtyItem.text())) if qtyItem and qtyItem.text() else 0
            except ValueError:
                QMessageBox.warning(
                    self,
                    "Invalid Quantity",
                    f"Invalid quantity on row {row+1}. Please enter a valid integer."
                )
                return

            # ---------------- Validate Price ----------------
            try:
                price = float(priceItem.text()) if priceItem and priceItem.text() else 0.0
            except ValueError:
                QMessageBox.warning(
                    self,
                    "Invalid Price",
                    f"Invalid unit price on row {row+1}. Please enter a valid number."
                )
                return

            # ---------------- Validate Discount ----------------
            try:
                discount = float(discountItem.text()) if discountItem and discountItem.text() else 0.0
            except ValueError:
                QMessageBox.warning(
                    self,
                    "Invalid Discount",
                    f"Invalid discount on row {row+1}. Please enter a valid number."
                )
                return

            productData = {
                "name": nameItem.text().strip(),
                "quantity": quantity,
                "price": price,
                "discount": discount
            }

            finalProductList.append(productData)

        # ------------------ Print Result ------------------
        print("\nFinal Product List:",finalProductList)

        # ------------------ Validate Products ------------------
        if not finalProductList:
            QMessageBox.warning(self, "No Products", "Please add at least one product before saving.")
            return

        # ------------------ Validate Payment ------------------
        checkedButton = self.paymentGroup.checkedButton()
        if not checkedButton:
            QMessageBox.warning(self, "Payment Type Required", "Please select a payment type before saving.")
            return

        saleData = {
        "saleDate": date.today(),
        "customerID": self.selectedCustomerDetails.get("customerID"),
        "paymentType": checkedButton.text(),
        "note": self.notesInput.text().strip(),
        "items": finalProductList  # list of dicts
                                            }

        response = self.dbClent.addSaleWithItems(saleData)
        print(response)

        # ------------------ Popup Result ------------------
        if response.get("status") == "Success":
            QMessageBox.information(
                self,
                "Sale Saved",
                f"Sale saved successfully!"
            )

            # Optional: clear UI after save
            self.productTable.setRowCount(0)
            self.notesInput.clear()
            self.customerInput.clear()
            self.selectedCustomerDetails.clear()

        else:
            QMessageBox.critical(
                self,
                "Save Failed",
                f"Failed to save sale.\n\n{response.get('error')}"
            )








