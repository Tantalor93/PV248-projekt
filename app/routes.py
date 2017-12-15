from flask import request, jsonify
import networkx as nx

from app import app

responseInvalidInputError = {"solution": None, "length": None, "error": "Invalid input"}
responseNoSolutionFound = {"solution": None, "length": None, "status": "No solution found"}


@app.route('/')
def root_get():
    return "PV248-projekt"


@app.route('/', methods=['POST'])
def root_post():
    inputData = request.json
    start = inputData['start']
    end = inputData['end']
    rooms = inputData['rooms']
    corridors = inputData['corridors']

    graph = create_graph(rooms, corridors)

    if graph is None:
        return jsonify(responseInvalidInputError)
    if not (start in graph.nodes and end in graph.nodes):
        return jsonify(responseInvalidInputError)

    try:
        solution = nx.shortest_path(graph, source=start, target=end)
        return jsonify(create_response(solution))
    except nx.NetworkXNoPath:
        return jsonify(responseNoSolutionFound)


def create_graph(rooms, corridors):
    graph = nx.Graph()
    graph.add_nodes_from(rooms)
    for corridor in corridors:
        if not (corridor[0] in graph.nodes and corridor[1] in graph.nodes):
            return None

    graph.add_edges_from(corridors)
    return graph


def create_response(solution):
    return {"solution": solution, "length": len(solution), "status": "OK"}
