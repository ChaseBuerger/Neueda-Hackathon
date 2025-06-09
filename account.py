class Account:
    def __init__(self, account_type):
        self.account_type = account_type
        self.balance = 0.0
        self.interest_rate = 0.02 if account_type == "savings" else 0.0

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return True
        return False

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            return True
        return False

    def calculate_interest(self):
        if self.account_type == "savings":
            return self.balance * self.interest_rate
        return 0.0

    def get_balance(self):
        return self.balance

    def to_dict(self):
        return {
            "account_type": self.account_type,
            "balance": self.balance,
            "interest_rate": self.interest_rate
        }

    @classmethod
    def from_dict(cls, data):
        account = cls(data["account_type"])
        account.balance = data["balance"]
        account.interest_rate = data["interest_rate"]
        return account
