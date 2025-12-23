import time
import math
import importlib.util
import os
from pathlib import Path

import Bellman_Ford

# Load Dijkstra module from file with a valid module name
_here = Path(__file__).resolve().parent
_dijkstra_path = _here / "Dijkstras-Shortest-Path-Algorithm.py"
_spec = importlib.util.spec_from_file_location("dijkstra_module", _dijkstra_path)
_dijkstra_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_dijkstra_module)  # type: ignore

import Johnson


def run_dijkstra(graph, start, end):
    start_time = time.perf_counter()
    path, dist = _dijkstra_module.dijkstra(graph, start, end)
    end_time = time.perf_counter()
    return dist, end_time - start_time


def run_bellman_ford(graph, start, end):
    bf_graph = {u: [(w, v) for v, w in adj] for u, adj in graph.items()}

    start_time = time.perf_counter()
    distances = Bellman_Ford.Bellman_Ford(bf_graph, start)
    end_time = time.perf_counter()

    if isinstance(distances, str):
        return math.inf, end_time - start_time

    return distances.get(end, math.inf), end_time - start_time


def run_johnson(graph, start, end):
    vertices = list(graph.keys())
    edges = [
        (u, v, w)
        for u, adj in graph.items()
        for v, w in adj
    ]

    start_time = time.perf_counter()
    all_pairs = Johnson.johnson(vertices, edges)
    end_time = time.perf_counter()

    return all_pairs[start][end], end_time - start_time


def build_tests():
    # Small positive-weight graph (same as in Dijkstra/Johnson examples)
    graph_small = {
        "A": [("B", 4), ("C", 2)],
        "B": [("A", 4), ("C", 1), ("D", 5)],
        "C": [("A", 2), ("B", 1), ("D", 8), ("E", 10)],
        "D": [("B", 5), ("C", 8), ("E", 2)],
        "E": [("C", 10), ("D", 2)],
    }

    # Larger positive-weight graph
    graph_large = {
        "S": [("A", 3), ("B", 1)],
        "A": [("C", 3), ("D", 7)],
        "B": [("A", 1), ("D", 2), ("E", 6)],
        "C": [("F", 2)],
        "D": [("C", 2), ("F", 4), ("G", 1)],
        "E": [("D", 1), ("G", 7)],
        "F": [("H", 3)],
        "G": [("F", 2), ("H", 1)],
        "H": [],
    }

    # Graph with negative edges (no negative cycles) from Bellman_Ford.make_graph,
    # adapted into (to_node, weight) format for Johnson
    bf_graph = Bellman_Ford.make_graph()
    graph_negative = {
        u: [(to_node, w) for (w, to_node) in adj]
        for u, adj in bf_graph.items()
    }

    tests = [
        {
            "name": "Small positive-weight graph",
            "graph": graph_small,
            "start": "A",
            "end": "E",
            "has_negative": False,
        },
        {
            "name": "Larger positive-weight graph",
            "graph": graph_large,
            "start": "S",
            "end": "H",
            "has_negative": False,
        },
        {
            "name": "Negative-edge graph (from Bellman_Ford)",
            "graph": graph_negative,
            "start": "S",
            "end": "A",
            "has_negative": True,
        },
    ]

    return tests


def main():
    tests = build_tests()

    for test in tests:
        name = test["name"]
        graph = test["graph"]
        start = test["start"]
        end = test["end"]
        has_negative = test["has_negative"]

        print("=" * 70)
        print(f"Test: {name}")
        print(f"From {start} to {end}")

        # Dijkstra (skip on negative-edge graphs)
        if has_negative:
            print("Dijkstra: skipped (graph has negative edge weights)")
            dijkstra_dist = None
        else:
            dijkstra_dist, dijkstra_time = run_dijkstra(graph, start, end)
            print(f"Dijkstra: distance={dijkstra_dist}, time={dijkstra_time:.6f}s")

        # Bellman-Ford
        bf_dist, bf_time = run_bellman_ford(graph, start, end)
        if math.isinf(bf_dist):
            print(f"Bellman-Ford: distance=INF/invalid, time={bf_time:.6f}s")
        else:
            print(f"Bellman-Ford: distance={bf_dist}, time={bf_time:.6f}s")

        # Johnson
        try:
            johnson_dist, johnson_time = run_johnson(graph, start, end)
            print(f"Johnson: distance={johnson_dist}, time={johnson_time:.6f}s")
        except ValueError as e:
            print(f"Johnson: error=<{e}>")

        # Simple consistency check when algorithms are all applicable
        if not has_negative and not math.isinf(bf_dist):
            consistent = (dijkstra_dist == bf_dist == johnson_dist)
            print(f"Distances consistent across algorithms: {consistent}")

    print("=" * 70)


if __name__ == "__main__":
    main()
