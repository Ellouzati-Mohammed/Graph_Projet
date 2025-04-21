# This will guarantee different results
vogel_costs = [
    [4, 3, 8],  # Row 0
    [2, 5, 7],  # Row 1 (absolute min = 2 at [1,0])
    [6, 1, 9]   # Row 2 (Vogel will prioritize this due to high penalty)
]
vogel_supply = [50, 75, 125]
vogel_demand = [100, 80, 70]