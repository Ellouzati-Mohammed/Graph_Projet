
from data.graph_models import MatriceAdjacence

graph = MatriceAdjacence(oriente=False)
graph.ajouter_arete('A', 'B', 1)
graph.ajouter_arete('B', 'C', 1)
graph.ajouter_arete('A', 'D', 1)
graph.ajouter_arete('B', 'E', 1)
graph.ajouter_arete('C', 'D', 1)
graph.ajouter_arete('C', 'E', 1)
graph.ajouter_arete('F', 'E', 1)
graph.ajouter_arete('L', 'E', 1)
graph.ajouter_arete('K', 'E', 1)
graph.ajouter_arete('K', 'A', 1)
graph.ajouter_arete('K', 'A', 1)
graph.ajouter_arete('K', 'E', 1)
graph.ajouter_arete('K', 'F', 1)

