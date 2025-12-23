# sidebar.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea,
    QSizePolicy, QTableWidget, QTableWidgetItem,
    QHBoxLayout, QMessageBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPalette, QColor

from productForm import ProductForm
from addNewCustomer import CustomerForm
from dbClient import DbClient


class SideBar(QWidget):
    customerAdded = Signal(dict)  # forward signal to main window

    def __init__(self, selectedCustomerDetails=None):
        super().__init__()

        if selectedCustomerDetails is None:
            self.selectedCustomerDetails = {}
        else:
            self.selectedCustomerDetails = selectedCustomerDetails

        # -------- Background --------
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#547792"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # -------- Main Layout --------
        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(10, 10, 10, 10)
        mainLayout.setSpacing(10)
        mainLayout.setAlignment(Qt.AlignTop)

        # -------- Buttons --------
        btnNames = ["Add Product to DB", "Add new Customer"]
        for name in btnNames:
            btn = QPushButton(name)

            if name == "Add Product to DB":
                btn.clicked.connect(self.openProductForm)
            elif name == "Add new Customer":
                btn.clicked.connect(self.openCustomerForm)

            btn.setStyleSheet("""
                QPushButton {
                    background-color: #3498DB;
                    color: white;
                    padding: 10px;
                    border-radius: 5px;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #2E86C1;
                }
            """)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            mainLayout.addWidget(btn)

        # -------- Scroll Area --------
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.scrollWidget = QWidget()
        self.scrollLayout = QVBoxLayout(self.scrollWidget)
        self.scrollLayout.setAlignment(Qt.AlignTop)

        self.scrollArea.setWidget(self.scrollWidget)
        mainLayout.addWidget(self.scrollArea, 1)

        self.updateCustomerInfo()

    # ---------------- Customer Info ----------------
    def updateCustomerInfo(self):
        # Clear existing widgets
        for i in reversed(range(self.scrollLayout.count())):
            widget = self.scrollLayout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        # ---------- No customer ----------
        if not self.selectedCustomerDetails:
            container = QWidget()
            containerLayout = QVBoxLayout(container)
            containerLayout.setContentsMargins(0, 0, 0, 0)

            label = QLabel("Select customer to see Sales History")
            label.setWordWrap(True)
            label.setStyleSheet("font-size: 14px; font-weight: bold; color: black;")
            containerLayout.addWidget(label)
            self.scrollLayout.addWidget(container)
            return

        cust = self.selectedCustomerDetails

        # ---------- Customer Info Box ----------
        infoBox = QWidget()
        infoBox.setStyleSheet("""
            QWidget {
                background-color: #FFFFFF;
                border: 1px solid #CCCCCC;
                border-radius: 6px;
                padding: 10px;
            }
        """)

        infoLayout = QVBoxLayout(infoBox)
        infoLayout.setSpacing(6)

        def infoLabel(text):
            lbl = QLabel(text)
            lbl.setWordWrap(True)
            lbl.setStyleSheet("font-size: 14px; font-weight: bold; color: black;")
            return lbl

        infoLayout.addWidget(infoLabel(f"Name: {cust.get('name', '')}"))
        infoLayout.addWidget(infoLabel(f"Address: {cust.get('address', '')}"))
        infoLayout.addWidget(infoLabel(f"Phone: {cust.get('phone', '')}"))
        infoLayout.addWidget(infoLabel(f"Email: {cust.get('email', '')}"))

        self.scrollLayout.addWidget(infoBox)

        # ---------- Update Button ----------
        updateBtn = QPushButton("Update")
        updateBtn.setCursor(Qt.PointingHandCursor)
        updateBtn.setFixedWidth(100)
        updateBtn.clicked.connect(self.openCustomerUpdateDialog)
        updateBtn.setStyleSheet("""
            QPushButton {
                background-color: #3498DB;
                color: white;
                padding: 6px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2E86C1;
            }
        """)

        btnLayout = QHBoxLayout()
        btnLayout.addStretch()
        btnLayout.addWidget(updateBtn)
        btnLayout.addStretch()
        btnWidget = QWidget()
        btnWidget.setLayout(btnLayout)
        self.scrollLayout.addWidget(btnWidget)

        # ---------- Show Sales ONLY if from DB ----------
        if "customerID" not in cust:
            return  # Newly added customer → no sales yet

        # ---------- Sales History ----------
        db = DbClient()
        sales = db.getCustomerSalesHistory(cust["customerID"])

        title = QLabel("Previous Sales History:")
        title.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 10px;")
        title.setWordWrap(True)
        self.scrollLayout.addWidget(title)

        if not sales:
            noSalesLabel = QLabel("No sales found")
            noSalesLabel.setWordWrap(True)
            noSalesLabel.setStyleSheet("font-size: 13px; color: #555555;")
            self.scrollLayout.addWidget(noSalesLabel)
            return

        # ---------- Sales Table ----------
        salesTable = QTableWidget()
        salesTable.setColumnCount(4)
        salesTable.setHorizontalHeaderLabels(["Date", "Item Name", "Qty", "Price"])
        salesTable.verticalHeader().setVisible(False)
        salesTable.setEditTriggers(QTableWidget.NoEditTriggers)
        salesTable.setSelectionMode(QTableWidget.NoSelection)
        salesTable.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: none;
            }
            QHeaderView::section {
                background-color: #F0F0F0;
                font-weight: bold;
                border: none;
            }
            QScrollBar:vertical, QScrollBar:horizontal {
                background: #E0F3FF; /* light blue track */
                border-radius: 4px;
                height: 10px;
                width: 10px;
            }
            QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
                background: #5BC0FF; /* slightly darker blue handle */
                min-height: 20px;
                min-width: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                height: 0px;
                width: 0px;
            }
        """)

        for row, (date, item, qty, price) in enumerate(sales):
            salesTable.insertRow(row)
            salesTable.setItem(row, 0, QTableWidgetItem(str(date)))
            salesTable.setItem(row, 1, QTableWidgetItem(item))
            salesTable.setItem(row, 2, QTableWidgetItem(str(qty)))
            salesTable.setItem(row, 3, QTableWidgetItem(f"{price:.2f}"))

        salesTable.resizeColumnsToContents()
        salesTable.resizeRowsToContents()

        salesScroll = QScrollArea()
        salesScroll.setWidgetResizable(True)
        salesScroll.setWidget(salesTable)
        salesScroll.setFixedHeight(300)
        salesScroll.setStyleSheet("""
            QScrollArea {
                border: 1px solid #CCCCCC;
                border-radius: 5px;
            }
            QScrollBar:vertical, QScrollBar:horizontal {
                background: #E0F3FF;
                border-radius: 4px;
                height: 10px;
                width: 10px;
            }
            QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
                background: #5BC0FF;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                height: 0px;
                width: 0px;
            }
        """)

        self.scrollLayout.addWidget(salesScroll)

        # ---------- Apply modern scrollbar to main sidebar scroll area ----------
        self.scrollArea.setStyleSheet("""
            QScrollBar:vertical, QScrollBar:horizontal {
                background: #E0F3FF;
                border-radius: 4px;
                height: 10px;
                width: 10px;
            }
            QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
                background: #5BC0FF;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                height: 0px;
                width: 0px;
            }
        """)



    # ---------------- Open Forms ----------------
    def openProductForm(self):
        self.productWindow = ProductForm()
        self.productWindow.show()

    def openCustomerForm(self):
        self.customerForm = CustomerForm()
        self.customerForm.customerAdded.connect(self.onCustomerAdded)
        self.customerForm.show()

    def onCustomerAdded(self, customerData):
        self.customerAdded.emit(customerData)  # forward signal

    def openCustomerUpdateDialog(self):
        QMessageBox.information(
            self,
            "Update Customer",
            "Customer update dialog coming soon."
        )
