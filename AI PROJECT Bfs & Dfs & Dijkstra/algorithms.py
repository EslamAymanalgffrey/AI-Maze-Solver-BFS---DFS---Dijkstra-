from collections import deque
import heapq


def get_neighbors(node, grid, rows, cols):
    r, c = node
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != 'wall':
            yield (nr, nc)


def bfs(grid, start, goal, rows, cols):
    queue = deque([start])
    visited = {start}
    parent = {}
    order = []

    while queue:
        node = queue.popleft()
        order.append(node)

        if node == goal:
            break

        for n in get_neighbors(node, grid, rows, cols):
            if n not in visited:
                visited.add(n)
                parent[n] = node
                queue.append(n)

    return order, parent


def dfs(grid, start, goal, rows, cols):
    stack = [start]
    visited = {start}
    parent = {}
    order = []

    while stack:
        node = stack.pop()
        order.append(node)

        if node == goal:
            break

        for n in get_neighbors(node, grid, rows, cols):
            if n not in visited:
                visited.add(n)
                parent[n] = node
                stack.append(n)

    return order, parent


def dijkstra(grid, start, goal, rows, cols):
    heap = [(0, start)]
    visited = set()
    parent = {}
    cost = {start: 0}
    order = []

    while heap:
        c, node = heapq.heappop(heap)

        if node in visited:
            continue

        visited.add(node)
        order.append(node)

        if node == goal:
            break

        for n in get_neighbors(node, grid, rows, cols):
            new_cost = c + 1
            if n not in cost or new_cost < cost[n]:
                cost[n] = new_cost
                parent[n] = node
                heapq.heappush(heap, (new_cost, n))

    return order, parent


def reconstruct_path(parent, start, goal):
    if goal not in parent and goal != start:
        return []

    path = []
    node = goal

    while node != start:
        path.append(node)
        node = parent[node]

    path.append(start)
    path.reverse()
    return path