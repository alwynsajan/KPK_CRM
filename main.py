# mainContent.py
import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
from sideBar import SideBar
from header import Header
from mainArea import MainArea
from PySide6.QtCore import Qt

class CRMWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CRM App")
        self.setStyleSheet("""
            background-color: #EBE8DB;  /* background */
            color: black;               /* default text color */
        """)

        # ------------------- Internal State Variables -------------------
        self.selectedCustomerDetails = {} 
        self.finalProductList = []

        # Make the window maximized by default
        self.setWindowState(Qt.WindowMaximized)

        # --- Main Layout ---
        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(0,0,0,0)
        mainLayout.setSpacing(0)
        self.setLayout(mainLayout)

        # Header
        self.header = Header()
        mainLayout.addWidget(self.header)

        # Main horizontal area
        mainContentLayout = QHBoxLayout()
        mainContentLayout.setContentsMargins(0,0,0,0)
        mainContentLayout.setSpacing(0)
        mainLayout.addLayout(mainContentLayout)

        # Sidebar
        self.sideBar = SideBar(selectedCustomerDetails=self.selectedCustomerDetails)
        mainContentLayout.addWidget(self.sideBar, stretch=1) 

        # Main area
        self.mainArea = MainArea(
            selectedCustomerDetails=self.selectedCustomerDetails,
            finalProductList=self.finalProductList,
            sidebar=self.sideBar 
        ) 
        mainContentLayout.addWidget(self.mainArea, stretch=6)
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CRMWindow()
    window.show()
    sys.exit(app.exec())
