# cash_register/item.py
from dataclasses import dataclass

@dataclass
class Item:
    """Represents a product being purchased."""
    name: str
    unit_price: float
    quantity: int = 1

    @property
    def total_price(self) -> float:
        return round(self.unit_price * self.quantity, 2)
