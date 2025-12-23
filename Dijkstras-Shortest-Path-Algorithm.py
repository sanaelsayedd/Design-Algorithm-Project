import heapq
import time

def ShortestPath(n, edges, src):
    adj = {}
    for i in range(n):
        adj[i] = []

    for s, dst, weight in edges:
        adj[s].append([dst, weight])

    shortest = {}
    minHeap = [[0, src]]

    while minHeap:
        w1, n1 = heapq.heappop(minHeap)
        if n1 in shortest:
            continue
        shortest[n1] = w1

        for n2, w2 in adj[n1]:
            if n2 not in shortest:
                heapq.heappush(minHeap, [w1 + w2, n2])

    for i in range(n):
        if i not in shortest:
            shortest[i] = -1

    return shortest

cities = {
        0: "Cairo",
        1: "Giza",
        2: "Alexandria",
        3: "Tanta",
        4: "Mansoura"
    }
n = len(cities)
edges = [
        (0, 1, 4),
        (0, 2, 1),
        (2, 1, 2),
        (1, 3, 1),
        (2, 3, 5),
        (3, 4, 3)
    ]
start_time = time.time()
end_time = time.time()
src = 0
result = ShortestPath(n, edges, src)
print("Shortest distances from Cairo:")

for city_id, dist in result.items():
    print(f"{cities[city_id]} : {dist} km")
r = end_time - start_time
print(f"Time: {r:.4f} seconds")
