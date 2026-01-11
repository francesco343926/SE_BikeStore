from dataclasses import dataclass

@dataclass
class Prodotto:
    id: int
    name : str
    category_id : int
    list_price : float
    num_vendite : int
    score : int

    def __hash__(self):
        return hash(self.id)