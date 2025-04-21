from collections import defaultdict

def fordFulkerson(sommets, matrice_adj, source, sink):
    # Create residual graph and initialize flows
    graph = defaultdict(dict)
    for i in range(len(sommets)):
        for j in range(len(sommets)):
            if matrice_adj[i][j] > 0:
                graph[sommets[i]][sommets[j]] = matrice_adj[i][j]
    
    parent = {}
    max_flow = 0
    
    # BFS to find augmenting paths
    def bfs(residual_graph, s, t):
        visited = set()
        queue = [s]
        visited.add(s)
        
        while queue:
            u = queue.pop(0)
            
            for v, capacity in residual_graph[u].items():
                if v not in visited and capacity > 0:
                    visited.add(v)
                    parent[v] = u
                    queue.append(v)
                    if v == t:
                        return True
        return False
    
    residual_graph = defaultdict(dict)
    for u in graph:
        for v, capacity in graph[u].items():
            residual_graph[u][v] = capacity
            residual_graph[v][u] = 0  # Initialize reverse edges
    
    # Find maximum flow
    while bfs(residual_graph, source, sink):
        path_flow = float("Inf")
        s = sink
        path = [sink]
        
        while s != source:
            path_flow = min(path_flow, residual_graph[parent[s]][s])
            s = parent[s]
            path.append(s)
        
        path = path[::-1]  # Reverse to get source to sink
        
        # Update residual capacities
        v = sink
        while v != source:
            u = parent[v]
            residual_graph[u][v] -= path_flow
            residual_graph[v][u] += path_flow
            v = u
        
        max_flow += path_flow
    
    return max_flow, residual_graph