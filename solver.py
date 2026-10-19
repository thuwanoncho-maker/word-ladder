from collections import deque


def bfs(graph, start, goal):
    """BFS ด้วย Queue: คืนค่า (เส้นทางสั้นสุด, จำนวนคำที่สำรวจ)"""
    queue = deque([start])
    parent = {start: None}
    explored = 0

    while queue:
        word = queue.popleft()
        explored += 1
        if word == goal:
            path = []
            while word is not None:
                path.append(word)
                word = parent[word]
            return path[::-1], explored
        for nxt in graph[word]:
            if nxt not in parent:
                parent[nxt] = word
                queue.append(nxt)
    return None, explored


def dfs(graph, start, goal):
    """DFS ด้วย Stack: คืนค่า (เส้นทางที่เจอ, จำนวนคำที่สำรวจ)"""
    stack = [start]
    parent = {start: None}
    explored = 0

    while stack:
        word = stack.pop()
        explored += 1
        if word == goal:
            path = []
            while word is not None:
                path.append(word)
                word = parent[word]
            return path[::-1], explored
        for nxt in graph[word]:
            if nxt not in parent:
                parent[nxt] = word
                stack.append(nxt)
    return None, explored