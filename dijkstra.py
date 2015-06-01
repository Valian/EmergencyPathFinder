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
                # calculate distance between start node and current node
                current_distance = graph[node][n].get('weight', 1) + node_info[node]['dist']
                prev_distance = node_info[n]['dist']
                # if calculated distance is smaller than previous distance, change results
                if current_distance < prev_distance:
                    node_info[n]['dist'] = current_distance
                    node_info[n]['prev'] = node
                    heapq.heappush(heap, (current_distance, n))

        # we take nodes from stack until we find unvisted one
        while node in visited:
            if len(heap) == 0:
                return None
            dist, node = heapq.heappop(heap)

    # rebuild path from end node to start node using nodes that we came from
    path = []
    while finish != -1:
        path.append(finish)
        finish = node_info[finish]['prev']

    return path