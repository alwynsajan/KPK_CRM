from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QListWidget, QPushButton,
    QLabel, QWidget, QHBoxLayout, QMessageBox, QFrame,
    QListWidgetItem, QGridLayout, QTableWidget,
    QTableWidgetItem, QHeaderView, QGroupBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from dbClient import DbClient
from generatePDF import generateInvoice, printPDF


# ------------------- Modern Button -------------------
class ModernButton(QPushButton):
    def __init__(self, text, style_type="primary", width=None):
        super().__init__(text)
        self.setFixedHeight(40)
        if width:
            self.setFixedWidth(width)
        self.setCursor(Qt.PointingHandCursor)
        
        styles = {
            "primary": """
                QPushButton {
                    background-color: #4A90E2;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 0px 24px;
                    font-size: 14px;
                    font-weight: 600;
                    min-width: 140px;
                }
                QPushButton:hover {
                    background-color: #3182CE;
                }
                QPushButton:pressed {
                    background-color: #2C5282;
                }
                QPushButton:disabled {
                    background-color: #E2E8F0;
                    color: #A0AEC0;
                }
            """,
            "success": """
                QPushButton {
                    background-color: #38A169;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 0px 24px;
                    font-size: 14px;
                    font-weight: 600;
                    min-width: 140px;
                }
                QPushButton:hover {
                    background-color: #2F855A;
                }
                QPushButton:pressed {
                    background-color: #276749;
                }
            """,
            "secondary": """
                QPushButton {
                    background-color: #EDF2F7;
                    color: #4A5568;
                    border: 1px solid #CBD5E0;
                    border-radius: 8px;
                    padding: 0px 24px;
                    font-size: 14px;
                    font-weight: 600;
                    min-width: 120px;
                }
                QPushButton:hover {
                    background-color: #E2E8F0;
                    border-color: #A0AEC0;
                }
            """
        }
        
        self.setStyleSheet(styles.get(style_type, styles["primary"]))

