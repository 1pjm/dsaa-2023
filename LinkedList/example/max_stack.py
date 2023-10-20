'''
문제: 기본적인 push, pop, top 연산을 지원하는 스택을 구현하되, getMax() 함수를 추가로 제공하여 현재 스택에서의 최대 값을 O(1)의 시간 복잡도로 반환하게 하세요.
'''

class MaxStack:
    def __init__(self):
        self.stack = []
        self.max_stack = []

    def push(self, val):
        self.stack.append(val)
        if not self.max_stack or val > self.max_stack[-1]:
            self.max_stack.append(val)
        else:
            self.max_stack.append(self.max_stack[-1])

    def pop(self):
        if self.stack:
            self.max_stack.pop()
            return self.stack.pop()

    def top(self):
        return self.stack[-1] if self.stack else None

    def getMax(self):
        return self.max_stack[-1] if self.max_stack else None

# 주 스택과 보조 스택 (최대값을 저장하는 스택) 두 개를 사용합니다. 항목을 푸시할 때마다 현재 최대값과 함께 보조 스택에 푸시합니다.