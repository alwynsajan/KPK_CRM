from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor


class Header(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent  # Store reference to main window
        self.setFixedHeight(100)
        
        # Set dark blue background with good contrast
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#1A3A5F"))  # Dark blue
        self.setPalette(palette)

        # Main layout
        headerLayout = QVBoxLayout()
        headerLayout.setContentsMargins(25, 12, 25, 12)
        headerLayout.setSpacing(8)

        # Top row: Logo and user info
        topRow = QHBoxLayout()
        
        # Company name with high contrast white
        self.titleLabel = QLabel("K.P.K ASSOCIATES")
        self.titleLabel.setStyleSheet("""
            font-size: 38px;
            font-weight:bold;
            color: Black;  
            letter-spacing: 0.5px;
        """)
        self.titleLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        topRow.addWidget(self.titleLabel)
        topRow.addStretch()
        
        headerLayout.addLayout(topRow)

        # Bottom row: Navigation and subtitle
        bottomRow = QHBoxLayout()
        
        # Subtitle with good contrast
        subtitle = QLabel("")
        subtitle.setStyleSheet("""
            font-size: 13px;
            font-weight: 400;
            color: #A0B4C8;  /* Light blue-gray */
            margin-left: 2px;
        """)
        subtitle.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        bottomRow.addWidget(subtitle)
        bottomRow.addStretch()

        # Navigation buttons with contrast
        btnNames = ["📊 Sales", "💳 Credits", "📤 Upload"]
        self.headerBtns = []
        
        for name in btnNames:
            btn = ModernNavButton(name)
            if name == "💳 Credits":
                btn.clicked.connect(self.openCreditSales)
            bottomRow.addWidget(btn)
            self.headerBtns.append(btn)
        
        headerLayout.addLayout(bottomRow)

        self.setLayout(headerLayout)
    
    def openCreditSales(self):
        """Open credit sales dialog"""
        if self.main_window:  # Check if we have a valid parent window
            # Import here to avoid circular imports
            from creditSalesDialog import CreditSalesDialog
            dialog = CreditSalesDialog(self.main_window)
            dialog.exec()
        else:
            print("Error: No parent window found for credit sales dialog")

# ------------------- Modern Navigation Button -------------------
class ModernNavButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setFixedHeight(34)
        self.setFixedWidth(110)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                background-color: rgba(74, 144, 226, 0.9);
                color: white;
                border: none;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 12px;
                font-weight: 600;
                min-width: 90px;
            }
            QPushButton:hover {
                background-color: rgba(52, 152, 219, 1.0);
            }
            QPushButton:pressed {
                background-color: #21618C;
            }
        """)