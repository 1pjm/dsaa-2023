import sys, time
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QTextEdit, QMessageBox
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal
from PyQt5.QtGui import QFont
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class PathFindingThread(QThread):
    update_graph_signal = pyqtSignal(list)

    def __init__(self, graph, start, end, method):
        QThread.__init__(self)
        self.graph = graph
        self.start = start
        self.end = end
        self.method = method

    def run(self):
        if self.method == 'BFS':
            path = nx.shortest_path(self.graph, self.start, self.end)
            self.update_graph_signal.emit([path])  # Emit a single path for BFS
        elif self.method == 'DFS':
            all_paths = list(nx.all_simple_paths(self.graph, self.start, self.end))
            for path in all_paths:
                self.update_graph_signal.emit([path])  # Emit paths one at a time for DFS
                time.sleep(1)  # Add a delay to visualize the paths one by one

class GraphVisualizer(QMainWindow):
    def __init__(self, graph):
        super().__init__()
        self.graph = graph
        self.update_positions()
        self.initUI()
        self.path_thread = None

    def update_positions(self):
        self.pos = nx.spring_layout(self.graph)  # Update node positions

    def initUI(self):
        self.setWindowTitle('Graph Visualizer')
        self.setGeometry(100, 100, 800, 600)
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        layout = QVBoxLayout(self.main_widget)

        self.start_node_dropdown = QComboBox(self)
        self.end_node_dropdown = QComboBox(self)
        self.start_node_dropdown.addItems(list(self.graph.nodes))
        self.end_node_dropdown.addItems(list(self.graph.nodes))

        layout.addWidget(QLabel('Start Node:'))
        layout.addWidget(self.start_node_dropdown)
        layout.addWidget(QLabel('End Node:'))
        layout.addWidget(self.end_node_dropdown)

        self.bfs_button = QPushButton('BFS', self)
        self.bfs_button.clicked.connect(self.onBFS)
        layout.addWidget(self.bfs_button)

        self.dfs_button = QPushButton('DFS', self)
        self.dfs_button.clicked.connect(self.onDFS)
        layout.addWidget(self.dfs_button)

        self.path_output = QTextEdit(self)
        self.path_output.setReadOnly(True)
        layout.addWidget(self.path_output)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

    @pyqtSlot()
    def onBFS(self):
        start_node = self.start_node_dropdown.currentText()
        end_node = self.end_node_dropdown.currentText()
        self.path_output.clear()
        if self.path_thread is not None and self.path_thread.isRunning():
            self.path_thread.terminate()
        self.path_thread = PathFindingThread(self.graph, start_node, end_node, 'BFS')
        self.path_thread.update_graph_signal.connect(self.update_graph)
        
        # start 메서드 호출 전 상태 확인
        if isinstance(self.path_thread, PathFindingThread):
            self.path_thread.start()
        else:
            QMessageBox.critical(self, "Error", "PathFindingThread is not correctly initialized")


    @pyqtSlot()
    def onDFS(self):
        start_node = self.start_node_dropdown.currentText()
        end_node = self.end_node_dropdown.currentText()
        self.path_output.clear()
        if self.path_thread is not None:  # Terminate existing thread
            self.path_thread.terminate()
        self.path_thread = PathFindingThread(self.graph, start_node, end_node, 'DFS')
        self.path_thread.update_graph_signal.connect(self.update_graph)
        self.path_thread.start()

    def update_graph(self, paths):
        ax = self.figure.gca()
        ax.clear()
        nx.draw(self.graph, self.pos, ax=ax, with_labels=True, node_color='lightblue', edge_color='gray')
        for path in paths:
            if path:
                edges_in_path = list(zip(path, path[1:]))
                nx.draw_networkx_nodes(self.graph, self.pos, nodelist=path, node_color='red', ax=ax)
                nx.draw_networkx_edges(self.graph, self.pos, edgelist=edges_in_path, edge_color='red', width=2, ax=ax)
        self.canvas.draw()
