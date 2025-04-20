import heapq

def djikstra(sommets, matrice_adj, debut, depart):
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
    
    # File de priorité
    heap = []
    heapq.heappush(heap, (0, start_idx))
    
    while heap:
        dist_actuelle, noeud_actuel = heapq.heappop(heap)
        
        # Si on atteint le nœud destination, on peut s'arrêter
        if noeud_actuel == end_idx:
            break
        
        # Ignorer les entrées obsolètes
        if dist_actuelle > distances[noeud_actuel]:
            continue
        
        # Explorer les voisins
        for voisin in range(n):
            poids = matrice_adj[noeud_actuel][voisin]
            
            # Vérifier s'il y a une connexion (suppose que 0 = pas de connexion)
            if poids != 0:
                nouvelle_distance = distances[noeud_actuel] + poids
                
                # Mise à jour si meilleur chemin trouvé
                if nouvelle_distance < distances[voisin]:
                    distances[voisin] = nouvelle_distance
                    predecesseurs[voisin] = noeud_actuel
                    heapq.heappush(heap, (nouvelle_distance, voisin))
    
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