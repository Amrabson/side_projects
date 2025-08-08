# cash_register/receipt.py
from .cart import Cart
from .register import CashRegister

class ReceiptPrinter:
    """Formats and outputs the receipt."""
    def __init__(self, cart: Cart, register: CashRegister):
        self.cart = cart
        self.register = register

    def print_to_console(self) -> None:
        print("\n====== Receipt ======")
        for idx, item in enumerate(self.cart._items, start=1):
            print(f"{idx}. {item.name} x{item.quantity} @ {item.unit_price:.2f} = {item.total_price:.2f}")
        print(f"\nSubtotal: {self.cart.subtotal:.2f}")
        print(f"Tax ({self.register.tax_rate * 100:.1f}%): {(self.cart.subtotal * self.register.tax_rate):.2f}")
        for d in self.register.discounts:
            print(f"Discount: -{d:.2f}")
        print(f"Total: {self.register.total:.2f}")
