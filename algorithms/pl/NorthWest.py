import numpy as np


def northwest_corner(supply, demand, costs=None):
    try:
        if sum(supply) != sum(demand):
            raise ValueError("Problème non équilibré (offre ≠ demande)")

        m = len(supply)
        n = len(demand)
        alloc = np.zeros((m, n))
        s = np.array(supply, dtype=float)
        d = np.array(demand, dtype=float)

        i = j = 0
        while i < m and j < n:
            quantity = min(s[i], d[j])
            alloc[i, j] = quantity
            s[i] -= quantity
            d[j] -= quantity

            if s[i] == 0:
                i += 1
            else:
                j += 1

        total_cost = np.sum(alloc * costs) if costs is not None else 0
        return True, "Solution trouvée", alloc, total_cost

    except Exception as e:
        return False, str(e), None, 0
