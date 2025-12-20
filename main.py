infinity = float("inf")

# (edge_weight, to_node)
def make_graph():
    return {  
        'S': [(8, 'E'), (10, 'A')],
        'A': [(2, 'C')],
        'B': [(1, 'A')],
        'C': [(-2, 'B')],     # Bellman-Ford can handle negative edge weights
        'D': [(-4, 'A'), (-1, 'C')],
        'E': [(1, 'D')],
    }

def Bellman_Ford(G, start):
    # Bellman-Ford and Dijkstra's have the same end result:
    # finding the shortest path from one source node to all other nodes
    
    shortest_paths = {}
    
    # Initialize all distances as infinity
    for node in G:
        shortest_paths[node] = infinity

    # Distance to the start node is zero
    shortest_paths[start] = 0
    
    size = len(G)  # Number of vertices |V|

    # Bellman-Ford Algorithm takes at most V-1 iterations
    # Time Complexity: O(|V| * |E|)
    for _ in range(size - 1):
        for node in G:
            for edge in G[node]:
                cost = edge[0]
                to_node = edge[1]
                
                # Bellman-Ford is NOT a greedy algorithm,
                # so it works with negative edge weights
                if shortest_paths[node] + cost < shortest_paths[to_node]:
                    shortest_paths[to_node] = shortest_paths[node] + cost

    # Extra iteration to detect negative cycles
    # Bellman-Ford and Dijkstra's both fail on graphs
    # with negative cycles because no shortest path exists
    for node in G:
        for edge in G[node]:
            cost = edge[0]
            to_node = edge[1]
            if shortest_paths[node] + cost < shortest_paths[to_node]:
                return 'INVALID - negative cycle detected'

    # Bellman-Ford guarantees the correct shortest paths
    # (unlike Dijkstra's, which fails with negative edges)
    return shortest_paths

start = 'S'

G = make_graph()
shortest_paths = Bellman_Ford(G, start)

print(f'Shortest path from {start}: {shortest_paths}')
