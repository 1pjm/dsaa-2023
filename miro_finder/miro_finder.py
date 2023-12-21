def get_maze_answer(maze, end_point=(1, 1)):
    # 미로의 크기를 구합니다
    max_x = max(coord[0] for coord in maze.keys())
    max_y = max(coord[1] for coord in maze.keys())
    start_point = (max_x, max_y)
    
    stack = [(start_point, [start_point])]
    visited = set()
    
    while stack:
        print(f"현재 스택: {stack}")  # 현재 스택을 출력합니다.
        position, path = stack.pop()
        if position in visited:
            continue
        visited.add(position)
        
        # 종료 지점에 도달했는지 확인합니다.
        if position == end_point:
            return path
        
        # 이동 가능한 방향: 동(E), 서(W), 북(N), 남(S)
        directions = {'E': (0, 1), 'W': (0, -1), 'N': (-1, 0), 'S': (1, 0)}
        for direction, (dx, dy) in directions.items():
            next_x, next_y = position[0] + dx, position[1] + dy
            next_position = (next_x, next_y)
            
            # next_position이 미로 범위 내에 있고 방문하지 않았는지 확인합니다.
            if 1 <= next_x <= max_x and 1 <= next_y <= max_y and maze[position][direction] and next_position not in visited:
                stack.append((next_position, path + [next_position]))
    
    # 경로를 찾지 못한 경우
    return None
