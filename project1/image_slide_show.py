#
#! 1. 기본 틀 구현
#! 2. PyQt5 기반 GUI 개발
#! 3. 프로젝트 세부 기능 구현
#! 4. 예외 처리

import sys, os, time
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QWidget, QFileDialog, QHBoxLayout, QGraphicsView, QGraphicsScene, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class ImageNode:
    def __init__(self, image_path, timestamp=None):
        self.image_path = image_path
        self.timestamp = timestamp if timestamp else time.time()
        self.next = None
        self.prev = None

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

        print(f"Image {image_path} added at {timestamp}")

    def next_image(self):
        if self.current and self.current.next:
            self.current = self.current.next
        else:
            # 루프 기능 추가
            self.current = self.head
        return self.current.image_path
    
    def prev_image(self):
        if self.current and self.current.prev:
            self.current = self.current.prev
        else:
            # 루프 기능 추가
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
            return
        self.tail.next = another_list.head
        another_list.head.prev = self.tail
        self.tail = another_list.tail

        print(f"List merged with another list containing {len(another_list)} images")

    # 연결 리스트 분할
    def split(self, index):
        if not self.head or index < 0:
            return None, None
        split_list = ImageLinkedList()
        current = self.head
        i = 0
        while current and i < index:
            current = current.next
            i += 1
        if i == index:
            split_list.head = current
            split_list.tail = self.tail
            split_list.current = current
            if current.prev:
                current.prev.next = None
            self.tail = current.prev
            current.prev = None
        return self, split_list
    
    # def split(self):
    #     mid_node = self.current  # split from current image
    #     if not mid_node:
    #         return None

    #     second_list = ImageLinkedList()
    #     second_list.head = mid_node.next
    #     second_list.tail = self.tail

    #     mid_node.next = None
    #     self.tail = mid_node

    #     return second_list

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
        return deleted_node.image_path
    

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
        self.image_label.setMinimumSize(600, 400)  # 이 값을 원하는 크기에 맞게 조정할 수 있습니다.
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

        #! 3.
        self.remove_img_btn = QPushButton('사진 제거', self)
        self.remove_img_btn.clicked.connect(self.remove_image)
        btn_layout.addWidget(self.remove_img_btn)
        #

    def load_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, '폴더 선택')
        # Add all images in the folder to the linked list
        # For simplicity, assume all files in the folder are images
        if folder_path:
            for filename in os.listdir(folder_path):
                if filename.endswith(('.png', '.jpg', '.jpeg')):
                    self.image_list.append(os.path.join(folder_path, filename))
                    self.update_image(self.image_list.current.image_path)
                    print(f'Added image from {self.image_list.current.image_path}')
            print(f"Loaded all images from folder {folder_path}")

    def load_image(self, file_path):
        file_path, _ = QFileDialog.getOpenFileName(self, '이미지 선택', '', 'Images (*.png *.xpm *.jpg *.jpeg)')
        if file_path:
            self.image_list.append(file_path)
            self.update_image(file_path)
            print(f"Image {file_path} added to the list")
        
        if not os.path.exists(file_path):
            self.show_error_message("파일 오류", "선택된 파일이 존재하지 않습니다.")
            return

        try:
            self.image_list.append(file_path)
            self.update_image(file_path)
        except Exception as e:
            self.show_error_message("이미지 추가 오류", str(e))

    def update_image(self, image_path):
        pixmap = QPixmap(image_path)

        # 이미지를 현재 윈도우의 크기에 맞게 조절
        scaled_pixmap = pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

        #!. 4. 예외 처리
        if pixmap.isNull():
            self.show_error_message("이미지 로딩 오류", "이미지를 로드할 수 없습니다. 유효하지 않은 형식이거나 경로가 잘못되었을 수 있습니다.")
            return

        self.image_label.setPixmap(scaled_pixmap)

    # Resize event를 재정의하여, 윈도우 크기 변경 시 이미지 크기를 업데이트
    def resizeEvent(self, event):
        if self.image_list.current:
            self.update_image(self.image_list.current.image_path)
        super().resizeEvent(event)

    def next_image(self):
        next_path = self.image_list.next_image()
        if next_path:
            self.update_image(next_path)

    def prev_image(self):
        prev_path = self.image_list.prev_image()
        if prev_path:
            self.update_image(prev_path)

    #! 3.
    def remove_image(self):
        removed_path = self.image_list.remove_image()
        if removed_path:
            if self.image_list.current:
                self.update_image(self.image_list.current.image_path)
            else:
                self.image_label.clear()
    #
        #! 4.
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




