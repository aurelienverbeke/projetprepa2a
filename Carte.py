class Carte:
    """
    Attributs :
        - motif (str) : couleur de la carte, peut valoir K pour carreau, C pour coeur, T pour trefle, P pour pic, J pour joker
        - valeur (int) : valeur de la carte, peut valoir un entier de 7 a 14, et 0 pour joker
    """

    def __init__(self, motif, valeur):
        """
        Parametres: voir attributs de la classe
        """
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





    def __str__(self):
        """
        Retourne le caractere unicode de la carte, pour pouvoir l'afficher
        """

        if self.motif == "J":
            return chr(0x1f0df)

        if self.motif == "P":
            if self.valeur = 14:
                return chr(0x1f0a1)
            return chr(0x1f0a0 + self.valeur)
        
        if self.motif == "C":
            if self.valeur = 14:
                return chr(0x1f0b1)
            return chr(0x1f0b0 + self.valeur)
        
        if self.motif == "K":
            if self.valeur = 14:
                return chr(0x1f0b1)
            return chr(0x1f0c0 + self.valeur)
        
        if self.motif == "T":
            if self.valeur = 14:
                return chr(0x1f0b1)
            return chr(0x1f0d0 + self.valeur)
