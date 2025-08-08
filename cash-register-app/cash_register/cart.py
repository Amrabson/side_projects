# cash_register/cart.py
from typing import List
from .item import Item

class Cart:
    """Manages a collection of Items."""
    def __init__(self):
        self._items: List[Item] = []

    def add_item(self, item: Item) -> None:
        self._items.append(item)

    def remove_item(self, index: int) -> None:
        del self._items[index]

    def update_quantity(self, index: int, quantity: int) -> None:
        self._items[index].quantity = quantity

    @property
    def subtotal(self) -> float:
        return sum(item.total_price for item in self._items)

    @property
    def item_count(self) -> int:
        return sum(item.quantity for item in self._items)

    def clear(self) -> None:
        self._items.clear()
