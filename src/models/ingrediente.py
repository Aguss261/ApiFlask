class Ingrediente:
    def __init__(self, huevo, lechuga, tomate, cebolla, bacon, pepino):
        self.huevo = huevo
        self.lechuga = lechuga
        self.tomate = tomate
        self.cebolla = cebolla
        self.bacon = bacon
        self.pepino = pepino

    def to_dict(self):
        return {
            "huevo": self.huevo,
            "lechuga": self.lechuga,
            "tomate": self.tomate,
            "cebolla": self.cebolla,
            "bacon": self.bacon,
            "pepino": self.pepino
        }
