from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor
from csvImportDialog import CSVImportDialog
from exportDialog import ExportDialog
# from reportsDialog import ReportsDialog


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
        btnNames = [
            "📈 Reports",
            "📊 Sales",
            "💳 Credits",
            "📤 Import Pdt Data",
            "📥 Export",
        ]
        self.headerBtns = []
        
        for name in btnNames:
            style = "export" if name == "📥 Export" else "default"
            btn = ModernNavButton(name, style_type=style)
            if name == "💳 Credits":
                btn.clicked.connect(self.openCreditSales)
            elif name == "📊 Sales":
                btn.clicked.connect(self.openSalesHistory)
            elif name == "📤 Import Pdt Data":
                btn.clicked.connect(self.openCSVImport)
            elif name == "📥 Export":
                btn.clicked.connect(self.openExportDialog)
            elif name == "📈 Reports":
                btn.clicked.connect(self.openReportsDialog)
            bottomRow.addWidget(btn)
            self.headerBtns.append(btn)
        
        headerLayout.addLayout(bottomRow)

        self.setLayout(headerLayout)
    
    # ------------------- Open Sales History -------------------
    def openCreditSales(self):
        """Open credit sales dialog"""
        if self.main_window:  # Check if we have a valid parent window
            # Import here to avoid circular imports
            from creditSalesDialog import CreditSalesDialog
            dialog = CreditSalesDialog(self.main_window)
            dialog.exec()
        else:
            print("Error: No parent window found for credit sales dialog")

    # ------------------- Open Sales History -------------------
    def openSalesHistory(self):
        """Open sales history dialog"""
        if self.main_window:
            from salesHistoryDialog import SalesHistoryDialog
            dialog = SalesHistoryDialog(self.main_window)
            dialog.exec()

    def openCSVImport(self):
        """Open CSV import dialog"""
        dialog = CSVImportDialog(self)
        dialog.exec()

    def openExportDialog(self):
        """Open CSV export dialog"""
        dialog = ExportDialog(self.main_window or self)
        dialog.exec()

    def openReportsDialog(self):
        dialog = ReportsDialog(self.main_window)
        dialog.exec()

# ------------------- Modern Navigation Button -------------------
class ModernNavButton(QPushButton):
    def __init__(self, text, style_type="default"):
        super().__init__(text)
        self.setFixedHeight(34)
        self.setMinimumWidth(110)
        self.setCursor(Qt.PointingHandCursor)

        styles = {
            "default": """
                QPushButton {
                    background-color: rgba(74, 144, 226, 0.9);
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 6px 12px;
                    font-size: 12px;
                    font-weight: 600;
                    min-width: 105px;
                }
                QPushButton:hover {
                    background-color: rgba(52, 152, 219, 1.0);
                }
                QPushButton:pressed {
                    background-color: #21618C;
                }
            """,
            "export": """
                QPushButton {
                    background-color: rgba(56, 161, 105, 0.95);
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 6px 12px;
                    font-size: 12px;
                    font-weight: 600;
                    min-width: 105px;
                }
                QPushButton:hover {
                    background-color: #2F855A;
                }
                QPushButton:pressed {
                    background-color: #276749;
                }
            """,
        }

        self.setStyleSheet(styles.get(style_type, styles["default"]))
