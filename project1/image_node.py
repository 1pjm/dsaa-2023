# image_node.py

class ImageNode:
    def __init__(self, image_data):
        self.image_data = image_data
        self.next_node = None
        self.prev_node = None

    def set_next(self, next_node):
        self.next_node = next_node

    def set_prev(self, prev_node):
        self.prev_node = prev_node

    def get_image(self):
        return self.image_data
