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

        # Make the window maximized by default
        self.setWindowState(Qt.WindowMaximized)

        # --- Main Layout ---
        mainLayout = QVBoxLayout()  # full window vertical layout
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
        self.sideBar = SideBar()
        mainContentLayout.addWidget(self.sideBar)

        # Main area
        self.mainArea = MainArea()
        mainContentLayout.addWidget(self.mainArea, stretch=1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CRMWindow()
    window.show()  # no need for showMaximized here, handled by setWindowState
    sys.exit(app.exec())
