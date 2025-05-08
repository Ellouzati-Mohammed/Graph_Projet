
from data.graph_models import MatriceAdjacence

graph = MatriceAdjacence(oriente=False)
graph.ajouter_arete('A', 'B', 2)   # A -> B (poids 2)
graph.ajouter_arete('A', 'D', 1)   # A -> D (poids 1)
graph.ajouter_arete('B', 'C', 3)   # B -> C (poids 3)
graph.ajouter_arete('B', 'E', 5)   # B -> E (poids 5)
graph.ajouter_arete('D', 'B', 1)   # D -> B (poids 1)
graph.ajouter_arete('D', 'E', 2)   # D -> E (poids 2)
graph.ajouter_arete('E', 'C', 1)   # E -> C (poids 1)