# ------------------- Card Frame -------------------
class CardFrame(QFrame):
    def __init__(self, title=None):
        super().__init__()
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #E2E8F0;
            }
        """)
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(12)
        
        if title:
            title_label = QLabel(title)
            title_label.setStyleSheet("""
                QLabel {
                    font-size: 16px;
                    font-weight: 600;
                    color: #2D3748;
                    margin-bottom: 4px;
                }
            """)
            self.layout.addWidget(title_label)

class CreditSalesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("Credit Sales")
        
        # Set window size - wider window
        screen = self.screen().availableGeometry()
        width = min(int(screen.width() * 0.85), 1200)  # Wider (85%)
        height = min(int(screen.height() * 0.85), 900)  # Taller (85%)
        self.resize(width, height)
        
        # Center the window
        self.move(
            screen.left() + (screen.width() - width) // 2,
            screen.top() + (screen.height() - height) // 3
        )
        
        # Modern window styling
        self.setStyleSheet("""
            QDialog {
                background-color: #E6E6E6;
                color: #2D3748;
                font-family: 'Segoe UI', 'Inter', -apple-system, sans-serif;
            }
        """)
        
        self.creditSales = []
        self.initUI()
        self.loadCreditSales()

    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(16)

        # Title
        title_label = QLabel("Credit Sales")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: 700;
                color: #2D3748;
                padding: 0px;
             
            }
        """)
        main_layout.addWidget(title_label)

        # Create main container with two columns
        container = QWidget()
        container_layout = QHBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(20)

        # Left column: Sales list (25%)
        left_card = CardFrame("Credit Sales List")
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(12)
        
        # Sales list
        self.salesList = QListWidget()
        self.salesList.setSelectionMode(QListWidget.SingleSelection)
        self.salesList.setFocusPolicy(Qt.StrongFocus)
        self.salesList.setStyleSheet("""
            QListWidget {
                background-color: white;
                border: 1px solid #E2E8F0;
                border-radius: 8px;
                font-size: 13px;
                outline: none;
                padding: 2px;
                min-height: 300px;
            }
            
            QListWidget::item {
                padding: 12px 15px;
                border-bottom: 2px solid #F7FAFC;
                color: #2D3748;
                font-weight: 400;
                min-height: 20px;
            }
            
            QListWidget::item:hover {
                background-color: #F7FAFC;
            }
            
            QListWidget::item:selected {
                background-color: #EBF8FF;
                color: #2C5282;
                font-weight: 500;
                border-left: 4px solid #4A90E2;
            }
            
            /* Custom scrollbar styling */
            QScrollBar:vertical {
                background-color: transparent;
                width: 8px;
                border-radius: 4px;
                margin: 2px;
            }
            
            QScrollBar::handle:vertical {
                background-color: #CBD5E0;
                border-radius: 4px;
                min-height: 30px;
            }
            
            QScrollBar::handle:vertical:hover {
                background-color: #A0AEC0;
            }
        """)
        left_layout.addWidget(self.salesList, 1)
        
        # List info
        self.listInfo = QLabel("No credit sales found")
        self.listInfo.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #718096;
                padding: 4px 0px;
            }
        """)
        left_layout.addWidget(self.listInfo)
        
        left_card.layout.addLayout(left_layout)
        container_layout.addWidget(left_card, 2)  # 25% width

        # Right column: Sale details (75%)
        right_container = QWidget()
        right_layout = QVBoxLayout(right_container)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(16)
        
        # Sale details header
        self.detailsHeader = QLabel("Select a sale to view details")
        self.detailsHeader.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: 600;
                color: #2D3748;
                margin-bottom: 4px;
            }
        """)
        right_layout.addWidget(self.detailsHeader)
        
        # Customer Details Card
        self.customerCard = CardFrame("Customer Details")
        self.customerCard.hide()
        self.customerLayout = QVBoxLayout()
        self.customerLayout.setContentsMargins(0, 0, 0, 0)
        self.customerCard.layout.addLayout(self.customerLayout)
        right_layout.addWidget(self.customerCard)
        
        # Items Details Card
        self.itemsCard = CardFrame("Sale Items")
        self.itemsCard.hide()
        self.itemsLayout = QVBoxLayout()
        self.itemsLayout.setContentsMargins(0, 0, 0, 0)
        self.itemsCard.layout.addLayout(self.itemsLayout)
        right_layout.addWidget(self.itemsCard)
        
        # Action buttons container
        self.actionButtons = QWidget()
        self.actionButtons.setFixedHeight(60)
        self.actionButtons.hide()
        action_layout = QHBoxLayout(self.actionButtons)
        action_layout.setContentsMargins(0, 0, 0, 0)
        action_layout.setSpacing(20)
        
        action_layout.addStretch()
        
        self.printInvoiceBtn = ModernButton("Print Invoice", "primary", width=160)
        self.saveInvoiceBtn = ModernButton("Save As PDF", "primary", width=160)
        self.printInvoiceBtn.clicked.connect(self.printInvoice)
        self.saveInvoiceBtn.clicked.connect(self.saveInvoice)

        self.markPaidBtn = ModernButton("Mark as Paid", "success", width=160)
        self.markPaidBtn.clicked.connect(self.markAsPaid)
        
        action_layout.addWidget(self.printInvoiceBtn)
        action_layout.addWidget(self.saveInvoiceBtn)
        action_layout.addWidget(self.markPaidBtn)
        action_layout.addStretch()
        
        right_layout.addWidget(self.actionButtons)
        
        container_layout.addWidget(right_container, 6)  # 75% width
        
        main_layout.addWidget(container, 1)

        # Connect selection change
        self.salesList.itemSelectionChanged.connect(self.showSaleDetails)

    def loadCreditSales(self):
        """Load credit sales from database"""
        db = DbClient()
        self.creditSales = db.getCreditSales()
        
        if not self.creditSales:
            self.listInfo.setText("No credit sales found")
            return
        
        self.salesList.clear()
        
        for sale in self.creditSales:
            # Format date
            sale_date = sale['saleDateTime'].strftime('%d/%m/%Y %H:%M:%S') if sale['saleDateTime'] else 'No Date'
            customer_name = sale['customerName'] or 'Unknown Customer'
            
            # Calculate total
            total = sum(item['cost'] * item['quantity'] for item in sale.get('items', []))
            
            # Create item text
            item_text = f"{customer_name}\n{sale_date}\n${total:.2f}"
            
            # Create list item
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, sale)
            
            # Set font
            font = QFont()
            font.setPointSize(12)
            item.setFont(font)
            
            self.salesList.addItem(item)
        
        self.listInfo.setText(f"Found {len(self.creditSales)} credit sale(s)")
        
        # Select first item if available
        if self.salesList.count() > 0:
            self.salesList.setCurrentRow(0)

    def clearLayout(self, layout):
        """Clear all widgets from a layout"""
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    sublayout = item.layout()
                    if sublayout is not None:
                        self.clearLayout(sublayout)

    def showSaleDetails(self):
        """Show details of selected sale - REPLACE instead of append"""
        selected_item = self.salesList.currentItem()
        
        if not selected_item:
            self.customerCard.hide()
            self.itemsCard.hide()
            self.actionButtons.hide()
            self.detailsHeader.setText("Select a sale to view details")
            return
        
        # Get sale data
        sale = selected_item.data(Qt.UserRole)
        
        # Update header
        sale_date = sale['saleDateTime'].strftime('%d/%m/%Y %H:%M:%S') if sale['saleDateTime'] else 'No Date'
        customer_name = sale['customerName'] or 'Unknown Customer'
        self.detailsHeader.setText(f"Sale Details - {sale_date} - {customer_name}")
        
        # Clear previous customer details
        self.clearLayout(self.customerLayout)
        
        # Create customer details grid
        customer_grid = QGridLayout()
        customer_grid.setVerticalSpacing(10)
        customer_grid.setHorizontalSpacing(20)
        
        row = 0
        
        # Customer Name
        if sale['customerName']:
            customer_label = QLabel("Customer Name:")
            customer_label.setStyleSheet("""
                QLabel {
                    font-size: 13px;
                    font-weight: 600;
                    color: #4A5568;
                    border: none;
                }
            """)
            customer_grid.addWidget(customer_label, row, 0)
            
            customer_value = QLabel(sale['customerName'])
            customer_value.setStyleSheet("""
                QLabel {
                    font-size: 13px;
                    color: #2D3748;
                    border: none;
                }
            """)
            customer_grid.addWidget(customer_value, row, 1)
            row += 1
        
        # Phone
        if sale['customerPhone']:
            phone_label = QLabel("Phone:")
            phone_label.setStyleSheet("""
                QLabel {
                    font-size: 13px;
                    font-weight: 600;
                    color: #4A5568;
                    border: none;
                }
            """)
            customer_grid.addWidget(phone_label, row, 0)
            
            phone_value = QLabel(sale['customerPhone'])
            phone_value.setStyleSheet("""
                QLabel {
                    font-size: 13px;
                    color: #2D3748;
                    border: none;
                }
            """)
            customer_grid.addWidget(phone_value, row, 1)
            row += 1
        
        # Email
        if sale['customerEmail']:
            email_label = QLabel("Email:")
            email_label.setStyleSheet("""
                QLabel {
                    font-size: 13px;
                    font-weight: 600;
                    color: #4A5568;
                    border: none;
                }
            """)
            customer_grid.addWidget(email_label, row, 0)
            
            email_value = QLabel(sale['customerEmail'])
            email_value.setStyleSheet("""
                QLabel {
                    font-size: 13px;
                    color: #2D3748;
                    border: none;
                }
            """)
            customer_grid.addWidget(email_value, row, 1)
            row += 1
        
        # Address
        if sale['customerAddress']:
            address_label = QLabel("Address:")
            address_label.setStyleSheet("""
                QLabel {
                    font-size: 13px;
                    font-weight: 600;
                    color: #4A5568;
                    border: none;
                }
            """)
            customer_grid.addWidget(address_label, row, 0)
            
            address_value = QLabel(sale['customerAddress'])
            address_value.setStyleSheet("""
                QLabel {
                    font-size: 13px;
                    color: #2D3748;
                    border: none;
                }
            """)
            address_value.setWordWrap(True)
            customer_grid.addWidget(address_value, row, 1)
            row += 1
        
        # State & Postcode
        if sale['customerState'] or sale['customerPostcode']:
            state_postcode_label = QLabel("State/Postcode:")
            state_postcode_label.setStyleSheet("""
                QLabel {
                    font-size: 13px;
                    font-weight: 600;
                    color: #4A5568;
                    border: none;
                }
            """)
            customer_grid.addWidget(state_postcode_label, row, 0)
            
            state_postcode = f"{sale['customerState'] or ''} {sale['customerPostcode'] or ''}".strip()
            state_postcode_value = QLabel(state_postcode)
            state_postcode_value.setStyleSheet("""
                QLabel {
                    font-size: 13px;
                    color: #2D3748;
                    border: none;
                }
            """)
            customer_grid.addWidget(state_postcode_value, row, 1)
            row += 1
        
        # Note
        if sale.get('note'):
            note_label = QLabel("Note:")
            note_label.setStyleSheet("""
                QLabel {
                    font-size: 13px;
                    font-weight: 600;
                    color: #4A5568;
                    border: none;
                }
            """)
            customer_grid.addWidget(note_label, row, 0)
            
            note_value = QLabel(sale['note'])
            note_value.setStyleSheet("""
                QLabel {
                    font-size: 13px;
                    color: #2D3748;
                    border: none;
                }
            """)
            note_value.setWordWrap(True)
            customer_grid.addWidget(note_value, row, 1)
            row += 1
        
        # Add customer grid to customer card
        self.customerLayout.addLayout(customer_grid)
        
        # Clear previous items details
        self.clearLayout(self.itemsLayout)
        
        # Add items table
        items = sale.get('items', [])
        if items:
            # Create items table
            items_table = QTableWidget()
            items_table.setColumnCount(4)
            items_table.setHorizontalHeaderLabels(["Product Name", "Quantity", "Unit Price", "Total"])
            items_table.horizontalHeader().setStretchLastSection(True)
            items_table.setEditTriggers(QTableWidget.NoEditTriggers)
            items_table.verticalHeader().setVisible(False)
            
            items_table.setStyleSheet("""
                QTableWidget {
                    background-color: white;
                    border: 1px solid #E2E8F0;
                    border-radius: 6px;
                    gridline-color: #E2E8F0;
                    font-size: 13px;
                }
                QHeaderView::section {
                    background-color: #F8FAFC;
                    color: #4A5568;
                    font-weight: 600;
                    padding: 10px;
                    border: none;
                    border-right: 1px solid #E2E8F0;
                }
                QTableWidget::item {
                    padding: 10px;
                    color: #2D3748;
                }
                QTableWidget::item:selected {
                    background-color: #EBF8FF;
                }
            """)
            
            # Set column widths
            header = items_table.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.Stretch)  # Product name stretches
            items_table.setColumnWidth(1, 100)  # Quantity
            items_table.setColumnWidth(2, 120)  # Unit Price
            items_table.setColumnWidth(3, 120)  # Total
            
            # Add items
            total_amount = 0
            items_table.setRowCount(len(items))
            for i, item in enumerate(items):
                # Product name
                product_item = QTableWidgetItem(item['productName'])
                items_table.setItem(i, 0, product_item)
                
                # Quantity
                qty_item = QTableWidgetItem(str(item['quantity']))
                qty_item.setTextAlignment(Qt.AlignCenter)
                items_table.setItem(i, 1, qty_item)
                
                # Price
                price_item = QTableWidgetItem(f"${item['cost']:.2f}")
                price_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                items_table.setItem(i, 2, price_item)
                
                # Total
                item_total = item['cost'] * item['quantity']
                total_item = QTableWidgetItem(f"${item_total:.2f}")
                total_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                items_table.setItem(i, 3, total_item)
                
                total_amount += item_total
            
            self.itemsLayout.addWidget(items_table)
            
            # Add total amount
            total_container = QWidget()
            total_layout = QHBoxLayout(total_container)
            total_layout.setContentsMargins(0, 10, 0, 0)
            
            total_label = QLabel("Total Amount:")
            total_label.setStyleSheet("""
                QLabel {
                    font-size: 15px;
                    font-weight: 600;
                    color: #2F855A;
                    background-color: #E6E6E6;
                }
            """)
            total_layout.addWidget(total_label)
            
            total_layout.addStretch()
            
            total_value = QLabel(f"${total_amount:.2f}")
            total_value.setStyleSheet("""
                QLabel {
                    font-size: 18px;
                    font-weight: 700;
                    color: #2F855A;
                    background-color: #E6E6E6;
                }
            """)
            total_layout.addWidget(total_value)
            
            self.itemsLayout.addWidget(total_container)
        
        # Store current sale for actions
        self.currentSale = sale
        
        # Show all elements
        self.customerCard.show()
        self.itemsCard.show()
        self.actionButtons.show()

    def markAsPaid(self):
        """Mark selected sale as paid"""
        if not hasattr(self, 'currentSale'):
            return
        
        reply = QMessageBox.question(
            self,
            "Mark as Paid",
            f"Are you sure you want to mark this sale as paid?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.No:
            return
        
        # Update payment type in database
        db = DbClient()
        response = db.updatePaymentType(self.currentSale['saleID'], "EFTPOS")
        
        if response["status"] == "Success":
            
            # Remove from list and reload
            current_row = self.salesList.currentRow()
            self.salesList.takeItem(current_row)
            self.creditSales = [s for s in self.creditSales if s['saleID'] != self.currentSale['saleID']]
            
            # Update info
            self.listInfo.setText(f"Found {len(self.creditSales)} credit sale(s)")
            
            # Clear details if no more sales
            if self.salesList.count() == 0:
                self.customerCard.hide()
                self.itemsCard.hide()
                self.actionButtons.hide()
                self.detailsHeader.setText("Select a sale to view details")
            else:
                # Select next item
                if current_row >= self.salesList.count():
                    current_row = self.salesList.count() - 1
                if current_row >= 0:
                    self.salesList.setCurrentRow(current_row)
        else:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to mark sale as paid.\n\nError: {response.get('message', 'Unknown error')}"
            )
    
    def saveInvoice(self):
        """Save invoice for selected sale"""
        if not hasattr(self, 'currentSale'):
            return
        
        sale = self.currentSale
        
        # Prepare customer data
        customerData = {
            "Name": sale['customerName'] or "",
            "Address": sale['customerAddress'] or "",
            "State": sale['customerState'] or "",
            "Postcode": sale['customerPostcode'] or "",
            "Phone": sale['customerPhone'] or ""
        }
        
        # Prepare product data
        productDataForPDF = []
        for item in sale.get('items', []):
            productDataForPDF.append({
                "Name": item['productName'],
                "Quantity": float(item['quantity']),
                "Price": float(item['cost'])
            })
        
        # Generate invoice
        try:
            filename=generateInvoice(
                customerData=customerData,
                productData=productDataForPDF,
                saleID=sale['saleID'],
                date=sale['saleDateTime'],
                saveToFile=True
            )
            
            QMessageBox.information(
                self,
                "Invoice Saved",
                f"Invoice saved successfully in the Invoices folder!\n\nFilename: {filename}"
            )
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to save invoice.\n\nError: {str(e)}"
            )
        

    def printInvoice(self):
        """Print invoice for selected sale"""
        if not hasattr(self, 'currentSale'):
            return
        
        sale = self.currentSale
        
        # Prepare customer data
        customerData = {
            "Name": sale['customerName'] or "",
            "Address": sale['customerAddress'] or "",
            "State": sale['customerState'] or "",
            "Postcode": sale['customerPostcode'] or "",
            "Phone": sale['customerPhone'] or ""
        }
        
        # Prepare product data
        productDataForPDF = []
        for item in sale.get('items', []):
            productDataForPDF.append({
                "Name": item['productName'],
                "Quantity": item['quantity'],
                "Price": float(item['cost'])
            })
        
        # Generate invoice
        try:
            buffer = generateInvoice(
                customerData=customerData,
                productData=productDataForPDF,
                saleID=sale['saleID'],
                date=sale['saleDateTime'],
                saveToFile=False
            )
            status= printPDF(buffer)
            
            # Show message
            if status["status"] == "Success":
                QMessageBox.information(self, "Print Status", status["message"])

            else:
                QMessageBox.critical(self, "Print Failed", status["message"])
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to generate invoice.\n\nError: {str(e)}"
            )