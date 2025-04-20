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

    used_colors = []  # Liste des couleurs utilisées
    print(matrice_adjacence)
    while len(colored_sommets) < len(sommets):

        current_color = (
            random.randint(0, 255) / 255,  # Normaliser la composante rouge
            random.randint(0, 255) / 255,  # Normaliser la composante verte
            random.randint(0, 255) / 255   # Normaliser la composante bleue
        )

        # Vérifie si la couleur a déjà été utilisée et génère une nouvelle couleur si nécessaire
        while current_color in used_colors:
            current_color = (
                random.randint(0, 255) / 255,
                random.randint(0, 255) / 255,
                random.randint(0, 255) / 255
            )
        colored_this_round = []

        for sommet_index, _ in degree_each_Vertex:
            # Vérifier si déjà colorié
            if any(s[0] == sommet_index for s in colored_sommets):
                continue  #si le sommet est deja colorier, en saut a l'iteration sivant sans continu le code

            # Vérifier s’il est adjacent à un sommet déjà colorié avec cette couleur
            conflict = False
            for index, is_adjacent in enumerate(matrice_adjacence[sommet_index]):
                if is_adjacent == 1:
                    for s_index, s_color in colored_sommets:
                        if s_index == index and s_color == current_color:
                            conflict = True
                            break
                if conflict:
                    break

            if not conflict:
                colored_sommets.append((sommet_index, current_color))
                colored_this_round.append(sommet_index)

        # Supprimer les sommets colorés de degree_each_Vertex
        degree_each_Vertex = [v for v in degree_each_Vertex if v[0] not in colored_this_round]


    return colored_sommets