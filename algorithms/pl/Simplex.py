import numpy as np

def simplexe_max(c, A, b):
    n_var = len(c)
    n_constr = len(A)

    # Création du tableau (matrice augmentée)
    tableau = np.zeros((n_constr + 1, n_var + n_constr + 1))

    # Remplissage des contraintes
    for i in range(n_constr):
        tableau[i, :n_var] = A[i]
        tableau[i, n_var + i] = 1  # variable d'appoint
        tableau[i, -1] = b[i]

    # Dernière ligne : -c (car on maximise)
    tableau[-1, :n_var] = -np.array(c)

    # Boucle du simplexe
    while any(tableau[-1, :-1] < 0):
        pivot_col = np.argmin(tableau[-1, :-1])
        ratios = []
        for i in range(n_constr):
            if tableau[i, pivot_col] > 0:
                ratios.append(tableau[i, -1] / tableau[i, pivot_col])
            else:
                ratios.append(np.inf)

        pivot_row = np.argmin(ratios)

        if ratios[pivot_row] == np.inf:
            return False, "Problème non borné", None, None

        # Opérations de pivot
        tableau[pivot_row] /= tableau[pivot_row, pivot_col]
        for i in range(n_constr + 1):
            if i != pivot_row:
                tableau[i] -= tableau[i, pivot_col] * tableau[pivot_row]

    # Affichage final du tableau
    print("Tableau final du simplexe :\n", np.round(tableau, 2))

    # Récupération de la solution
    solution = np.zeros(n_var)
    for j in range(n_var):
        col = tableau[:, j]
        col = np.round(col, decimals=10)
        if list(col).count(1) == 1 and list(col).count(0) == len(col) - 1:
            i = list(col).index(1)
            solution[j] = tableau[i, -1]

    Z = tableau[-1, -1]

    return True, "Solution optimale trouvée", solution, Z

# def main():
#     c = [3, 2]  # Max Z = 3x + 2y
#     A = [
#         [1, 1],
#         [1, 0],
#         [0, 1]
#     ]
#     b = [4, 2, 3]

#     status, message, solution, z = simplexe_max(c, A, b)

#     print("\nStatut :", message)
#     if status:
#         for i in range(len(solution)):
#             print(f"  x{i+1} = {solution[i]}")
#         print(f"  Z maximum = {z}")

# if __name__ == "__main__":
#     main()
