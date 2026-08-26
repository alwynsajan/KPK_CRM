from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QListWidget, QPushButton,
    QLabel, QWidget, QHBoxLayout, QMessageBox, QFrame,
    QListWidgetItem, QGridLayout, QTableWidget,
    QTableWidgetItem, QHeaderView, QComboBox, QScrollArea,QCheckBox,
    QSizePolicy
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont
from dbClient import DbClient
from generatePDF import generateInvoice,printPDF
from datetime import datetime

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

# ------------------- Modern ComboBox -------------------
class ModernComboBox(QComboBox):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(40)
        self.setStyleSheet("""
            QComboBox {
                background-color: #FFFFFF;
                color: #2D3748;
                border: 1px solid #E2E8F0;
                border-radius: 8px;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: 400;
                min-width: 150px;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid #4A5568;
                margin-right: 10px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                border: 1px solid #E2E8F0;
                border-radius: 8px;
                selection-background-color: #EBF8FF;
                selection-color: #2C5282;
                padding: 4px;
            }
            QComboBox:hover {
                border-color: #A0AEC0;
            }
            QComboBox:focus {
                border: 2px solid #4A90E2;
            }
        """)

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

class SalesHistoryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("Sales History")
        
        # Set window to full screen
        screen = self.screen().availableGeometry()
        self.setGeometry(screen)
        
        # Modern window styling with custom scrollbars
        self.setStyleSheet("""
            QDialog {
                background-color: #F7FAFC;
                color: #2D3748;
                font-family: 'Segoe UI', 'Inter', -apple-system, sans-serif;
            }
            
            /* Custom scrollbar styling for ALL scrollbars */
            QScrollBar:vertical {
                background-color: #F7FAFC;
                width: 10px;
                border-radius: 5px;
                border: none;
                margin: 2px;
            }
            
            QScrollBar::handle:vertical {
                background-color: #CBD5E0;
                border-radius: 5px;
                min-height: 30px;
            }
            
            QScrollBar::handle:vertical:hover {
                background-color: #A0AEC0;
            }
            
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
                background: none;
                border: none;
            }
            
            QScrollBar:horizontal {
                background-color: #F7FAFC;
                height: 10px;
                border-radius: 5px;
                border: none;
                margin: 2px;
            }
            
            QScrollBar::handle:horizontal {
                background-color: #CBD5E0;
                border-radius: 5px;
                min-width: 30px;
            }
            
            QScrollBar::handle:horizontal:hover {
                background-color: #A0AEC0;
            }
        """)
        
        self.current_date = datetime.now()
        self.current_month = self.current_date.month
        self.current_year = self.current_date.year
        self.initUI()
        self.loadMonths()

    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(16)

        # Title
        title_label = QLabel("Sales History")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: 700;
                color: #2D3748;
                padding: 0px;
                margin-bottom: 4px;
            }
        """)
        main_layout.addWidget(title_label)

        # Month filter row
        filter_container = QWidget()
        filter_layout = QHBoxLayout(filter_container)
        filter_layout.setContentsMargins(0, 0, 0, 0)
        filter_layout.setSpacing(20)
        
        # Month filter
        month_label = QLabel("Select Month:")
        month_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: 600;
                color: #4A5568;
            }
        """)
        filter_layout.addWidget(month_label)
        
        self.monthCombo = ModernComboBox()
        self.monthCombo.currentIndexChanged.connect(self.loadDaysForMonth)
        filter_layout.addWidget(self.monthCombo)
        
        # Year filter
        year_label = QLabel("Year:")
        year_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: 600;
                color: #4A5568;
            }
        """)
        filter_layout.addWidget(year_label)
        
        self.yearCombo = ModernComboBox()
        self.yearCombo.currentTextChanged.connect(self.updateMonthCombo)
        filter_layout.addWidget(self.yearCombo)
        
        filter_layout.addStretch()
        main_layout.addWidget(filter_container)

        # Create three-column layout
        columns_container = QWidget()
        columns_layout = QHBoxLayout(columns_container)
        columns_layout.setContentsMargins(0, 0, 0, 0)
        columns_layout.setSpacing(20)

        # Column 1: Days list (20%)
        self.daysCard = CardFrame("Days in Month")
        self.daysLayout = QVBoxLayout()
        self.daysLayout.setContentsMargins(0, 0, 0, 0)
        self.daysLayout.setSpacing(12)
        
        self.daysList = QListWidget()
        self.daysList.setSelectionMode(QListWidget.SingleSelection)
        self.daysList.setStyleSheet("""
            QListWidget {
                background-color: white;
                border: 1px solid #E2E8F0;
                border-radius: 8px;
                font-size: 15px;
                outline: none;
                padding: 2px;
                min-height: 400px;
            }
            
            QListWidget::item {
                padding: 12px 16px;
                border-bottom: 1px solid #F7FAFC;
                color: #2D3748;
                font-weight: 400;
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
        """)
        self.daysList.itemSelectionChanged.connect(self.loadSalesForDay)
        self.daysLayout.addWidget(self.daysList)
        
        self.daysInfo = QLabel("Loading current month...")
        self.daysInfo.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #718096;
                padding: 4px 0px;
            }
        """)
        self.daysLayout.addWidget(self.daysInfo)
        
        self.daysCard.layout.addLayout(self.daysLayout)
        self.daysCard.setMinimumWidth(140)
        columns_layout.addWidget(self.daysCard, 20)  # 20% width

        # Column 2: Sales list (20%)

        self.salesCard = CardFrame(f"Sales for Selected Day")
        self.salesCard.hide()
        self.salesLayout = QVBoxLayout()
        self.salesLayout.setContentsMargins(0, 0, 0, 0)
        self.salesLayout.setSpacing(12)
        
        self.salesList = QListWidget()
        self.salesList.setSelectionMode(QListWidget.SingleSelection)
        self.salesList.setStyleSheet("""
            QListWidget {
                background-color: white;
                border: 1px solid #E2E8F0;
                border-radius: 8px;
                font-size: 15px;
                outline: none;
                padding: 2px;
                min-height: 400px;
            }
            
            QListWidget::item {
                padding: 12px 16px;
                border-bottom: 1px solid #F7FAFC;
                color: #2D3748;
                font-weight: 400;
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
        """)
        self.salesList.itemSelectionChanged.connect(self.showSaleDetails)
        self.salesLayout.addWidget(self.salesList)
        
        self.salesInfo = QLabel("Select a day to view sales")
        self.salesInfo.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #718096;
                padding: 4px 0px;
            }
        """)
        self.salesLayout.addWidget(self.salesInfo)
        
        self.salesCard.layout.addLayout(self.salesLayout)
        self.salesCard.setMinimumWidth(140)
        columns_layout.addWidget(self.salesCard, 20)  # 20% width

        # Column 3: Sale details (60%)
        self.detailsCard = CardFrame("Sale Details")
        self.detailsCard.hide()
        
        # Create scroll area for details with more height
        self.detailsScroll = QScrollArea()
        self.detailsScroll.setWidgetResizable(True)
        self.detailsScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.detailsScroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.detailsScroll.setMinimumHeight(500)  
        
        self.detailsContainer = QWidget()
        self.detailsContainerLayout = QVBoxLayout(self.detailsContainer)
        self.detailsContainerLayout.setContentsMargins(0, 0, 20, 0)  
        self.detailsContainerLayout.setSpacing(12)  

        self.detailsScroll.setWidget(self.detailsContainer)
        self.detailsCard.layout.addWidget(self.detailsScroll)
        self.detailsCard.setMinimumWidth(360)
        columns_layout.addWidget(self.detailsCard, 60)  # 60% width
        
        main_layout.addWidget(columns_container, 1)

    def loadMonths(self):
        """Load unique months and years from database"""
        db = DbClient()
        months = db.getUniqueSalesMonths()
        
        if not months:
            current_date = datetime.now()
            months = [{
                'year': current_date.year,
                'month': current_date.month,
                'month_name': current_date.strftime('%B')
            }]
        
        # Populate year combo
        years = sorted({int(m['year']) for m in months}, reverse=True)
        self.yearCombo.blockSignals(True)
        self.yearCombo.clear()
        for year in years:
            self.yearCombo.addItem(str(year), year)
        
        # Set current year
        if self.current_year in years:
            self.yearCombo.setCurrentText(str(self.current_year))
        elif years:
            self.yearCombo.setCurrentText(str(years[0]))
        self.yearCombo.blockSignals(False)
        
        # Load months for selected year (also loads days)
        self.updateMonthCombo()

    def updateMonthCombo(self):
        """Update month combo based on selected year"""
        if not self.yearCombo.currentText():
            return

        selected_year = int(self.yearCombo.currentText())
        
        db = DbClient()
        months = db.getUniqueSalesMonths()
        
        # Filter months for selected year (coerce types for safe compare)
        year_months = [m for m in months if int(m['year']) == selected_year]
        
        # If no months for selected year, create a list of all months with "No Data" flag
        if not year_months:
            import calendar
            year_months = []
            for month_num in range(1, 13):
                month_name = calendar.month_name[month_num]
                year_months.append({
                    'year': selected_year,
                    'month': month_num,
                    'month_name': month_name,
                    'no_data': True
                })
        else:
            for month in year_months:
                month['no_data'] = False
        
        # Sort months in descending order
        year_months.sort(key=lambda x: int(x['month']), reverse=True)
        
        self.monthCombo.blockSignals(True)
        self.monthCombo.clear()
        for month_data in year_months:
            month_num = int(month_data['month'])
            if month_data.get('no_data', False):
                display_text = f"{month_data['month_name']} (No Data)"
            else:
                display_text = f"{month_data['month_name']}"
            self.monthCombo.addItem(display_text, month_num)
        
        # Prefer current calendar month if present, otherwise first item
        selected_index = 0
        for i in range(self.monthCombo.count()):
            if self.monthCombo.itemData(i) == self.current_month:
                selected_index = i
                break
        if self.monthCombo.count() > 0:
            self.monthCombo.setCurrentIndex(selected_index)
        self.monthCombo.blockSignals(False)

        self.loadDaysForMonth()

    def loadDaysForMonth(self):
        """Load days for selected month and year"""
        month = self.monthCombo.currentData()
        year_text = self.yearCombo.currentText()
        if month is None or not year_text:
            return

        year = int(year_text)
        month = int(month)
        month_name = self.monthCombo.currentText().replace(" (No Data)", "")
        
        db = DbClient()
        days = db.getSalesByMonthYear(month, year)
        
        self.daysList.clear()
        
        if not days:
            # Update card title even if no sales
            self.daysCard.layout.itemAt(0).widget().setText(f"Days in {month_name}")
            self.daysInfo.setText(f"No sales found for {month_name} {year}")
            self.salesCard.hide()
            self.detailsCard.hide()
            return
        
        # Calculate total sales for the month
        monthly_total = 0
        
        # Get daily totals and calculate monthly total
        daily_totals = {}
        for day_data in days:
            sale_date = day_data['saleDate']
            if isinstance(sale_date, str):
                sale_date = datetime.strptime(sale_date, '%Y-%m-%d').date()
            
            # Get sales for this day to calculate total
            date_str = sale_date.strftime('%Y-%m-%d')
            sales_for_day = db.getSalesByDate(date_str)
            daily_total = sum(sale['total_amount'] for sale in sales_for_day)
            daily_totals[sale_date] = daily_total
            monthly_total += daily_total  # Add to monthly total
        
        # Update the card title with month name and monthly total
        self.daysCard.layout.itemAt(0).widget().setText(f"Sales in {month_name}:\n ${monthly_total:.2f}")
        
        for day_data in days:
            sale_date = day_data['saleDate']
            if isinstance(sale_date, str):
                sale_date = datetime.strptime(sale_date, '%Y-%m-%d').date()
            
            # Format date
            day_name = sale_date.strftime('%A')
            date_str = sale_date.strftime('%d %b, %Y')
            daily_total = daily_totals.get(sale_date, 0)
            
            # Create item 
            item_text = f"{day_name}\n{date_str}\nTotal: ${daily_total:.2f}"
            item = QListWidgetItem()
            item.setText(item_text)
            item.setData(Qt.UserRole, sale_date)
            
            font = QFont()
            font.setPointSize(14)
            item.setFont(font)
            
            self.daysList.addItem(item)
        
        self.daysInfo.setText(f"Found {len(days)} day(s) with sales")
        self.salesCard.hide()
        self.detailsCard.hide()
        
        # Select first day if available
        if self.daysList.count() > 0:
            self.daysList.setCurrentRow(0)

    def loadSalesForDay(self):
        """Load sales for selected day"""
        selected_item = self.daysList.currentItem()
        
        if not selected_item:
            self.salesCard.hide()
            self.detailsCard.hide()
            return
        
        sale_date = selected_item.data(Qt.UserRole)
        date_str = sale_date.strftime('%Y-%m-%d')
        
        db = DbClient()
        sales = db.getSalesByDate(date_str)
        
        self.salesList.clear()
        
        if not sales:
            self.salesInfo.setText(f"No sales found for {sale_date.strftime('%d %b, %Y')}")
            self.salesCard.hide()
            self.detailsCard.hide()
            return
        
        for sale in sales:
            sale_time = sale['saleDateTime']
            if isinstance(sale_time, str):
                sale_time = datetime.strptime(sale_time, '%Y-%m-%d %H:%M:%S')
            
            time_str = sale_time.strftime('%I:%M %p')
            customer_name = sale['customerName'] or "Walk-in Customer"
            total = sale['total_amount']
            
            item_text = f"{time_str} - {customer_name}\n${total:.2f}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, sale)
            
            font = QFont()
            font.setPointSize(14)
            item.setFont(font)
            
            self.salesList.addItem(item)
        
        self.salesInfo.setText(f"Found {len(sales)} sale(s) for {sale_date.strftime('%d %b, %Y')}")
        self.salesCard.show()
        self.detailsCard.hide()
        
        # Select first sale if available
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
        """Show details of selected sale"""
        selected_item = self.salesList.currentItem()
        
        if not selected_item:
            self.detailsCard.hide()
            return
        
        sale = selected_item.data(Qt.UserRole)
        
        # Clear previous details
        self.clearLayout(self.detailsContainerLayout)
        
        # Sale header (no sale ID)
        sale_time = sale['saleDateTime']
        if isinstance(sale_time, str):
            sale_time = datetime.strptime(sale_time, '%Y-%m-%d %H:%M:%S')
        
        header_text = f"Sale on {sale_time.strftime('%d %B, %Y at %I:%M %p')}"
        header_label = QLabel(header_text)
        header_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: 600;
                color: #2D3748;
                margin-bottom: 8px;
                background-color: none;
            }
        """)
        self.detailsContainerLayout.addWidget(header_label)
        
        # Create details grid with reduced spacing
        details_grid = QGridLayout()
        details_grid.setVerticalSpacing(8) 
        details_grid.setHorizontalSpacing(300)
        
        row = 0
        
        # Customer Name (if available)
        if sale['customerName']:
            customer_label = QLabel("Customer:")
            customer_label.setStyleSheet("""
                QLabel {
                    font-size: 14px;
                    font-weight: 600;
                    color: #4A5568;
                    background-color: none;
                }
            """)
            details_grid.addWidget(customer_label, row, 0)
            
            customer_value = QLabel(sale['customerName'])
            customer_value.setStyleSheet("""
                QLabel {
                    font-size: 14px;
                    color: #2D3748;
                    background-color: none;
                    font-weight: bold;
                }
            """)
            details_grid.addWidget(customer_value, row, 1)
            row += 1
        
        # Payment Type
        payment_label = QLabel("Payment:")
        payment_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: 600;
                color: #4A5568;
                background-color: none;
            }
        """)
        details_grid.addWidget(payment_label, row, 0)
        
        payment_value = QLabel(sale['paymentType'])
        payment_value.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #2D3748;
                background-color: none;
            }
        """)
        details_grid.addWidget(payment_value, row, 1)
        row += 1

        # Official Status
        official_label = QLabel("Official Sale:")
        official_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: 600;
                color: #4A5568;
                background-color: none;
            }
        """)
        details_grid.addWidget(official_label, row, 0)

        # Container layout for toggle + status label
        official_container = QHBoxLayout()
        official_container.setSpacing(10)

        # Toggle Button
        official_toggle = QCheckBox()
        official_toggle.setChecked(bool(sale.get("official", 0)))
        official_toggle.setCursor(Qt.PointingHandCursor)

        official_toggle.setStyleSheet("""
            QCheckBox::indicator {
                width: 40px;
                height: 20px;
                border-radius: 10px;
            }

            QCheckBox::indicator:unchecked {
                background-color: #E2E8F0;
                border: 2px solid #CBD5E0;
            }

            QCheckBox::indicator:checked {
                background-color: #38A169;
                border: 2px solid #38A169;
            }
        """)

        # Status Label (Yes / No)
        official_status_label = QLabel()
        official_status_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
            }
        """)

        def updateOfficialUI(checked):
            if checked:
                official_status_label.setText("Yes")
                official_status_label.setStyleSheet("""
                    QLabel {
                        font-size: 14px;
                        font-weight: bold;
                        color: #38A169;
                        background-color: none;
                    }
                """)
            else:
                official_status_label.setText("No")
                official_status_label.setStyleSheet("""
                    QLabel {
                        font-size: 14px;
                        font-weight: bold;
                        color: #E53E3E;
                        background-color: none;
                    }
                """)

        official_toggle.toggled.connect(updateOfficialUI)

        # Set initial state
        updateOfficialUI(official_toggle.isChecked())

        # Add to horizontal layout
        official_container.addWidget(official_toggle)
        official_container.addWidget(official_status_label)
        official_container.addStretch()

        details_grid.addLayout(official_container, row, 1)
        row += 1


        def onOfficialToggled(checked, saleID=sale["saleID"]):
            db = DbClient()
            result = db.updateSaleOfficialStatus(
                saleID,
                1 if checked else 0
            )

            if result["status"] != "Success":
                QMessageBox.warning(
                    self,
                    "Update Failed",
                    "Could not update official status."
                )
                official_toggle.blockSignals(True)
                official_toggle.setChecked(not checked)
                official_toggle.blockSignals(False)
        
        official_toggle.toggled.connect(onOfficialToggled)

        # Customer Contact (if available)
        if sale['customerPhone']:
            phone_label = QLabel("Phone:")
            phone_label.setStyleSheet("""
                QLabel {
                    font-size: 14px;
                    font-weight: 600;
                    color: #4A5568;
                    background-color: none;
                }
            """)
            details_grid.addWidget(phone_label, row, 0)
            
            phone_value = QLabel(sale['customerPhone'])
            phone_value.setStyleSheet("""
                QLabel {
                    font-size: 14px;
                    color: #2D3748;
                    background-color: none;
                }
            """)
            details_grid.addWidget(phone_value, row, 1)
            row += 1
        
        # Customer Address (if available)
        if sale['customerAddress']:
            address_label = QLabel("Address:")
            address_label.setStyleSheet("""
                QLabel {
                    font-size: 14px;
                    font-weight: 600;
                    color: #4A5568;
                    background-color: none;
                }
            """)
            details_grid.addWidget(address_label, row, 0)
            
            address_value = QLabel(sale['customerAddress'])
            address_value.setStyleSheet("""
                QLabel {
                    font-size: 14px;
                    color: #2D3748;
                    background-color: none;
                }
            """)
            address_value.setWordWrap(True)
            details_grid.addWidget(address_value, row, 1)
            row += 1
        
        # State & Postcode (if available)
        if sale['customerState'] or sale['customerPostcode']:
            location_label = QLabel("Location:")
            location_label.setStyleSheet("""
                QLabel {
                    font-size: 14px;
                    font-weight: 600;
                    color: #4A5568;
                    background-color: none;
                }
            """)
            details_grid.addWidget(location_label, row, 0)
            
            location_value = QLabel(f"{sale['customerState'] or ''} {sale['customerPostcode'] or ''}".strip())
            location_value.setStyleSheet("""
                QLabel {
                    font-size: 14px;
                    color: #2D3748;
                    background-color: none;
                }
            """)
            details_grid.addWidget(location_value, row, 1)
            row += 1
        
        # Note (if available)
        if sale.get('note'):
            note_label = QLabel("Note:")
            note_label.setStyleSheet("""
                QLabel {
                    font-size: 14px;
                    font-weight: 600;
                    color: #4A5568;
                }
            """)
            details_grid.addWidget(note_label, row, 0)
            
            note_value = QLabel(sale['note'])
            note_value.setStyleSheet("""
                QLabel {
                    font-size: 14px;
                    color: #2D3748;
                }
            """)
            note_value.setWordWrap(True)
            details_grid.addWidget(note_value, row, 1, 1, 2)
            row += 1
        
        self.detailsContainerLayout.addLayout(details_grid)
        
        # Items table
        items = sale.get('items', [])
        if items:
            # Items header
            items_header = QLabel("Items Purchased:")
            items_header.setStyleSheet("""
                QLabel {
                    font-size: 16px;
                    font-weight: 600;
                    color: #2D3748;
                    margin-top: 16px;
                    margin-bottom: 8px;
                    background-color: none;
                }
            """)
            self.detailsContainerLayout.addWidget(items_header)
            
            # Create items table
            items_table = QTableWidget()
            items_table.setColumnCount(4)
            items_table.setHorizontalHeaderLabels(["Product", "Quantity", "Unit Price", "Total"])
            items_table.horizontalHeader().setStretchLastSection(True)
            items_table.setEditTriggers(QTableWidget.NoEditTriggers)
            items_table.verticalHeader().setVisible(False)
            
            items_table.setStyleSheet("""
                QTableWidget {
                    background-color: white;
                    border: 1px solid #E2E8F0;
                    border-radius: 8px;
                    gridline-color: #E2E8F0;
                    font-size: 13px;
                }
                QHeaderView::section {
                    background-color: #F8FAFC;
                    color: #4A5568;
                    font-weight: 600;
                    padding: 12px;
                    border: none;
                    border-right: 1px solid #E2E8F0;
                }
                QTableWidget::item {
                    padding: 12px;
                    color: #2D3748;
                }
            """)
            
            # Set column widths
            header = items_table.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.Stretch)
            items_table.setColumnWidth(1, 100)
            items_table.setColumnWidth(2, 120)
            items_table.setColumnWidth(3, 120)
            
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
            
            self.detailsContainerLayout.addWidget(items_table)
            
            # Total amount
            total_container = QWidget()
            total_layout = QHBoxLayout(total_container)
            total_layout.setContentsMargins(0, 16, 0, 0)
            
            total_label = QLabel("Total Amount:")
            total_label.setStyleSheet("""
                QLabel {
                    font-size: 16px;
                    font-weight: 600;
                    color: #2F855A;
                    background-color: none;
                }
            """)
            total_layout.addWidget(total_label)
            
            total_layout.addStretch()
            
            total_value = QLabel(f"${total_amount:.2f}")
            total_value.setStyleSheet("""
                QLabel {
                    font-size: 20px;
                    font-weight: 700;
                    color: #2F855A;
                    background-color: none;
                }
            """)
            total_layout.addWidget(total_value)
            
            self.detailsContainerLayout.addWidget(total_container)
        
        # Action buttons
        buttons_container = QWidget()
        buttons_layout = QHBoxLayout(buttons_container)
        buttons_layout.setContentsMargins(0, 20, 0, 0)
        buttons_layout.setSpacing(20)
        
        buttons_layout.addStretch()
        
        self.printInvoiceBtn = ModernButton("Print Invoice", "primary", width=160)
        self.printInvoiceBtn.clicked.connect(lambda: self.printInvoice(sale))
        buttons_layout.addWidget(self.printInvoiceBtn)

        # Save As PDF button 
        self.savePDFBtn = ModernButton("Save As PDF", "secondary", width=160)
        self.savePDFBtn.clicked.connect(lambda: self.saveAsPDF(sale))
        buttons_layout.addWidget(self.savePDFBtn)
        
        # Only show mark as paid for credit sales
        if sale['paymentType'].lower() == 'credit':
            self.markPaidBtn = ModernButton("Mark as Paid", "secondary", width=160)
            self.markPaidBtn.clicked.connect(lambda: self.markAsPaid(sale))
            buttons_layout.addWidget(self.markPaidBtn)
        
        buttons_layout.addStretch()
        
        self.detailsContainerLayout.addWidget(buttons_container)
        self.detailsContainerLayout.addStretch()
        
        self.detailsCard.show()

    def saveAsPDF(self, sale):
        """Save invoice as PDF for selected sale"""
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
            filename = generateInvoice(
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
                f"Failed to generate invoice.\n\nError: {str(e)}"
            )

    def printInvoice(self, sale):
        """Print invoice for selected sale"""
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

    def markAsPaid(self, sale):
        """Mark selected sale as paid"""
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
        response = db.updatePaymentType(sale['saleID'], "EFTPOS")
        
        if response["status"] == "Success":
            QMessageBox.information(
                self,
                "Success",
                f"Sale has been marked as paid!"
            )
            
            # Reload current day's sales to reflect change
            self.loadSalesForDay()
        else:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to mark sale as paid.\n\nError: {response.get('message', 'Unknown error')}"
            )