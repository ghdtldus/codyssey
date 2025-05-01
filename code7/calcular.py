import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QGridLayout, QLineEdit
from PyQt5.QtCore import Qt
from decimal import Decimal, ROUND_HALF_UP

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("계산기")
        self.setFixedSize(370, 540)
        self.initUI()

    def initUI(self):
        # 결과창
        self.result = QLineEdit('0')
        self.result.setAlignment(Qt.AlignRight)
        self.result.setReadOnly(True)
        self.result.setStyleSheet("font-size: 40px; padding: 20px; border: none; background-color: black; color: white;")

        # 전체 레이아웃
        vbox = QVBoxLayout()
        vbox.addWidget(self.result)

        # 버튼 그리드 레이아웃
        grid = QGridLayout()
        grid.setSpacing(0)  # 버튼 간 여백 최소화

        buttons = [
            ['AC', '+/-', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=']
        ]

        for row, line in enumerate(buttons):
            for col, btn_text in enumerate(line):
                btn = QPushButton(btn_text)
                
                # 0버튼은 넓게 설정
                if btn_text == '0':
                    btn.setFixedSize(180, 88)
                    btn.setStyleSheet(
                        "font-size: 24px; text-align: left; padding-left: 26px; "
                        "border-radius: 44px; margin: 2px; background-color: #333333; color: white;"
                    )
                    grid.addWidget(btn, row + 1, 0, 1, 2)
                    btn.clicked.connect(self.on_button_click)
                    continue

                # 공통 스타일
                btn.setFixedSize(88, 88)
                base_style = "font-size: 24px; border-radius: 44px; margin: 2px;"

                # 색상 분기
                if btn_text in ['AC', '+/-', '%']:
                    btn.setStyleSheet(base_style + "background-color: #A5A5A5; color: black;")
                elif btn_text in ['÷', '×', '-', '+', '=']:
                    btn.setStyleSheet(base_style + "background-color: #FF9500; color: white;")
                else:
                    btn.setStyleSheet(base_style + "background-color: #333333; color: white;")

                btn.clicked.connect(self.on_button_click)

                if btn_text == '.' and len(line) == 3:
                    grid.addWidget(btn, row + 1, 2)
                elif btn_text == '=' and len(line) == 3:
                    grid.addWidget(btn, row + 1, 3)
                else:
                    grid.addWidget(btn, row + 1, col)

        vbox.addLayout(grid)
        self.setLayout(vbox)
        self.setStyleSheet("background-color: black;")

    def on_button_click(self):
        text = self.sender().text()

        if text == 'AC':
            self.reset()
        elif text == '+/-':
            self.negative_positive()
        elif text == '%':
            self.percent()
        elif text == '=':
            self.equal()
        elif text in ['+', '-', '×', '÷']:
            self.append_operator(text)
        elif text == '.':
            self.append_dot()
        else:
            self.append_number(text)    

    def reset(self):
        self.adjust_font_size("0")  
        self.result.setText('0')

    def negative_positive(self):
        current = self.result.text()
        for op in ['+', '-', '×', '÷']:
            if op in current[1:]:
                parts = current.rsplit(op, 1)
                num = parts[1]
                if num.startswith('-'):
                    num = num[1:]
                else:
                    num = '-' + num
                self.result.setText(parts[0] + op + num)
                return
        if current.startswith('-'):
            self.result.setText(current[1:])
        else:
            self.result.setText('-' + current)

    def percent(self):
        try:
            expression = self.result.text().replace('×', '*').replace('÷', '/')
            value = eval(expression)
            self.result.setText(str(value / 100))
        except:
            self.result.setText('Error')

    def append_operator(self, op):
        current = self.result.text()
        if current[-1] in '+-×÷':
            self.result.setText(current[:-1] + op)
        else:
            self.result.setText(current + op)

    def append_dot(self):
        current = self.result.text()
        if current[-1] in '+-×÷':
            self.result.setText(current + '0.')
            return

        parts = current.rsplit('+', 1)
        for op in ['+', '-', '×', '÷']:
            if op in current:
                parts = current.rsplit(op, 1)
                if '.' not in parts[1]:
                    self.result.setText(current + '.')
                return
        if '.' not in current:
            self.result.setText(current + '.')

    def append_number(self, num):
        current = self.result.text()
        if current == '0':
            self.result.setText(num)
        else:
            self.result.setText(current + num)

    def equal(self):
        try:
            expression = self.result.text().replace('×', '*').replace('÷', '/')
            result = eval(expression)

            if isinstance(result, float):
                result_str_raw = str(result)
                if '.' in result_str_raw:
                    fractional_part = result_str_raw.split('.')[1]
                    if len(fractional_part) <= 6:
                        # 6자리 이하일 경우 → 반올림
                        rounded = Decimal(str(result)).quantize(Decimal('0.000001'), rounding=ROUND_HALF_UP)
                        result_str = format(rounded.normalize(), 'f')
                    else:
                        # 6자리 초과일 경우 → 그대로 출력
                        result_str = result_str_raw
                else:
                    result_str = result_str_raw
            else:
                result_str = str(result)

            self.adjust_font_size(result_str)
            self.result.setText(result_str)

        except ZeroDivisionError:
            message = "Cannot divide by 0"
            self.adjust_font_size(message)
            self.result.setText(message)
        except:
            message = "Error"
            self.adjust_font_size(message)
            self.result.setText(message)
                    

    def adjust_font_size(self, text):
        length = len(text)
        if length <= 9:
            font_size = 40
        elif length <= 13:
            font_size = 30
        elif length <= 18:
            font_size = 24
        else:
            font_size = 18  # 

        self.result.setStyleSheet(
            f"font-size: {font_size}px; padding: 20px; border: none; background-color: black; color: white;"
        )



    # 사칙연산 메소드
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ZeroDivisionError
        return a / b
    
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())
