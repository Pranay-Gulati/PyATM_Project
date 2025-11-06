# account_module.py
import os
from typing import Dict, Tuple
import time

ACCOUNTS_FILE = "accounts.txt"

# ---------------- PIN masked input (*) → Cross-platform ----------------
def get_pin(prompt="Enter 4-digit PIN: "):
    """Cross-platform PIN input with stars, works on Windows too"""
    import sys

    # fallback for Windows
    try:
        import msvcrt  # Windows-only
        print(prompt, end="", flush=True)
        pin = ""
        while True:
            ch = msvcrt.getch()
            if ch in [b"\r", b"\n"]:
                print()
                break
            elif ch == b"\x08":  # backspace
                if len(pin) > 0:
                    pin = pin[:-1]
                    print("\b \b", end="", flush=True)
            elif ch.isdigit() and len(pin) < 4:
                pin += ch.decode()
                print("*", end="", flush=True)
    except ImportError:
        # fallback to normal input if msvcrt not available
        pin = input(prompt)
    return pin



# ---------------- Utilities ----------------
def _ensure_accounts_file():
    if not os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, "w", encoding="utf-8") as f:
            f.write("")

def validate_account_number(acc: str) -> bool:
    return acc.isdigit() and len(acc) == 12

def validate_pin(pin: str) -> bool:
    return pin.isdigit() and len(pin) == 4

def mask_account(acc: str) -> str:
    return "********" + acc[-4:]


# ---------------- File operations ----------------
def load_accounts() -> Dict[str, Tuple[str, float]]:
    _ensure_accounts_file()
    data = {}
    try:
        with open(ACCOUNTS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                parts = [p.strip() for p in line.split(",")]
                if len(parts) != 3:
                    continue
                acc, pin, bal = parts
                if not validate_account_number(acc) or not validate_pin(pin):
                    continue
                try:
                    bal = float(bal)
                except:
                    continue
                data[acc] = (pin, bal)
    except:
        pass
    return data

def save_accounts(data: Dict[str, Tuple[str, float]]) -> bool:
    try:
        with open(ACCOUNTS_FILE, "w", encoding="utf-8") as f:
            for acc, (pin, bal) in data.items():
                f.write(f"{acc},{pin},{bal}\n")
        return True
    except:
        return False


# ---------------- Account create / display ----------------
def create_account_interactive(data, get_pin):
    import time
    print("\n==== Create Account ====\n")
    while True:
        acc = input("Enter 12-digit Account Number: ").strip()
        if not validate_account_number(acc):
            print("Invalid account number.\n")
            continue
        if acc in data:
            print("Account already exists.\n")
            continue
        break

    while True:
        pin = get_pin("Create 4-digit PIN: ")
        if not validate_pin(pin):
            print("Invalid PIN.\n")
            continue
        pin2 = get_pin("Re-enter PIN: ")
        if pin != pin2:
            print("PIN mismatch.\n")
            continue
        break

    data[acc] = (pin, 0.0)
    if save_accounts(data):
        print(f"\nAccount Created: {mask_account(acc)}, Balance ₹0.00\n")
        input("Press Enter to continue...")
        
        return acc
    print("\nFailed to create account.\n")
    input("Press Enter to continue...")
    return ""


def display_account_info(acc, data):
    if acc not in data:
        print("Account not found.\n")
        return
    pin, bal = data[acc]
    print("\n------ Account Info ------")
    print(f"Account: {mask_account(acc)}")
    print(f"Balance: ₹{bal:.2f}")
    print("--------------------------\n")
    input("Press Enter to continue...")       
