# linked_list.py

from image_node import ImageNode

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.current = None

    def is_empty(self):
        return self.head is None

    def append(self, image_data):
        new_node = ImageNode(image_data)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            new_node.set_prev(self.tail)
            self.tail.set_next(new_node)
            self.tail = new_node

    def remove(self, image_data):
        current_node = self.head
        while current_node is not None:
            if current_node.get_image() == image_data:
                if current_node.prev_node:
                    current_node.prev_node.set_next(current_node.next_node)
                else:
                    self.head = current_node.next_node

                if current_node.next_node:
                    current_node.next_node.set_prev(current_node.prev_node)
                else:
                    self.tail = current_node.prev_node

                if current_node == self.current:
                    self.current = current_node.next_node
                return True
            current_node = current_node.next_node
        return False

    def start_slideshow(self):
        if not self.is_empty():
            self.current = self.head

    def next_image(self):
        if self.current and self.current.next_node:
            self.current = self.current.next_node
        else:
            self.current = self.head

    def previous_image(self):
        if self.current and self.current.prev_node:
            self.current = self.current.prev_node
        else:
            self.current = self.tail

    def get_current_image(self):
        if self.current:
            return self.current.get_image()
        return None

# 예제 사용
if __name__ == "__main__":
    linked_list = DoublyLinkedList()

    # 이미지 추가
    linked_list.append("image1.jpg")
    linked_list.append("image2.jpg")
    linked_list.append("image3.jpg")

    # 슬라이드쇼 시작
    linked_list.start_slideshow()

    while True:
        current_image = linked_list.get_current_image()
        if current_image:
            print("Current Image:", current_image)
            choice = input("Enter 'n' for next, 'p' for previous, 'q' to quit: ")
            if choice == 'n':
                linked_list.next_image()
            elif choice == 'p':
                linked_list.previous_image()
            elif choice == 'q':
                break
        else:
            print("No images in the list.")
            break
