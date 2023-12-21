import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv


class TreeNode:
    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone
        self.height = 1
        self.left = None
        self.right = None


class AVLTree:
    def __init__(self):
        self.root_node = None  # root_node를 AVLTree의 속성으로 추가

    def insert_node(self, name, email, phone):
        self.root_node = self.insert(self.root_node, name, email, phone)

    def delete_node(self, key):
        self.root_node = self.delete(self.root_node, key)

    def visualize(self, node=None, indent="", last='updown'):
        if node is None:
            node = self.root_node

        # 시각화 로직
        if node is not None:
            up = '┌── '
            down = '└── '
            extend = '    '
            tee = '├── '
            if last == 'up':
                joint = up
                extend = '│   '
            elif last == 'down':
                joint = down
            else:
                joint = tee
            line = f"{indent}{joint}{node.name}"

            if node.left or node.right:
                if node.right:
                    ext = extend if node.left else '    '
                    line += '\n' + \
                        self.visualize(node.right, f"{indent}{ext}", 'up')
                if node.left:
                    line += '\n' + \
                        self.visualize(node.left, f"{indent}{extend}", 'down')
            return line
        return ''

    def print_tree(self):
        # 시각화된 트리를 문자열로 가져온다.
        visualization = self.visualize(self.root_node)
        # 전체 트리 출력의 끝에만 줄바꿈을 추가한다.
        print(visualization + "\n")

    def insert(self, root, name, email, phone):
        if not root:
            return TreeNode(name, email, phone)

        if self.compare_names(name, root.name) < 0:
            root.left = self.insert(root.left, name, email, phone)
        else:
            root.right = self.insert(root.right, name, email, phone)

        # 2. Update the height of the ancestor node
        root.height = 1 + max(self.getHeight(root.left),
                                self.getHeight(root.right))

        # 3. Get the balance factor
        balance = self.getBalance(root)

        # 4. If the node is unbalanced, then try out the 4 cases
        # Case 1 - Left Left
        if balance > 1 and name < root.left.name:
            return self.rightRotate(root)

        # Case 2 - Right Right
        if balance < -1 and name > root.right.name:
            return self.leftRotate(root)

        # Case 3 - Left Right
        if balance > 1 and name > root.left.name:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)

        # Case 4 - Right Left
        if balance < -1 and name < root.right.name:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)

        return root

    def compare_names(self, name1, name2):
        # 한글 자음과 모음의 순서
        consonants = 'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ'
        vowels = 'ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ'

        # 이름을 비교하는 로직
        for char1, char2 in zip(name1, name2):
            # 자음 또는 모음인 경우 순서 비교
            if char1 in consonants and char2 in consonants:
                if consonants.index(char1) != consonants.index(char2):
                    return consonants.index(char1) - consonants.index(char2)
            elif char1 in vowels and char2 in vowels:
                if vowels.index(char1) != vowels.index(char2):
                    return vowels.index(char1) - vowels.index(char2)
            # 일반 문자열 비교
            elif char1 != char2:
                return (char1 > char2) - (char1 < char2)
        return len(name1) - len(name2)

    def leftRotate(self, z):
        y = z.right
        T2 = y.left

        # Perform rotation
        y.left = z
        z.right = T2

        # Update heights
        z.height = 1 + max(self.getHeight(z.left), self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left), self.getHeight(y.right))

        # Return the new root
        return y

    def rightRotate(self, y):
        x = y.left
        T2 = x.right

        # Perform rotation
        x.right = y
        y.left = T2

        # Update heights
        y.height = 1 + max(self.getHeight(y.left), self.getHeight(y.right))
        x.height = 1 + max(self.getHeight(x.left), self.getHeight(x.right))

        # Return the new root
        return x

    def getHeight(self, root):
        if not root:
            return 0
        return root.height

    def getBalance(self, root):
        if not root:
            return 0
        return self.getHeight(root.left) - self.getHeight(root.right)

    def preOrder(self, root):
        if not root:
            return
        print("{0} ".format(root.name), end="")
        self.preOrder(root.left)
        self.preOrder(root.right)

    def delete(self, root, key):
        if not root:
            return root

        if self.compare_names(key, root.name) < 0:
            root.left = self.delete(root.left, key)
        elif self.compare_names(key, root.name) > 0:
            root.right = self.delete(root.right, key)
        else:
            if root.left is None:
                temp = root.right
                root = None
                return temp

            elif root.right is None:
                temp = root.left
                root = None
                return temp

            temp = self.getMinValueNode(root.right)
            root.name = temp.name
            root.email = temp.email
            root.phone = temp.phone
            root.right = self.delete(root.right, temp.name)

        # If the tree has only one node, simply return it
        if root is None:
            return root

        # 2. Update the height of the current node
        root.height = 1 + max(self.getHeight(root.left),
                                self.getHeight(root.right))

        # 3. Get the balance factor
        balance = self.getBalance(root)

        # 4. Balance the tree
        # Left Left
        if balance > 1 and self.getBalance(root.left) >= 0:
            return self.rightRotate(root)

        # Left Right
        if balance > 1 and self.getBalance(root.left) < 0:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)

        # Right Right
        if balance < -1 and self.getBalance(root.right) <= 0:
            return self.leftRotate(root)

        # Right Left
        if balance < -1 and self.getBalance(root.right) > 0:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)

        return root

    def getMinValueNode(self, root):
        if root is None or root.left is None:
            return root
        return self.getMinValueNode(root.left)


class AddressBookGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AVL 기반 주소록 관리 시스템")

        # AVL 트리 초기화
        self.avl_tree = AVLTree()
        self.root_node = None

        # GUI 요소 설정
        self.setup_ui()

    def setup_ui(self):
        # 메뉴 버튼
        self.menu_button = tk.Menubutton(
            self.root, text="메뉴", relief=tk.RAISED)
        self.menu = tk.Menu(self.menu_button, tearoff=0)
        self.menu.add_command(label="파일 불러오기", command=self.load_csv)
        self.menu.add_command(label="저장", command=self.save_to_csv)
        self.menu_button['menu'] = self.menu
        self.menu_button.grid(row=0, column=0, padx=10, pady=10)

        # 선택삭제 버튼
        self.delete_selected_button = tk.Button(
            self.root, text="선택삭제", command=self.delete_selected)
        self.delete_selected_button.grid(row=0, column=1, padx=10, pady=10)

        # 전체삭제 버튼
        self.delete_all_button = tk.Button(
            self.root, text="전체삭제", command=self.delete_all)
        self.delete_all_button.grid(row=0, column=2, padx=10, pady=10)

        # 수정 버튼
        self.edit_button = tk.Button(
            self.root, text="수정", command=self.toggle_edit_mode)
        self.edit_button.grid(row=0, column=3, padx=10, pady=10)

        # 입력 필드
        self.name_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.email_var = tk.StringVar()

        tk.Label(self.root, text="이름").grid(row=1, column=0, padx=10, pady=5)
        tk.Entry(self.root, textvariable=self.name_var).grid(
            row=1, column=1, padx=10, pady=5)

        tk.Label(self.root, text="전화번호").grid(row=2, column=0, padx=10, pady=5)
        tk.Entry(self.root, textvariable=self.phone_var).grid(
            row=2, column=1, padx=10, pady=5)

        tk.Label(self.root, text="이메일").grid(row=3, column=0, padx=10, pady=5)
        tk.Entry(self.root, textvariable=self.email_var).grid(
            row=3, column=1, padx=10, pady=5)

        # 입력 버튼
        tk.Button(self.root, text="입력", command=self.add_contact).grid(
            row=4, column=1, padx=10, pady=5, sticky=tk.E)

        # 검색 필드
        self.search_var = tk.StringVar()
        tk.Entry(self.root, textvariable=self.search_var).grid(
            row=5, column=0, padx=10, pady=5, columnspan=2, sticky=tk.EW)
        tk.Button(self.root, text="검색", command=self.search_contact).grid(
            row=5, column=2, padx=10, pady=5)

        # 주소록 표시 트리뷰
        self.tree = ttk.Treeview(self.root, columns=(
            "Name", "Phone", "Email"), show='headings')
        self.tree.heading("Name", text="이름")
        self.tree.heading("Phone", text="전화번호")
        self.tree.heading("Email", text="이메일")
        self.tree.grid(row=6, column=0, columnspan=3,
                    padx=10, pady=10, sticky='nsew')

        # 트리뷰 스크롤바
        self.scrollbar = ttk.Scrollbar(
            self.root, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(row=6, column=3, pady=10, sticky='ns')

        # 트리뷰 스타일 설정
        style = ttk.Style()
        style.theme_use("default")
        style.map('Treeview')

    def delete_selected(self):
        # 선택된 연락처를 삭제하는 기능
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("경고", "삭제할 항목을 선택하세요.")
            return
        for item in selected_items:
            item_values = self.tree.item(item)['values']
            # 트리뷰와 AVL 트리에서 삭제
            self.tree.delete(item)
            self.root_node = self.avl_tree.delete(
                self.root_node, item_values[0])

        self.avl_tree.delete_node(item_values[0])
        self.avl_tree.print_tree()  # 시각화 함수 호출

    def delete_all(self):
        # 사용자 확인 후 전체 삭제 진행
        if messagebox.askyesno("확인", "모든 연락처를 삭제하시겠습니까?"):
            # 트리뷰의 모든 항목 삭제
            self.tree.delete(*self.tree.get_children())
            # AVL 트리를 새로운 비어있는 상태로 재설정
            self.avl_tree = AVLTree()
            # 콘솔 창에 AVL 트리 시각화를 업데이트하여 비어있음을 표시
            self.avl_tree.print_tree()

    def toggle_edit_mode(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("경고", "수정할 연락처를 선택하세요.")
            return

        if self.edit_button.cget('text') == '수정':
            # '수정' 모드로 변경
            self.selected = self.tree.item(selected_item[0])['values']
            self.name_var.set(self.selected[0])
            self.phone_var.set(self.selected[1])
            self.email_var.set(self.selected[2])
            self.edit_button.config(text='완료')
        else:
            # 변경 사항을 적용하고 '수정' 모드를 종료
            self.update_contact(selected_item[0])
            self.edit_button.config(text='수정')

    def update_contact(self, item_id):
        # 기존 정보 가져오기
        original_name = self.tree.item(item_id)['values'][0]

        # 입력 필드에서 정보 가져오기
        updated_name = self.name_var.get()
        updated_phone = self.phone_var.get()
        updated_email = self.email_var.get()

        # AVL 트리에서 기존 노드를 삭제
        self.avl_tree.delete_node(original_name)

        # AVL 트리에 수정된 정보로 새 노드를 삽입
        self.avl_tree.insert_node(updated_name, updated_email, updated_phone)

        # 트리뷰의 항목 업데이트
        self.tree.item(item_id, values=(
            updated_name, updated_phone, updated_email))

        # AVL 트리 시각화를 업데이트
        self.avl_tree.print_tree()

        # 입력 필드 초기화
        self.name_var.set("")
        self.phone_var.set("")
        self.email_var.set("")

    def load_csv(self):
        filename = filedialog.askopenfilename(
            title="Open CSV",
            filetypes=[("CSV files", "*.csv")],
            initialdir="."
        )
        if not filename:
            return

        # 트리뷰의 모든 항목 삭제
        self.tree.delete(*self.tree.get_children())

        # AVL 트리를 새로 초기화
        self.avl_tree = AVLTree()

        with open(filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)  # 첫 번째 줄(헤더)을 건너뜀

            for row in reader:
                if len(row) == 3:
                    # 트리뷰에 연락처 추가
                    self.tree.insert('', tk.END, values=row)
                    # AVL 트리에 연락처 추가
                    self.avl_tree.insert_node(*row)

            # 콘솔 창에 AVL 트리 시각화 출력
            self.avl_tree.print_tree()

    def save_to_csv(self):
        # 현재 주소록을 CSV 파일로 저장하는 함수
        filename = filedialog.asksaveasfilename(
            title="Save CSV",
            filetypes=[("CSV files", "*.csv")],
            defaultextension=".csv",
            initialdir="./"  # 현재 스크립트가 있는 디렉토리를 기본 경로로 설정
        )
        if not filename:
            return  # 사용자가 파일 선택을 취소한 경우

        # CSV 파일로 저장
        with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            # 헤더 작성
            csv_writer.writerow(["이름", "전화번호", "이메일"])
            # 트리뷰의 내용을 순회하며 CSV 파일에 작성
            for child in self.tree.get_children():
                csv_writer.writerow(self.tree.item(child)['values'])

    # 연락처 추가 함수
    def add_contact(self):
        name = self.name_var.get()
        phone = self.phone_var.get()
        email = self.email_var.get()

        # 연락처 입력 검증
        if not (name and phone and email):
            messagebox.showerror("오류", "모든 필드를 채워주세요.")
            return

        # AVL 트리에 연락처 추가
        self.avl_tree.insert_node(name, email, phone)

        # 트리뷰에 연락처 추가
        self.tree.insert('', 'end', values=(name, phone, email))

        # AVL 트리 시각화
        self.avl_tree.print_tree()

        # 입력 필드 초기화
        self.name_var.set("")
        self.phone_var.set("")
        self.email_var.set("")

    def search_contact(self):
        # 연락처 검색 함수
        search_query = self.search_var.get().strip()
        if not search_query:
            messagebox.showerror("오류", "검색어를 입력해주세요.")
            return

        # 검색 결과를 담을 변수
        found_items = []

        # 트리뷰의 모든 항목을 순회하면서 정확히 일치하는 연락처를 찾는다
        for child in self.tree.get_children():
            item = self.tree.item(child)['values']
            # 정확히 일치하는 경우를 검사한다 (대소문자를 구분하지 않음)
            if search_query.lower() == str(item[0]).lower() or search_query == str(item[1]) or search_query.lower() == str(item[2]).lower():
                found_items.append(child)

        # 검색 결과에 따라 다른 액션 수행
        if found_items:
            # 검색된 항목들을 선택하고 보여준다
            self.tree.selection_set(found_items)
            self.tree.see(found_items[0])
        else:
            # 검색된 항목이 없으면 메시지를 표시
            messagebox.showinfo("결과", "정확히 일치하는 연락처가 없습니다.")


# 메인 코드
if __name__ == "__main__":
    root = tk.Tk()
    app = AddressBookGUI(root)
    root.mainloop()
