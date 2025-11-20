# header.py
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QSizePolicy
from PySide6.QtCore import Qt

class Header(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #F2F2F2;")
        
        headerLayout = QVBoxLayout()
        headerLayout.setContentsMargins(10, 5, 10, 5)
        headerLayout.setSpacing(5)

        # Title
        self.titleLabel = QLabel("K.P.K Associates")
        self.titleLabel.setStyleSheet("""
            font-size: 28px; 
            font-weight: bold; 
            background-color: transparent;
        """)
        self.titleLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.titleLabel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        headerLayout.addWidget(self.titleLabel)

        # Button layout
        buttonLayout = QHBoxLayout()
        buttonLayout.setSpacing(5)
        buttonLayout.setAlignment(Qt.AlignLeft)

        # Buttons
        primaryButtonStyle = """
            QPushButton {
                background-color: #3498DB;
                color: white;
                padding: 5px 15px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2E86C1;
            }
        """
        failureButtonStyle = """
            QPushButton {
                background-color: #E74C3C;
                color: white;
                padding: 5px 15px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
        """

        self.selectCustomerBtn = QPushButton("Select Customer")
        self.selectProductBtn = QPushButton("Select Product")
        self.voidSaleBtn = QPushButton("Void Sale")
        self.selectCustomerBtn.setStyleSheet(primaryButtonStyle)
        self.selectProductBtn.setStyleSheet(primaryButtonStyle)
        self.voidSaleBtn.setStyleSheet(failureButtonStyle)

        for btn in [self.selectCustomerBtn, self.selectProductBtn, self.voidSaleBtn]:
            btn.setFixedHeight(28)

        # buttonLayout.addWidget(self.selectCustomerBtn)
        # buttonLayout.addWidget(self.selectProductBtn)
        buttonLayout.addWidget(self.voidSaleBtn)

        headerLayout.addLayout(buttonLayout)
        self.setLayout(headerLayout)
        self.setMaximumHeight(100)  # optional: keeps header compact
