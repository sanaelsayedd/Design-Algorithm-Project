import heapq
import time


def bellman_ford(weights, vertices, source):
	dist = {v: float("inf") for v in vertices}
	dist[source] = 0

	for _ in range(len(vertices) - 1):
		updated = False
		for (u, v), w in weights.items():
			if dist[u] + w < dist[v]:
				dist[v] = dist[u] + w
				updated = True
		if not updated:
			break

	for (u, v), w in weights.items():
		if dist[u] + w < dist[v]:
			return None

	return dist


def dijkstra(adj_list, source):
	dist = {v: float("inf") for v in adj_list}
	dist[source] = 0
	pq = [(0, source)]

	while pq:
		current_dist, u = heapq.heappop(pq)
		if current_dist > dist[u]:
			continue
		for v, w in adj_list[u]:
			new_dist = current_dist + w
			if new_dist < dist[v]:
				dist[v] = new_dist
				heapq.heappush(pq, (new_dist, v))

	return dist


def johnson(vertices, edges):
	weights = {(u, v): w for u, v, w in edges}

	q = "Q"
	for v in vertices:
		weights[(q, v)] = 0

	h = bellman_ford(weights, vertices + [q], q)
	if h is None:
		raise ValueError("Graph contains a negative-weight cycle")

	reweighted_adj = {v: [] for v in vertices}
	for u, v, w in edges:
		new_w = w + h[u] - h[v]
		reweighted_adj[u].append((v, new_w))

	all_pairs = {}
	for u in vertices:
		dist_u = dijkstra(reweighted_adj, u)
		all_pairs[u] = {v: dist_u[v] - h[u] + h[v] for v in vertices}

	return all_pairs

graph = {
	"A": [("B", 4), ("C", 2)],
	"B": [("A", 4), ("C", 1), ("D", 5)],
	"C": [("A", 2), ("B", 1), ("D", 8), ("E", 10)],
	"D": [("B", 5), ("C", 8), ("E", 2)],
	"E": [("C", 10), ("D", 2)],
}

start = "A"
end = "E"

vertices = list(graph.keys())
edges = [
	(u, v, w)
	for u, adj in graph.items()
	for v, w in adj
]

start_time = time.perf_counter()
all_pairs = johnson(vertices, edges)
end_time = time.perf_counter()

distance = all_pairs[start][end]

print(f"Shortest distance from {start} to {end} (Johnson's algorithm): {distance}")
print(f"Execution Time: {end_time - start_time:.6f} seconds")

