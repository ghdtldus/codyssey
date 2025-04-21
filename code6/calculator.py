import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QGridLayout, QLineEdit
from PyQt5.QtCore import Qt

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("iPhone 스타일 계산기")
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
        sender = self.sender()
        text = sender.text()
        current = self.result.text()

        if text == 'AC':
            self.result.setText('0')

        elif text == '+/-':
            # 마지막 숫자만 부호 변경
            for op in ['+', '-', '×', '÷']:
                if op in current[1:]:
                    parts = current.rsplit(op, 1)
                    if len(parts) == 2:
                        num = parts[1]
                        if num.startswith('-'):
                            num = num[1:]
                        else:
                            num = '-' + num
                        self.result.setText(parts[0] + op + num)
                        return
            # 전체 항에 대해 토글
            if current.startswith('-'):
                self.result.setText(current[1:])
            else:
                self.result.setText('-' + current)

        elif text == '=':
            try:
                expression = current.replace('×', '*').replace('÷', '/')
                result = str(eval(expression))
                self.result.setText(result)
            except:
                self.result.setText('Error')

        elif text in ['+', '-', '×', '÷']:
            if current[-1] in '+-×÷':
                self.result.setText(current[:-1] + text)
            else:
                self.result.setText(current + text)

        elif text == '%':
            try:
                value = eval(current.replace('×', '*').replace('÷', '/'))
                self.result.setText(str(value / 100))
            except:
                self.result.setText('Error')

        else:
            if current == '0' and text != '.':
                self.result.setText(text)
            else:
                self.result.setText(current + text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())
