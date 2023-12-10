import sys
import os
import time
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QTextEdit, QFileDialog, QComboBox


class File:
    def __init__(self, name, size, creation_date):
        self.name = name
        self.size = size
        self.creation_date = creation_date

    def __repr__(self):
        return f"{self.name} ({self.size}, {self.creation_date})"


def bubble_sort(files, key, reverse=False):
    n = len(files)
    swap_count = 0
    for i in range(n):
        for j in range(0, n - i - 1):
            if (reverse and getattr(files[j], key) < getattr(files[j + 1], key)) or \
                    (not reverse and getattr(files[j], key) > getattr(files[j + 1], key)):
                files[j], files[j + 1] = files[j + 1], files[j]
                swap_count += 1
                print(f"Bubble Sort Step: {files}")
    return files, swap_count


def selection_sort(files, key, reverse=False):
    swap_count = 0
    for i in range(len(files)):
        idx = i
        for j in range(i+1, len(files)):
            if (reverse and getattr(files[j], key) > getattr(files[idx], key)) or \
                    (not reverse and getattr(files[j], key) < getattr(files[idx], key)):
                idx = j
        if idx != i:
            files[i], files[idx] = files[idx], files[i]
            swap_count += 1
            print(f"Selection Sort Step: {files}")
    return files, swap_count


def insertion_sort(files, key, reverse=False):
    swap_count = 0
    for i in range(1, len(files)):
        key_file = files[i]
        j = i - 1
        while j >= 0 and ((reverse and getattr(files[j], key) < getattr(key_file, key)) or
                          (not reverse and getattr(files[j], key) > getattr(key_file, key))):
            files[j + 1] = files[j]
            j -= 1
            swap_count += 1
            print(f"Insertion Sort Step: {files}")
        files[j + 1] = key_file
    return files, swap_count


def quick_sort(files, key, reverse=False):
    def _quick_sort(items, low, high):
        swap_count = 0
        if low < high:
            pivot_index, pivot_swap_count = partition(items, low, high)
            swap_count += pivot_swap_count
            left_swap_count = _quick_sort(items, low, pivot_index)
            right_swap_count = _quick_sort(items, pivot_index + 1, high)
            swap_count += left_swap_count + right_swap_count
        return swap_count

    def partition(items, low, high):
        pivot = getattr(items[(low + high) // 2], key)
        swap_count = 0
        while True:
            while (reverse and getattr(items[low], key) > pivot) or \
                    (not reverse and getattr(items[low], key) < pivot):
                low += 1
            while (reverse and getattr(items[high], key) < pivot) or \
                    (not reverse and getattr(items[high], key) > pivot):
                high -= 1
            if low >= high:
                return high, swap_count
            items[low], items[high] = items[high], items[low]
            swap_count += 1
            print(f"Quick Sort Swap: {items}")
            low += 1
            high -= 1

    total_swap_count = _quick_sort(files, 0, len(files) - 1)
    return files, total_swap_count


def merge_sort(files, key, reverse=False):
    def _merge_sort(items, swap_count):
        if len(items) > 1:
            mid = len(items) // 2
            left_half = items[:mid]
            right_half = items[mid:]

            swap_count = _merge_sort(left_half, swap_count)
            swap_count = _merge_sort(right_half, swap_count)

            i = j = k = 0
            while i < len(left_half) and j < len(right_half):
                if (reverse and getattr(left_half[i], key) > getattr(right_half[j], key)) or \
                        (not reverse and getattr(left_half[i], key) < getattr(right_half[j], key)):
                    items[k] = left_half[i]
                    i += 1
                else:
                    items[k] = right_half[j]
                    j += 1
                k += 1
                swap_count += 1
                print(f"Merge Sort Step: {items}")

            while i < len(left_half):
                items[k] = left_half[i]
                i += 1
                k += 1

            while j < len(right_half):
                items[k] = right_half[j]
                j += 1
                k += 1

        return swap_count

    swap_count = _merge_sort(files, 0)
    return files, swap_count


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.sort_order = "오름차순"
        self.sort_criterion = "파일 이름"
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
            self.create_dummy_files(folder_path)
        self.line_edit.setText(folder_path)

    def update_sort_criterion(self, index):
        self.sort_criterion = self.sort_criteria_dropdown.currentText()

    def update_sort_order(self, index):
        self.sort_order = self.sort_order_dropdown.currentText()

    def sort_files(self):
        sorting_algorithm = self.sender().text()
        folder_path = self.line_edit.text()

        if not folder_path:
            folder_path = os.getcwd()
            self.create_dummy_files(folder_path)
            self.line_edit.setText(folder_path)

        if sorting_algorithm == '전체 선택':
            results = []
            for alg in ['버블 정렬', '선택 정렬', '삽입 정렬', '퀵 정렬', '머지 정렬']:
                alg_name, alg_time = self.execute_sorting_algorithm(
                    alg, folder_path)
                results.append((alg_name, alg_time))
            fastest_alg = min(results, key=lambda x: x[1])
            self.text_edit.append(
                f"Fastest Algorithm: {fastest_alg[0]} with time {fastest_alg[1]:.2f} seconds")
        else:
            self.execute_sorting_algorithm(sorting_algorithm, folder_path)

    def execute_sorting_algorithm(self, algorithm, folder_path):
        files = self.read_files(folder_path)
        reverse = True if self.sort_order == "내림차순" else False
        key = "size" if self.sort_criterion == "크기" else "creation_date" if self.sort_criterion == "생성 날짜" else "name"

        swap_count = 0
        time_complexity = ""
        start_time = time.time()
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

        end_time = time.time()
        print("정렬이 끝났습니다.\n")
        elapsed_time = end_time - start_time

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
                file_stats = os.stat(filepath)
                file_list.append(File(filename, file_stats.st_size, datetime.fromtimestamp(
                    file_stats.st_ctime).strftime("%Y-%m-%d")))
        return file_list

    def create_dummy_files(self, folder_path):
        for i in range(100):
            file_name = f"dummy_file_{i}.txt"
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
