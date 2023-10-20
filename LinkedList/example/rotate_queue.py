'''
**문제: Doubly Linked List 기반의 Rotate Queue 구현**

아래는 Doubly Linked List를 기반으로 한 Rotate Queue의 초기 구조입니다. 이 구조는 큐의 마지막 요소를 맨 앞으로 회전시키는 `rotate()` 메서드를 지원해야 합니다. 해당 메서드의 구현을 완성하십시오.

- `Node` 클래스: value, next, prev 속성을 갖는다.
- `RotateQueue` 클래스: head, tail 속성을 갖고, 아래의 메서드들을 지원한다.

    1. `enqueue(value)`: 큐의 끝에 요소를 추가한다.
    2. `dequeue()`: 큐의 처음 요소를 제거하고 반환한다.
    3. `rotate()`: 큐의 마지막 요소를 맨 앞으로 회전시킨다.

이제 문제에 대한 해결 방법을 제시하는 코드를 작성하겠습니다.
'''


class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None

class RotateQueue:
    def __init__(self):
        self.head = None
        self.tail = None

    def enqueue(self, value):
        new_node = Node(value)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

    def dequeue(self):
        if not self.head:
            return None
        value = self.head.value
        self.head = self.head.next
        if self.head:
            self.head.prev = None
        else:
            self.tail = None
        return value

    def rotate(self):
        if not self.head or not self.tail or self.head == self.tail:
            return

        last_node = self.tail
        last_node.next = self.head
        self.head.prev = last_node
        self.head = last_node
        self.tail = last_node.prev
        self.tail.next = None

# Test
q = RotateQueue()
q.enqueue(1)
q.enqueue(2)
q.enqueue(3)
print(q.head.value)  # 1
print(q.tail.value)  # 3

q.rotate()
print(q.head.value)  # 3
print(q.tail.value)  # 2


# 이 코드는 주어진 단계에 따라 Doubly Linked List 기반의 Rotate Queue를 구현한 것입니다.