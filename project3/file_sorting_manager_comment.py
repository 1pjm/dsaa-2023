import sys  # 파이썬 인터프리터와 관련된 명령어와 함수 제공 모듈
import os  # 운영 체제와 상호 작용하기 위한 기능 제공 모듈
import time  # 시간 관련 함수를 제공하는 모듈
from datetime import datetime  # 날짜와 시간을 다루기 위한 클래스 제공 모듈
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QTextEdit, QFileDialog, QComboBox


class File:  # 파일 정보를 나타내는 클래스
    def __init__(self, name, size, creation_date):
        # 생성자 함수, 인스턴스가 생성될 때 호출,
        self.name = name  # 파일의 이름,
        self.size = size  # 파일의 크기,
        self.creation_date = creation_date  # 파일의 생성 날짜 변수로 저장

    def __repr__(self):  # 문자열로 반환
        return f"{self.name} ({self.size}, {self.creation_date})"


def bubble_sort(files, key, reverse=False):  # 버블 정렬 함수
# 최선(배열이 이미 정렬되어 있는 경우): O(n)
# 평균 및 최악(배열이 역순으로 정렬되어 있는 경우): O(n^2)
    # 세 개의 매개변수를 받음
    # files: 정렬할 객체의 리스트
    # key: 정렬 기준이 되는 객체의 속성
    # reverse: 정렬 순서를 역순으로 할지 결정하는 불리언 값, 기본값 False
    n = len(files)  # n에 리스트 길이 저장
    swap_count = 0  # swap_count 초기화
    for i in range(n):  # 바깥쪽 반복문: 리스트 n번 순회
        for j in range(0, n - i - 1):
            # 내부 반복문: 각 반복에서 리스트의 인접한 요소 비교, 필요에 따라 위치 변환
            # j: 리스트 내의 현재 인덱스
            # n-i-1로 설정하는 이유: 버블 정렬 특성상 각 반복마다 최소 한 개의 요소가 그 자리를 찾아 정렬되므로, 이미 정렬된 부분은 다시 검사할 필요x
            if (reverse and getattr(files[j], key) < getattr(files[j + 1], key)) or \
                    (not reverse and getattr(files[j], key) > getattr(files[j + 1], key)):
                # if 조건문을 사용해 요소를 비교하고, 필요한 경우 위치를 바꿈.
                # getattr 함수를 사용해 key에 해당하는 속성 값을 가져옴.
                # reverse가 True면 내림차순, False면 오름차순 정렬
                files[j], files[j + 1] = files[j + 1], files[j]  # 두 요소의 위치를 바꿈
                swap_count += 1  # 위치 바뀔 때마다 swap_count 1 증가
                print(f"Bubble Sort Step: {files}")
    return files, swap_count  # 정렬된 리스트와 swap 횟수 반환


def selection_sort(files, key, reverse=False):  # 선택 정렬 함수
# O(n^2)
    swap_count = 0
    for i in range(len(files)):  # 바깥 반복문: 리스트 각 요소 순회
        idx = i  # 현재 반복의 인덱스(i) 할당
        for j in range(i+1, len(files)):
            # 안쪽 반복문: i번째 요소 다음부터 리스트 끝까지 순회, 현재 선택된 요소 files[i]와 나머지 요소들을 비교
            if (reverse and getattr(files[j], key) > getattr(files[idx], key)) or \
                    (not reverse and getattr(files[j], key) < getattr(files[idx], key)):
                # if 조건문 사용해 현재 요소 files[j]가 현재 선택된 요소 files[idx]보다 더 작거나 큰지 비교
                idx = j  # 현재 요소가 선택된 요소보다 작거나 크면 idx를 현재 요소의 인덱스 j로 업데이트
        if idx != i:  # idx가 초기값 i와 다르면 가장 작거나 가장 큰 요소를 찾은 것이므로
            files[i], files[idx] = files[idx], files[i]  # 두 요소 위치 바꿈
            swap_count += 1
            print(f"Selection Sort Step: {files}")
    return files, swap_count


def insertion_sort(files, key, reverse=False):  # 삽입 정렬 함수
# 최선(배열이 이미 정렬되어 있는 경우): O(n)
# 평균 및 최악(배열이 역순 or 무작위인 경우): O(n^2)
    swap_count = 0
    for i in range(1, len(files)):
        key_file = files[i]  # 현재 정렬 중인 요소 key_file을 files[i]로 설정
        j = i - 1  # key_file보다 앞에 있는 요소들을 순차적으로 비교
        while j >= 0 and ((reverse and getattr(files[j], key) < getattr(key_file, key)) or
                        (not reverse and getattr(files[j], key) > getattr(key_file, key))):
            # while 루프를 이용해 key_file이 적절한 위치를 찾을 때까지 반복
            # j 인덱스에 있는 요소가 key_file보다 크거나 (오름차순 정렬의 경우) 또는 작은 경우 (내림차순 정렬의 경우)
            files[j + 1] = files[j]  # files[j] 요소를 오른쪽으로 이동
            j -= 1  # j를 감소시켜 이전 위치로 이동
            swap_count += 1
            print(f"Insertion Sort Step: {files}")
        files[j + 1] = key_file
        # 루프가 종료되면 j는 key_file이 들어갈 위치 바로 앞의 인덱스를 가리킴
    return files, swap_count


