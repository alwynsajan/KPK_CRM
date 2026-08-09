from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QFileDialog, QMessageBox, QFrame, QCheckBox
)
from PySide6.QtCore import Qt
import csv
import os
from datetime import date, datetime
from decimal import Decimal
from dbClient import DbClient


# ------------------- Modern Button -------------------
class ModernButton(QPushButton):
    def __init__(self, text, style_type="primary", width=None):
        super().__init__(text)
        self.setFixedHeight(44)
        if width:
            self.setFixedWidth(width)
        self.setCursor(Qt.PointingHandCursor)

        styles = {
            "primary": """
                QPushButton {
                    background-color: #38A169;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 0px 24px;
                    font-size: 14px;
                    font-weight: 600;
                }
                QPushButton:hover {
                    background-color: #2F855A;
                }
                QPushButton:pressed {
                    background-color: #276749;
                }
                QPushButton:disabled {
                    background-color: #E2E8F0;
                    color: #A0AEC0;
                }
            """,
            "secondary": """
                QPushButton {
                    background-color: #EDF2F7;
                    color: #4A5568;
                    border: 1px solid #CBD5E0;
                    border-radius: 8px;
                    padding: 0px 24px;
                    font-size: 14px;
                    font-weight: 600;
                }
                QPushButton:hover {
                    background-color: #E2E8F0;
                    border-color: #A0AEC0;
                }
            """
        }

        self.setStyleSheet(styles.get(style_type, styles["primary"]))


class ExportDialog(QDialog):
    TABLES = [
        ("customerData", "Customers"),
        ("productData", "Products"),
        ("sales", "Sales"),
        ("saleItems", "Sale Items"),
        ("perDaySale", "Per-Day Sales"),
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Export Data")
        self.setFixedSize(420, 460)
        self.setStyleSheet("""
            QDialog {
                background-color: #F7FAFC;
                font-family: 'Segoe UI', 'Inter', -apple-system, sans-serif;
            }
            QLabel {
                color: #2D3748;
            }
            QCheckBox {
                font-size: 14px;
                color: #2D3748;
                spacing: 10px;
                padding: 6px 4px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #CBD5E0;
                border-radius: 4px;
                background: white;
            }
            QCheckBox::indicator:checked {
                background-color: #38A169;
                border-color: #38A169;
            }
        """)
        self.db = DbClient()
        self.table_checks = []
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(16)

        title = QLabel("Export Database Tables")
        title.setStyleSheet("""
            QLabel {
                font-size: 22px;
                font-weight: 700;
                color: #1A202C;
            }
        """)
        layout.addWidget(title)

        subtitle = QLabel("Select one or more tables, then click Export.")
        subtitle.setStyleSheet("""
            QLabel {
                font-size: 13px;
                color: #718096;
            }
        """)
        layout.addWidget(subtitle)

        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E2E8F0;
                border-radius: 12px;
            }
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 16, 20, 16)
        card_layout.setSpacing(4)

        self.select_all_check = QCheckBox("Select All")
        self.select_all_check.setStyleSheet("""
            QCheckBox {
                font-size: 14px;
                font-weight: 600;
                color: #2D3748;
                spacing: 10px;
                padding: 6px 4px;
            }
        """)
        self.select_all_check.toggled.connect(self.toggleSelectAll)
        card_layout.addWidget(self.select_all_check)

        for table_name, label in self.TABLES:
            check = QCheckBox(label)
            check.setProperty("tableName", table_name)
            check.toggled.connect(self.updateSelectAllState)
            self.table_checks.append(check)
            card_layout.addWidget(check)

        layout.addWidget(card)
        layout.addStretch()

        button_row = QHBoxLayout()
        button_row.setSpacing(12)

        close_btn = ModernButton("Close", "secondary")
        close_btn.clicked.connect(self.reject)
        button_row.addWidget(close_btn)

        self.export_btn = ModernButton("Export", "primary")
        self.export_btn.clicked.connect(self.exportSelected)
        button_row.addWidget(self.export_btn)

        layout.addLayout(button_row)

    def toggleSelectAll(self, checked):
        for check in self.table_checks:
            check.blockSignals(True)
            check.setChecked(checked)
            check.blockSignals(False)

    def updateSelectAllState(self):
        all_checked = all(check.isChecked() for check in self.table_checks)
        self.select_all_check.blockSignals(True)
        self.select_all_check.setChecked(all_checked)
        self.select_all_check.blockSignals(False)

    def _selectedTables(self):
        return [
            check.property("tableName")
            for check in self.table_checks
            if check.isChecked()
        ]

    def _formatCell(self, value):
        if value is None:
            return ""
        if isinstance(value, datetime):
            return value.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(value, date):
            return value.strftime("%Y-%m-%d")
        if isinstance(value, Decimal):
            return f"{value:.2f}"
        return str(value)

    def _writeCsv(self, table_name, file_path):
        result = self.db.getTableRowsForExport(table_name)
        if result.get("status") != "Success":
            raise RuntimeError(result.get("message", f"Failed to read {table_name}"))

        columns = result["columns"]
        rows = result["rows"]

        with open(file_path, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(columns)
            for row in rows:
                writer.writerow([self._formatCell(row.get(col)) for col in columns])

        return len(rows)

    def exportSelected(self):
        selected = self._selectedTables()
        if not selected:
            QMessageBox.warning(
                self,
                "No Table Selected",
                "Please select at least one table to export."
            )
            return

        exported = []
        try:
            if len(selected) == 1:
                table_name = selected[0]
                file_path, _ = QFileDialog.getSaveFileName(
                    self,
                    f"Export {table_name}",
                    f"{table_name}.csv",
                    "CSV Files (*.csv)"
                )
                if not file_path:
                    return
                if not file_path.lower().endswith(".csv"):
                    file_path += ".csv"

                row_count = self._writeCsv(table_name, file_path)
                exported.append((table_name, row_count, file_path))
            else:
                folder = QFileDialog.getExistingDirectory(
                    self,
                    "Select folder for CSV exports"
                )
                if not folder:
                    return

                for table_name in selected:
                    file_path = os.path.join(folder, f"{table_name}.csv")
                    row_count = self._writeCsv(table_name, file_path)
                    exported.append((table_name, row_count, file_path))

            summary = "\n".join(
                f"• {name}: {count} row(s)" for name, count, _ in exported
            )
            QMessageBox.information(
                self,
                "Export Complete",
                f"Successfully exported {len(exported)} table(s):\n\n{summary}"
            )
        except (OSError, RuntimeError) as err:
            QMessageBox.critical(
                self,
                "Export Failed",
                f"Could not complete export.\n\n{err}"
            )
