# sidebar.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor
from productForm import ProductForm


class SideBar(QWidget):
    def __init__(self, selectedCustomerDetails=None):
        super().__init__()
        self.selectedCustomerDetails = selectedCustomerDetails or {}

        # Set background color
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#547792"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # --- Main Layout ---
        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(10, 10, 10, 10)
        mainLayout.setSpacing(10)
        mainLayout.setAlignment(Qt.AlignTop)
        self.setLayout(mainLayout)

        # --- Vertical Buttons ---
        self.headerBtns = []
        btnNames = [ "Add Product to DB", "Miscellanious", "Upload Pdt Details"]
        for name in btnNames:
            btn = QPushButton(name)

            if name == "Add Product to DB":
                btn.clicked.connect(self.openProductForm)

            btn.setStyleSheet("""
                QPushButton {
                    background-color: #3498DB;
                    color: white;
                    padding: 10px;
                    border-radius: 5px;
                    text-align: center;
                }
                QPushButton:hover {
                    background-color: #2E86C1;
                }
            """)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            mainLayout.addWidget(btn)
            self.headerBtns.append(btn)

        mainLayout.addSpacing(10)  # space between buttons and scroll area

        # --- Scrollable Content Area ---
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Widget inside scroll area
        self.scrollWidget = QWidget()
        self.scrollLayout = QVBoxLayout()
        self.scrollLayout.setAlignment(Qt.AlignTop)
        self.scrollWidget.setLayout(self.scrollLayout)

        self.scrollArea.setWidget(self.scrollWidget)
        mainLayout.addWidget(self.scrollArea, stretch=1)  # stretch to fill remaining space

        # --- Initial Info Label ---
        self.infoLabel = QLabel()
        self.infoLabel.setStyleSheet("color: black; font-size: 16px; font-weight: bold;")
        self.infoLabel.setAlignment(Qt.AlignCenter)
        self.updateCustomerInfo()  # display default text if empty
        self.scrollLayout.addWidget(self.infoLabel)

    def updateCustomerInfo(self):
        """Update the scroll area content when customer is selected"""
        # Clear all widgets except header buttons
        for i in reversed(range(self.scrollLayout.count())):
            widget = self.scrollLayout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        # Update info
        if not self.selectedCustomerDetails:
            self.infoLabel = QLabel("Select customer to see Sales")
        else:
            cust = self.selectedCustomerDetails
            info = f"Customer: {cust.get('name','')}\nPhone: {cust.get('phone','')}\nAddress: {cust.get('address','')}"
            self.infoLabel = QLabel(info)

        self.infoLabel.setStyleSheet("color: black; font-size: 16px; font-weight: bold;text-align: center;")
        self.infoLabel.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.infoLabel.setWordWrap(True)
        self.scrollLayout.addWidget(self.infoLabel)

    def openProductForm(self):
        self.productWindow = ProductForm()
        self.productWindow.show()

