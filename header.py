from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor, QFont


class Header(QWidget):
    def __init__(self):
        super().__init__()
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
        
        # User info with light gray for contrast
        userWidget = QWidget()
        userWidget.setStyleSheet("background: transparent;")
        userLayout = QHBoxLayout(userWidget)
        userLayout.setSpacing(10)
        
        userIcon = QLabel("👤")
        userIcon.setStyleSheet("font-size: 16px; color: #E0E6ED;")
        
        userName = QLabel("Admin User")
        userName.setStyleSheet("""
            color: #E0E6ED;  /* Light gray for contrast */
            font-weight: 500;
            font-size: 14px;
        """)
        
        userLayout.addWidget(userIcon)
        userLayout.addWidget(userName)
        topRow.addWidget(userWidget)
        
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
            bottomRow.addWidget(btn)
            self.headerBtns.append(btn)
        
        headerLayout.addLayout(bottomRow)

        self.setLayout(headerLayout)

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