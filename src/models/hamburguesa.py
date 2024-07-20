from src.models.ingrediente import Ingrediente


class Hamburguesa:
    def __init__(self, id, nombre, price, descripcion, imgUrl, ingredientes=None):
        self.id = id
        self.nombre = nombre
        self.price = price
        self.descripcion = descripcion
        self.imgUrl = imgUrl
        self.ingredientes = Ingrediente(**(ingredientes or {}))

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "price": self.price,
            "descripcion": self.descripcion,
            "imgUrl": self.imgUrl,
            "ingredientes": self.ingredientes
        }