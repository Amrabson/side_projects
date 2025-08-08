# cash_register/payment.py
from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    """Abstract base for payment processing."""
    @abstractmethod
    def process(self, amount: float) -> bool:
        pass

class CashPaymentProcessor(PaymentProcessor):
    def process(self, amount: float) -> bool:
        # real world: open cash drawer, record payment
        print(f"Received cash: {amount:.2f}")
        return True
