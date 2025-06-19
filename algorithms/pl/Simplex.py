import numpy as np
from typing import Tuple, Union, Dict, List

EPS = 1e-8


class SimplexSolver:
    def __init__(self):
        self.max_iterations = 1000
        self.epsilon = 1e-10  # For floating point comparisons

    def solve(
        self,
        c: List[float],
        A: List[List[float]],
        b: List[float],
        optimization_type: str = "max",
    ) -> Dict:
        """
        Main solver method that handles both maximization and minimization problems
        using appropriate simplex methods.
        """
        try:
            # Validate input dimensions
            self._validate_inputs(c, A, b)

            # Convert minimization to maximization
            if optimization_type == "min":
                c = [-x for x in c]

            # First try standard simplex
            status, message, solution, Z = self.simplex(c, A, b)

            if status:
                if optimization_type == "min":
                    Z = -Z  # Convert back to minimization value
                return {
                    "status": "optimal",
                    "message": message,
                    "solution": solution,
                    "optimal_value": Z,
                    "method": "standard simplex",
                }

            # If standard simplex failed, try two-phase method
            status, message, solution, Z = self.two_phase_simplex(c, A, b)

            if status:
                if optimization_type == "min":
                    Z = -Z
                return {
                    "status": "optimal",
                    "message": message,
                    "solution": solution,
                    "optimal_value": Z,
                    "method": "two-phase simplex",
                }

            # If both methods failed
            return {
                "status": "failed",
                "message": message,
                "solution": None,
                "optimal_value": None,
                "method": None,
            }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "solution": None,
                "optimal_value": None,
                "method": None,
            }

    def _validate_inputs(self, c: List[float], A: List[List[float]], b: List[float]):
        """Validate the dimensions of input matrices"""
        if not all(len(row) == len(c) for row in A):
            raise ValueError(
                "Each constraint must have same number of coefficients as objective function"
            )
        if len(A) != len(b):
            raise ValueError(
                "Number of constraints must match number of right-hand side values"
            )
        if len(c) == 0 or len(A) == 0:
            raise ValueError(
                "Problem must have at least one variable and one constraint"
            )

    def simplex(
        self, c: List[float], A: List[List[float]], b: List[float]
    ) -> Tuple[bool, str, List[float], float]:
        """
        Standard simplex method implementation for maximization problems.
        Returns (success, message, solution, optimal_value)
        """
        n_var = len(c)
        n_constr = len(A)
        iterations = 0

        # Create initial tableau
        tableau = self._create_initial_tableau(c, A, b)

        # Main simplex loop
        while iterations < self.max_iterations:
            iterations += 1

            # Check if optimal
            if all(x >= -self.epsilon for x in tableau[-1, :-1]):
                break

            # Select entering variable (most negative reduced cost)
            entering = np.argmin(tableau[-1, :-1])

            # Calculate ratios
            ratios = []
            for i in range(n_constr):
                if tableau[i, entering] > self.epsilon:
                    ratios.append(tableau[i, -1] / tableau[i, entering])
                else:
                    ratios.append(np.inf)

            # Check for unboundedness
            if all(r == np.inf for r in ratios):
                return False, "Problem is unbounded", None, None

            # Select leaving variable
            leaving = np.argmin(ratios)

            # Perform pivot operation
            self._pivot(tableau, leaving, entering)

        if iterations >= self.max_iterations:
            return False, "Maximum iterations reached", None, None

        # Extract solution
        solution = np.zeros(n_var)
        for j in range(n_var):
            col = tableau[:-1, j]
            if (
                np.sum(
                    np.abs(col - (np.arange(len(col)) == np.argmax(col)).astype(float))
                )
                < self.epsilon
            ):
                solution[j] = tableau[np.argmax(col), -1]

        Z = tableau[-1, -1]

        return True, "Optimal solution found", solution, Z

    def two_phase_simplex(
        self, c: List[float], A: List[List[float]], b: List[float]
    ) -> Tuple[bool, str, List[float], float]:
        """
        Two-phase simplex method for problems without obvious initial feasible solutions.
        """
        n_var = len(c)
        n_constr = len(A)

        # Phase 1: Create auxiliary problem to find feasible solution
        aux_c = [0] * n_var + [-1] * n_constr
        aux_A = [
            row + [0] * i + [1] + [0] * (n_constr - i - 1) for i, row in enumerate(A)
        ]

        # Solve phase 1
        tableau = self._create_initial_tableau(aux_c, aux_A, b)
        basis = list(range(n_var, n_var + n_constr))  # Artificial variables in basis

        # Optimize phase 1
        success, message, _, _ = self._simplex_phase(tableau, basis, phase=1)

        if not success or abs(tableau[-1, -1]) > self.epsilon:
            return False, "Problem is infeasible", None, None

        # Phase 2: Remove artificial variables and solve original problem
        # Remove artificial variable columns
        tableau = np.delete(tableau, range(n_var, n_var + n_constr), axis=1)

        # Restore original objective
        tableau[-1, :n_var] = -np.array(c)
        tableau[-1, -1] = 0

        # Update reduced costs
        for j in range(n_var):
            if j in basis:
                pivot_row = basis.index(j)
                tableau[-1] -= tableau[-1, j] * tableau[pivot_row]

        # Solve phase 2
        success, message, solution, Z = self._simplex_phase(tableau, basis, phase=2)

        if not success:
            return False, message, None, None

        return True, message, solution[:n_var], Z

    def _simplex_phase(
        self, tableau: np.ndarray, basis: List[int], phase: int
    ) -> Tuple[bool, str, List[float], float]:
        """Helper method for simplex phases"""
        iterations = 0
        n_constr = tableau.shape[0] - 1

        while iterations < self.max_iterations:
            iterations += 1

            # Check if optimal
            if all(x >= -self.epsilon for x in tableau[-1, :-1]):
                break

            # Select entering variable
            entering = np.argmin(tableau[-1, :-1])

            # Calculate ratios
            ratios = []
            for i in range(n_constr):
                if tableau[i, entering] > self.epsilon:
                    ratios.append(tableau[i, -1] / tableau[i, entering])
                else:
                    ratios.append(np.inf)

            if all(r == np.inf for r in ratios):
                if phase == 1:
                    return False, "Phase 1 unbounded (shouldn't happen)", None, None
                else:
                    return False, "Problem is unbounded", None, None

            # Select leaving variable
            leaving = np.argmin(ratios)

            # Update basis
            basis[leaving] = entering

            # Perform pivot
            self._pivot(tableau, leaving, entering)

        if iterations >= self.max_iterations:
            return False, "Maximum iterations reached", None, None

        # Extract solution
        solution = np.zeros(tableau.shape[1] - 1)
        for j in range(len(solution)):
            if j in basis:
                solution[j] = tableau[basis.index(j), -1]

        Z = tableau[-1, -1]

        return True, "Optimal solution found", solution, Z

    def _create_initial_tableau(
        self, c: List[float], A: List[List[float]], b: List[float]
    ) -> np.ndarray:
        """Create initial simplex tableau"""
        n_var = len(c)
        n_constr = len(A)

        tableau = np.zeros((n_constr + 1, n_var + n_constr + 1))

        # Fill constraints
        for i in range(n_constr):
            tableau[i, :n_var] = A[i]
            tableau[i, n_var + i] = 1  # Slack variable
            tableau[i, -1] = b[i]

        # Fill objective
        tableau[-1, :n_var] = -np.array(c)

        return tableau

    def _pivot(self, tableau: np.ndarray, leaving: int, entering: int):
        """Perform pivot operation on tableau"""
        # Normalize pivot row
        pivot_val = tableau[leaving, entering]
        tableau[leaving] /= pivot_val

        # Update other rows
        for i in range(tableau.shape[0]):
            if i != leaving and abs(tableau[i, entering]) > self.epsilon:
                multiplier = tableau[i, entering]
                tableau[i] -= multiplier * tableau[leaving]

    def robust_simplex(
        self,
        c: List[float],
        A: List[List[float]],
        b: List[float],
        optimization_type: str = None,
    ) -> Dict:
        """
        Try all available simplex methods in order and return the first successful solution.
        """
        if optimization_type is None:
            # Try both max and min if not specified
            max_result = self.solve(c, A, b, "max")
            if max_result["status"] == "optimal":
                return max_result
            return self.solve(c, A, b, "min")

        return self.solve(c, A, b, optimization_type)


