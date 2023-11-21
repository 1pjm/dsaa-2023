import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QTextEdit

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Set main window title and initial size
        self.setWindowTitle('Sample Application')
        self.setGeometry(100, 100, 600, 300)

        # Create central widget and set it to the main window
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create layouts
        main_layout = QVBoxLayout(central_widget)  # Main vertical layout
        top_layout = QHBoxLayout()  # Top horizontal layout
        middle_layout = QHBoxLayout()  # Middle horizontal layout
        bottom_layout = QVBoxLayout()  # Bottom vertical layout

        # Create top layout widgets
        button1 = QPushButton('Button 1')
        button2 = QPushButton('Button 2')
        button3 = QPushButton('Button 3')

        # Add widgets to top layout
        top_layout.addWidget(button1)
        top_layout.addWidget(button2)
        top_layout.addWidget(button3)

        # Create middle layout widgets
        label1 = QLabel('Label 1')
        line_edit = QLineEdit()
        button4 = QPushButton('Button 4')

        # Add widgets to middle layout
        middle_layout.addWidget(label1)
        middle_layout.addWidget(line_edit)
        middle_layout.addWidget(button4)

        # Create bottom layout widget
        text_edit = QTextEdit()

        # Add widget to bottom layout
        bottom_layout.addWidget(text_edit)

        # Add sub-layouts to main layout
        main_layout.addLayout(top_layout)
        main_layout.addLayout(middle_layout)
        main_layout.addLayout(bottom_layout)

        # Set layout to the central widget
        central_widget.setLayout(main_layout)

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()