import tkinter as tk
from tkinter import messagebox

# === Custom Exceptions ===
class InvalidInputError(Exception):
    pass

class InvalidTransferError(Exception):
    pass

# === BankAccount Class ===
class BankAccount:
    def __init__(self, name, balance=0.0):
        self.name = name
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise ValueError("Insufficient balance.")
        self.balance -= amount

    def transfer(self, other_account, amount):
        if not isinstance(other_account, BankAccount):
            raise InvalidTransferError("Recipient must be a BankAccount.")
        self.withdraw(amount)
        other_account.deposit(amount)

    def get_balance(self):
        return self.balance

    def set_name(self, new_name):
        self.name = new_name

# === Top-Up Function ===
def top_up_mobile(phone_number, amount):
    if not (phone_number.isdigit() and len(phone_number) >= 8):
        raise InvalidInputError("Invalid phone number.")
    if amount <= 0:
        raise ValueError("Top-up amount must be positive.")
    return f"Topped up Nu{amount:.2f} to {phone_number}"

# === GUI Application ===
class BankingApp:
    def __init__(self, master):
        self.master = master
        master.title("Banking App - Karma Namsel Dema")

        self.acc1 = BankAccount("Karma", 1000)
        self.acc2 = BankAccount("Dema", 500)

        # Account Holder
        tk.Label(master, text="Account Holder Name:").grid(row=0, column=0, sticky="e", pady=5)
        self.name_entry = tk.Entry(master)
        self.name_entry.insert(0, self.acc1.name)
        self.name_entry.grid(row=0, column=1)

        # Amount Input
        tk.Label(master, text="Amount (Nu):").grid(row=1, column=0, sticky="e", pady=5)
        self.amount_entry = tk.Entry(master)
        self.amount_entry.grid(row=1, column=1)

        # Phone Number Input
        tk.Label(master, text="Phone Number:").grid(row=2, column=0, sticky="e", pady=5)
        self.phone_entry = tk.Entry(master)
        self.phone_entry.grid(row=2, column=1)

        # Buttons
        tk.Button(master, text="Set Account Holder", command=self.set_account_holder).grid(row=3, column=0, columnspan=2, sticky="ew")
        tk.Button(master, text="Deposit", command=self.deposit).grid(row=4, column=0, sticky="ew")
        tk.Button(master, text="Withdraw", command=self.withdraw).grid(row=4, column=1, sticky="ew")
        tk.Button(master, text="Transfer", command=self.transfer).grid(row=5, column=0, sticky="ew")
        tk.Button(master, text="Mobile Top-Up", command=self.topup).grid(row=5, column=1, sticky="ew")
        tk.Button(master, text="Check Balance", command=self.check_balance).grid(row=6, column=0, columnspan=2, sticky="ew")

        self.output = tk.Label(master, text="", fg="blue")
        self.output.grid(row=7, column=0, columnspan=2, pady=10)

    def get_amount(self):
        try:
            return float(self.amount_entry.get())
        except ValueError:
            raise InvalidInputError("Please enter a valid number for amount.")

    def get_phone_number(self):
        phone = self.phone_entry.get()
        if not (phone.isdigit() and len(phone) >= 8):
            raise InvalidInputError("Invalid phone number.")
        return phone

    def set_account_holder(self):
        new_name = self.name_entry.get().strip()
        if not new_name:
            messagebox.showerror("Error", "Account holder name cannot be empty.")
            return
        self.acc1.set_name(new_name)
        self.output.config(text=f"Account holder updated to {new_name}.")

    def deposit(self):
        try:
            amount = self.get_amount()
            self.acc1.deposit(amount)
            self.output.config(text=f"Deposit successful to {self.acc1.name}.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def withdraw(self):
        try:
            amount = self.get_amount()
            self.acc1.withdraw(amount)
            self.output.config(text=f"Withdrawal successful from {self.acc1.name}.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def transfer(self):
        try:
            amount = self.get_amount()
            self.acc1.transfer(self.acc2, amount)
            self.output.config(text=f"Transferred Nu{amount:.2f} from {self.acc1.name} to {self.acc2.name}.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def topup(self):
        try:
            phone = self.get_phone_number()
            amount = self.get_amount()
            # Subtract the top-up amount from the account balance
            self.acc1.withdraw(amount)
            result = top_up_mobile(phone, amount)
            self.output.config(text=result)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def check_balance(self):
        balance = self.acc1.get_balance()
        self.output.config(text=f"{self.acc1.name}'s Balance: Nu{balance:.2f}")

# === Launch App ===
if __name__ == "__main__":
    root = tk.Tk()
    app = BankingApp(root)
    root.mainloop()

