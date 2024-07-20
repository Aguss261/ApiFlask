from datetime import datetime
from typing import List

from src.models.hamburguesa import Hamburguesa


class Pedido:
    def __init__(self,
                 user_id: int,
                 direccion: str,
                 price: float,
                 state: [str] ,
                 hora: [datetime],
                 fecha: [datetime],
                 hamburguesas = None):

        self.user_id = user_id
        self.hamburguesas = Hamburguesa(**(hamburguesas or {}))
        self.direccion = direccion
        self.price = price
        self.state = state
        self.hora = hora
        self.fecha = fecha

    def to_dict(self) -> dict:
        return {
            'user_id': self.user_id,
            'hamburguesas': self.hamburguesas,
            'direccion': self.direccion,
            'price': self.price,
            'state': self.state,
            'hora': self.hora.isoformat() if self.hora else None,
            'fecha': self.fecha.isoformat() if self.fecha else None
        }