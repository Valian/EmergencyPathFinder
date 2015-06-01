import networkx as nx
import matplotlib.pyplot as plt

from dijkstra import find_path


class EmergencyPathFinder(object):
    def __init__(self, edges, starting_node, ending_node):
        self.graph = nx.Graph(edges)
        self.starting_node = starting_node
        self.ending_node = ending_node
        self.pos = nx.fruchterman_reingold_layout(self.graph)
        self.original_path = find_path(self.graph, starting_node, ending_node)

    def get_original_path(self):
        return self.original_path

    def find_emergency_path(self, removed_edge):
        graph = self.graph.copy()
        graph.remove_edge(*removed_edge)

        return find_path(graph, self.starting_node, self.ending_node)

    def get_path_length(self, path):
        return sum(self.graph[path[i]][path[i+1]].get('weight', 1) for i in xrange(len(path) - 1))

    def print_graph(self, deleted_edge=None, emergency_path=None):
        edge_labels = dict([((u, v), self.graph[u][v].get('weight', 1)) for u, v, d in self.graph.edges(data=True)])
        nx.draw_networkx(self.graph, self.pos, with_labels=True, edge_color='b')
        nx.draw_networkx_edge_labels(self.graph, self.pos, edge_labels=edge_labels)

        if self.original_path:
            self._draw_path(self.original_path, self.pos, edge_color='g', width=5, alpha=0.5)

        if deleted_edge:
            self._draw_path(deleted_edge, self.pos, edge_color='r', width=5, style='dashed')

        if emergency_path:
            self._draw_path(emergency_path, self.pos, edge_color='y', width=5, alpha=0.8)

        plt.axis('off')
        plt.legend((
            'nodes', 'edges', 'original path, dist: {0}'.format(self._get_path_length_label(self.original_path)),
            'removed edge {0}'.format(deleted_edge),
            'emergency path, dist: {0}'.format(self._get_path_length_label(emergency_path))))
        plt.show()

    def _get_path_length_label(self, path):
        return self.get_path_length(path) if path else 'None'

    @staticmethod
    def _draw_path(path, pos, **kwargs):
        graph = nx.Graph()
        graph.add_path(path)
        nx.draw_networkx_edges(graph, pos, **kwargs)


