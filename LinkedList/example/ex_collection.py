'''
연결 리스트, 스택, 큐의 개념을 이용하여 여러 문제를 만들어 볼 수 있습니다:

2. **응용 문제**:
    - 주어진 연결 리스트가 회문(palindrome)인지 판별하는 함수를 작성하십시오. (힌트: 스택 사용)
    - 주어진 문자열에서 중복된 괄호 (`((..))`)나 괄호 불일치(`(]`) 같은 오류를 찾아내는 함수를 작성하십시오. (힌트: 스택 사용)
    - 주어진 연결 리스트를 두 개의 큐를 사용하여 짝수와 홀수로 분리하는 함수를 작성하십시오.

3. **심화 문제**:
    - 주어진 연결 리스트에서 중간 노드를 찾는 함수를 작성하십시오. (힌트: 두 개의 포인터 사용, 하나는 한 번에 한 칸, 다른 하나는 두 칸씩 이동)
    - 주어진 연결 리스트를 스택을 사용하여 역순으로 출력하는 함수를 작성하십시오.
    - 주어진 문자열에서 가장 긴 괄호로 묶인 유효한 부분 문자열의 길이를 반환하는 함수를 작성하십시오. 예: `input: "(()", output: 2`
'''


#! 1. 주어진 연결 리스트가 회문(palindrome)인지 판별하는 함수

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

def is_palindrome(head):
    if not head:
        return True
    
    # 스택을 사용하여 연결 리스트의 값을 복사
    stack = []
    temp = head
    while temp:
        stack.append(temp.value)
        temp = temp.next
    
    # 연결 리스트를 다시 순회하며 스택과 값을 비교
    temp = head
    while temp:
        if temp.value != stack.pop():
            return False
        temp = temp.next
        
    return True


#! 2. 주어진 문자열에서 중복된 괄호 (`((..))`)나 괄호 불일치(`(]`) 같은 오류를 찾아내는 함수

def check_parentheses(s):
    stack = []
    for char in s:
        if char in "([{":
            stack.append(char)
        elif char in ")]}":
            if not stack:
                return False
            if char == ')' and stack[-1] != '(':
                return False
            if char == ']' and stack[-1] != '[':
                return False
            if char == '}' and stack[-1] != '{':
                return False
            stack.pop()
    return not stack  # 스택이 비어있으면 모든 괄호가 일치


#! 3. 주어진 연결 리스트에서 중간 노드를 찾는 함수

def find_middle_node(head):
    slow_pointer = head
    fast_pointer = head
    
    while fast_pointer and fast_pointer.next:
        slow_pointer = slow_pointer.next
        fast_pointer = fast_pointer.next.next
        
    return slow_pointer.value if slow_pointer else None


#! 4. 주어진 연결 리스트를 스택을 사용하여 역순으로 출력하는 함수

def print_reverse(head):
    stack = []
    temp = head
    while temp:
        stack.append(temp.value)
        temp = temp.next
        
    while stack:
        print(stack.pop())


#! 5. 주어진 문자열에서 가장 긴 괄호로 묶인 유효한 부분 문자열의 길이를 반환하는 함수

def longest_valid_parentheses(s):
    stack = []
    left, max_len = 0, 0
    for i in range(len(s)):
        if s[i] == '(':
            left += 1
        else:
            left -= 1
        if left == 0:
            max_len = max(max_len, i+1)
        elif left < 0:
            left = 0
            stack = []

    left, right = 0, 0
    for i in range(len(s) - 1, -1, -1):
        if s[i] == '(':
            left += 1
        else:
            left -= 1
        if left == 0:
            max_len = max(max_len, i+1)
        elif left > 0:
            left = 0
            stack = []

    return max_len
