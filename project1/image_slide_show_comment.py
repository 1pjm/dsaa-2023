#
# 필요한 라이브러리와 모듈들 불러오기
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
# : double linked list의 구조를 활용해 이미지의 리스트 표현, 이미지 관리 위한 여러 메서드 제공
class ImageLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.current = None

    # 새로운 이미지 리스트 마지막에 추가
    def append(self, image_path, timestamp=None):
        new_node = ImageNode(image_path, timestamp)
        if not self.head: # 리스트가 비어있으면
            self.head = new_node
            self.tail = new_node
            self.current = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        # 이미지 경로가 주어지면 새로운 ImageNode를 생성

        # 리스트에 노드가 없을 경우 (self.head가 None일 때):
        # 생성한 노드를 head, tail, 그리고 current로 설정

        # 이미 노드가 있는 경우:
        # 새로 생성한 노드의 prev 속성을 현재 tail로 설정
        # 현재 tail의 next 속성을 새로 생성한 노드로 설정
        # tail을 새로 생성한 노드로 업데이트
        # 따라서 매번 이미지가 추가될 때마다 새로운 노드가 연결 리스트의 끝에 추가되며, 이 노드가 tail이 됨

        self.print_list() # 리스트 상태 출력

    # 현재 노드의 다음 이미지로 이동
    def next_image(self):
        if self.current and self.current.next:
        # current 노드가 존재하고 그 다음 노드도 존재하면
            self.current = self.current.next
            # current를 다음 노드로 업데이트
        else:
            self.current = self.head
            # 리스트의 시작(head)으로 돌아감
        return self.current.image_path
        # 현재 선택된 이미지 경로 반환
    
    # 현재 노드의 이전 이미지로 이동
    def prev_image(self):
        if self.current and self.current.prev:
            self.current = self.current.prev
        else:
            self.current = self.tail
            # 리스트의 끝(tail)으로 이동
        return self.current.image_path

    # 다른 ImageLinkedList를 현재의 리스트에 병합
    def merge(self, another_list):
        if not another_list.head:
        # another_list에 노드가 없으면
            return # 아무것도 하지 않고 반환
        
        if not self.head:
        # 현재 리스트에 노드가 없으면
            self.head = another_list.head
            self.tail = another_list.tail
            self.current = another_list.head
            return
        
        # 둘 다 노드가 있는 경우:
        self.tail.next = another_list.head
        another_list.head.prev = self.tail
        self.tail = another_list.tail
        # tail을 another_list의 tail로 업데이트

        print(f"List merged with another list containing {len(another_list)} images")

    # append 메서드를 호출해 이미지 추가
    def add_image(self, image_path):
        self.append(image_path)

    # current 노드를 리스트에서 제거
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

        deleted_node = self.current # 현재 노드를 deleted_node에 저장
        if self.current.next:
            self.current = self.current.next
        elif self.current.prev:
            self.current = self.current.prev
        else:
            self.current = None
        
        print(f"Image {deleted_node.image_path} removed") # 제거된 이미지 출력
        self.print_list() # 리스트 상태 출력
        return deleted_node.image_path # 제거된 노드 이미지 경로 반환
    
    # 현재 리스트의 모든 노드의 메모리 주소 순서대로 출력
    def print_list(self):
        current = self.head # current 변수를 self.head로 초기화
        addresses = [] # 빈 리스트 생성: 각 노드 메모리 주소 저장하기 위한 목적
        while current:
        # while 루프를 사용해 current가 None이 될 때까지 연결 리스트 순회
            addresses.append(str(id(current)))
            # id 함수를 사용해 현재 노드의 메모리 주소값을 반환 -> str() 사용해 이 주소를 문자열로 변환 -> 문자열을 addresses 리스트에 추가
            current = current.next
            # current 변수를 다음 노드로 이동시킴, current가 마지막 노드라면 next는 None이 되어 while 루프 종료
        print(" -> ".join(addresses))
        # 주소값들을 "->" 문자로 연결하여 출력
        # join(): 문자열 메서드, 주어진 반복 가능한 객체(리스트, 튜플)의 각 항목을 연결하여 하나의 문자열로 만듦

