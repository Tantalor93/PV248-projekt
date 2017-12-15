# author: Ondrej Benkovsky (422583)
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
    if not (start in graph.nodes and end in graph.nodes):  # check that start and end are valid rooms
        return jsonify(responseInvalidInputError)

    try:
        solution = nx.shortest_path(graph, source=start, target=end)  # find shortest path from start to end
        return jsonify(create_response(solution))
    except nx.NetworkXNoPath:
        return jsonify(responseNoSolutionFound)


def create_graph(rooms, corridors):
    graph = nx.Graph()
    for room in rooms:
        if room in graph.nodes:  # checking duplicates
            return None
        graph.add_node(room)

    for corridor in corridors:
        if not (corridor[0] in graph.nodes and corridor[1] in graph.nodes):  # check that both ends of edge exists
            return None

    graph.add_edges_from(corridors)
    return graph


def create_response(solution):
    return {"solution": solution, "length": len(solution), "status": "OK"}
