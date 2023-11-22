import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel

class BracketCheckerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # UI 구성 요소 생성
        self.input_expr_label = QLabel("수식 입력:", self)
        self.input_expr = QTextEdit(self)
        self.check_button = QPushButton("검사하기", self)
        self.output_label = QLabel("결과:", self)
        self.output_area = QTextEdit(self)
        self.output_area.setReadOnly(True)

        # 버튼에 기능 연결
        self.check_button.clicked.connect(self.check_brackets)

        # 레이아웃 설정
        layout = QVBoxLayout()
        layout.addWidget(self.input_expr_label)
        layout.addWidget(self.input_expr)
        layout.addWidget(self.check_button)
        layout.addWidget(self.output_label)
        layout.addWidget(self.output_area)

        self.setLayout(layout)

        # 기본 창 설정
        self.setWindowTitle('괄호 검사기')
        self.setGeometry(300, 300, 400, 300)

    def check_brackets(self):
        expr = self.input_expr.toPlainText()

        if not expr.strip():  # 입력받은 문자열이 비어있는 경우
            self.output_area.setPlainText("Empty expression provided.")
            return

        checker = BracketChecker()
        messages, is_valid = checker.check_brackets(expr)

        print("\n" + "-" * 50 + "\n")

        # 파이썬 콘솔에 상세 결과 출력
        for message in messages:
            print(message)

        # '괄호 검사기' 창에 간단한 결과 표시
        if is_valid:
            self.output_area.setPlainText("Valid expression.")
        else:
            self.output_area.setPlainText("Invalid expression.")


class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def __repr__(self):
        return " -> ".join([str(item) for item in self.items])


class BracketChecker:
    def __init__(self):
        self.stack = Stack()

    def is_matching_pair(self, open_bracket, close_bracket):
        return (open_bracket == "(" and close_bracket == ")") or \
            (open_bracket == "{" and close_bracket == "}") or \
            (open_bracket == "[" and close_bracket == "]")

    def check_brackets(self, expression):
        self.stack = Stack()  # 스택 초기화
        result_messages = []

        for char in expression:
            if char in ["(", "{", "["]:
                self.stack.push(char)
                result_messages.append(f"입력값: {char} \nstack 상태: {self.stack}")

            elif char in [")", "}", "]"]:
                result_messages.append(f"입력값: {char}")

                if self.stack.is_empty() or not self.is_matching_pair(self.stack.peek(), char):
                    result_messages[-1] += f" \nstack 상태: {self.stack}    # 오류: 짝이 맞지 않는 '{char}'가 있습니다."
                    return result_messages, False
                else:
                    self.stack.pop()
                    result_messages[-1] += f" \nstack 상태: {self.stack}"

        return result_messages, self.stack.is_empty()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BracketCheckerApp()
    ex.show()
    sys.exit(app.exec_())
