#
import sys, os, time
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QWidget, QFileDialog, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

# 이미지 노드 클래스
# : 이미지 경로와 시간 정보를 담기 위한 노드 클래스
class ImageNode:
    def __init__(self, image_path, timestamp=None):
        self.image_path = image_path
        self.timestamp = timestamp if timestamp else time.time()
        self.next = None
        self.prev = None

# 이미지 연결 리스트
# : 이미지들을 연결 리스트 형태로 관리하기 위한 클래스
class ImageLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.current = None

    def append(self, image_path, timestamp=None):
        new_node = ImageNode(image_path, timestamp)
        if not self.head:
            self.head = new_node
            self.tail = new_node
            self.current = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node

        self.print_list()

    # 현재 노드의 다음 이미지로 이동
    def next_image(self):
        if self.current and self.current.next:
            self.current = self.current.next
        else:
            self.current = self.head
        return self.current.image_path
    
    def prev_image(self):
        if self.current and self.current.prev:
            self.current = self.current.prev
        else:
            self.current = self.tail
        return self.current.image_path
    
    # 두 연결 리스트 병합
    def merge(self, another_list):
        if not another_list.head:
            return
        
        if not self.head:
            self.head = another_list.head
            self.tail = another_list.tail
            self.current = another_list.head
        else:
            self.tail.next = another_list.head
            another_list.head.prev = self.tail
            self.tail = another_list.tail

        print(f"List merged with another list containing {len(another_list)} images")

    def add_image(self, image_path):
        self.append(image_path)

    def remove_image(self):
        if not self.current:
            return None
        
        if self.current.prev:
            self.current.prev.next = self.current.next
        else:
            self.head = self.current.next
        if self.current.next:
            self.current.next.prev = self.current.prev
        else:
            self.tail = self.current.prev

        deleted_node = self.current
        if self.current.next:
            self.current = self.current.next
        elif self.current.prev:
            self.current = self.current.prev
        else:
            self.current = None
        
        print(f"Image {deleted_node.image_path} removed")
        self.print_list()
        return deleted_node.image_path
    
    def print_list(self):
        current = self.head
        addresses = []
        while current:
            addresses.append(str(id(current)))
            current = current.next
        print(" -> ".join(addresses))

class ImageBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Image Browser')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        btn_layout = QHBoxLayout()
        self.folder_btn = QPushButton('폴더', self)
        self.folder_btn.clicked.connect(self.load_folder)
        self.add_img_btn = QPushButton('사진 추가', self)
        self.add_img_btn.clicked.connect(self.load_image)
        
        btn_layout.addWidget(self.folder_btn)
        btn_layout.addWidget(self.add_img_btn)

        layout.addLayout(btn_layout)

        # 이미지 표시를 위한 라벨 정의
        self.image_label = QLabel(self)
        self.image_label.setMinimumSize(600, 400)
        layout.addWidget(self.image_label, alignment=Qt.AlignCenter)

        nav_layout = QHBoxLayout()
        self.prev_btn = QPushButton('<', self)
        self.prev_btn.clicked.connect(self.prev_image)
        self.next_btn = QPushButton('>', self)
        self.next_btn.clicked.connect(self.next_image)
        nav_layout.addWidget(self.prev_btn)
        nav_layout.addWidget(self.next_btn)

        layout.addLayout(nav_layout)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.image_list = ImageLinkedList()

        self.remove_img_btn = QPushButton('사진 제거', self)
        self.remove_img_btn.clicked.connect(self.remove_image)
        btn_layout.addWidget(self.remove_img_btn)

    def load_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, '폴더 선택')
        
        if folder_path:
            for filename in os.listdir(folder_path):
                if filename.endswith(('.png', '.jpg', '.jpeg')):
                    full_image_path = os.path.join(folder_path, filename)
                    self.image_list.append(full_image_path)
                    self.update_image(full_image_path)
                    print(f'Added image from {full_image_path}')
            
            print(f"Loaded all images from folder {folder_path}")

    def load_image(self, file_path):
        file_path, _ = QFileDialog.getOpenFileName(self, '이미지 선택', '', 'Images (*.png *.xpm *.jpg *.jpeg)')
        if file_path:
            self.image_list.append(file_path)
            self.update_image(file_path)
            print(f'Added image from {file_path}')

    def update_image(self, image_path):
        pixmap = QPixmap(image_path)

        # 이미지를 현재 윈도우의 크기에 맞게 조절
        scaled_pixmap = pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

        if pixmap.isNull():
            self.show_error_message("이미지 로딩 오류", "이미지를 로드할 수 없습니다. 유효하지 않은 형식이거나 경로가 잘못되었을 수 있습니다.")
            return

        self.image_label.setPixmap(scaled_pixmap)

    def next_image(self):
        next_path = self.image_list.next_image()
        if next_path:
            self.update_image(next_path)

    def prev_image(self):
        prev_path = self.image_list.prev_image()
        if prev_path:
            self.update_image(prev_path)

    def remove_image(self):
        removed_path = self.image_list.remove_image()
        if removed_path:
            if self.image_list.current:
                self.update_image(self.image_list.current.image_path)
            else:
                self.image_label.clear()
            return
    
        if not self.image_list.current:
            self.show_error_message("이미지 오류", "제거할 이미지가 없습니다.")
            return

    def show_error_message(self, title, message):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    browser = ImageBrowser()
    browser.show()
    sys.exit(app.exec_())




