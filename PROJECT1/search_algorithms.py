from collections import deque
import heapq
import time
import graph_setup  # for haversine_distance if needed


def bfs(graph, start, goal, max_time=5.0):
    """
    Breadth-First Search (BFS) for an unweighted graph,
    returning (path, cost) or (None, float('inf')) if not found or time-out.
    """
    start_time = time.perf_counter()
    queue = deque([(start, [start])])
    visited = set()

    while queue:
        # Time-out check
        if (time.perf_counter() - start_time) > max_time:
            print("BFS timed out!")
            return None, float('inf')

        current, path = queue.popleft()
        if current == goal:
            return path, len(path) - 1  # BFS "cost" in edges

        if current not in visited:
            visited.add(current)
            for neighbor in graph.get(current, []):
                queue.append((neighbor, path + [neighbor]))

    return None, float('inf')


def dfs(graph, start, goal, max_time=5.0):
    """
    Depth-First Search (DFS),
    returning (path, cost) or (None, float('inf')) if not found or time-out.
    """
    start_time = time.perf_counter()
    stack = [(start, [start])]
    visited = set()

    while stack:
        if (time.perf_counter() - start_time) > max_time:
            print("DFS timed out!")
            return None, float('inf')

        current, path = stack.pop()
        if current == goal:
            return path, len(path) - 1

        if current not in visited:
            visited.add(current)
            for neighbor in reversed(graph.get(current, [])):
                stack.append((neighbor, path + [neighbor]))

    return None, float('inf')


def id_dfs(graph, start, goal, max_depth=10, max_time=5.0):
    """
    Iterative Deepening DFS up to max_depth,
    returning (path, cost) or (None, float('inf')) if not found or time-out.
    """
    start_time = time.perf_counter()

    def dls(node, goal, depth, path):
        # Time-out check in recursion
        if (time.perf_counter() - start_time) > max_time:
            return None  # Signal time-out at this deeper level

        if node == goal:
            return path, len(path) - 1

        if depth == 0:
            return None

        for neighbor in graph.get(node, []):
            if neighbor not in path:
                result = dls(neighbor, goal, depth - 1, path + [neighbor])
                if result:
                    return result
        return None

    for depth in range(max_depth + 1):
        result = dls(start, goal, depth, [start])
        if result:
            return result

    return None, float('inf')


def best_first_search(graph, start, goal, coordinates, max_time=5.0):
    """
    Best-First Search using a heuristic = straight-line distance to goal,
    returning (path, cost) or (None, float('inf')) if not found or time-out.
    """
    start_time = time.perf_counter()

    def heuristic(city):
        return graph_setup.haversine_distance(city, goal, coordinates)

    visited = set()
    queue = [(heuristic(start), [start])]

    while queue:
        if (time.perf_counter() - start_time) > max_time:
            print("Best-First Search timed out!")
            return None, float('inf')

        _, path = heapq.heappop(queue)
        current = path[-1]

        if current == goal:
            return path, len(path) - 1

        if current not in visited:
            visited.add(current)
            for neighbor in graph.get(current, []):
                heapq.heappush(queue, (heuristic(neighbor), path + [neighbor]))

    return None, float('inf')


def a_star_search(graph, start, goal, coordinates, max_time=5.0):
    """
    A* Search using Haversine for both heuristic and path cost,
    returning (path, cost) or (None, float('inf')) if not found or time-out.
    """
    start_time = time.perf_counter()

    def heuristic(city):
        return graph_setup.haversine_distance(city, goal, coordinates)

    queue = [(0, 0, [start])]  # (f, g, path)
    visited = {}

    while queue:
        if (time.perf_counter() - start_time) > max_time:
            print("A* timed out!")
            return None, float('inf')

        f, g_cost, path = heapq.heappop(queue)
        current = path[-1]

        if current == goal:
            return path, g_cost

        # Only proceed if not visited or found cheaper cost
        if current not in visited or g_cost < visited[current]:
            visited[current] = g_cost
            for neighbor in graph.get(current, []):
                travel_cost = graph_setup.haversine_distance(current, neighbor, coordinates)
                new_g = g_cost + travel_cost
                new_f = new_g + heuristic(neighbor)
                heapq.heappush(queue, (new_f, new_g, path + [neighbor]))

    return None, float('inf')
