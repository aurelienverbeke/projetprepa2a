class Cartes:
    
    def __init__(self, motif, valeur):
        self.motif = motif
        self.valeur = valeur
        
        
    def __it__(self, other):
        if other.valeur == 1:
            return True
        elif self.valeur == 1:
            return False
        return self.valeur < other.valeur
    
    def __gt__(self, other):
        return other.__it__(self)
