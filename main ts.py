import sys
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QGridLayout, QLabel, QLineEdit, 
                             QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QCheckBox, QHeaderView)
from PyQt6.QtCore import Qt
from PyQt6.QtCharts import QChart, QChartView, QPieSeries
from PyQt6.QtGui import QColor, QPainter, QBrush

class FixedCalc(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ипотечный калькулятор MVP")
        
        self.resize(650, 600)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        main_layout = QVBoxLayout(main_widget)

        top_layout = QHBoxLayout()
        main_layout.addLayout(top_layout)

        inputs_widget = QWidget()
        grid = QGridLayout(inputs_widget)
        grid.setHorizontalSpacing(10)
        grid.setColumnStretch(2, 1)
        top_layout.addWidget(inputs_widget)

        grid.addWidget(QLabel("Сумма кредита:"), 0, 0)
        self.txt_sum = QLineEdit("3 000 000")
        self.txt_sum.setFixedWidth(250)
        grid.addWidget(self.txt_sum, 0, 1)

        grid.addWidget(QLabel("Срок кредита (лет):"), 1, 0)
        self.txt_term = QLineEdit("10")
        self.txt_term.setFixedWidth(250)
        grid.addWidget(self.txt_term, 1, 1)

        grid.addWidget(QLabel("Процентная ставка (%):"), 2, 0)
        self.txt_rate = QLineEdit("12")
        self.txt_rate.setFixedWidth(250)
        grid.addWidget(self.txt_rate, 2, 1)

        grid.addWidget(QLabel("Тип платежа:"), 3, 0)
        self.combo_type = QComboBox()
        self.combo_type.addItems(["Аннуитетный", "Дифференцированный"])
        self.combo_type.setFixedWidth(250)
        grid.addWidget(self.combo_type, 3, 1)

        grid.addWidget(QLabel("Дата получения:"), 4, 0)
        self.txt_date = QLineEdit("01.06.2026")
        self.txt_date.setFixedWidth(250)
        grid.addWidget(self.txt_date, 4, 1)

        self.check_inflation = QCheckBox("Учитывать инфляцию")
        grid.addWidget(self.check_inflation, 5, 0)
        
        self.txt_inflation_percent = QLineEdit("4.0")
        self.txt_inflation_percent.setFixedWidth(250)
        grid.addWidget(self.txt_inflation_percent, 5, 1)

        self.txt_sum.textChanged.connect(lambda: self.format_number_input(self.txt_sum))

        #кнокпи ебать
        self.btn_calc = QPushButton("Рассчитать")
        self.btn_calc.clicked.connect(self.calculate)
        grid.addWidget(self.btn_calc, 6, 0, 1, 2)

        self.btn_clear = QPushButton("Очистить")
        self.btn_clear.clicked.connect(self.clear_all)
        grid.addWidget(self.btn_clear, 7, 0, 1, 2)

        self.lbl_res = QLabel("Результаты расчета будут здесь")
        grid.addWidget(self.lbl_res, 8, 0, 1, 2)

        # даиграма
        self.chart = QChart()
        self.chart.setTitle("Соотношение выплат")
        self.chart.setBackgroundBrush(QBrush(QColor("#000000")))
        self.chart.setTitleBrush(QBrush(QColor("#FFFFFF")))

        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.chart_view.setBackgroundBrush(QBrush(QColor("#000000")))
        self.chart_view.setFixedSize(300, 250) 
        top_layout.addWidget(self.chart_view)

        # бля таблицп
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Месяц", "Платеж", "Проценты", "Остаток долга"])
        
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setTabKeyNavigation(False)
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        
        main_layout.addWidget(self.table)
    #функция про разделение чисел
    def format_number_input(self, line_edit):
        line_edit.blockSignals(True)
        cursor_pos = line_edit.cursorPosition()
        orig_text = line_edit.text()
        
        clean_text = orig_text.replace(" ", "")
        if clean_text.isdigit():
            formatted = f"{int(clean_text):,}".replace(",", " ")
            line_edit.setText(formatted)
            
            spaces_before = orig_text[:cursor_pos].count(" ")
            spaces_after = formatted[:cursor_pos].count(" ")
            line_edit.setCursorPosition(cursor_pos + (spaces_after - spaces_before))
            
        line_edit.blockSignals(False)