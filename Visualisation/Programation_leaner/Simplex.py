import numpy as np


def robust_simplex(a, b, c, n, m, optimization_type="max"):
    """
    Tries all simplex strategies: max/simple, min/simple, max/two-phase, min/two-phase.
    Returns: (status, message, solution, optimal_value, method)
    """
    # Import or define your simplexe_max and two-phase functions here
    # For now, use simplexe_max as the only available simplex
    # You can add two-phase logic if you have it
    from copy import deepcopy

    # Try maximization (standard)
    if optimization_type == "max":
        status, message, solution, z = simplexe_max(c, a, b)
        if status:
            return status, message + " (max/simple)", solution, z, "max/simple"
        # Try minimization (standard)
        c_min = [-x for x in c]
        status, message, solution, z = simplexe_max(c_min, a, b)
        if status:
            return status, message + " (min/simple)", solution, -z, "min/simple"
        # Try maximization (two-phase) - placeholder
        # status, message, solution, z = two_phase_simplex(c, a, b, maximize=True)
        # if status:
        #     return status, message + ' (max/two-phase)', solution, z, 'max/two-phase'
        # Try minimization (two-phase) - placeholder
        # status, message, solution, z = two_phase_simplex(c, a, b, maximize=False)
        # if status:
        #     return status, message + ' (min/two-phase)', solution, -z, 'min/two-phase'
        return False, "Aucune méthode n'a réussi", None, None, None
    else:
        # Try minimization (standard)
        c_min = [-x for x in c]
        status, message, solution, z = simplexe_max(c_min, a, b)
        if status:
            return status, message + " (min/simple)", solution, -z, "min/simple"
        # Try maximization (standard)
        status, message, solution, z = simplexe_max(c, a, b)
        if status:
            return status, message + " (max/simple)", solution, z, "max/simple"
        # Try minimization (two-phase) - placeholder
        # status, message, solution, z = two_phase_simplex(c, a, b, maximize=False)
        # if status:
        #     return status, message + ' (min/two-phase)', solution, -z, 'min/two-phase'
        # Try maximization (two-phase) - placeholder
        # status, message, solution, z = two_phase_simplex(c, a, b, maximize=True)
        # if status:
        #     return status, message + ' (max/two-phase)', solution, z, 'max/two-phase'
        return False, "Aucune méthode n'a réussi", None, None, None


if __name__ == "__main__":
    a, b, c, n, m = ReadEquation()
    # Default to maximization if not specified
    optimization_type = "max"
    try:
        inp = input("Type d'optimisation (max/min) [max]: ").strip().lower()
        if inp in ["max", "min"]:
            optimization_type = inp
    except Exception:
        pass
    status, message, solution, z, method = robust_simplex(
        a, b, c, n, m, optimization_type
    )
    print(message)
    PrintColumn(solution)
    if status:
        print(f"Valeur optimale: {z}")
        print(f"Méthode utilisée: {method}")
