from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QPushButton, QLabel, 
    QFileDialog, QMessageBox, QProgressBar,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QGroupBox, QHBoxLayout
)
from PySide6.QtCore import Qt
import csv
import os
from dbClient import DbClient

# ------------------- Modern Button -------------------
class ModernButton(QPushButton):
    def __init__(self, text, style_type="primary", width=None):
        super().__init__(text)
        self.setFixedHeight(40)
        if width:
            self.setFixedWidth(width)
        self.setCursor(Qt.PointingHandCursor)
        
        styles = {
            "primary": """
                QPushButton {
                    background-color: #4A90E2;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 0px 24px;
                    font-size: 14px;
                    font-weight: 600;
                }
                QPushButton:hover {
                    background-color: #3182CE;
                }
                QPushButton:pressed {
                    background-color: #2C5282;
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

class CSVImportDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Import Product Data from CSV")
        self.setFixedSize(700, 600)
        self.setStyleSheet("""
            QDialog {
                background-color: #F7FAFC;
                font-family: 'Segoe UI', 'Inter', -apple-system, sans-serif;
            }
            QLabel {
                color: #2D3748;
                font-size: 14px;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #E2E8F0;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #4A5568;
            }
        """)
        
        self.csv_data = []
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title = QLabel("Import Product Data from CSV")
        title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #2D3748;
                margin-bottom: 10px;
            }
        """)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Instructions
        instructions = QLabel(
            "Select a CSV file containing product data.\n"
            "Required columns: productBarCode, name, price, pdtType\n"
        )
        instructions.setStyleSheet("""
            QLabel {
                color: #718096;
                font-size: 13px;
                padding: 10px;
                background-color: #EDF2F7;
                border-radius: 6px;
                border: 1px solid #E2E8F0;
            }
        """)
        instructions.setAlignment(Qt.AlignCenter)
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
        
        # File selection group
        file_group = QGroupBox("Step 1: Select CSV File")
        file_layout = QVBoxLayout()
        
        self.file_label = QLabel("No file selected")
        self.file_label.setStyleSheet("""
            QLabel {
                color: #4A5568;
                padding: 8px;
                background-color: white;
                border: 1px solid #E2E8F0;
                border-radius: 6px;
                min-height: 40px;
            }
        """)
        file_layout.addWidget(self.file_label)
        
        file_btn_layout = QHBoxLayout()
        self.select_file_btn = ModernButton("Browse CSV File", "primary")
        self.select_file_btn.clicked.connect(self.selectCSVFile)
        file_btn_layout.addWidget(self.select_file_btn)
        
        file_btn_layout.addStretch()
        file_layout.addLayout(file_btn_layout)
        
        file_group.setLayout(file_layout)
        layout.addWidget(file_group)
        
        # Preview group
        self.preview_group = QGroupBox("Step 2: Preview Data")
        self.preview_group.setVisible(False)
        preview_layout = QVBoxLayout()
        
        self.preview_table = QTableWidget()
        self.preview_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #E2E8F0;
                border-radius: 6px;
                gridline-color: #E2E8F0;
                font-size: 12px;
            }
            QHeaderView::section {
                background-color: #F8FAFC;
                color: #4A5568;
                font-weight: 600;
                padding: 10px;
                border: none;
                border-right: 1px solid #E2E8F0;
            }
            QTableWidget::item {
                padding: 8px;
                color: #2D3748;
            }
        """)
        self.preview_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.preview_table.verticalHeader().setVisible(False)
        preview_layout.addWidget(self.preview_table)
        
        self.preview_info = QLabel("")
        self.preview_info.setStyleSheet("color: #718096; font-size: 12px;")
        preview_layout.addWidget(self.preview_info)
        
        self.preview_group.setLayout(preview_layout)
        layout.addWidget(self.preview_group)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #E2E8F0;
                border-radius: 6px;
                background-color: white;
                text-align: center;
                height: 30px;
            }
            QProgressBar::chunk {
                background-color: #4A90E2;
                border-radius: 5px;
            }
        """)
        layout.addWidget(self.progress_bar)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        self.cancel_btn = ModernButton("Cancel", "secondary", width=120)
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.cancel_btn)
        
        self.import_btn = ModernButton("Import Data", "primary", width=140)
        self.import_btn.clicked.connect(self.importData)
        self.import_btn.setEnabled(False)
        btn_layout.addWidget(self.import_btn)
        
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
    def selectCSVFile(self):
        """Open file dialog to select CSV file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select CSV File",
            "",
            "CSV Files (*.csv);;All Files (*)"
        )
        
        if file_path:
            self.file_path = file_path
            self.file_label.setText(f"Selected: {os.path.basename(file_path)}")
            self.loadCSVPreview(file_path)
    
    def loadCSVPreview(self, file_path):
        """Load and preview CSV data"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                # Try different delimiters
                sample = file.read(1024)
                file.seek(0)
                
                if ',' in sample:
                    delimiter = ','
                elif ';' in sample:
                    delimiter = ';'
                elif '\t' in sample:
                    delimiter = '\t'
                else:
                    delimiter = ','
                
                reader = csv.DictReader(file, delimiter=delimiter)
                self.csv_data = list(reader)
                
                if not self.csv_data:
                    QMessageBox.warning(self, "Empty File", "The CSV file is empty.")
                    return
                
                # Display preview
                headers = reader.fieldnames
                self.preview_table.setColumnCount(len(headers))
                self.preview_table.setHorizontalHeaderLabels(headers)
                self.preview_table.setRowCount(min(10, len(self.csv_data)))
                
                for i, row in enumerate(self.csv_data[:10]):
                    for j, header in enumerate(headers):
                        item = QTableWidgetItem(str(row.get(header, '')))
                        self.preview_table.setItem(i, j, item)
                
                # Auto-resize columns
                self.preview_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
                
                # Update info
                self.preview_info.setText(f"Preview showing first 10 of {len(self.csv_data)} rows")
                self.preview_group.setVisible(True)
                self.import_btn.setEnabled(True)
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to read CSV file:\n{str(e)}")
    
    def importData(self):
        """Import CSV data to database"""
        if not hasattr(self, 'csv_data') or not self.csv_data:
            QMessageBox.warning(self, "No Data", "No data to import.")
            return
        
        # Check required columns
        required_columns = ['productBarCode', 'name', 'price']
        first_row = self.csv_data[0]
        missing_columns = [col for col in required_columns if col not in first_row]
        
        if missing_columns:
            QMessageBox.warning(
                self,
                "Missing Columns",
                f"CSV file is missing required columns: {', '.join(missing_columns)}"
            )
            return
        
        # Show progress bar
        self.progress_bar.setVisible(True)
        self.progress_bar.setMaximum(len(self.csv_data))
        
        # Import data
        db = DbClient()
        success_count = 0
        error_rows = []
        
        for i, row in enumerate(self.csv_data):
            try:
                # Prepare product data
                product_data = {
                    "productBarCode": str(row['productBarCode']),
                    "name": row['name'],
                    "price": float(row['price']),
                    "pdtType": row.get('pdtType', '')
                }
                
                # Insert into database
                result = db.addProductData(product_data)
                if result["status"] == "Success":
                    success_count += 1
                else:
                    error_rows.append(i + 1)
                
            except (ValueError, KeyError) as e:
                error_rows.append(i + 1)
            except Exception as e:
                error_rows.append(i + 1)
            
            # Update progress
            self.progress_bar.setValue(i + 1)
        
        # Hide progress bar
        self.progress_bar.setVisible(False)
        
        # Show results
        if error_rows:
            result_msg = (
                f"Import completed with some errors:\n\n"
                f"✅ Successfully imported: {success_count} products\n"
                f"❌ Failed to import: {len(error_rows)} rows\n"
                f"Failed rows: {', '.join(map(str, error_rows[:10]))}"
                f"{'...' if len(error_rows) > 10 else ''}"
            )
            QMessageBox.warning(self, "Import Results", result_msg)
        else:
            result_msg = f"✅ Successfully imported {success_count} products!"
            QMessageBox.information(self, "Import Successful", result_msg)
            self.accept()