# 이미지 브라우저
# : PyQt5를 이용한 이미지 브라우저 애플리케이션 구현
class ImageBrowser(QMainWindow):
# QMainWindow를 상속받아 메인 윈도우 구성

    # ImageBrowser 인스턴스가 생성될 때 기본적인 설정을 수행하고, 그 후 사용자 인터페이스를 초기화하는 역할
    def __init__(self):
        super().__init__() # super(): QMainWindow
        self.initUI() # ImageBrowser 생성 시 UI 초기화 작업 함께 수행

    # PyQt5를 사용하여 ImageBrowser 클래스의 사용자 인터페이스(UI)를 초기화
    def initUI(self):
        self.setWindowTitle('Image Browser') # 메인 윈도우 제목 설정
        self.setGeometry(100, 100, 800, 600) # 메인 윈도우 크기 설정

        layout = QVBoxLayout() # 전체 윈도우에 사용될 수직 레이아웃 QVBoxLayout 생성

        btn_layout = QHBoxLayout()
        # 폴더 불러오기, 이미지 추가, 이미지 제거 버튼을 수평으로 배치하기 위한 수평 레이아웃(QHBoxLayout)을 생성

        self.folder_btn = QPushButton('폴더', self)
        self.folder_btn.clicked.connect(self.load_folder)
        self.add_img_btn = QPushButton('사진 추가', self)
        self.add_img_btn.clicked.connect(self.load_image)
        # 버튼 생성 후 각각의 클릭 이벤트에 해당하는 함수 연결
        
        btn_layout.addWidget(self.folder_btn)
        btn_layout.addWidget(self.add_img_btn)
        # addWidget: PyQt5 메서드
        # : 주로 레이아웃 객체(QHBoxLayout, QVBoxLayout 등) 내에서 사용
        # : 레이아웃에 위젯(버튼, 라벨, 텍스트 입력 상자 등)을 추가하는데 사용

        layout.addLayout(btn_layout)

        # 이미지 표시를 위한 라벨 정의
        self.image_label = QLabel(self)
        self.image_label.setMinimumSize(600, 400) # 최소 크기 설정
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
        # 메인 윈도우의 중앙 위젯 설정
        # 생성된 레이아웃을 이 위젯에 설정한 후, 전체 윈도우의 중앙 위젯으로 지정

        self.image_list = ImageLinkedList()
        # 이미지 경로를 저장 및 관리할 ImageLinkedList 초기화

        self.remove_img_btn = QPushButton('사진 제거', self)
        self.remove_img_btn.clicked.connect(self.remove_image)
        btn_layout.addWidget(self.remove_img_btn)

    # 폴더 선택 시 해당 폴더 내 이미지 파일들을 연결 리스트에 추가
    def load_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, '폴더 선택') # 폴더 선택 대화상자 열기
        
        if folder_path:
            for filename in os.listdir(folder_path):
            # os 모듈의 listdir 함수를 사용해 folder_path에 있는 모든 파일/디렉토리 이름을 리스트 형태로 반환, 반환된 리스트에 있는 각 항목(파일/디렉토리 이름)에 대해 반복문 실행
                if filename.endswith(('.png', '.jpg', '.jpeg')): # .endswith() 메서드를 사용해 확장자 확인
                    full_image_path = os.path.join(folder_path, filename)
                    # folder_path와 filename을 합쳐 전체 이미지 파일 경로 생성
                    # os.path.join(): 경로를 결합하여 새 경로 생성

                    self.image_list.append(full_image_path)
                    # 생성된 이미지 경로를 self.image_list(이미지 연결 리스트)에 추가

                    self.update_image(full_image_path)
                    # 이미지를 화면에 표시

                    print(f'Added image from {full_image_path}')
            
            print(f"Loaded all images from folder {folder_path}")
            # 선택한 폴더에서 모든 이미지 파일이 로드될 경우 출력

    # 사용자에게 파일 선택 대화상자를 표시하여 이미지 파일을 선택받고, 선택된 이미지 파일의 경로를 연결 리스트에 추가하고 화면에 표시
    def load_image(self, file_path):
        file_path, _ = QFileDialog.getOpenFileName(self, '이미지 선택', '', 'Images (*.png *.xpm *.jpg *.jpeg)')
        # 이미지 선택 대화상자 열기
        # '': 대화상자가 처음 열렸을 때의 기본 경로, 최근에 열려진 위치나 기본 폴더에서 시작하게 됨
        # QFileDialog.getOpenFileName은 선택된 파일의 경로와 선택된 필터를 반환, 여기선 파일 경로만 필요하므로 _ 를 사용해 필터는 무시
        if file_path:
        # 파일 선택 후 열기를 클릭했다면 file_path에 선택된 파일의 경로가 저장
            self.image_list.append(file_path)
            # 선택한 이미지 파일 경로를 self.image_list에 추가
            self.update_image(file_path)
            # 이미지를 화면에 표시하기 위해 update_image 메서드 호출, file_path를 인자로 전달
            print(f'Added image from {file_path}')

    # 이미지 경로를 인자로 받아 해당 이미지를 라벨에 표시
    def update_image(self, image_path):
        pixmap = QPixmap(image_path)
        # 주어진 image_path 경로의 이미지를 읽어 QPixmap 객체를 생성, QPixmap은 PyQt에서 이미지를 표현하기 위한 클래스

        # 이미지를 현재 윈도우의 크기에 맞게 조절
        scaled_pixmap = pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        # self.image_label.size(): 이미지를 표시하기 위한 라벨의 크기를 반환, 이 크기에 맞게 이미지의 크기를 조절
        # Qt.KeepAspectRatio: 이미지의 원래 종횡비를 유지하면서 크기를 조절하는 옵션
        # Qt.SmoothTransformation: 이미지 크기 조절 시 부드러운 변환을 사용하는 옵션, 이 옵션을 사용하면 이미지의 품질이 떨어지지 않고 부드럽게 확대/축소

        if pixmap.isNull(): # 이미지가 올바르게 로드되지 않았을 경우 (pixmap.isNull(): True를 반환)
            self.show_error_message("이미지 로딩 오류", "이미지를 로드할 수 없습니다. 유효하지 않은 형식이거나 경로가 잘못되었을 수 있습니다.")
            return

        self.image_label.setPixmap(scaled_pixmap)
        # 조절된 크기의 이미지(scaled_pixmap)를 라벨에 설정하여 화면에 표시

    # 연결 리스트에서 다음 이미지의 경로를 가져와 update_image 메서드를 호출하여 화면에 표시
    def next_image(self):
        next_path = self.image_list.next_image()
        # next_image(): 연결 리스트에서 현재 이미지의 다음 이미지의 경로를 반환, 다음 이미지가 없으면 None 반환
        if next_path:
            self.update_image(next_path)

    # 연결 리스트에서 이전 이미지의 경로를 가져와 update_image 메서드를 호출하여 화면에 표시
    def prev_image(self):
        prev_path = self.image_list.prev_image()
        if prev_path:
            self.update_image(prev_path)

    # 현재 선택된 이미지를 연결 리스트에서 제거, 제거 후 다음 이미지를 표시하거나 이미지가 없으면 라벨 삭제
    def remove_image(self):
        removed_path = self.image_list.remove_image()
        if removed_path:
            if self.image_list.current:
            # image_list에서 이미지를 제거한 후에도 현재 이미지가 있는지 확인, 있으면
                self.update_image(self.image_list.current.image_path)
                # 현재 이미지의 경로를 update_image 메서드에 전달하여 해당 이미지를 화면에 표시
            else: # 없으면
                self.image_label.clear()
                # 이미지 라벨의 내용을 지움 (화면에 표시되는 이미지 제거)
            return
    
        if not self.image_list.current: # 연결 리스트에 현재 선택된 이미지가 없으면
            self.show_error_message("이미지 오류", "제거할 이미지가 없습니다.")
            return

    # 주어진 제목과 메시지로 에러 메시지 박스를 생성하고 사용자에게 표시
    def show_error_message(self, title, message):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Critical) # 메시지 박스에 표시될 아이콘 설정
        msg_box.setWindowTitle(title) # 메시지 박스의 제목 표시줄에 표시될 텍스트 설정
        msg_box.setText(message) # 본문에 표시될 텍스트 설정
        msg_box.exec() # 사용자가 OK 버튼을 클릭해 박스를 닫을 때까지 프로그램 이 줄에서 일시 중지

# ImageBrowser GUI 애플리케이션을 시작하고 사용자가 이를 종료할 때까지 실행하는 역할, 프로그램을 종료하면 이벤트 루프는 종료되고 프로그램도 종료
if __name__ == '__main__':
# 스크립트가 직접 실행될 때만 내부 코드 실행하도록 함
# 이 구문을 사용하는 이유는 이 스크립트가 모듈로 다른 코드에서 임포트될 때, 이 부분이 실행되지 않게 하기 위해서
    app = QApplication(sys.argv)
    # QApplication: PyQt의 GUI 애플리케이션을 시작하기 위해 필요한 객체
    # sys.argv: 커맨드 라인 인자를 QApplication에 전달해 애플리케이션을 더 유연하게 사용할 수 있게 함
    browser = ImageBrowser()
    # ImageBrowser 클래스의 인스턴스를 생성
    browser.show()
    # show() 메서드를 호출해 이미지 브라우저 윈도우를 화면에 표시
    sys.exit(app.exec_())
    # app.exec_(): 애플리케이션의 메인 이벤트 루프 시작
    # sys.exit(): 애플리케이션 종료 시 반환된 상태 코드를 반환해 프로그램 종료
