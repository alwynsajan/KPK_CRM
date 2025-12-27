from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QHBoxLayout, QMessageBox, QFrame
)
from PySide6.QtCore import Qt
from dbClient import DbClient

# ------------------- Modern Line Edit -------------------
class ModernLineEdit(QLineEdit):
    def __init__(self, placeholder=""):
        super().__init__()
        self.setPlaceholderText(placeholder)
        self.setFixedHeight(40)
        self.setStyleSheet("""
            QLineEdit {
                background-color: #FFFFFF;
                color: #2D3748;
                border: 1px solid #E2E8F0;
                border-radius: 8px;
                padding: 10px 16px;
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
            "danger": """
                QPushButton {
                    background-color: #E53E3E;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 0px 24px;
                    font-size: 14px;
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

# ------------------- Modern Label -------------------
class ModernLabel(QLabel):
    def __init__(self, text, required=False):
        super().__init__(text)
        if required:
            text = f"{text} <span style='color: #E53E3E'>*</span>"
        self.setText(text)
        self.setStyleSheet("""
            QLabel {
                font-size: 13px;
                font-weight: 600;
                color: #2D3748;
                margin-bottom: 4px;
            }
        """)

# ------------------- Card Frame -------------------
class CardFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #E2E8F0;
            }
        """)

class ProductForm(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Add New Product")
        
        # Set window flags for modern look
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)
        
        # Modern window styling
        self.setStyleSheet("""
            QWidget {
                background-color: #F7FAFC;
                color: #2D3748;
                font-family: 'Segoe UI', 'Inter', -apple-system, sans-serif;
            }
        """)

        # Window size - slightly smaller to match others
        screen = self.screen().availableGeometry()
        self.resize(
            min(int(screen.width() * 0.38), 480),
            min(int(screen.height() * 0.40), 400)
        )

        self.move(
            (screen.width() - self.width()) // 2,
            (screen.height() - self.height()) // 4
        )

        # Main layout with reduced margins
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(16)

        # Title with less margin
        title_label = QLabel("Add New Product")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: 700;
                color: #2D3748;
                padding: 0px;
                margin-bottom: 2px;
            }
        """)
        main_layout.addWidget(title_label)

        # Description with less margin
        desc_label = QLabel("Enter product details below. Fields marked with * are required.")
        desc_label.setStyleSheet("""
            QLabel {
                font-size: 13px;
                color: #718096;
                margin-bottom: 16px;
            }
        """)
        desc_label.setWordWrap(True)
        main_layout.addWidget(desc_label)

        # Create main card with reduced margins
        card = CardFrame()
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(16)

        # --- Product Bar Code ---
        card_layout.addWidget(ModernLabel("Product Bar Code"))
        self.barcodeInput = ModernLineEdit("Optional - enter product barcode")
        card_layout.addWidget(self.barcodeInput)

        # --- Product Name ---
        card_layout.addWidget(ModernLabel("Product Name", required=True))
        self.nameInput = ModernLineEdit("Enter product name")
        card_layout.addWidget(self.nameInput)

        # --- Price ---
        card_layout.addWidget(ModernLabel("Price", required=True))
        
        # Price input with currency symbol
        price_container = QWidget()
        price_layout = QHBoxLayout(price_container)
        price_layout.setContentsMargins(0, 0, 0, 0)
        price_layout.setSpacing(8)
        
        currency_label = QLabel("$")
        currency_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: 600;
                color: #4A5568;
                padding-left: 5px;
            }
        """)
        currency_label.setFixedWidth(25)
        price_layout.addWidget(currency_label)
        
        self.priceInput = ModernLineEdit("0.00")
        price_layout.addWidget(self.priceInput)
        
        card_layout.addWidget(price_container)

        # Add card to main layout
        main_layout.addWidget(card)

        # --- Button Container ---
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(12)
        
        button_layout.addStretch()
        
        self.clearBtn = ModernButton("Clear", "secondary", width=90)
        self.clearBtn.clicked.connect(self.clearFields)
        
        self.addBtn = ModernButton("Add Product", "primary", width=130)
        self.addBtn.clicked.connect(self.addProduct)
        
        button_layout.addWidget(self.clearBtn)
        button_layout.addWidget(self.addBtn)
        
        main_layout.addWidget(button_container)

    def clearFields(self):
        self.barcodeInput.clear()
        self.nameInput.clear()
        self.priceInput.clear()
        
        # Set focus to name input for better UX
        self.nameInput.setFocus()

    def addProduct(self):
        barcode = self.barcodeInput.text().strip()
        name = self.nameInput.text().strip()
        price_text = self.priceInput.text().strip()

        # Validation
        errors = []
        
        if not name:
            errors.append("Product name is required")
            self.nameInput.setStyleSheet("""
                QLineEdit {
                    background-color: #FFFFFF;
                    color: #2D3748;
                    border: 2px solid #E53E3E;
                    border-radius: 8px;
                    padding: 10px 16px;
                    font-size: 14px;
                }
                QLineEdit:focus {
                    border: 2px solid #E53E3E;
                }
            """)
        else:
            self.nameInput.setStyleSheet(ModernLineEdit().styleSheet())
        
        if not price_text:
            errors.append("Price is required")
            self.priceInput.setStyleSheet("""
                QLineEdit {
                    background-color: #FFFFFF;
                    color: #2D3748;
                    border: 2px solid #E53E3E;
                    border-radius: 8px;
                    padding: 10px 16px;
                    font-size: 14px;
                }
                QLineEdit:focus {
                    border: 2px solid #E53E3E;
                }
            """)
        else:
            try:
                price = float(price_text)
                if price <= 0:
                    errors.append("Price must be greater than 0")
                    self.priceInput.setStyleSheet("""
                        QLineEdit {
                            background-color: #FFFFFF;
                            color: #2D3748;
                            border: 2px solid #E53E3E;
                            border-radius: 8px;
                            padding: 10px 16px;
                            font-size: 14px;
                        }
                    """)
                else:
                    self.priceInput.setStyleSheet(ModernLineEdit().styleSheet())
            except ValueError:
                errors.append("Price must be a valid number")
                self.priceInput.setStyleSheet("""
                    QLineEdit {
                        background-color: #FFFFFF;
                        color: #2D3748;
                        border: 2px solid #E53E3E;
                        border-radius: 8px;
                        padding: 10px 16px;
                        font-size: 14px;
                    }
                """)
        
        if not barcode:
            barcode = 0
        else:
            try:
                barcode = int(barcode)
                if barcode < 0:
                    errors.append("Barcode must be a positive number")
                    self.barcodeInput.setStyleSheet("""
                        QLineEdit {
                            background-color: #FFFFFF;
                            color: #2D3748;
                            border: 2px solid #E53E3E;
                            border-radius: 8px;
                            padding: 10px 16px;
                            font-size: 14px;
                        }
                    """)
                else:
                    self.barcodeInput.setStyleSheet(ModernLineEdit().styleSheet())
            except ValueError:
                errors.append("Barcode must be a valid number")
                self.barcodeInput.setStyleSheet("""
                    QLineEdit {
                        background-color: #FFFFFF;
                        color: #2D3748;
                        border: 2px solid #E53E3E;
                        border-radius: 8px;
                        padding: 10px 16px;
                        font-size: 14px;
                    }
                """)
        
        if errors:
            QMessageBox.warning(
                self,
                "Validation Error",
                "Please fix the following errors:\n\n• " + "\n• ".join(errors)
            )
            return

        # Get price value
        try:
            price = float(price_text)
        except ValueError:
            price = 0

        # Database operation
        db = DbClient()
        response = db.addProductData({
            "productBarCode": barcode,
            "name": name,
            "price": price
        })

        if response["status"] != "Success":
            QMessageBox.critical(
                self,
                "Database Error",
                f"Failed to add product.\n\nError: {response.get('message', 'Unknown error')}"
            )
            return

        # Success message
        QMessageBox.information(
            self,
            "Success",
            f"Product '{name}' has been added successfully!"
        )
        
        # Clear fields after success
        self.clearFields()