# Example usage
if __name__ == "__main__":
    solver = SimplexSolver()

    # Example problem
    c = [3, 2]  # Objective coefficients
    A = [[1, 1], [2, 1], [1, 0]]  # Constraint coefficients
    b = [4, 5, 2]  # Right-hand side values

    # Solve with maximization
    result = solver.robust_simplex(c, A, b, "max")
    print("\nMaximization results:")
    print(f"Status: {result['status']}")
    print(f"Message: {result['message']}")
    if result["solution"] is not None:
        print(f"Solution: {result['solution']}")
        print(f"Optimal value: {result['optimal_value']}")
        print(f"Method used: {result['method']}")

    # Solve with minimization (same problem but minimized)
    result = solver.robust_simplex(c, A, b, "min")
    print("\nMinimization results:")
    print(f"Status: {result['status']}")
    print(f"Message: {result['message']}")
    if result["solution"] is not None:
        print(f"Solution: {result['solution']}")
        print(f"Optimal value: {result['optimal_value']}")
        print(f"Method used: {result['method']}")

    # Test with your unbounded problem
    c = [2, 3]
    A = [[-1, 1], [1, -2]]
    b = [-1, -2]

    result = solver.robust_simplex(c, A, b, "max")
    print("\nUnbounded problem results:")
    print(f"Status: {result['status']}")
    print(f"Message: {result['message']}")

# Add this at the bottom to make the class available for import
__all__ = ["SimplexSolver"]

# --- Add these top-level wrappers for import ---
def simplexe_max(c, A, b):
    solver = SimplexSolver()
    return solver.simplex(c, A, b)

def two_phase_simplex(c, A, b, maximize=True):
    solver = SimplexSolver()
    return solver.two_phase_simplex(c, A, b)

def robust_simplex(A, b, c, n, m, optimization_type='max'):
    solver = SimplexSolver()
    return solver.robust_simplex(c, A, b, optimization_type)
