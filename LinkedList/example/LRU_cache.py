'''
LRU Cache (Least Recently Used)

문제: LRU 캐시를 구현하세요. 이 캐시는 정해진 용량이 있으며, 새로운 항목을 추가할 때 용량이 초과되면 가장 최근에 사용되지 않은 항목을 제거해야 합니다. 이 문제는 해시 테이블과 이중 연결 리스트를 함께 사용하여 
O(1)의 시간 복잡도로 구현할 수 있습니다.
'''

class LRUNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.head = LRUNode(0, 0)
        self.tail = LRUNode(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        prev, nxt = node.prev, node.next
        prev.next, nxt.prev = nxt, prev

    def _add(self, node):
        prev, nxt = self.tail.prev, self.tail
        prev.next, node.prev = node, prev
        node.next, nxt.prev = nxt, node

    def get(self, key):
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._add(node)
            return node.value
        return -1

    def put(self, key, value):
        if key in self.cache:
            self._remove(self.cache[key])
        node = LRUNode(key, value)
        self._add(node)
        self.cache[key] = node
        if len(self.cache) > self.capacity:
            n = self.head.next
            self._remove(n)
            del self.cache[n.key]

# 이중 연결 리스트와 해시 테이블을 함께 사용하여 O(1)의 시간 복잡도로 LRU 캐시를 구현합니다. 

# 이중 연결 리스트는 캐시된 항목의 순서를 추적하며, 해시 테이블은 빠른 항목 검색을 위해 사용됩니다.