import numpy as np

def moindre_cout(costs, supply, demand):
    # Créer une copie des coûts, offre et demande pour éviter de modifier les originaux
    costs_copy = np.array(costs, dtype=float)
    supply_copy = np.array(supply, dtype=float)
    demand_copy = np.array(demand, dtype=float)
    
    # Initialiser la matrice d'allocation
    allocation = np.zeros_like(costs_copy)
    
    while np.sum(supply_copy) > 0 and np.sum(demand_copy) > 0:
        # Trouver la case avec le coût minimal
        min_cost = np.inf
        min_i, min_j = -1, -1
        
        for i in range(len(supply_copy)):
            for j in range(len(demand_copy)):
                if supply_copy[i] > 0 and demand_copy[j] > 0 and costs_copy[i, j] < min_cost:
                    min_cost = costs_copy[i, j]
                    min_i, min_j = i, j
        
        if min_i == -1:  # Aucune case trouvée (offre/demande nulle)
            break
        
        # Allouer le maximum possible
        quantity = min(supply_copy[min_i], demand_copy[min_j])
        allocation[min_i, min_j] = quantity
        
        # Mettre à jour l'offre et la demande
        supply_copy[min_i] -= quantity
        demand_copy[min_j] -= quantity
        
        # Marquer la case comme traitée (coût = infini)
        costs_copy[min_i, min_j] = np.inf
    
    # Calculer le coût total
    total_cost = np.sum(allocation * costs)
    
    return allocation, total_cost

