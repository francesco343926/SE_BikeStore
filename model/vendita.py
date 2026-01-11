from dataclasses import dataclass
import datetime

@dataclass
class Vendita:
    id: int
    order_id: int
    product_id: int
    quantity: int
    list_price : float
    discount: float
    date: datetime.datetime