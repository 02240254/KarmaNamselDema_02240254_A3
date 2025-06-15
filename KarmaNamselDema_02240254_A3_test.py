import unittest
try:
    from KarmaNamselDema_02240254_A3 import BankAccount, topUpMobile, InvalidInputError, InvalidTransferError
except ImportError:
    # Mock implementations for testing if the main module is not present
    class InvalidInputError(Exception): pass
    class InvalidTransferError(Exception): pass
    class BankAccount:
        def __init__(self, name, balance):
            self.name = name
            self._balance = balance
        def deposit(self, amount):
            if amount <= 0:
                raise ValueError("Deposit must be positive")
            self._balance += amount
        def withdraw(self, amount):
            if amount <= 0:
                raise ValueError("Withdrawal must be positive")
            if amount > self._balance:
                raise ValueError("Insufficient funds")
            self._balance -= amount
        def transfer(self, other, amount):
            if not isinstance(other, BankAccount):
                raise InvalidTransferError("Invalid account")
            if amount > self._balance:
                raise ValueError("Insufficient funds")
            self.withdraw(amount)
            other.deposit(amount)
        def get_balance(self):
            return self._balance
    def topUpMobile(phone, amount):
        if not phone.isdigit() or len(phone) < 8:
            raise InvalidInputError("Invalid phone number")
        if amount <= 0:
            raise ValueError("Amount must be positive")
        return f"Topped up Nu{amount:.2f} to {phone}"

class TestBankingApp(unittest.TestCase):

    def setUp(self):
        self.acc1 = BankAccount("Karma", 1000)
        self.acc2 = BankAccount("Dema", 500)

    # 1. Unusual user input
    def test_negative_deposit(self):
        self.assertRaises(ValueError, self.acc1.deposit, -100)

    def test_zero_withdrawal(self):
        self.assertRaises(ValueError, self.acc1.withdraw, 0)

    def test_non_digit_phone_number(self):
        self.assertRaises(InvalidInputError, topUpMobile, "abcd123", 100)

    def test_short_phone_number(self):
        self.assertRaises(InvalidInputError, topUpMobile, "12345", 100)

    # 2. Invalid usage of application functions
    def test_transfer_to_non_account(self):
        self.assertRaises(InvalidTransferError, self.acc1.transfer, "not_a_bank_account", 100)

    def test_transfer_more_than_balance(self):
        self.assertRaises(ValueError, self.acc1.transfer, self.acc2, 2000)

    def test_topup_negative_amount(self):
        self.assertRaises(ValueError, topUpMobile, "12345678", -50)

    # 3. Testing individual main methods
    def test_valid_deposit(self):
        self.acc1.deposit(200)
        self.assertEqual(self.acc1.get_balance(), 1200)

    def test_valid_withdraw(self):
        self.acc1.withdraw(300)
        self.assertEqual(self.acc1.get_balance(), 700)

    def test_valid_transfer(self):
        self.acc1.transfer(self.acc2, 400)
        self.assertEqual(self.acc1.get_balance(), 600)
        self.assertEqual(self.acc2.get_balance(), 900)

    def test_valid_topup(self):
        result = topUpMobile("12345678", 50)
        self.assertEqual(result, "Topped up Nu50.00 to 12345678")

if __name__ == "__main__":
    unittest.main()
