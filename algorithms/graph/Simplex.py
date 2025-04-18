import numpy as np

def simplexe_max(c, A, b):
    n_var = len(c)
    n_constr = len(A)

    tableau = np.zeros((n_constr + 1, n_var + n_constr + 1))

    for i in range(n_constr):
        tableau[i, :n_var] = A[i]
        tableau[i, n_var + i] = 1
        tableau[i, -1] = b[i]

    tableau[-1, :n_var] = -np.array(c)

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
            raise Exception("Problème non borné.")

        tableau[pivot_row] /= tableau[pivot_row, pivot_col]

        for i in range(n_constr + 1):
            if i != pivot_row:
                tableau[i] -= tableau[i, pivot_col] * tableau[pivot_row]

    solution = np.zeros(n_var)
    for j in range(n_var):
        col = tableau[:, j]
        if list(col).count(1) == 1 and list(col).count(0) == len(col) - 1:
            i = list(col).index(1)
            solution[j] = tableau[i, -1]

    Z = tableau[-1, -1]
    return solution, Z


def main():
    # Problème : Max Z = 3x + 2y
    # s.c. :
    #   x + y <= 4
    #   x <= 2
    #   y <= 3

    c = [3, 2]  # Coefficients de la fonction objectif Z
    A = [
        [1, 1],  # x + y <= 4
        [1, 0],  # x <= 2
        [0, 1]   # y <= 3
    ]
    b = [4, 2, 3]

    solution, z = simplexe_max(c, A, b)

    print("✅ Résultat :")
    for i in range(len(solution)):
        print(f"  x{i+1} = {solution[i]}")
    print(f"  Z maximum = {z}")


if __name__ == "__main__":
    main()
