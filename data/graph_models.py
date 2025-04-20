
class MatriceAdjacence:

    def __init__(self,oriente=False):
        self.sommets = []
        self.matrice = []
        self.oriente = oriente
   
    def ajouter_sommet(self, sommet):
        if sommet not in self.sommets:
            self.sommets.append(sommet)
            for ligne in self.matrice:
                ligne.append(0) #ajouter uun nouvelle colone
            self.matrice.append([0] * len(self.sommets))   # Ajouter une nouvelle ligne

    def ajouter_arete(self, sommet1, sommet2, poids=1): #pour n Graphe non pondéré, le poid et toujour1, si non on peut specifier le poid
        if sommet1 not in self.sommets:
            self.ajouter_sommet(sommet1)
        if sommet2 not in self.sommets:
            self.ajouter_sommet(sommet2)

        i = self.sommets.index(sommet1)
        j = self.sommets.index(sommet2)

        self.matrice[i][j] = poids
        if not self.oriente:  # le cas de non orienter
            self.matrice[j][i] = poids
    
    def get_graphe(self):
        return {
            "sommets": self.sommets,
            "matrice": self.matrice,
            "oriente": self.oriente
        }