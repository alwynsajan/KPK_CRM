import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
from sideBar import SideBar
from header import Header
from mainArea import MainArea
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor, QFont


class CRMWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("K.P.K ASSOCIATES - CRM System")
        
        # Set window icon and style
        self.setStyleSheet("""
            QWidget {
                background-color: #E6E6E6;
                color: #2D3748;
                font-family: 'Segoe UI', 'Inter', Arial, sans-serif;
            }
            QMainWindow::separator {
                background-color: #E2E8F0;
                width: 2px;
                height: 2px;
            }
        """)
        
        # Set application palette for better contrast
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#F7FAFC"))
        palette.setColor(QPalette.WindowText, QColor("#2D3748"))
        palette.setColor(QPalette.Base, QColor("#FFFFFF"))
        palette.setColor(QPalette.AlternateBase, QColor("#EDF2F7"))
        palette.setColor(QPalette.Text, QColor("#2D3748"))
        palette.setColor(QPalette.Button, QColor("#4A90E2"))
        palette.setColor(QPalette.ButtonText, QColor("#FFFFFF"))
        palette.setColor(QPalette.Highlight, QColor("#4A90E2"))
        palette.setColor(QPalette.HighlightedText, QColor("#FFFFFF"))
        self.setPalette(palette)

        self.setWindowState(Qt.WindowMaximized)

        # ------------------- Shared State -------------------
        self.selectedCustomerDetails = {}
        self.finalProductList = []

        # ------------------- Main Layout -------------------
        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)

        # Header
        self.header = Header()
        mainLayout.addWidget(self.header)

        # Horizontal content area
        contentArea = QHBoxLayout()
        contentArea.setContentsMargins(0, 0, 0, 0)
        contentArea.setSpacing(0)

        # Sidebar
        self.sideBar = SideBar(
            selectedCustomerDetails=self.selectedCustomerDetails
        )

        # Main Area
        self.mainArea = MainArea(
            selectedCustomerDetails=self.selectedCustomerDetails,
            finalProductList=self.finalProductList,
            sidebar=self.sideBar
        )

        # Add widgets with stretch control
        contentArea.addWidget(self.sideBar, 2)  
        contentArea.addWidget(self.mainArea, 8)  

        mainLayout.addLayout(contentArea)

        # Connect signals
        self.sideBar.customerAdded.connect(self.handleCustomerAdded)


    # ------------------- Signal Handler -------------------
    def handleCustomerAdded(self, customerData):
        # Update shared state
        self.selectedCustomerDetails.clear()
        self.selectedCustomerDetails.update(customerData)

        # Update MainArea input field
        self.mainArea.updateCustomerInput()

        # Refresh sidebar UI
        self.sideBar.updateCustomerInfo()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set application-wide font for better readability
    font = QFont("Segoe UI", 9)
    app.setFont(font)
    
    # Set application style
    app.setStyle("Fusion")
    
    window = CRMWindow()
    window.show()
    sys.exit(app.exec())