import sys
import json
import networkx as nx
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QTextEdit, QMessageBox
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# 그래프 생성 함수
def create_graph_from_data(usernameList, outList, outWeight):
    G = nx.DiGraph()
    for username in usernameList:
        G.add_node(username)

    for i, out_edges in enumerate(outList):
        for j, target in enumerate(out_edges):
            # 가중치가 제공되었는지 확인
            if outWeight is not None:
                weight = outWeight[i][j]
                G.add_edge(usernameList[i], usernameList[target], weight=weight)
            else:
                # 가중치 없이 엣지 추가
                G.add_edge(usernameList[i], usernameList[target])

    return G


class GraphVisualizer(QMainWindow):
    def __init__(self, graph):
        super().__init__()
        self.graph = graph
        self.pos = nx.spring_layout(self.graph)
        self.initUI()

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
        path = nx.shortest_path(self.graph, start_node, end_node)
        self.path_output.setText(" -> ".join(path))
        self.update_graph(path)

    @pyqtSlot()
    def onDFS(self):
        start_node = self.start_node_dropdown.currentText()
        end_node = self.end_node_dropdown.currentText()
        paths = list(nx.all_simple_paths(self.graph, start_node, end_node))
        self.path_output.setText("\n".join([" -> ".join(path) for path in paths]))
        for path in paths:
            self.update_graph(path)

    def update_graph(self, path):
        ax = self.figure.add_subplot(111)
        ax.clear()
        nx.draw(self.graph, self.pos, ax=ax, with_labels=True, node_color='lightblue', edge_color='gray')
        edges_in_path = list(zip(path, path[1:]))
        nx.draw_networkx_nodes(self.graph, self.pos, nodelist=path, node_color='red', ax=ax)
        nx.draw_networkx_edges(self.graph, self.pos, edgelist=edges_in_path, edge_color='red', ax=ax)
        self.canvas.draw()

# 데이터 로드 및 메인 코드
if __name__ == '__main__':
    app = QApplication(sys.argv)
    font = QFont("Arial", 10)
    app.setFont(font)

    # 데이터 로드
    with open('congress_network_data.json', 'r') as file:
        data = json.load(file)
    inList = data[0]['inList']  # 첫 번째 요소에 접근
    outList = data[0]['outList']
    usernameList = data[0]['usernameList']

    # 그래프 생성
    G = create_graph_from_data(usernameList, outList, None)

    # GUI 실행
    visualizer = GraphVisualizer(G)
    visualizer.show()
    sys.exit(app.exec_())
