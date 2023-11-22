import sys
# Python 표준 라이브러리, 시스템 관련 정보 및 함수에 접근할 때 사용
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel
# PyQt5 라이브러리에서 GUI 구성 요소 제공 모듈 
# 해당 클래스들을 가져옴

class BracketCheckerApp(QWidget):
# QWidget 클래스를 상속받아 만들어짐, BracketCheckerApp은 GUI 창을 나타내는 클래스
    def __init__(self): # BracketCheckerApp 객체 생성 시 자동 호출
        super().__init__()
        # 부모 클래스인 QWidget의 생성자 호출, 기본적인 윈도우 설정 초기화
        self.init_ui()
        # GUI 구성 요소 생성 및 배치

    def init_ui(self):
        # UI 구성 요소 생성
        self.input_expr_label = QLabel("수식 입력:", self)
        # 텍스트 레이블
        self.input_expr = QTextEdit(self) # 텍스트 입력 영역, 수식을 입력
        self.check_button = QPushButton("검사하기", self)
        self.output_label = QLabel("결과:", self)
        # 텍스트 레이블
        self.output_area = QTextEdit(self) # 텍스트 출력 영역, 결과 확인
        self.output_area.setReadOnly(True)  # 결과 출력 영역은 읽기 전용으로 설정

        # 버튼에 기능 연결
        self.check_button.clicked.connect(self.check_brackets)
        # clicked.connect() 메서드 사용해 check_button에 클릭 이벤트 연결, 버튼 클릭 시 self.check_brackets 실행

        # 레이아웃 설정
        layout = QVBoxLayout() # 수직 레이아웃 생성
        layout.addWidget(self.input_expr_label)
        layout.addWidget(self.input_expr)
        layout.addWidget(self.check_button)
        layout.addWidget(self.output_label)
        layout.addWidget(self.output_area)

        self.setLayout(layout)
        # 앞서 구성한 레이아웃을 현재 윈도우에 적용

        # 기본 창 설정
        self.setWindowTitle('괄호 검사기') # 윈도우 제목 설정
        self.setGeometry(300, 300, 400, 300) # 윈도우 위치, 크기 설정
    '''
    init_ui 메서드는 BracketCheckerApp 클래스의 GUI를 구성합니다. 이 메서드는 레이블, 텍스트 필드, 버튼 등의 위젯을 생성하고, 이들을 레이아웃에 배치하여 사용자에게 깔끔하고 직관적인 인터페이스를 제공합니다.
    '''


    def check_brackets(self):
    # BracketCheckerApp 클래스의 check_brackets 메서드 구현 부분, 사용자가 입력한 수식의 괄호가 올바르게 닫혔는지 검사
        expr = self.input_expr.toPlainText()
        # self.input_expr.toPlainText()를 통해 사용자가 입력한 텍스트 읽어옴
        # self.input_expr는 사용자가 수식을 입력하는 QTextEdit 위젯

        if not expr.strip():  # 입력받은 문자열이 비어있는 경우
        # strip(): 입력된 문자열의 앞뒤 공백을 제거
            self.output_area.setPlainText("Empty expression provided.") # self.output_area에 메시지 표시 후
            return # 메서드 종료 후 호출한 곳으로 돌아감
            # QPushButton의 클릭 이벤트에 의해 호출됨

        checker = BracketChecker() # BracketChecker() 클래스의 인스턴스 생성
        messages, is_valid = checker.check_brackets(expr)
        # checker.check_brackets(expr) 메서드 호출해 사용자 입력에 대한 괄호 검사 수행, 이 메서드는 messages, is_valid를 반환함
        # messages: 괄호 검사 과정에서 발생한 모든 메시지 리스트
        # is_valid: 괄호가 올바르게 닫혔는지를 나타내는 불리언 값

        print("\n" + "-" * 50 + "\n")

        # 파이썬 콘솔에 상세 결과 출력
        for message in messages:
        # for 루프를 사용해 messages 리스트의 모든 메시지를
            print(message) # 콘솔에 출력


        # '괄호 검사기' 창에는 간단한 결과만 표시
        if is_valid: # 괄호가 올바르게 닫혔으면
            self.output_area.setPlainText("Valid expression.")
        else: # 아니면
            self.output_area.setPlainText("Invalid expression.")
    '''
    check_brackets 메서드는 사용자의 입력을 받아 괄호가 올바르게 닫혔는지 검사하는 기능을 수행합니다. 검사 결과는 파이썬 콘솔에 상세하게, 그리고 GUI 창에는 간략하게 표시됩니다. 이 메서드는 사용자의 입력을 처리하고, BracketChecker 클래스를 사용하여 괄호 검사를 수행한 뒤, 결과를 적절하게 사용자에게 제공하는 역할을 합니다.
    '''


