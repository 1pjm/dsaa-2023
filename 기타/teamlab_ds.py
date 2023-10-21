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
    