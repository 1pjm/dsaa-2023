'''
Palindrome Checker (이중 연결 리스트 활용)

문제: 주어진 문자열이 회문(palindrome)인지 확인하려고 합니다. 이를 위해 이중 연결 리스트를 사용하여 문자열을 저장하고, 양 끝에서 시작하여 중간까지 문자를 비교하여 회문을 확인하세요.

제약 조건: 추가 메모리를 사용하지 않고, 
O(n)의 시간 복잡도로 문제를 해결하세요.
'''

class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

def is_palindrome(head, tail):
    while head != tail and head.prev != tail:
        if head.data != tail.data:
            return False
        head = head.next
        tail = tail.prev
    return True

# 먼저, 문자열의 각 문자를 이중 연결 리스트의 노드로 변환합니다. 그런 다음, 앞과 뒤에서 두 포인터를 사용하여 중앙으로 이동하면서 문자를 비교합니다.