class Stack: # 스택 자료구조(스택의 기본 연산, LIFO) 구현하는 클래스
    def __init__(self): # 생성자 메서드, 스택 초기화 시 호출
        self.items = [] # 스택에 저장될 요소들을 담는 리스트, 초기에는 비어있음

    def push(self, item): # 스택에 새로운 요소 추가하는 메서드, O(1)
        self.items.append(item)
        # 스택의 맨 위에 항목을 추가한다. (리스트의 끝에 item을 추가)

    def pop(self): # 스택 맨 위의 요소를 제거하고 반환하는 메서드, O(1)
        if not self.is_empty(): # 스택이 비어있지 않으면
            return self.items.pop() # pop 메서드로 맨 위의 요소 제거하고 반환
        return None # 스택이 비어있다면 None 반환

    def peek(self): # 스택 맨 위의 요소를 반환하는 메서드 (제거 X)
        if not self.is_empty(): # 스택이 비어있지 않으면
            return self.items[-1] # items 리스트의 마지막 요소 반환
        return None # 스택이 비어있다면 None 반환

    def is_empty(self): # 스택이 비어있는지 여부 확인하는 메서드(불리언), O(1)
        return len(self.items) == 0
        # self.items의 길이가 0이면 True, 아니면 False 반환

    def size(self): # 스택에 저장된 요소의 수를 반환하는 메서드, O(1)
        return len(self.items) # self.items의 길이 반환

    def __repr__(self): # 스택의 요소들을 문자열로 나타내기 위한 메서드
        return " -> ".join([str(item) for item in self.items])
        # [str(item) for item in self.items]
        # : self.items 리스트의 각 요소를 문자열로 변환하여 새로운 리스트 생성 (ex: [1, 2, 3]일 경우 ['1', '2', '3'] 생성)
        # join을 사용해 -> 문자열로 연결
'''
Stack 클래스는 스택 자료구조의 표준 연산들을 구현합니다. 이 클래스를 통해 요소를 스택에 추가하고, 제거하고, 확인할 수 있으며, 스택이 비어 있는지와 스택의 크기를 확인할 수 있습니다. 이러한 기능은 괄호 검사기와 같은 알고리즘에서 유용하게 사용됩니다.
'''


class BracketChecker:
# 괄호의 짝이 올바르게 맞는지 검사하는 클래스
    def __init__(self):
        self.stack = Stack() # Stack 클래스의 인스턴스 생성

    def is_matching_pair(self, open_bracket, close_bracket):
    # 두 괄호 문자가 올바른 짝인지 확인하는 메서드 (불리언)
        return (open_bracket == "(" and close_bracket == ")") or \
            (open_bracket == "{" and close_bracket == "}") or \
            (open_bracket == "[" and close_bracket == "]")
        # 이 중 하나라도 참이면(두 괄호가 올바른 짝이면) True 반환, 아니면 False 반환

    def check_brackets(self, expression):
    # 입력된 수식의 괄호가 올바르게 짝지어져 있는지 확인하는 메서드
    # expression: 주어진 수식을 문자열 형태로 나타내는 매개변수
        self.stack = Stack()  # 스택 초기화
        result_messages = [] # 결과 메시지 저장할 빈 리스트 생성

        for char in expression: 
        # 입력된 수식 문자열(expression)들을 순회
            if char in ["(", "{", "["]: # 입력 문자가 여는 괄호인 경우
                self.stack.push(char) # 스택에 괄호를 푸시
                result_messages.append(f"입력값: {char} \nstack 상태: {self.stack}")
                # 입력값과 스택 상태를 결과 메시지에 추가

            elif char in [")", "}", "]"]:
            # 입력 문자가 닫는 괄호인 경우
                result_messages.append(f"입력값: {char}")
                # 입력값을 결과 메시지에 추가

                if self.stack.is_empty() or not self.is_matching_pair(self.stack.peek(), char):
                # 스택이 비어있거나, 스택 최상위 값이 현재 닫는 괄호와 짝이 안맞는 경우
                    result_messages[-1] += f" \nstack 상태: {self.stack}    # 오류: 짝이 맞지 않는 '{char}'가 있습니다."
                    return result_messages, False
                    # result_messages의 마지막 요소(가장 최근에 추가된 메시지, 즉 현재 처리 중인 괄호에 대한 메시지)에 스택 상태와 현재 처리 중인 닫힌 괄호에 대한 메시지 추가
                    # 결과 메시지와 False 반환 (함수 종료)
                else: # 스택 최상위 값이 현재 닫는 괄호와 짝이 맞는 경우
                    self.stack.pop() # 스택에서 최상위 항목 pop
                    result_messages[-1] += f" \nstack 상태: {self.stack}"

        return result_messages, self.stack.is_empty()
        # 모든 문자를 순회한 뒤 결과 메시지와 스택이 비어 있는지 여부 반환(True or False)
        # check_brackets 메서드가 처리한 결과를 다른 메서드에서 사용하기 위해 return 사용 (BracketChecker 클래스에서 괄호 검사의 결과를 BracketCheckerApp 클래스로 전달하는 데 사용)

# 코드 실행 시 시작점
if __name__ == '__main__': # 스크립트가 직접 실행될 때만 내부 코드 실행, 모듈로 임포트 시 실행 X
    app = QApplication(sys.argv)
    # QApplication: PyQt의 GUI 애플리케이션을 시작하기 위해 필요한 객체
    # sys.argv: 커맨드 라인 인자를 QApplication에 전달해 애플리케이션을 더 유연하게 사용할 수 있게 함
    ex = BracketCheckerApp() # BracketCheckerApp 클래스의 인스턴스 생성
    ex.show() # BracketCheckerApp 윈도우를 화면에 표시
    sys.exit(app.exec_())
    # app.exec_(): 애플리케이션의 메인 이벤트 루프 시작
    # sys.exit(): 애플리케이션 종료 시 반환된 상태 코드를 반환해 프로그램 종료
