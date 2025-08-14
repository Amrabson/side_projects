# Cash Register App

A modular, object-oriented cash register application built in Python.  
Designed as a package, it provides a command-line interface for managing sales, calculating totals, applying taxes/discounts, processing payments, and printing receipts.

---

## Features

- **Add, update, or remove items** to a shopping cart
- **Automatic subtotal, tax, and total calculations**
- **Command-line interface** for easy operation and demonstration
- **Abstracted payment processing** (extensible for future types)
- **Formatted receipt printing** to the console
- Modular package structure for reusability and testing

---

## Project Structure
cash_register_app/ <br>
    ├── cash_register/       <-- your package<br>
    │   ├── __init__.py<br>
    │   ├── cart.py<br>
    │   ├── cli.py<br>
    │   ├── item.py<br>
    │   ├── payment.py<br>
    │   ├── register.py<br>
    │   └── receipt.py<br>
    └── main.py              <-- your launcher stub<br>

---

## How to Run

1. **Install requirements:**  
   (Python 3.7+ recommended; no external dependencies needed)

2. **Run the app:**  
   From the root directory:
   ```bash
   python main.py --tax 0.07
3. **Usage in CLI:**
  - To add an item:
  Enter: Milk,2.99,2 (name, price, quantity)
  - To pay:
  Enter: pay
  - To exit without paying:
  Enter: quit
  - Receipt is printed to the console upon payment

---

**Example** <br>
=== Cash Register === <br>
Add item (name,price,qty), 'pay', or 'quit': Bread,3.49,1 <br>
Added: 1 x 'Bread' at 3.49 each. <br>
Add item (name,price,qty), 'pay', or 'quit': pay <br>
Received cash: 3.73 <br>

====== Receipt ====== <br>
1. Bread x1 @ 3.49 = 3.49 <br>

Subtotal: 3.49 <br>
Tax (7.0%): 0.24 <br>
Total: 3.73

---

**Author**
Aharon Rabson
GitHub: @Amrabson

