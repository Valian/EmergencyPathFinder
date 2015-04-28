import json
import logging

from emergency_path_finder import EmergencyPathFinder
from argparse import ArgumentParser

EDGES = [
    (1, 2, {'weight': 2}),
    (2, 3, {'weight': 1}),
    (3, 4, {'weight': 5}),
    (1, 3, {'weight': 6}),
    (2, 4, {'weight': 4}),
    (4, 5, {'weight': 70}),
    (5, 6, {'weight': 2.3}),
    (6, 7, {'weight': 3.2}),
    (7, 8, {'weight': 2.8}),
    (3, 5, {'weight': 2.8}),
    (1, 7, {'weight': 2}),
    (5, 9, {'weight': 5})
]

REMOVED_EDGE = (2, 3)


def get_args():
    parser = ArgumentParser(description="Application for finding paths in a graph in case of emergency edges.")
    parser.add_argument('-i', dest='input', type=str, help='path to json file containing list of edges, eg. input.json')
    parser.add_argument('-o', dest='output', type=str, help='path to output file, eg. out.txt')
    parser.add_argument('-r', dest='removed', type=int, nargs=2, help='edge to remove eg. 1 3')
    parser.add_argument('-d', action='store_true', dest='draw', help='Draw graphs')
    parser.add_argument('start', type=int, help='Start node number, eg. 1')
    parser.add_argument('end', type=int, help='End node number, eg. 3')

    return parser.parse_args()


def load_edges(filename):
    with open(filename) as f:
        try:
            return json.load(f)
        except Exception as e:
            logging.error("Error while loading file. More info: {0}".format(e))
            return None


def get_edge_data(args):
    if not args.input:
        logging.info("No input path, using default test data")
        return EDGES
    data = load_edges(args.input)
    if not data:
        logging.info("Using default test data")
        return EDGES
    return data['edges']


def get_removed_edges(args, path):
    if not args.removed:
        logging.info("No removed edge specified, iterating through all edges on path")
        return [(path[i], path[i+1]) for i in xrange(len(path) - 1)]

    return [tuple(args.removed)]


def log_path(finder, path):
    logging.info('distance: {0}, path {1}\n'.format(finder.get_path_length(path), '->'.join(map(str, path))))


def configure_logger(output):
    logging.basicConfig(filename=output, format='%(message)s', level=logging.DEBUG)


def log_input_data(edges):
    logging.info('Input graph:')
    for start, end, props in edges:
        logging.info('{0} -> {1}, weight: {2}'.format(start, end, props.get('weight', 1)))
    logging.info('')


def run():
    args = get_args()
    configure_logger(args.output)
    edges = get_edge_data(args)
    finder = EmergencyPathFinder(edges, args.start, args.end)

    log_input_data(edges)

    original_path = finder.get_original_path()
    logging.info('Original path from node {0} to node {1}'.format(args.start, args.end))
    log_path(finder, original_path)

    removed_edges = get_removed_edges(args, original_path)
    for removed_edge in removed_edges:
        emergency_path = finder.find_emergency_path(removed_edge)
        logging.info('Emergency path for removed edge {0}'.format(removed_edge, emergency_path))
        log_path(finder, emergency_path)
        if args.draw:
            finder.print_graph(removed_edge, emergency_path)

if __name__ == '__main__':
    run()
