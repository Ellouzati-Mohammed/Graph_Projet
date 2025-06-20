import numpy as np

class SimplexSolver:
    def __init__(self, c, A, b, relations, opt_type='max'):
        self.c = np.array(c, dtype=float)
        self.A = np.array(A, dtype=float)
        self.b = np.array(b, dtype=float)
        self.relations = relations
        self.opt_type = opt_type.lower()

        if self.opt_type == 'min':
            self.c = -self.c

        self.n_vars = len(self.c)
        self.n_constraints = len(self.b)
        
        self.tableau = None
        self.basis = None
        self.status = "not_solved"
        self.solution = None
        self.optimal_value = None
        self.artificial_vars = []

    def solve(self):
        self._prepare_tableau()

        if self.artificial_vars:
            phase1_success = self._solve_phase1()
            if not phase1_success:
                self.status = "infeasible"
                if self.opt_type == 'min':
                    self.c = -self.c # Restore original objective
                return self.get_results()

        phase2_success = self._solve_phase2()
        if not phase2_success:
            self.status = "unbounded"
        else:
            self.status = "optimal"
            self._extract_solution()
        
        if self.opt_type == 'min':
            self.c = -self.c # Restore original objective

        return self.get_results()

    def _prepare_tableau(self):
        # Standardize relations: < becomes <=, > becomes >=
        self.relations = ['<=' if r == '<' else r for r in self.relations]
        self.relations = ['>=' if r == '>' else r for r in self.relations]

        # Standardize b to be non-negative
        for i in range(self.n_constraints):
            if self.b[i] < 0:
                self.b[i] *= -1
                self.A[i] *= -1
                if self.relations[i] == '<=': self.relations[i] = '>='
                elif self.relations[i] == '>=': self.relations[i] = '<='
        
        n_slack = self.relations.count('<=')
        n_surplus = self.relations.count('>=')
        
        self.artificial_vars = []
        art_var_counter = 0

        tableau_A = self.A.copy()
        identity_part = np.zeros((self.n_constraints, n_slack + n_surplus))
        slack_idx, surplus_idx = 0, 0

        for i, rel in enumerate(self.relations):
            if rel == '<=':
                identity_part[i, slack_idx] = 1
                slack_idx += 1
            elif rel == '>=':
                identity_part[i, n_slack + surplus_idx] = -1
                surplus_idx += 1
            # For '=' and '>=' we will add artificial vars later

        tableau_A = np.hstack((tableau_A, identity_part))
        
        art_cols = []
        for i, rel in enumerate(self.relations):
            if rel == '>=' or rel == '=':
                art_col = np.zeros((self.n_constraints, 1))
                art_col[i, 0] = 1
                art_cols.append(art_col)
                self.artificial_vars.append(self.n_vars + n_slack + n_surplus + art_var_counter)
                art_var_counter += 1
        
        if art_cols:
            tableau_A = np.hstack([tableau_A] + art_cols)

        # Full tableau with objective row and RHS
        n_total_vars = tableau_A.shape[1]
        self.tableau = np.zeros((self.n_constraints + 1, n_total_vars + 1))
        self.tableau[:-1, :-1] = tableau_A
        self.tableau[:-1, -1] = self.b

        # Objective row
        self.tableau[-1, :self.n_vars] = -self.c
        
        self.basis = [0] * self.n_constraints
        s_idx, art_idx_count = 0, 0
        for i in range(self.n_constraints):
            if self.relations[i] == '<=':
                self.basis[i] = self.n_vars + s_idx
                s_idx += 1
            else: # '>=' or '='
                self.basis[i] = self.artificial_vars[art_idx_count]
                art_idx_count += 1
    
    def _solve_phase1(self):
        original_obj = self.tableau[-1, :].copy()
        
        # Phase 1 objective: minimize sum of artificial variables
        phase1_obj = np.zeros(self.tableau.shape[1])
        phase1_obj[self.artificial_vars] = 1
        self.tableau[-1, :] = phase1_obj
        
        # Make basis columns 0 in objective row
        for i, basis_var in enumerate(self.basis):
            if basis_var in self.artificial_vars:
                self.tableau[-1, :] -= self.tableau[i, :]

        self._run_simplex()
        
        if self.tableau[-1, -1] > 1e-6: # Infeasible if sum of artificials > 0
            return False
        
        # Restore original objective, remove artificial vars
        self.tableau[-1, :] = original_obj
        
        # Make basis columns 0 in objective row again
        for i, var_idx in enumerate(self.basis):
            if self.tableau[-1, var_idx] != 0:
                self.tableau[-1, :] -= self.tableau[-1, var_idx] * self.tableau[i, :]

        # Drop artificial variable columns
        self.tableau = np.delete(self.tableau, self.artificial_vars, axis=1)

        return True

    def _solve_phase2(self):
        self._run_simplex()
        # Check for unboundedness
        for col in range(self.tableau.shape[1] -1):
            if self.tableau[-1, col] < -1e-6:
                if np.all(self.tableau[:-1, col] <= 1e-6):
                    self.status = "unbounded"
                    return False # Unbounded
        return True

    def _run_simplex(self):
        while np.any(self.tableau[-1, :-1] < -1e-6):
            pivot_col = np.argmin(self.tableau[-1, :-1])
            
            ratios = np.full(self.n_constraints, np.inf)
            for i in range(self.n_constraints):
                if self.tableau[i, pivot_col] > 1e-6:
                    ratios[i] = self.tableau[i, -1] / self.tableau[i, pivot_col]
            
            if np.all(ratios == np.inf):
                self.status = "unbounded" # Should be caught by caller
                return

            pivot_row = np.argmin(ratios)
            
            self.basis[pivot_row] = pivot_col
            
            pivot_element = self.tableau[pivot_row, pivot_col]
            self.tableau[pivot_row, :] /= pivot_element
            
            for i in range(self.n_constraints + 1):
                if i != pivot_row:
                    self.tableau[i, :] -= self.tableau[i, pivot_col] * self.tableau[pivot_row, :]

    def _extract_solution(self):
        self.solution = np.zeros(self.n_vars)
        for i, basis_var in enumerate(self.basis):
            if basis_var < self.n_vars:
                self.solution[basis_var] = self.tableau[i, -1]
        
        self.optimal_value = self.tableau[-1, -1]
        if self.opt_type == 'min':
            self.optimal_value *= -1

    def get_results(self):
        message_map = {
            'not_solved': 'Le solveur n\'a pas été exécuté.',
            'optimal': 'Solution optimale trouvée.',
            'infeasible': 'Le problème est infaisable.',
            'unbounded': 'Le problème est non borné.',
        }
        return {
            'status': self.status,
            'message': message_map.get(self.status, 'Une erreur inconnue est survenue.'),
            'solution': self.solution.tolist() if self.solution is not None else None,
            'optimal_value': self.optimal_value,
            'tableau': self.tableau.tolist() if self.tableau is not None else None
        }

def robust_simplex(data):
    """
    Wrapper function to maintain compatibility with the old API.
    """
    try:
        c = data.get('c')
        A = data.get('A')
        b = data.get('b')
        opt_type = data.get('optimization_type', 'max')
        relations = data.get('relations')

        if relations is None:
            # Fallback for old data without relations
            relations = ['<='] * len(b)
        
        if not all([c, A, b, opt_type, relations]):
            return {'status': 'error', 'message': 'Données d\'entrée manquantes ou invalides.'}

        solver = SimplexSolver(c, A, b, relations, opt_type)
        return solver.solve()
    except Exception as e:
        return {'status': 'error', 'message': f"Une erreur inattendue est survenue: {str(e)}"}


