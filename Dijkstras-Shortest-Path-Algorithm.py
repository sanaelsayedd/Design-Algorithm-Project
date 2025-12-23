import heapq
import time

def dijkstra(graph, start, end):
    pq = [(0, start)]
    dist = {node: float('inf') for node in graph}
    prev = {node: None for node in graph}
    dist[start] = 0

    while pq:
        current_dist, u = heapq.heappop(pq)

        if u == end:
            break

        if current_dist > dist[u]:
            continue

        for v, weight in graph[u]:
            new_dist = current_dist + weight
            if new_dist < dist[v]:
                dist[v] = new_dist
                prev[v] = u
                heapq.heappush(pq, (new_dist, v))

    path = []
    node = end
    while node:
        path.append(node)
        node = prev[node]

    return path[::-1], dist[end]

if __name__ == "__main__":
    graph = {
        'A': [('B', 4), ('C', 2)],
        'B': [('A', 4), ('C', 1), ('D', 5)],
        'C': [('A', 2), ('B', 1), ('D', 8), ('E', 10)],
        'D': [('B', 5), ('C', 8), ('E', 2)],
        'E': [('C', 10), ('D', 2)]
    }

    start_time = time.perf_counter()
    path, distance = dijkstra(graph, 'A', 'E')
    end_time = time.perf_counter()

    print("Shortest Path:", path)
    print("Total Distance:", distance)
    print(f"Execution Time: {end_time - start_time:.6f} seconds")