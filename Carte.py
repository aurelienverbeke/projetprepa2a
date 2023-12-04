class Carte:

    def __init__(self, motif, valeur):
        self.motif = motif
        self.valeur = valeur
        
    def __lt__(self, other):
        return self.valeur < other.valeur
    
    def __gt__(self, other):
        return other.__it__(self)
    
    def __eq__(self, other):
        return self.valeur == other.valeur
    
    def __ge__(self, other):
        return self.valeur >= other.valeur
    
    def __le__(self, other):
        return self.valeur <= other.valeur