def quick_sort(files, key, reverse=False):  # 퀵 정렬 함수
# 최선, 평균: O(n log n)
# 최악(정렬된 경우): O(n^2)
    def _quick_sort(items, low, high):
        # 이 함수는 재귀적으로 호출되어 리스트의 특정 부분 정렬
        # low: 정렬할 부분의 시작 인덱스, high: 끝
        swap_count = 0
        if low < high:  # 현재 분할된 부분이 유효한지 (즉, 두 개 이상의 요소가 있는지) 확인
            pivot_index, pivot_swap_count = partition(items, low, high)
            # partition 함수를 호출하여 pivot 기준으로 리스트를 분할
            # 분할된 리스트에서 pivot의 위치(pivot_index)와 이 과정에서 발생한 swap 횟수(pivot_swap_count)를 반환
            swap_count += pivot_swap_count
            # pivot을 기준으로 분할하는 과정에서 발생한 swap 횟수를 swap_count에 추가
            left_swap_count = _quick_sort(items, low, pivot_index)
            right_swap_count = _quick_sort(items, pivot_index + 1, high)
            # pivot을 기준으로 분할된 두 부분을 각각 재귀적으로 정렬합니다. 각 부분에서 발생한 swap 횟수를 반환
            swap_count += left_swap_count + right_swap_count
            # 왼쪽과 오른쪽 부분의 정렬 과정에서 발생한 swap 횟수를 swap_count에 추가
        return swap_count

    def partition(items, low, high):
        # 리스트를 pivot을 기준으로 두 부분으로 나누는 함수
        pivot = getattr(items[(low + high) // 2], key)
        # pivot 값은 중간 지점의 요소를 기준으로 선택
        swap_count = 0
        while True:  # 리스트가 올바르게 분할될 때까지 무한 루프
            while (reverse and getattr(items[low], key) > pivot) or \
                    (not reverse and getattr(items[low], key) < pivot):
                low += 1
                # low 인덱스를 pivot 값보다 크거나 작은 요소를 찾을 때까지 증가
            while (reverse and getattr(items[high], key) < pivot) or \
                    (not reverse and getattr(items[high], key) > pivot):
                high -= 1
                # high 인덱스를 pivot 값보다 작거나 큰 요소를 찾을 때까지 감소
            if low >= high:
                return high, swap_count
                # low와 high가 교차하거나 만날 경우, 분할이 완료되었음을 의미하며, 현재의 high 위치와 swap 횟수를 반환
            items[low], items[high] = items[high], items[low]
            swap_count += 1
            # low와 high 위치에 있는 요소들을 교환(swap)하고, swap 횟수를 1 증가
            print(f"Quick Sort Swap: {items}")
            low += 1
            high -= 1

    total_swap_count = _quick_sort(files, 0, len(files) - 1)
    # _quick_sort 함수를 처음 호출하여 전체 리스트에 대해 정렬을 수행하고, 발생한 총 swap 횟수를 total_swap_count에 저장
    return files, total_swap_count


def merge_sort(files, key, reverse=False):  # 머지 정렬 함수
# 최선, 평균, 최악: O(n log n)
    def _merge_sort(items, swap_count):
        # 이 함수는 재귀적으로 호출되어 리스트의 특정 부분을 정렬
        if len(items) > 1:
            # 현재 부분 리스트의 길이가 1보다 큰 경우에만 정렬을 수행
            # 길이가 1 이하면 이미 정렬된 것으로 간주
            mid = len(items) // 2
            left_half = items[:mid]
            right_half = items[mid:]
            # 리스트를 두 개의 하위 리스트로 분할: 왼쪽 부분(left_half)과 오른쪽 부분(right_half)

            swap_count = _merge_sort(left_half, swap_count)
            swap_count = _merge_sort(right_half, swap_count)
            # 분할된 두 부분을 각각 재귀적으로 정렬
            # 각 부분에서 발생한 swap 횟수를 누적

            i = j = k = 0
            # i, j, k 인덱스를 초기화
            # i와 j는 각각 왼쪽과 오른쪽 부분 리스트의 인덱스를, k는 병합된 리스트에서의 인덱스를 나타냄
            while i < len(left_half) and j < len(right_half):
                # 두 부분 리스트의 모든 요소를 병합할 때까지 반복
                if (reverse and getattr(left_half[i], key) > getattr(right_half[j], key)) or \
                        (not reverse and getattr(left_half[i], key) < getattr(right_half[j], key)):
                    # 두 부분 리스트의 현재 요소를 비교하여 적절한 요소를 선택
                    items[k] = left_half[i]
                    i += 1
                else:
                    items[k] = right_half[j]
                    j += 1
                    # 선택된 요소를 병합된 리스트에 추가하고, 해당 부분 리스트의 인덱스를 증가
                k += 1  # 병합된 리스트의 인덱스를 증가
                swap_count += 1
                print(f"Merge Sort Step: {items}")

            while i < len(left_half):
                items[k] = left_half[i]
                i += 1
                k += 1
                # 왼쪽 부분 리스트의 나머지 요소를 병합된 리스트에 추가

            while j < len(right_half):
                items[k] = right_half[j]
                j += 1
                k += 1
                # 오른쪽 부분 리스트의 나머지 요소를 병합된 리스트에 추가

        return swap_count

    swap_count = _merge_sort(files, 0)
    # _merge_sort 함수를 처음 호출하여 전체 리스트에 대해 정렬을 수행하고, 발생한 총 swap 횟수를 swap_count에 저장
    return files, swap_count


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.sort_order = "오름차순"  # 기본값
        self.sort_criterion = "파일 이름"  # 기본값
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('File Sorting Manager')
        self.setGeometry(100, 100, 800, 400)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        top_layout = QHBoxLayout()
        middle_layout = QHBoxLayout()
        bottom_layout = QVBoxLayout()

        self.sort_buttons = {
            '버블 정렬': QPushButton('버블 정렬'),
            '선택 정렬': QPushButton('선택 정렬'),
            '삽입 정렬': QPushButton('삽입 정렬'),
            '퀵 정렬': QPushButton('퀵 정렬'),
            '머지 정렬': QPushButton('머지 정렬'),
            '전체 선택': QPushButton('전체 선택')
        }

        for button in self.sort_buttons.values():
            top_layout.addWidget(button)
            button.clicked.connect(self.sort_files)

        self.sort_criteria_dropdown = QComboBox()
        self.sort_criteria_dropdown.addItems(['파일 이름', '크기', '생성 날짜'])
        self.sort_criteria_dropdown.currentIndexChanged.connect(
            self.update_sort_criterion)

        self.sort_order_dropdown = QComboBox()
        self.sort_order_dropdown.addItems(['오름차순', '내림차순'])
        self.sort_order_dropdown.currentIndexChanged.connect(
            self.update_sort_order)

        top_layout.addWidget(self.sort_criteria_dropdown)
        top_layout.addWidget(self.sort_order_dropdown)

        label1 = QLabel('경로')
        self.line_edit = QLineEdit()
        folder_select_button = QPushButton('폴더 선택')
        folder_select_button.clicked.connect(self.select_folder)

        middle_layout.addWidget(label1)
        middle_layout.addWidget(self.line_edit)
        middle_layout.addWidget(folder_select_button)

        self.text_edit = QTextEdit()
        bottom_layout.addWidget(self.text_edit)

        main_layout.addLayout(top_layout)
        main_layout.addLayout(middle_layout)
        main_layout.addLayout(bottom_layout)

    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Select Folder')
        if not folder_path:  # 폴더 선택이 취소되었을 때 처리
            folder_path = os.getcwd()
            # 사용자가 폴더를 선택하지 않았을 경우, os.getcwd()를 호출하여 현재 작업 디렉토리의 경로를 folder_path에 할당
            self.create_dummy_files(folder_path)
            # create_dummy_files 메서드를 호출하여 folder_path 경로에 더미 파일을 생성
        self.line_edit.setText(folder_path)

    def update_sort_criterion(self, index):
        # 드롭다운 메뉴에서 선택된 정렬 기준을 업데이트하는 함수
        self.sort_criterion = self.sort_criteria_dropdown.currentText()

    def update_sort_order(self, index):
    # 사용자가 드롭다운 메뉴에서 정렬 순서를 선택할 때마다, 선택한 순서를 self.sort_order에 업데이트하는 역할
        self.sort_order = self.sort_order_dropdown.currentText()

    def sort_files(self):
        sorting_algorithm = self.sender().text()
        # 현재 클릭된 버튼에서 텍스트를 가져와서 sorting_algorithm 변수에 저장
        # : 어떤 정렬 알고리즘이 선택되었는지 알 수 있음
        folder_path = self.line_edit.text()

        if not folder_path:
            folder_path = os.getcwd() # 경로를 현재 작업 디렉토리로 설정
            self.create_dummy_files(folder_path)
            self.line_edit.setText(folder_path)

        if sorting_algorithm == '전체 선택':
            results = []
            for alg in ['버블 정렬', '선택 정렬', '삽입 정렬', '퀵 정렬', '머지 정렬']:
            # 모든 가능한 정렬 알고리즘에 대해 반복
                alg_name, alg_time = self.execute_sorting_algorithm(
                    alg, folder_path)
                # 선택된 정렬 알고리즘(alg)을 실행하고 실행 시간과 알고리즘 이름을 반환
                results.append((alg_name, alg_time))
            fastest_alg = min(results, key=lambda x: x[1])
            # 결과 리스트에서 실행 시간이 가장 짧은 알고리즘을 찾아 fastest_alg 변수에 저장
            # key=lambda x: x[1]
            # : min 함수는 리스트의 요소 중에서 최솟값을 찾을 때, key 매개변수에 지정된 함수를 사용하여 최솟값을 결정
            # 이 함수는 x를 입력으로 받아서 x[1] 값을 반환하는 람다 함수, x[1]은 results 리스트의 각 요소에서 두 번째 값, 즉 실행 시간을 나타냄
            self.text_edit.append(
                f"Fastest Algorithm: {fastest_alg[0]} with time {fastest_alg[1]:.2f} seconds")
        else:# 전체 선택이 아닌 경우
            self.execute_sorting_algorithm(sorting_algorithm, folder_path)
            # 선택된 정렬 알고리즘을 실행하고 결과를 처리하는 execute_sorting_algorithm 메서드를 호출

    def execute_sorting_algorithm(self, algorithm, folder_path):
        files = self.read_files(folder_path)
        reverse = True if self.sort_order == "내림차순" else False
        key = "size" if self.sort_criterion == "크기" else "creation_date" if self.sort_criterion == "생성 날짜" else "name"

        swap_count = 0
        time_complexity = "" # 시간 복잡도 초기화
        start_time = time.time() # 정렬 시작 시간을 기록
        print("\n정렬을 시작합니다.")

        if algorithm == '버블 정렬':
            sorted_files, swap_count = bubble_sort(files.copy(), key, reverse)
            time_complexity = "O(n^2)"
        elif algorithm == '선택 정렬':
            sorted_files, swap_count = selection_sort(
                files.copy(), key, reverse)
            time_complexity = "O(n^2)"
        elif algorithm == '삽입 정렬':
            sorted_files, swap_count = insertion_sort(
                files.copy(), key, reverse)
            time_complexity = "O(n^2)"
        elif algorithm == '퀵 정렬':
            sorted_files, swap_count = quick_sort(files.copy(), key, reverse)
            time_complexity = "O(n log n)"
        elif algorithm == '머지 정렬':
            sorted_files, swap_count = merge_sort(files.copy(), key, reverse)
            time_complexity = "O(n log n)"
        else:
            return None, None

        end_time = time.time() # 정렬 완료 시간을 기록
        print("정렬이 끝났습니다.\n")
        elapsed_time = end_time - start_time # 실행에 걸린 시간

        self.text_edit.append(
            f"Sorted using {algorithm} - {self.sort_criterion} - {self.sort_order}")
        self.text_edit.append(f"Time Complexity: {time_complexity}")
        self.text_edit.append(f"Total time: {elapsed_time:.2f} seconds")
        self.text_edit.append(f"Total swaps: {swap_count}")

        print(f"Sorted files: {sorted_files}\n")

        return algorithm, elapsed_time

    def read_files(self, folder_path):
        file_list = []
        for filename in os.listdir(folder_path):
            filepath = os.path.join(folder_path, filename)
            if os.path.isfile(filepath):
            # filepath가 실제로 파일인지 확인
                file_stats = os.stat(filepath)
                # os.stat(): 파일의 상태 정보 얻어옴
                file_list.append(File(filename, file_stats.st_size, datetime.fromtimestamp(
                    file_stats.st_ctime).strftime("%Y-%m-%d")))
                    # 파일 생성 날짜를 YYYY-MM-DD 형식의 문자열로 변환
        return file_list

    def create_dummy_files(self, folder_path):
        for i in range(100):
            file_name = f"dummy_file_{i}.txt" # 0~99까지 더미파일 생성
            with open(os.path.join(folder_path, file_name), 'w') as file:
                file.write("This is a dummy file.")
        self.text_edit.append(
            "100 dummy files created in the current directory.")


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
