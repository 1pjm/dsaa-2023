import json
import sys
from PyQt5.QtWidgets import QApplication
import networkx as nx

# viral_centrality.py에서 함수 불러오기
from viral_centrality import viral_centrality

# graphVisualizer.py에서 class 불러오기
from graphVisualizer import GraphVisualizer

# 그래프 생성 함수 정의
def create_graph_from_data(usernameList, outList, outWeight):
    import networkx as nx
    G = nx.DiGraph()
    for username in usernameList:
        G.add_node(username)

    for i, out_edges in enumerate(outList):
        for j, target in enumerate(out_edges):
            G.add_edge(usernameList[i], usernameList[target], weight=outWeight[i][j])

    return G

# 데이터 로드
with open('congress_network_data.json', 'r') as file:
    data = json.load(file)

# 데이터에서 필요한 정보 추출
inList = data[0]['inList']
inWeight = data[0]['inWeight']
outList = data[0]['outList']
outWeight = data[0]['outWeight']
usernameList = data[0]['usernameList']

# 그래프 구성
G = create_graph_from_data(usernameList, outList, outWeight)

# Viral Centrality 계산
viral_centralities = viral_centrality(inList, inWeight, outList)

# 메인 코드
if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 여기서 G를 GraphVisualizer에 전달합니다.
    visualizer = GraphVisualizer(G)  # 수정된 부분
    visualizer.show()
    sys.exit(app.exec_())
