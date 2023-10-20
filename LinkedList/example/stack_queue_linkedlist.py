'''
다음 조건에 따라 연결 리스트를 사용하여 스택 및 큐를 지원하는 자료 구조를 구현하십시오:

1. push(value): 값을 리스트의 끝에 추가합니다.
2. pop(): 리스트의 마지막 요소를 제거하고 반환합니다.
3. pop(0): 리스트의 첫 번째 요소를 제거하고 반환합니다.

예시:
lst = LinkedList()
lst.push(1)
lst.push(2)
lst.push(3)
lst.push(4)
print(lst)  # 출력: [1, 2, 3, 4]
print(lst.pop())  # 출력: 4
print(lst)  # 출력: [1, 2, 3]
print(lst.pop(0))  # 출력: 1
print(lst)  # 출력: [2, 3]
'''


class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def push(self, value):
        new_node = Node(value)
        if not self.head:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1

    def pop(self, idx=0):
        if idx == 0:
            if not self.head:
                return None
            removed_value = self.head.value
            self.head = self.head.next
            if not self.head:
                self.tail = None
            self.size -= 1
            return removed_value
        elif idx == -1 or idx == self.size - 1:
            if not self.head:
                return None
            if self.size == 1:
                removed_value = self.head.value
                self.head = self.tail = None
            else:
                cur = self.head
                while cur.next and cur.next.next:
                    cur = cur.next
                removed_value = cur.next.value
                cur.next = None
                self.tail = cur
            self.size -= 1
            return removed_value
        else:
            raise ValueError("Only supports removing from the start (0) or end (-1)")

    def __str__(self):
        values = []
        cur = self.head
        while cur:
            values.append(cur.value)
            cur = cur.next
        return str(values)

# Driver Code
if __name__ == "__main__":
    lst = LinkedList()
    lst.push(1)
    lst.push(2)
    lst.push(3)
    lst.push(4)
    print(lst)  # [1, 2, 3, 4]
    print(lst.pop())  # 4
    print(lst)  # [1, 2, 3]
    print(lst.pop(0))  # 1
    print(lst)  # [2, 3]
