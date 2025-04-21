import numpy as np

def vogels_approximation(costs, supply, demand):
    # Create copies to avoid modifying originals
    costs_copy = np.array(costs, dtype=float)
    supply_copy = np.array(supply, dtype=float)
    demand_copy = np.array(demand, dtype=float)
    
    # Initialize allocation matrix
    allocation = np.zeros_like(costs_copy)
    
    while np.sum(supply_copy) > 0 and np.sum(demand_copy) > 0:
        # Calculate penalty (difference between two smallest costs) for each row and column
        row_penalties = []
        for i in range(len(supply_copy)):
            if supply_copy[i] > 0:
                row = [costs_copy[i,j] for j in range(len(demand_copy)) if demand_copy[j] > 0]
                if len(row) >= 2:
                    row_sorted = sorted(row)
                    row_penalties.append(row_sorted[1] - row_sorted[0])
                else:
                    row_penalties.append(0)
            else:
                row_penalties.append(-1)  # Mark exhausted rows
        
        col_penalties = []
        for j in range(len(demand_copy)):
            if demand_copy[j] > 0:
                col = [costs_copy[i,j] for i in range(len(supply_copy)) if supply_copy[i] > 0]
                if len(col) >= 2:
                    col_sorted = sorted(col)
                    col_penalties.append(col_sorted[1] - col_sorted[0])
                else:
                    col_penalties.append(0)
            else:
                col_penalties.append(-1)  # Mark exhausted columns
        
        # Find maximum penalty
        max_row_penalty = max(row_penalties)
        max_col_penalty = max(col_penalties)
        
        if max_row_penalty >= max_col_penalty:
            # Select row with maximum penalty
            selected_row = row_penalties.index(max_row_penalty)
            
            # Find minimum cost in selected row
            min_cost = np.inf
            selected_col = -1
            for j in range(len(demand_copy)):
                if demand_copy[j] > 0 and costs_copy[selected_row, j] < min_cost:
                    min_cost = costs_copy[selected_row, j]
                    selected_col = j
        else:
            # Select column with maximum penalty
            selected_col = col_penalties.index(max_col_penalty)
            
            # Find minimum cost in selected column
            min_cost = np.inf
            selected_row = -1
            for i in range(len(supply_copy)):
                if supply_copy[i] > 0 and costs_copy[i, selected_col] < min_cost:
                    min_cost = costs_copy[i, selected_col]
                    selected_row = i
        
        if selected_row == -1 or selected_col == -1:
            break
        
        # Allocate as much as possible
        quantity = min(supply_copy[selected_row], demand_copy[selected_col])
        allocation[selected_row, selected_col] = quantity
        
        # Update supply and demand
        supply_copy[selected_row] -= quantity
        demand_copy[selected_col] -= quantity
        
        # Mark exhausted rows/columns in cost matrix
        if supply_copy[selected_row] == 0:
            costs_copy[selected_row, :] = np.inf
        if demand_copy[selected_col] == 0:
            costs_copy[:, selected_col] = np.inf
    
    # Calculate total cost
    total_cost = np.sum(allocation * costs)
    
    return allocation, total_cost