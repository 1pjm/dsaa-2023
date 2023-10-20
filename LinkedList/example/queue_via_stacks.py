# 문제: 두 개의 스택을 사용하여 큐를 구현하세요. 이 큐는 기본적인 enqueue, dequeue, peek 연산을 지원해야 합니다.

class QueueViaStacks:
    def __init__(self):
        self.stack1 = []
        self.stack2 = []

    def enqueue(self, val):
        self.stack1.append(val)

    def dequeue(self):
        if not self.stack2:
            while self.stack1:
                self.stack2.append(self.stack1.pop())
        return self.stack2.pop() if self.stack2 else None

    def peek(self):
        if not self.stack2:
            while self.stack1:
                self.stack2.append(self.stack1.pop())
        return self.stack2[-1] if self.stack2 else None

# 두 개의 스택을 사용하여 큐 연산을 구현합니다. enqueue는 첫 번째 스택에 푸시하고, dequeue는 두 번째 스택에서 팝합니다.