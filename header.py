from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QSizePolicy
from PySide6.QtCore import Qt

class Header(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(120)  # slightly taller to fit buttons
        self.setAutoFillBackground(True)

        # Main vertical layout
        headerLayout = QVBoxLayout()
        headerLayout.setContentsMargins(10, 5, 10, 5)
        headerLayout.setSpacing(5)

        # Title
        self.titleLabel = QLabel("K.P.K ASSOCIATES")
        self.titleLabel.setStyleSheet("""
            font-size: 42px; 
            font-weight: bold; 
            color: Black;
        """)
        self.titleLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.titleLabel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        headerLayout.addWidget(self.titleLabel)

        # Horizontal layout for buttons
        buttonLayout = QHBoxLayout()
        buttonLayout.setSpacing(10)

        btnNames = ["Sales", "Credits","Stocks"]
        self.headerBtns = []
        for name in btnNames:
            btn = QPushButton(name)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #3498DB;
                    color: white;
                    padding: 8px 15px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #2E86C1;
                }
            """)
            btn.setCursor(Qt.PointingHandCursor)
            buttonLayout.addWidget(btn)
            self.headerBtns.append(btn)

        buttonLayout.addStretch()  # push buttons to left
        headerLayout.addLayout(buttonLayout)

        self.setLayout(headerLayout)
