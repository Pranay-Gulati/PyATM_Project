import os
from datetime import datetime
from typing import Dict

# ---------------- Transaction Manager ----------------
class TransactionManager:
    def __init__(self, account: str, data: Dict[str, tuple], stack_limit=20):
        self.account = account
        self.data = data
        self.stack_limit = stack_limit
        self._history_stack = []

    @property
    def _trans_file(self):
        return f"transactions_{self.account}.txt"

    def _timestamp(self):
        return datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    def _push(self, entry):
        self._history_stack.append(entry)
        if len(self._history_stack) > self.stack_limit:
            self._history_stack.pop(0)

    def _append_log(self, entry):
        try:
            with open(self._trans_file, "a", encoding="utf-8") as f:
                f.write(entry + "\n")
        except:
            pass

    def _save_balance(self, new_balance):
        pin, _ = self.data[self.account]
        self.data[self.account] = (pin, new_balance)
        try:
            with open("accounts.txt", "w", encoding="utf-8") as f:
                for acc, (pin, bal) in self.data.items():
                    f.write(f"{acc},{pin},{bal}\n")
            return True
        except:
            return False

    def balance(self):
        import time
        pin, bal = self.data[self.account]
        entry = f"[{self._timestamp()}] BALANCE: ₹{bal:.2f}"
        self._push(entry)
        self._append_log(entry)
        print(f"\nBalance: ₹{bal:.2f}\n")
        input("Press Enter to continue...")
        return bal

    def deposit(self, amount):
        import time
        if amount <= 0:
            print("Invalid amount.\n")
            return False
        pin, bal = self.data[self.account]
        new_bal = bal + amount
        if not self._save_balance(new_bal):
            print("Failed.\n")
            return False
        entry = f"[{self._timestamp()}] DEPOSIT: +₹{amount:.2f} | ₹{new_bal:.2f}"
        self._push(entry)
        self._append_log(entry)
        print("\nDeposit Successful.\n")
        input("Press Enter to continue...")
        return True

    def withdraw(self, amount):
        import time
        if amount <= 0:
            print("Invalid amount.\n")
            return False
        pin, bal = self.data[self.account]
        if amount > bal:
            print("Insufficient balance.\n")
            return False
        new_bal = bal - amount
        if not self._save_balance(new_bal):
            print("Failed.\n")
            return False
        entry = f"[{self._timestamp()}] WITHDRAW: -₹{amount:.2f} | ₹{new_bal:.2f}"
        self._push(entry)
        self._append_log(entry)
        print("\nWithdraw Successful.\n")
        input("Press Enter to continue...")
        return True

    def recent_history(self):
        import time
        if not self._history_stack:
            print("\nNo transaction history.\n")
            time.sleep(0.5)
            return
        print("\n---- Recent Transactions ----")
        for x in self._history_stack[-10:]:
            print(x)
        print("-----------------------------\n")
        input("Press Enter to continue...")
