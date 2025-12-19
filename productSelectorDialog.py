from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QListWidget, QPushButton,
    QLineEdit, QLabel, QWidget, QHBoxLayout, QListWidgetItem, QSizePolicy
)
from PySide6.QtCore import Qt
from dbClient import DbClient


class ProductSelectorDialog(QDialog):
    def __init__(self, parent=None, addProductRow=None):
        super().__init__(parent)

        self.addProductRow = addProductRow
        self.products = []

        self.setWindowTitle("Select Product")

        # --- Window Size ---
        screen = self.screen().availableGeometry()
        self.resize(
            int(screen.width() * 0.5),
            int(screen.height() * 0.5)
        )

        self.setStyleSheet("""
            background-color: #EBE8DB;
            color: black;
            font-size: 12px;
        """)

        self.initUI()
        self.loadProducts()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)

        # --- Search ---
        layout.addWidget(QLabel("Search Product Name"))
        self.searchInput = QLineEdit()
        self.searchInput.setPlaceholderText("Type product name...")
        self.searchInput.textChanged.connect(self.filterProducts)
        self.searchInput.setClearButtonEnabled(True)
        self.searchInput.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 2px solid lightblue;
                border-radius: 6px;
                padding-left: 6px;
                height: 28px;
            }
        """)
        layout.addWidget(self.searchInput)

        # --- Product List ---
        self.productList = QListWidget()
        self.productList.setSelectionMode(QListWidget.SingleSelection)
        self.productList.setFocusPolicy(Qt.NoFocus)
        self.productList.setSpacing(0)
        self.productList.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.productList.setStyleSheet("""
            QListWidget {
                background-color: white;
                border-radius: 6px;
            }
            QListWidget::item:hover {
                background-color: #D6EAF8;
            }

            /* --- Vertical Scrollbar --- */
            QScrollBar:vertical {
                background: transparent;
                width: 10px;
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
            }
            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: none;
            }
        """)

        layout.addWidget(self.productList)

        # --- Select Button ---
        self.selectBtn = QPushButton("Add Product")
        self.selectBtn.setEnabled(False)
        self.selectBtn.clicked.connect(self.selectProduct)
        self.selectBtn.setCursor(Qt.PointingHandCursor)
        self.selectBtn.setStyleSheet("""
            QPushButton {
                background-color: #B0B0B0;
                color: white;
                padding: 10px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:enabled {
                background-color: #3498DB;
            }
            QPushButton:hover:enabled {
                background-color: #2E86C1;
            }
        """)
        layout.addWidget(self.selectBtn)

        # Enable button only when an item is selected
        self.productList.itemSelectionChanged.connect(
            lambda: self.selectBtn.setEnabled(
                self.productList.currentItem() is not None
            )
        )

        self.setLayout(layout)

    # ----------------- DATA -----------------
    def loadProducts(self):
        db = DbClient()
        self.products = db.getAllProducts()  # [(id, name, price), ...]

        if not self.products:
            return

        self.populateList(self.products)

    def populateList(self, products):
        self.productList.clear()
        for index, (pid, name, price) in enumerate(products):
            itemWidget = QWidget()
            layout = QHBoxLayout()
            layout.setContentsMargins(5, 2, 5, 2)
            layout.setSpacing(0)

            # Name label
            nameLabel = QLabel(name)
            nameLabel.setStyleSheet("font-size: 14px;")
            nameLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            nameLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

            # Price label
            priceLabel = QLabel(f"${price:.2f}")
            priceLabel.setStyleSheet("font-size: 14px; font-weight: bold;")
            priceLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            priceLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)

            layout.addWidget(nameLabel)
            layout.addWidget(priceLabel)
            itemWidget.setLayout(layout)

            # Alternating row colors
            base_color = "#FFFFFF" if index % 2 == 0 else "#E7EFF5"
            itemWidget.setProperty("baseColor", base_color)
            itemWidget.setStyleSheet(f"""
                background-color: {base_color};
            """)

            # Add item to QListWidget
            listItem = QListWidgetItem()
            listItem.setSizeHint(itemWidget.sizeHint())
            self.productList.addItem(listItem)
            self.productList.setItemWidget(listItem, itemWidget)

        # Update selection color dynamically
        self.productList.itemSelectionChanged.connect(self.updateSelectionColor)
        self.productList.clearSelection()
        self.selectBtn.setEnabled(False)

    def updateSelectionColor(self):
        for i in range(self.productList.count()):
            item = self.productList.item(i)
            widget = self.productList.itemWidget(item)
            baseColor = widget.property("baseColor")
            if item.isSelected():
                widget.setStyleSheet("background-color: #3498DB; color: white;")
            else:
                widget.setStyleSheet(f"background-color: {baseColor}; color: black;")

    def filterProducts(self, text):
        filtered = [
            p for p in self.products
            if text.lower() in p[1].lower()
        ]
        self.populateList(filtered)

    # ----------------- SELECTION -----------------
    def selectProduct(self):
        row = self.productList.currentRow()
        if row < 0:
            return

        productID, name, price = self.products[row]

        productData = {
            "productID": productID,
            "name": name,
            "price": price
        }

        if self.addProductRow:
            self.addProductRow(productData)

        self.accept()
