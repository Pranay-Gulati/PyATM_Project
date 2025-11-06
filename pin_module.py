import time
from account_module import mask_account, validate_pin, save_accounts

MAX_ATTEMPTS = 3

# ---------------- Login / PIN Change ----------------
def login_flow(data, get_pin):
    print("\n==== ATM Login ====\n")
    acc = input("Enter 12-digit Account Number: ").strip()
    if not acc.isdigit() or len(acc) != 12:
        print("Invalid account number.\n")
        time.sleep(0.5)
        return ""
    if acc not in data:
        print("Account not found.\n")
        time.sleep(0.5)
        return ""
    stored_pin, _ = data[acc]

    attempts = 0
    while attempts < MAX_ATTEMPTS:
        pin = get_pin("Enter PIN: ")
        if pin == stored_pin:
            print("\nLogin successful.\n")
            time.sleep(0.5)
            return acc
        attempts += 1
        print(f"Wrong PIN. Attempts left: {MAX_ATTEMPTS - attempts}\n")
        time.sleep(0.5)

    print("Account locked due to 3 incorrect attempts.\n")
    time.sleep(0.5)
    return ""

def change_pin_flow(acc, data, get_pin):
    if acc not in data:
        print("Account not found.\n")
        time.sleep(0.5)
        return False
    stored_pin, bal = data[acc]

    old = get_pin("Enter old PIN: ")
    if old != stored_pin:
        print("Incorrect old PIN.\n")
        time.sleep(0.5)
        return False

    new1 = get_pin("Enter new PIN: ")
    if not validate_pin(new1):
        print("Invalid PIN. Must be 4 digits.\n")
        time.sleep(0.5)
        return False

    new2 = get_pin("Re-enter new PIN: ")
    if new1 != new2:
        print("PIN mismatch. Try again.\n")
        time.sleep(0.5)
        return False

    data[acc] = (new1, bal)
    if save_accounts(data):
        print(f"PIN successfully changed for account {mask_account(acc)}.\n")
        time.sleep(0.5)
        return True
    else:
        print("Failed to save new PIN.\n")
        time.sleep(0.5)
        return False
