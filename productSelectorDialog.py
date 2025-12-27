from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QListWidget, QPushButton,
    QLineEdit, QLabel, QWidget, QHBoxLayout, QListWidgetItem, 
    QSizePolicy, QMessageBox, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from dbClient import DbClient

# ------------------- Modern Line Edit with Clear Button -------------------
class ModernSearchLineEdit(QLineEdit):
    def __init__(self, placeholder=""):
        super().__init__()
        self.setPlaceholderText(placeholder)
        self.setFixedHeight(40)
        
        # Create clear button
        self.clear_button = QPushButton("✕")
        self.clear_button.setCursor(Qt.PointingHandCursor)
        self.clear_button.setFixedSize(20, 20)
        self.clear_button.setStyleSheet("""
            QPushButton {
                background-color: #CBD5E0;
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 12px;
                font-weight: bold;
                margin-right: 5px;
            }
            QPushButton:hover {
                background-color: #A0AEC0;
            }
            QPushButton:pressed {
                background-color: #718096;
            }
        """)
        
        self.clear_button.clicked.connect(self.clear)
        self.clear_button.hide()
        self.textChanged.connect(self.onTextChanged)
        
        self.setStyleSheet("""
            QLineEdit {
                background-color: #FFFFFF;
                color: #2D3748;
                border: 1px solid #E2E8F0;
                border-radius: 8px;
                padding: 10px 35px 10px 40px;
                font-size: 14px;
                font-weight: 400;
                selection-background-color: #4A90E2;
            }
            QLineEdit:focus {
                border: 2px solid #4A90E2;
                background-color: #F8FAFC;
                outline: none;
            }
            QLineEdit::placeholder {
                color: #A0AEC0;
                font-weight: 400;
            }
        """)
    
    def onTextChanged(self, text):
        self.clear_button.setVisible(bool(text))
    
    def setClearButtonWidget(self, button):
        self.clear_button = button
    
    def getClearButton(self):
        return self.clear_button

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
                }
                QPushButton:hover {
                    background-color: #E2E8F0;
                    border-color: #A0AEC0;
                }
            """
        }
        
        self.setStyleSheet(styles.get(style_type, styles["primary"]))

class ProductSelectorDialog(QDialog):
    def __init__(self, parent=None, addProductRow=None):
        super().__init__(parent)

        self.addProductRow = addProductRow
        self.products = []

        self.setWindowTitle("Select Product")

        # Set larger window size for more visible items
        screen = self.screen().availableGeometry()
        self.resize(
            min(int(screen.width() * 0.5), 700),
            min(int(screen.height() * 0.7), 800)
        )

        # Modern dialog styling
        self.setStyleSheet("""
            QDialog {
                background-color: #F7FAFC;
                color: #2D3748;
                font-family: 'Segoe UI', 'Inter', -apple-system, sans-serif;
            }
        """)

        self.initUI()
        self.loadProducts()

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # -------- Search Bar with Clear Button --------
        search_container = QWidget()
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(0, 0, 0, 0)
        search_layout.setSpacing(10)
        
        # Search icon
        search_icon = QLabel("🔍")
        search_icon.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: #A0AEC0;
                padding-left: 5px;
            }
        """)
        search_icon.setFixedWidth(30)
        search_layout.addWidget(search_icon)
        
        # Search input with clear button
        self.searchInput = ModernSearchLineEdit("Search products...")
        self.searchInput.textChanged.connect(self.filterProducts)
        search_layout.addWidget(self.searchInput)
        
        # Add clear button to the layout
        clear_button = self.searchInput.getClearButton()
        search_layout.addWidget(clear_button)
        
        layout.addWidget(search_container)

        # -------- Product List Header --------
        header_widget = QWidget()
        header_widget.setStyleSheet("""
            QWidget {
                background-color: #F8FAFC;
                border-radius: 6px;
                padding: 10px 16px;
                border: 1px solid #E2E8F0;
            }
        """)
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(16, 8, 16, 8)
        header_layout.setSpacing(0)
        
        # Product header
        product_header = QLabel("PRODUCT")
        product_header.setStyleSheet("""
            QLabel {
                font-size: 11px;
                font-weight: 600;
                color: #4A5568;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
        """)
        product_header.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        
        # Price header
        price_header = QLabel("PRICE")
        price_header.setStyleSheet("""
            QLabel {
                font-size: 11px;
                font-weight: 600;
                color: #4A5568;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
        """)
        price_header.setFixedWidth(80)
        price_header.setAlignment(Qt.AlignRight)
        
        header_layout.addWidget(product_header)
        header_layout.addWidget(price_header)
        layout.addWidget(header_widget)

        # -------- Product List (Takes most space) --------
        self.productList = QListWidget()
        self.productList.setSelectionMode(QListWidget.SingleSelection)
        self.productList.setFocusPolicy(Qt.StrongFocus)
        self.productList.setSpacing(0)
        self.productList.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # Set smaller font and item height to show more items
        self.productList.setStyleSheet("""
            QListWidget {
                background-color: white;
                border: 1px solid #E2E8F0;
                border-radius: 8px;
                padding: 0px;
                outline: none;
                font-size: 12px;
            }
            
            QListWidget::item {
                min-height: 28px;
                max-height: 28px;
                border: none;
                padding: 0px;
                margin: 0px;
            }
            
            QListWidget::item:selected {
                background-color: transparent;
                border: none;
                outline: none;
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
            
            QScrollBar:horizontal {
                height: 8px;
                background: transparent;
            }
            
            QScrollBar::handle:horizontal {
                background-color: #CBD5E0;
                border-radius: 4px;
                min-width: 30px;
            }
        """)

        layout.addWidget(self.productList, 1)  # Give stretch factor to take most space

        # -------- Selection Info --------
        self.selectionInfo = QLabel("")
        self.selectionInfo.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #718096;
                padding: 5px 0px;
            }
        """)
        self.selectionInfo.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.selectionInfo)

        # -------- Button Container --------
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(15)
        
        button_layout.addStretch()
        
        self.selectBtn = ModernButton("Add Product", "primary", width=140)
        self.selectBtn.setEnabled(False)
        self.selectBtn.clicked.connect(self.selectProduct)
        button_layout.addWidget(self.selectBtn)
        
        layout.addWidget(button_container)

        # Connect selection change
        self.productList.itemSelectionChanged.connect(self.updateSelectionState)

    # ----------------- DATA -----------------
    def loadProducts(self):
        db = DbClient()
        self.products = db.getAllProducts()  # [(id, name, price), ...]

        if not self.products:
            QMessageBox.information(
                self,
                "No Products",
                "No products found in the database.\n\nPlease add products first."
            )
            self.reject()
            return

        # Sort products by name
        self.products.sort(key=lambda x: x[1].lower())
        self.populateList(self.products)
        self.updateSelectionInfo(len(self.products))

    def populateList(self, products):
        self.productList.clear()
        
        for index, (pid, name, price) in enumerate(products):
            # Create a container widget for the entire row
            row_widget = QWidget()
            row_widget.setProperty("baseColor", "#FFFFFF" if index % 2 == 0 else "#F8FAFC")
            
            # Main layout for the row
            row_layout = QHBoxLayout(row_widget)
            row_layout.setContentsMargins(0, 0, 0, 0)  # No margins in the container
            row_layout.setSpacing(0)
            
            # Create the content widget that will have the border
            content_widget = QWidget()
            content_widget.setProperty("baseColor", "#FFFFFF" if index % 2 == 0 else "#F8FAFC")
            content_layout = QHBoxLayout(content_widget)
            content_layout.setContentsMargins(16, 6, 16, 6)  # Padding inside the content
            content_layout.setSpacing(0)

            # Name label
            nameLabel = QLabel(name)
            nameLabel.setStyleSheet("""
                QLabel {
                    font-size: 12px;
                    color: #2D3748;
                    font-weight: 400;
                }
            """)
            nameLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            nameLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

            # Price label
            priceLabel = QLabel(f"${price:.2f}")
            priceLabel.setStyleSheet("""
                QLabel {
                    font-size: 12px;
                    color: #2F855A;
                    font-weight: 600;
                }
            """)
            priceLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            priceLabel.setFixedWidth(80)

            content_layout.addWidget(nameLabel)
            content_layout.addWidget(priceLabel)
            
            # Add content widget to row widget
            row_layout.addWidget(content_widget)
            
            # Set initial styling
            base_color = "#FFFFFF" if index % 2 == 0 else "#F8FAFC"
            content_widget.setStyleSheet(f"""
                QWidget {{
                    background-color: {base_color};
                    border-bottom: 1px solid #F1F5F9;
                }}
            """)

            # Add item to QListWidget
            listItem = QListWidgetItem()
            listItem.setSizeHint(row_widget.sizeHint())
            listItem.setData(Qt.UserRole, (pid, name, price))  # Store data
            self.productList.addItem(listItem)
            self.productList.setItemWidget(listItem, row_widget)

        # Clear selection
        self.productList.clearSelection()
        self.selectBtn.setEnabled(False)
        self.selectionInfo.setText(f"Found {len(products)} product(s)")

    def updateSelectionState(self):
        selected = self.productList.currentItem()
        is_enabled = selected is not None
        self.selectBtn.setEnabled(is_enabled)
        
        # Update selection colors
        for i in range(self.productList.count()):
            item = self.productList.item(i)
            row_widget = self.productList.itemWidget(item)
            if row_widget:
                # Find the content widget inside the row widget
                content_widget = row_widget.findChild(QWidget)
                if content_widget:
                    baseColor = content_widget.property("baseColor") or "#FFFFFF"
                    
                    if item.isSelected():
                        # Apply border directly to the content widget
                        content_widget.setStyleSheet(f"""
                            QWidget {{
                                background-color: #EBF8FF;
                            }}
                        """)
                        # Get product data
                        product_data = item.data(Qt.UserRole)
                        if product_data:
                            pid, name, price = product_data
                            self.selectionInfo.setText(f"Selected: {name} (${price:.2f})")
                    else:
                        # No border-left for unselected items
                        content_widget.setStyleSheet(f"""
                            QWidget {{
                                background-color: {baseColor};
                                border-bottom: 1px solid #F1F5F9;
                                border-left: 0px solid transparent;
                            }}
                        """)

    def filterProducts(self, text):
        if not self.products:
            return
            
        if text.strip() == "":
            # Show all sorted by name when search is empty
            filtered = sorted(self.products, key=lambda x: x[1].lower())
        else:
            # Filter by name and sort by name
            filtered = [
                (pid, name, price) for pid, name, price in self.products
                if text.lower() in name.lower()
            ]
            filtered = sorted(filtered, key=lambda x: x[1].lower())
            
        self.populateList(filtered)
        self.updateSelectionInfo(len(filtered), text)

    def updateSelectionInfo(self, count, search_text=""):
        if search_text:
            if count == 0:
                self.selectionInfo.setText(f"No products found matching '{search_text}'")
            else:
                self.selectionInfo.setText(f"Found {count} product(s) matching '{search_text}'")
        else:
            self.selectionInfo.setText(f"Showing {count} product(s)")

    # ----------------- SELECTION -----------------
    def selectProduct(self):
        item = self.productList.currentItem()
        if not item:
            return

        # Get product data from stored role
        productID, name, price = item.data(Qt.UserRole)

        productData = {
            "productID": productID,
            "name": name,
            "price": price
        }

        if self.addProductRow:
            self.addProductRow(productData)

        self.accept()

# Utility function to open the dialog
def openProductSelector(parent=None, addProductRow=None):
    db = DbClient()
    products = db.getAllProducts()

    if not products:
        QMessageBox.information(
            parent,
            "No Products",
            "No products found in the database.\n\nPlease add products first."
        )
        return

    dialog = ProductSelectorDialog(
        parent=parent,
        addProductRow=addProductRow
    )
    dialog.exec()