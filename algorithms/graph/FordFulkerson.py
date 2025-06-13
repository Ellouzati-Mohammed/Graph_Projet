def fordFulkerson(sommets, matrice_adj, source, sink):
    # Create residual graph and flow matrix
    n = len(sommets)
    flow_matrix = [[0] * n for _ in range(n)]
    residual_graph = [[0] * n for _ in range(n)]

    # Initialize residual graph with capacities
    for i in range(n):
        for j in range(n):
            residual_graph[i][j] = matrice_adj[i][j]

    parent = [-1] * n
    max_flow = 0

    # BFS to find augmenting paths
    def bfs(residual_graph, s, t, parent):
        visited = [False] * n
        queue = []
        queue.append(s)
        visited[s] = True

        while queue:
            u = queue.pop(0)

            for v in range(n):
                if not visited[v] and residual_graph[u][v] > 0:
                    visited[v] = True
                    parent[v] = u
                    queue.append(v)
                    if v == t:
                        return True
        return False

    # Find maximum flow
    while bfs(residual_graph, sommets.index(source), sommets.index(sink), parent):
        path_flow = float("Inf")
        s = sommets.index(sink)

        # Find minimum residual capacity along the path
        while s != sommets.index(source):
            path_flow = min(path_flow, residual_graph[parent[s]][s])
            s = parent[s]

        # Update residual capacities and flow matrix
        v = sommets.index(sink)
        while v != sommets.index(source):
            u = parent[v]
            residual_graph[u][v] -= path_flow
            residual_graph[v][u] += path_flow
            flow_matrix[u][v] += path_flow
            v = u

        max_flow += path_flow

    return max_flow, flow_matrix
