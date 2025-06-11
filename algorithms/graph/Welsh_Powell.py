import random

def Welsh_Powell(sommets, matrice_adjacence):
    n = len(sommets)
    # Étape 1 : Calculer le degré de chaque sommet
    degrees = []
    for i in range(n):
        deg = sum(1 for j in range(n) if matrice_adjacence[i][j] > 0)
        degrees.append((i, deg))
    
    # Étape 2 : Trier par degré décroissant
    degrees.sort(key=lambda x: x[1], reverse=True)
    ordre_sommets = [idx for idx, _ in degrees]  # Ordre des indices
    
    # Tableau de couleurs (None = non coloré)
    couleurs = [None] * n
    used_colors = []
    
    # Tant qu'il reste des sommets non colorés
    while any(c is None for c in couleurs):
        # Générer une nouvelle couleur aléatoire non utilisée
        current_color = (
            random.randint(0, 255) / 255,
            random.randint(0, 255) / 255,
            random.randint(0, 255) / 255
        )
        while current_color in used_colors:
            current_color = (
                random.randint(0, 255) / 255,
                random.randint(0, 255) / 255,
                random.randint(0, 255) / 255
            )
        used_colors.append(current_color)
        
        # Parcourir tous les sommets dans l'ordre trié
        for idx in ordre_sommets:
            # Passer les sommets déjà colorés
            if couleurs[idx] is not None:
                continue
                
            # Vérifier les conflits avec les voisins
            conflit = False
            for voisin in range(n):
                # Si les sommets sont adjacents ET le voisin a la couleur courante
                if matrice_adjacence[idx][voisin] > 0 and couleurs[voisin] == current_color:
                    conflit = True
                    break
                    
            # Si pas de conflit, attribuer la couleur
            if not conflit:
                couleurs[idx] = current_color
                
    # Formatage du résultat comme dans la version originale
    colored_sommets = [(i, couleurs[i]) for i in range(n)]
    return colored_sommets