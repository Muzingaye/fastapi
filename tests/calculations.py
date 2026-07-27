def add(num1: int, num2):
    return num1 + num2


def subtract(num1: int, num2):
    return num1 - num2


class BankAccount:
    def __init__(self, account_holder, initial_balance=0):
        self.account_holder = account_holder
        self.balance = initial_balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise ValueError("Insufficient funds.")
        self.balance -= amount
        return self.balance

    def get_balance(self):
        return self.balance

    def collect_interest(self, rate):
        if rate < 0:
            raise ValueError("Interest rate cannot be negative.")
        self.balance += self.balance * rate
        return self.balance

    def __str__(self):
        return f"Account Holder: {self.account_holder}, Balance: R{self.balance:.2f}"