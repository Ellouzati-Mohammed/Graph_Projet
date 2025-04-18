
from data.graph_models import MatriceAdjacence

graph = MatriceAdjacence(oriente=False)
graph.ajouter_arete('A', 'B', 1)
graph.ajouter_arete('B', 'C', 1)
graph.ajouter_arete('A', 'D', 1)
graph.ajouter_arete('B', 'E', 2)
graph.ajouter_arete('C', 'D', 7)
graph.ajouter_arete('C', 'E', 1)
graph.ajouter_arete('D', 'E', 1)