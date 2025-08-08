# cash_register/cli.py

"""
Command-Line Interface for the Cash Register application.
Handles parsing arguments, reading user commands, processing payments, and printing receipts.
"""

import argparse                                   # For parsing command-line options
from .item import Item                            # Data model for each product
from .payment import CashPaymentProcessor         # Concrete cash payment processor
from .register import CashRegister                # Core register logic (totals, taxes, etc.)
from .receipt import ReceiptPrinter               # Formats and prints the receipt
from .cart import Cart                            # Holds Items and computes subtotals

def main():
    """
    Entry point for the Cash Register CLI.
    - Parses --tax option
    - Repeatedly prompts for commands:
        * “<name>,<price>,<qty>” to add an item
        * “pay” to process payment and print a receipt
        * “quit” to exit without payment
    """
    # 1. Parse command-line arguments
    parser = argparse.ArgumentParser(description="Cash Register CLI")
    parser.add_argument(
        "--tax",
        type=float,
        default=0.0,
        help="Tax rate (e.g. 0.07 for 7%)"
    )
    args = parser.parse_args()

    # 2. Initialize core components
    cart = Cart()
    register = CashRegister(
        cart=cart,
        payment_processor=CashPaymentProcessor(),
        tax_rate=args.tax
    )

    # 3. Welcome message
    print("=== Cash Register ===")

    # 4. Main input loop
    while True:
        cmd = input("Add item (name,price,qty), 'pay', or 'quit': ").strip()

        # Quit command
        if cmd.lower() == "quit":
            print("Exiting without payment.")
            break

        # Payment command: attempt to charge and print receipt
        if cmd.lower() == "pay":
            success = register.charge()
            if success:
                ReceiptPrinter(cart, register).print_to_console()
                break
            else:
                print("Payment failed. Please try again.")
                continue

        # Otherwise, try to parse “name,price,qty” and add to cart
        try:
            name, price_str, qty_str = cmd.split(",")
            item = Item(
                name=name.strip(),
                unit_price=float(price_str),
                quantity=int(qty_str)
            )
            cart.add_item(item)
            print(f"Added: {item.quantity} x '{item.name}' at {item.unit_price:.2f} each.")
        except ValueError:
            # Triggered if split fails or conversion to float/int fails
            print("Invalid input. Usage: <name>,<price>,<quantity>")
        except Exception as e:
            # Catch-all for unexpected errors
            print(f"Error: {e}. Please try again.")
