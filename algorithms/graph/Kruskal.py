def kruskal(sommets, matrice_adjacence):

    # Fonction pour trouver la racine d'un sommet avec compression de chemin
    def find(parent, sommet):
        if parent[sommet] != sommet:
            parent[sommet] = find(parent, parent[sommet])  # Compression de chemin
        return parent[sommet]

    # Fonction pour unir deux composants sous la même racine
    def union(parent, rank, sommet1, sommet2):
        root1 = find(parent, sommet1)
        root2 = find(parent, sommet2)

        if root1 != root2:
            # Union par rang
            if rank[root1] > rank[root2]:
                parent[root2] = root1
            elif rank[root1] < rank[root2]:
                parent[root1] = root2
            else:
                parent[root2] = root1
                rank[root1] += 1

    # Initialisation des structures parent et rang
    parent = {sommet: sommet for sommet in sommets}
    rank = {sommet: 0 for sommet in sommets}

    # Créer une liste d'arêtes avec leurs poids
    edges = []
    for i in range(len(sommets)):
        for j in range(len(sommets)):
            if matrice_adjacence[i][j] > 0:  # Seulement les arêtes avec poids
                edges.append((sommets[i], sommets[j], matrice_adjacence[i][j]))

    # Trier les arêtes par poids croissant
    edges.sort(key=lambda x: x[2])

    # Appliquer l'algorithme de Kruskal pour obtenir le MST
    mst = []
    for sommet1, sommet2, poids in edges:
        if find(parent, sommet1) != find(parent, sommet2):
            union(parent, rank, sommet1, sommet2)
            mst.append((sommet1, sommet2, poids))

    return mst
