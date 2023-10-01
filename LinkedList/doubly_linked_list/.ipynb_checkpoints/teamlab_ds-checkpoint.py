class Node:
    def __init__(self, next=None, prev=None, data=None):
        self.next = next 
        self.prev = prev 
        self.data = data
    
    def __str__(self):
        return str(self.data)
    
    def __repr__(self):
        return str(self.data)

class DoublyLinkedList:
    def __init__(self):
        self.head = None
 
    def push(self, new_data): 
        new_node = Node(new_data)
        new_node.next = self.head

        if self.head is not None:
            self.head.prev = new_node
 
        self.head = new_node
 
    def insertAfter(self, prev_node, new_data):
 
        # 1. Check if the given prev_node is None
        if prev_node is None:
            print ("the given previous node cannot be NULL")
            return
 
        # 2. allocate new node
        # 3. put in the data
        new_node = Node(new_data)
 
        # 4. Make net of new node as next of prev node
        new_node.next = prev_node.next
 
        # 5. Make prev_node as previous of new_node
        prev_node.next = new_node
 
        # 6. Make prev_node ass previous of new_node
        new_node.prev = prev_node
 
        # 7. Change previous of new_nodes's next node
        if new_node.next:
            new_node.next.prev = new_node
 
    def append(self, new_data):
 
        # 1. Allocates node
        # 2. Put in the data
        new_node = Node(new_data)
 
        # 3. This new node is going to be the last node,
        # so make next of it as None
        # (It already is initialized as None)
 
        # 4. If the Linked List is empty, then make the
        # new node as head
        if self.head is None:
            self.head = new_node
            return
 
        # 5. Else traverse till the last node
        last = self.head
        while last.next:
            last = last.next
 
        # 6. Change the next of last node
        last.next = new_node
 
        # 7. Make last node as previous of new node
        new_node.prev = last
 
        return
 
    # This function prints contents of linked list
    # starting from the given node
    def printList(self, node):
 
        print ("\nTraversal in forward direction")
        while node:
            print (" % d" % (node.data),)
            last = node
            node = node.next
 
        print ("\nTraversal in reverse direction")
        while last:
            print (" % d" % (last.data),)
            last = last.prev
 
        