### 2주차

from typing import Any

class Node:
    """
    A class to represent a Node for an explanation of data structure.

    Attributes:
        data : Any
            data that user store on Node instance
        next : Node
            object connected to the next node in a linked list.
    """ # Docstring 작성

    def __init__(self, data : Any = None, next : 'Node' = None) -> None: # Type hint 작성
        """
        Args:
            data (Any, optional): data that user store on Node instance
            next (Node, optional): object connected to the next node in a linked list

        Returns:
            None
        """
        self._data = data
        self._next = None
        # 언더바 연산자를 넣으면 외부에서 접근 못함 (information hiding)

    # information hiding -> 접근
    @property # 데코레이터
    def data(self):
        return self._data
    
    @property
    def next(self):
        return self._next
    
    @data.setter
    def data(self, value : Any) -> None:
        self._data = value

    @next.setter
    def next(self, node : 'Node') -> None:
        self._next = node

    def __str__(self) -> str:
        return_str = f'I have a data : {self.data}\n' \
                    + f'I have a next node : {id(self._next)}'
        return return_str
    
    def __repr__(self) -> str:
        return_str = f'Node({self._data})'
        return return_str
    
    def __add__(self, other) -> None:
        self.next = other

class LinkedListBag(object):
    """
    docstring
    """

    def __init__(self, first_node : Node = None) -> None:
        super().__init__()
        self._head = first_node
        self._tail = first_node
        self._size = 0 # __len__에서 while을 돌리지 않고 사용

        if first_node is None:
            self._size = 0
        else:
            self._size = self._count()

    def __contains__(self, target : int):
        cur_node = self._head
        while cur_node is not None:
            if cur_node.data == target:
                return True
            cur_node = cur_node.next
        else:
            return False
        
    def _count(self) -> int:
        counter = 0
        cur_node = self._head
        while cur_node is not None:
            counter += 1
            cur_node = cur_node.next
        return counter

    def __len__(self):
        return self._size
    
    def __repr__(self) -> str:
        cur_node = self._head
        if self._size == 0:
            return None

        return_str = ""
        while cur_node is not None:
            return_str += f"{cur_node.data} -> "
            cur_node = cur_node.next
        return_str += f"End of Linked List"
        return return_str
    
    def append(self, new_node : Node) -> bool:
        try:
            if self._size == 0:
                self._head = new_node
                self._tail = new_node
            else:
                self._tail.next = new_node
                self._tail = new_node
            self._size += 1
            return True
        except Exception as e:
            print(e)
            return False

    def insert(self, new_node : Node, index_number : int) -> bool:
        index_counter = 0
        cur_node = self._head

        if index_number == 0:
            new_node.next = self._head
            self._head = new_node
            # new_node가 head 앞으로 들어가면 head가 앞에 들어간 new_node를 가리켜야 하고(2번), new_node는 원래 head가 가리키고 있던 노드를 가리켜야함(1번)
            self._size += 1
            return True

        while cur_node is not None:
            if index_number == index_counter: # 값을 찾은 경우
                pred_node.next = new_node # ppt p.20 그림 1번
                new_node.next = cur_node # ppt p.20 그림 2번
                self._size += 1
                return True
            else:
                pred_node = cur_node
                cur_node = cur_node.next
                index_counter += 1 # 값을 찾지 않았을 경우 한 칸씩 전진
        return False

    def remove(self, target_value : int) -> bool:
        cur_node = self._head

        while cur_node is not None:
            if cur_node.data == target_value:
                pred_node.next = cur_node.next
                del(cur_node)
                self._size -= 1
                return True
            else:
                pred_node = cur_node
                cur_node = cur_node.next
        return False

    def __iter__(self):
        return _BagIterator(self._head)


    @property
    def head(self) -> Node:
        return self._head


class _BagIterator():
    def __init__(self, head_node) -> None:
        self._cur_node = head_node

    def __iter__(self):
        return self
    
    def __next__(self):
        if self._cur_node is None:
            raise StopIteration
        else:
            node = self._cur_node
            self._cur_node = self._cur_node.next
            # 다음에 iterator가 next를 호출할 때마다 그 다음 값을 앞으로 전진하면서 호출
            return node