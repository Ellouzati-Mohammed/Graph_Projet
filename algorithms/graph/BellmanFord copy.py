def bellmanFord(sommets, matrice_adj, debut, depart):
    # Vérification des nœuds de départ et d'arrivée
    try:
        start_idx = sommets.index(debut)
        end_idx = sommets.index(depart)
    except ValueError:
        raise ValueError("Le nœud de départ ou d'arrivée n'existe pas")
    
    n = len(sommets)
    # Vérification de la taille de la matrice
    if len(matrice_adj) != n or any(len(row) != n for row in matrice_adj):
        raise ValueError("Matrice d'adjacence invalide")
    
    # Initialisation des distances et du chemin
    distances = [float('inf')] * n
    distances[start_idx] = 0
    predecesseurs = [None] * n
    
    # Relaxation des arêtes (n-1 fois)
    for _ in range(n - 1):
        for u in range(n):
            for v in range(n):
                poids = matrice_adj[u][v]
                if poids != 0:  # Si arête existe
                    if distances[u] + poids < distances[v]:
                        distances[v] = distances[u] + poids
                        predecesseurs[v] = u
    
    # Vérification des cycles de poids négatif
    for u in range(n):
        for v in range(n):
            poids = matrice_adj[u][v]
            if poids != 0 and distances[u] + poids < distances[v]:
                raise ValueError("Le graphe contient un cycle de poids négatif")
    
    # Reconstruction du chemin
    chemin = []
    current = end_idx
    
    # Si le nœud d'arrivée est inaccessible
    if distances[current] == float('inf'):
        return []
    
    while current is not None:
        chemin.append(sommets[current])
        current = predecesseurs[current]
    
    return chemin[::-1]  # Inverser pour avoir du départ à l'arrivée