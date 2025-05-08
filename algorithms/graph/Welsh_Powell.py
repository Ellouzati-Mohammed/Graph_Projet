import random

def Welsh_Powell(sommets, matrice_adjacence):
    degree_each_Vertex = []
    colored_sommets = []  # Liste de tuples (index, couleur)

    # Étape 1 : Calculer le degré de chaque sommet
    for sommet_index, ligne in enumerate(matrice_adjacence):
        degre = sum(1 for arc in ligne if arc > 0)
        degree_each_Vertex.append((sommet_index, degre))

    # Étape 2 : Trier les sommets par degré décroissant
    degree_each_Vertex.sort(key=lambda item: item[1], reverse=True)

    used_colors = []

    while len(colored_sommets) < len(sommets):
        # Générer une couleur unique
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
        used_colors.append(current_color)  # ✅ important

        colored_this_round = []

        for sommet_index, _ in degree_each_Vertex:
            if any(s[0] == sommet_index for s in colored_sommets):
                continue

            # Vérifier les conflits de couleur avec les voisins
            conflict = any(
                is_adjacent and (index, current_color) in colored_sommets
                for index, is_adjacent in enumerate(matrice_adjacence[sommet_index])
            )

            if not conflict:
                colored_sommets.append((sommet_index, current_color))
                colored_this_round.append(sommet_index)

        # Mise à jour : supprimer les sommets déjà colorés
        degree_each_Vertex = [v for v in degree_each_Vertex if v[0] not in colored_this_round]

    return colored_sommets
