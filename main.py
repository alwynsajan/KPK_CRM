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
            background-color: #EBE8DB;
            color: black;
        """)

        # ------------------- Shared State -------------------
        self.selectedCustomerDetails = {}
        self.finalProductList = []

        self.setWindowState(Qt.WindowMaximized)

        # ------------------- Layout -------------------
        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)

        # Header
        self.header = Header()
        mainLayout.addWidget(self.header)

        # Horizontal content
        mainContentLayout = QHBoxLayout()
        mainLayout.addLayout(mainContentLayout)

        # Sidebar
        self.sideBar = SideBar(
            selectedCustomerDetails=self.selectedCustomerDetails
        )
        mainContentLayout.addWidget(self.sideBar, stretch=1)

        # Main Area
        self.mainArea = MainArea(
            selectedCustomerDetails=self.selectedCustomerDetails,
            finalProductList=self.finalProductList,
            sidebar=self.sideBar
        )
        mainContentLayout.addWidget(self.mainArea, stretch=5)

        # IMPORTANT: signal wiring happens HERE
        self.sideBar.customerAdded.connect(self.handleCustomerAdded)

    # ------------------- Signal Handler -------------------
    def handleCustomerAdded(self, customerData):
        print(self.selectedCustomerDetails )
        """
        Called when a new customer is added from sidebar form
        """

        # Update shared state
        self.selectedCustomerDetails.clear()
        self.selectedCustomerDetails.update(customerData)

        # Update MainArea input field
        self.mainArea.updateCustomerInput()

        # Refresh sidebar UI
        self.sideBar.updateCustomerInfo()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CRMWindow()
    window.show()
    sys.exit(app.exec())
