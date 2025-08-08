# cash_register/register.py
from typing import Optional, List
from .cart import Cart
from .payment import PaymentProcessor

class CashRegister:
    """Handles totals, taxes, discounts, and payments."""
    def __init__(self,
                 cart: Optional[Cart] = None,
                 payment_processor: Optional[PaymentProcessor] = None,
                 tax_rate: float = 0.0,
                 discounts: Optional[List[float]] = None):
        self.cart = cart or Cart()
        self.payment_processor = payment_processor
        self.tax_rate = tax_rate
        self.discounts = discounts or []

    @property
    def total(self) -> float:
        total = self.cart.subtotal
        total += total * self.tax_rate
        for d in self.discounts:
            total -= d
        return round(total, 2)

    def charge(self) -> bool:
        if not self.payment_processor:
            raise RuntimeError("No payment processor configured")
        return self.payment_processor.process(self.total)
