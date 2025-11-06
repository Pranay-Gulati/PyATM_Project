import os
import sys
import time
from datetime import datetime
from account_module import (
    load_accounts,
    create_account_interactive,
    display_account_info,
    get_pin
)
from transaction_module import TransactionManager
from pin_module import login_flow, change_pin_flow

# ---------------- Clear Screen Utility ----------------
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# ---------------- Session Menu ----------------
def session_menu(account, data):
    tm = TransactionManager(account, data)
    session_start = datetime.now()
    total_deposited = 0
    total_withdrawn = 0
    dcount = 0
    wcount = 0

    while True:
        clear_screen()
        print("===== ATM Menu =====")
        print("1. Check Account Balance")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. View Transaction History")
        print("5. Change ATM PIN")
        print("6. Account Information")
        print("7. LOG OUT")
        choice = input("Select (1-7): ").strip()

        if choice == "1":
            tm.balance()

        elif choice == "2":
            try:
                amt = float(input("Enter deposit amount: "))
            except:
                print("Invalid amount.\n")
                time.sleep(0.5)
                continue
            if tm.deposit(amt):
                dcount += 1
                total_deposited += amt

        elif choice == "3":
            try:
                amt = float(input("Enter withdrawal amount: "))
            except:
                print("Invalid amount.\n")
                time.sleep(0.5)
                continue
            if tm.withdraw(amt):
                wcount += 1
                total_withdrawn += amt

        elif choice == "4":
            tm.recent_history()

        elif choice == "5":
            if change_pin_flow(account, data, get_pin):
                print("Please login again.\n")
                time.sleep(1)
                return

        elif choice == "6":
            display_account_info(account, data)

        elif choice == "7":
            session_end = datetime.now()
            _, final_bal = data[account]
            print("\n==== Session Summary ====")
            print(f"Account:  {tm.account[-4:].rjust(12, '*')}")
            print(f"Login:    {session_start.strftime('%d-%m-%Y %H:%M:%S')}")
            print(f"Logout:   {session_end.strftime('%d-%m-%Y %H:%M:%S')}")
            print(f"Deposits: {dcount}  (₹{total_deposited:.2f})")
            print(f"Withdraw: {wcount}  (₹{total_withdrawn:.2f})")
            print(f"Final Balance: ₹{final_bal:.2f}\n")
            print("Thank you for using PyATM! Have a great day! 💳\n")
            print("\n==================================")
            time.sleep(1)
            return

        else:
            print("Invalid option. Try again.\n")
            time.sleep(0.5)

# ---------------- MAIN ----------------
def main():
    clear_screen()
    print("====================================")
    print("       💳 Welcome to PyATM 💳")
    print("====================================\n")
    time.sleep(0.5)

    data = load_accounts()

    while True:
        print("1. Login")
        print("2. Create Account")
        print("3. Exit")
        cmd = input("Select (1-3): ").strip()

        if cmd == "1":
            acc = login_flow(data, get_pin)
            if acc:
                session_menu(acc, data)

        elif cmd == "2":
            create_account_interactive(data, get_pin)

        elif cmd == "3":
            print("\nExiting PyATM. Thank you! 💳\n")
            time.sleep(1)
            sys.exit()

        else:
            print("Invalid option. Try again.\n")
            time.sleep(0.5)


if __name__ == "__main__":
    main()
