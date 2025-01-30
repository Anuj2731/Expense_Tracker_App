from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QComboBox, QTableWidgetItem, QDateEdit, QTableWidget, QVBoxLayout, QHBoxLayout, QMessageBox, QTableWidget, QHeaderView
from PyQt6.QtCore import QDate, Qt
from database import fetch_expenses, add_expenses, delete_expenses

class ExpenseApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Expense Tracker App")
        self.initUI()
        self.load_table_data()

    def settings(self):
        self.geometry(300, 300, 550, 500)

    def initUI(self):
        self.date_box = QDateEdit()
        self.date_box.setDate(QDate.currentDate())
        self.dropdown = QComboBox()
        self.amount = QLineEdit()
        self.description = QLineEdit()

        self.btn_add = QPushButton("Add Expense")
        self.btn_delete = QPushButton("Delete Expense")
        
        self.table = QTableWidget(0,5)
        self.table.setHorizontalHeaderLabels(["ID", "Date", "Category", "Amount", "Description"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.populate_dropdown()

        self.btn_add.clicked.connect(self.add_expense)
        self.btn_add.setObjectName("btn_add")
        self.btn_delete.clicked.connect(self.delete_expense)
        self.btn_delete.setObjectName("btn_delete")

        self.apply_styles()
        self.setup_layout()

    def setup_layout(self):


        master = QVBoxLayout()
        row1 = QHBoxLayout()
        row2 = QHBoxLayout()
        row3 = QHBoxLayout()

        row1.addWidget(QLabel("Date"))
        row1.addWidget(self.date_box)
        row1.addWidget(QLabel("Category"))
        row1.addWidget(self.dropdown)

        row2.addWidget(QLabel("Amount"))
        row2.addWidget(self.amount)
        row2.addWidget(QLabel("Description"))
        row2.addWidget(self.description)

        row3.addWidget(self.btn_add)
        row3.addWidget(self.btn_delete)

        master.addLayout(row1)
        master.addLayout(row2)
        master.addLayout(row3)
        master.addWidget(self.table)

        self.setLayout(master)        

    def populate_dropdown(self):
        categories = ["Food", "Rent", "Bills", "Entertainment", "Shopping", "Other"]
        self.dropdown.addItems(categories)
    
    def apply_styles(self):
        self.setStyleSheet("""
            /* Base styling */
            QWidget {
                background-color: #f4f7fb;
                font-family: Arial, sans-serif;
                font-size: 14px;
                color: #2f3640;
            }

            /* Headings for labels */
            QLabel {
                font-size: 16px;
                color: #34495e;
                font-weight: bold;
                padding: 5px;
            }

            /* Styling for input fields */
            QLineEdit, QComboBox, QDateEdit {
                background-color: #ffffff;
                font-size: 14px;
                color: #2f3640;
                border: 1px solid #b0bfc6;
                border-radius: 5px;
                padding: 1px;
            }
            QLineEdit:hover, QComboBox:hover, QDateEdit:hover {
                border: 1px solid #1abc9c;
            }
            QLineEdit:focus, QComboBox:focus, QDateEdit:focus {
                border: 1px solid #2980b9;
                background-color: #ecf0f1;
            }

            /* Table styling */
            QTableWidget {
                background-color: #ffffff;
                alternate-background-color: #f8f9fa;
                gridline-color: #c0c9d0;
                selection-background-color: #3498db;
                selection-color: white;
                font-size: 14px;
                border: 1px solid #cfd9e1;
            }
            QHeaderView::section {
                background-color: #1abc9c;
                color: white;
                font-weight: bold;
                padding: 4px;
                border: 1px solid #dcdfe1;
            }

            /* Scroll bar styling */
            QScrollBar:vertical {
                width: 12px;
                background-color: #f7f7f7;
                border: none;
            }
            QScrollBar::handle:vertical {
                background-color: #1abc9c;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
            }

            /* Buttons */
            #btn_add {
                background-color: #3498db;
                color: white;
                padding: 10px 15px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
                transition: background-color 0.3s;
            }
            #btn_add:hover {
                background-color: #2980b9;
            }
            #btn_add:pressed {
                background-color: #2471a3;
            }
            #btn_add:disabled {
                background-color: #bdc3c7;
                color: #6e6e6e;
            }

            #btn_delete {
                background-color: #e74c3c;
                color: white;
                padding: 10px 15px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
                transition: background-color 0.3s;
            }
            #btn_delete:hover {
                background-color: #c0392b;
            }
            #btn_delete:pressed {
                background-color: #922b21;
            }
            #btn_delete:disabled {
                background-color: #bdc3c7;
                color: #6e6e6e;
            }
            /* Tooltip styling */
            QToolTip {
                background-color: #34495e;
                color: #ffffff;
                border: 1px solid #2c3e50;
                font-size: 12px;
                padding: 5px;
                border-radius: 4px;
            }
""")
        
    def load_table_data(self):
        expenses = fetch_expenses()
        self.table.setRowCount(0)
        for row_idx, expense in enumerate(expenses):
            self.table.insertRow(row_idx)
            for col_idx, data in enumerate(expense):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))

    def clear_inputs(self):
        self.date_box.setDate(QDate.currentDate())
        self.dropdown.setCurrentIndex(0)
        self.amount.clear()
        self.description.clear()

    def add_expense(self):
        date = self.date_box.date().toString("yyyy-MM-dd")
        category = self.dropdown.currentText()
        amount = self.amount.text()
        description = self.description.text()

        if not amount or not description:
            QMessageBox.warning(self, "Input Error","Amount and Description can not be empty")
            return
        
        if add_expenses(date, category, amount, description):
            self.load_table_data()
            self.clear_inputs()
        else:
            QMessageBox.critical(self, "Error", "Failed to add expense")

    def delete_expense(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self,"Oops", "You need to choose a row to delete")
            return
        expense_id = int(self.table.item(selected_row, 0).text())
        confirm = QMessageBox.question(self, "Confirm","Are you sure you want to delete?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if confirm == QMessageBox.StandardButton.Yes and delete_expenses(expense_id):
            self.load_table_data()