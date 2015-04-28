import networkx
import heapq

INF = 1000000


def find_path(graph, start, finish):
    visited = set()
    node_info = {node: {'prev': -1, 'dist': INF if node != start else 0} for node in graph}
    heap = []

    node = start
    while node != finish:
        visited.add(node)
        for n in graph.neighbors_iter(node):
            if n not in visited:
                current_distance = graph[node][n].get('weight', 1) + node_info[node]['dist']
                prev_distance = node_info[n]['dist']
                if current_distance < prev_distance:
                    node_info[n]['dist'] = current_distance
                    node_info[n]['prev'] = node
                    heapq.heappush(heap, (current_distance, n))

        while node in visited:
            if len(heap) == 0:
                return None
            dist, node = heapq.heappop(heap)

    path = []
    while finish != -1:
        path.append(finish)
        finish = node_info[finish]['prev']

    return path