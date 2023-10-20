'''
Rotated Sorted Linked List Search

문제: 회전된 정렬된 연결 리스트에서 주어진 값 x를 찾는 함수를 작성하세요. 예를 들어, 연결 리스트 4->5->6->1->2->3 에서 값 2는 찾을 수 있어야 합니다.

제약 조건: 
O(log n)의 시간 복잡도로 문제를 해결하세요.
'''

class ListNode:
    def __init__(self, value=0, next=None):
        self.value = value
        self.next = next

def search_rotated_linked_list(head, target):
    # Find the minimum element of the list
    min_node = head
    while head and head.next and head.value < head.next.value:
        head = head.next
    if head and head.next:
        min_node = head.next

    # Binary search
    start, end = min_node, None
    while start != end:
        mid = get_middle(start, end)
        if mid.value == target:
            return True
        elif mid.value < target:
            start = mid.next
        else:
            end = mid
    return False

def get_middle(start, end):
    fast, slow = start, start
    while fast != end and fast.next != end:
        fast = fast.next.next
        slow = slow.next
    return slow

# 이진 탐색을 사용하여 회전된 연결 리스트에서 값을 찾을 수 있습니다.

# 먼저 최소값의 위치를 찾은 다음, 해당 위치를 기준으로 이진 탐색을 수행합니다.