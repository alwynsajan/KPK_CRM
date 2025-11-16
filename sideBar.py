# sidebar.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt

class SideBar(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(200)
        self.setStyleSheet("background-color: #E6E6E6;")

        # Layout
        sideBarLayout = QVBoxLayout()
        sideBarLayout.setAlignment(Qt.AlignTop)

        # Buttons
        self.sidebarBtns = []
        btnNames = ["Sales", "Credits", "Misc", "Upload Pdt Details"]
        for name in btnNames:
            btn = QPushButton(name)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #E6E6E6;
                    color: #333;
                    padding: 10px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #D9D9D9;
                }
            """)
            sideBarLayout.addWidget(btn)
            self.sidebarBtns.append(btn)

        self.setLayout(sideBarLayout)
