# sidebar.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea,
    QSizePolicy, QTableWidget, QTableWidgetItem,
    QHBoxLayout, QMessageBox, QFrame, QSpacerItem
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPalette, QColor

from productForm import ProductForm
from addNewCustomer import CustomerForm
from dbClient import DbClient
from customerUpdateDialog import openCustomerUpdateDialog as openUpdateDialog


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
        palette.setColor(QPalette.Window, QColor("#1e293b"))  # Dark slate background
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # -------- Main Layout --------
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(16, 16, 16, 16)
        self.mainLayout.setSpacing(16)
        self.mainLayout.setAlignment(Qt.AlignTop)

        # -------- Buttons with modern design --------
        btnNames = ["Add New Product", "Add new Customer"]
        btnIcons = ["📦", "👤"]
        
        for name, icon in zip(btnNames, btnIcons):
            btn = QPushButton(f"{icon}  {name}")
            
            if name == "Add New Product":
                btn.clicked.connect(self.openProductForm)
            elif name == "Add new Customer":
                btn.clicked.connect(self.openCustomerForm)

            btn.setStyleSheet("""
                QPushButton {
                    background-color: #3b82f6;
                    color: white;
                    padding: 14px;
                    border-radius: 10px;
                    font-size: 14px;
                    font-weight: 600;
                    border: none;
                    text-align: left;
                    padding-left: 20px;
                    margin-left: 2px;
                    margin-right: 2px;
                }
                QPushButton:hover {
                    background-color: #2563eb;
                }
                QPushButton:pressed {
                    background-color: #1d4ed8;
                }
            """)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.setMinimumHeight(50)
            self.mainLayout.addWidget(btn)

        # -------- Content Area (No Scroll Area) --------
        self.contentWidget = QWidget()
        self.contentWidget.setStyleSheet("background-color: transparent;")
        self.contentLayout = QVBoxLayout(self.contentWidget)
        self.contentLayout.setContentsMargins(2, 0, 2, 0)
        self.contentLayout.setSpacing(16)
        self.contentLayout.setAlignment(Qt.AlignTop)
        
        # Add content widget with stretch factor
        self.mainLayout.addWidget(self.contentWidget, 1)

        self.updateCustomerInfo()

    # ---------------- Customer Info ----------------
    def updateCustomerInfo(self):
        # Clear existing widgets
        while self.contentLayout.count():
            item = self.contentLayout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # Remove any existing spacer
        for i in reversed(range(self.contentLayout.count())):
            item = self.contentLayout.itemAt(i)
            if isinstance(item, QSpacerItem):
                self.contentLayout.removeItem(item)

        # ---------- No customer ----------
        if not self.selectedCustomerDetails:
            # Add the "Select customer" label
            label = QLabel("👈 Select a customer to view details and sales history")
            label.setWordWrap(True)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("""
                QLabel {
                    font-size: 14px;
                    font-weight: 500;
                    color: grey;
                    padding: 40px 20px;
                    background-color: rgba(255, 255, 255, 0.05);
                    border-radius: 12px;
                    border: 2px dashed #475569;
                }
            """)
            label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.contentLayout.addWidget(label, 1)  # Add with stretch factor
            return

        cust = self.selectedCustomerDetails

        # ---------- Customer Details Card ----------
        detailsCard = QFrame()
        detailsCard.setFrameShape(QFrame.StyledPanel)
        detailsCard.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border-radius: 12px;
                border: 1px solid #e2e8f0;
            }
        """)
        detailsCard.setMinimumHeight(180)  # Minimum height, can expand if needed
        detailsCard.setMaximumHeight(220)  # Maximum height to prevent excessive growth
        
        detailsLayout = QVBoxLayout(detailsCard)
        detailsLayout.setContentsMargins(20, 16, 20, 16)
        detailsLayout.setSpacing(10)

        # Title
        titleLabel = QLabel("👤 Customer Details")
        titleLabel.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: 700;
                color: #1e293b;
                padding-bottom: 8px;
                border-bottom: 2px solid #f1f5f9;
            }
        """)
        detailsLayout.addWidget(titleLabel)

        # Details container with scroll for long content
        detailsContainer = QScrollArea()
        detailsContainer.setWidgetResizable(True)
        detailsContainer.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        detailsContainer.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        detailsContainer.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background-color: #f1f5f9;
                width: 6px;
                border-radius: 3px;
            }
            QScrollBar::handle:vertical {
                background-color: #cbd5e1;
                border-radius: 3px;
                min-height: 20px;
            }
        """)
        
        detailsContent = QWidget()
        detailsContentLayout = QVBoxLayout(detailsContent)
        detailsContentLayout.setContentsMargins(0, 0, 0, 0)
        detailsContentLayout.setSpacing(8)
        
        # Customer details with icons
        details = [
            ("📝", "Name", cust.get('name', 'N/A')),
            ("🏠", "Address", cust.get('address', 'N/A')),
            ("📱", "Phone", cust.get('phone', 'N/A')),
            ("📧", "Email", cust.get('email', 'N/A'))
        ]
        
        for icon, label, value in details:
            rowWidget = QWidget()
            rowLayout = QHBoxLayout(rowWidget)
            rowLayout.setContentsMargins(0, 0, 0, 0)
            rowLayout.setSpacing(10)
            
            iconLabel = QLabel(icon)
            iconLabel.setStyleSheet("font-size: 14px; color: #64748b;")
            
            labelLabel = QLabel(f"{label}:")
            labelLabel.setStyleSheet("""
                QLabel {
                    font-size: 14px;
                    font-weight: 600;
                    color: #475569;
                    min-width: 70px;
                }
            """)
            
            valueLabel = QLabel(str(value))
            valueLabel.setWordWrap(True)
            valueLabel.setStyleSheet("""
                QLabel {
                    font-size: 14px;
                    color: #1e293b;
                    padding: 4px 0;
                }
            """)
            valueLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            
            rowLayout.addWidget(iconLabel)
            rowLayout.addWidget(labelLabel)
            rowLayout.addWidget(valueLabel, 1)
            detailsContentLayout.addWidget(rowWidget)
        
        detailsContentLayout.addStretch()
        detailsContainer.setWidget(detailsContent)
        detailsLayout.addWidget(detailsContainer, 1)
        
        self.contentLayout.addWidget(detailsCard)

        # ---------- Update Button ----------
        updateBtn = QPushButton("✏️ Update Customer Details")
        updateBtn.setFixedHeight(40)
        updateBtn.setCursor(Qt.PointingHandCursor)
        updateBtn.clicked.connect(self.openCustomerUpdateDialog)
        updateBtn.setStyleSheet("""
            QPushButton {
                background-color: #8b5cf6;
                color: white;
                padding: 10px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 600;
                border: none;
            }
            QPushButton:hover {
                background-color: #7c3aed;
            }
            QPushButton:pressed {
                background-color: #6d28d9;
            }
        """)
        self.contentLayout.addWidget(updateBtn)

        # ---------- If customer not from DB ----------
        if "customerID" not in cust:
            self.contentLayout.addStretch(1)
            return

        # ---------- Sales History Card ----------
        salesCard = QFrame()
        salesCard.setFrameShape(QFrame.StyledPanel)
        salesCard.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border-radius: 12px;
                border: 1px solid #e2e8f0;
            }
        """)
        # Sales card will expand to fill remaining space
        salesCard.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        salesLayout = QVBoxLayout(salesCard)
        salesLayout.setContentsMargins(20, 16, 20, 16)
        salesLayout.setSpacing(12)

        # Sales title
        salesTitle = QLabel("📊 Sales History")
        salesTitle.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: 700;
                color: #1e293b;
                padding-bottom: 8px;
                border-bottom: 2px solid #f1f5f9;
            }
        """)
        salesLayout.addWidget(salesTitle)

        # Get sales data
        db = DbClient()
        sales = db.getCustomerSalesHistory(cust["customerID"])

        if not sales:
            noSalesLabel = QLabel("No sales records found")
            noSalesLabel.setAlignment(Qt.AlignCenter)
            noSalesLabel.setStyleSheet("""
                QLabel {
                    font-size: 14px;
                    color: #94a3b8;
                    font-style: italic;
                    padding: 20px 0;
                }
            """)
            salesLayout.addWidget(noSalesLabel, 1)
            self.contentLayout.addWidget(salesCard, 1)  # Add with stretch factor
            return

        # Sales table in scrollable area
        salesScroll = QScrollArea()
        salesScroll.setWidgetResizable(True)
        salesScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        salesScroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        salesScroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical, QScrollBar:horizontal {
                background-color: #f1f5f9;
                width: 8px;
                height: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
                background-color: #cbd5e1;
                border-radius: 4px;
                min-height: 20px;
                min-width: 20px;
            }
            QScrollBar::handle:vertical:hover, QScrollBar::handle:horizontal:hover {
                background-color: #94a3b8;
            }
        """)

        salesTable = QTableWidget()
        salesTable.setColumnCount(4)
        salesTable.setHorizontalHeaderLabels(["📅 Date", "🛍️ Item", "🔢 Qty", "💰 Price"])
        salesTable.verticalHeader().setVisible(False)
        salesTable.setEditTriggers(QTableWidget.NoEditTriggers)
        salesTable.setSelectionMode(QTableWidget.NoSelection)
        
        # Style the table - All rows have white background
        salesTable.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: none;
                gridline-color: #f1f5f9;
                font-size: 13px;
            }
            QHeaderView::section {
                background-color: #f8fafc;
                font-weight: 600;
                color: #475569;
                padding: 10px;
                border: none;
                border-bottom: 2px solid #e2e8f0;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #f1f5f9;
                background-color: white;
            }
            QTableWidget::item:selected {
                background-color: #dbeafe;
            }
            QTableWidget QTableCornerButton::section {
                background-color: #f8fafc;
                border: none;
            }
        """)

        # Populate table - all rows will have white background
        for row, (date, item, qty, price) in enumerate(sales):
            salesTable.insertRow(row)
            
            # Date column
            dateItem = QTableWidgetItem(date.strftime("%d/%m/%Y"))
            dateItem.setBackground(QColor("#ffffff"))
            salesTable.setItem(row, 0, dateItem)
            
            # Item column
            itemItem = QTableWidgetItem(item)
            itemItem.setBackground(QColor("#ffffff"))
            salesTable.setItem(row, 1, itemItem)
            
            # Quantity column
            qtyItem = QTableWidgetItem(str(qty))
            qtyItem.setBackground(QColor("#ffffff"))
            salesTable.setItem(row, 2, qtyItem)
            
            # Price column
            priceItem = QTableWidgetItem(f"${price:.2f}")
            priceItem.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            priceItem.setBackground(QColor("#ffffff"))
            salesTable.setItem(row, 3, priceItem)

        salesTable.resizeColumnsToContents()
        salesTable.horizontalHeader().setStretchLastSection(True)
        
        # Set minimum column widths
        for col in range(4):
            width = salesTable.columnWidth(col)
            salesTable.setColumnWidth(col, max(width, 80))

        salesScroll.setWidget(salesTable)
        salesLayout.addWidget(salesScroll, 1)  # Add with stretch factor
        self.contentLayout.addWidget(salesCard, 1)  # Add with stretch factor

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
        """Open customer update dialog with current customer details"""
        if not self.selectedCustomerDetails:
            QMessageBox.warning(
                self,
                "No Customer Selected",
                "Please select a customer first."
            )
            return
        
        # Open the dialog
        openUpdateDialog(self, self.selectedCustomerDetails)
        
        # Refresh the sidebar if customer was updated
        self.updateCustomerInfo()