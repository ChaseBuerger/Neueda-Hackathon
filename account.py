class Account:
    def __init__(self, account_type, account_name=None):
        self.account_type = account_type
        self.account_name = account_name  # New property
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

    def apply_interest(self, months=1):
        """
        Apply interest to the account balance for the given number of months.
        Only applicable for savings accounts.
        """
        if self.account_type == "savings":
            for _ in range(months):
                self.balance += self.balance * self.interest_rate

    def get_balance(self):
        return self.balance

    def get_account_name(self):
        return self.account_name

    def set_account_name(self, name):
        self.account_name = name

    def to_dict(self):
        return {
            "account_type": self.account_type,
            "account_name": self.account_name,  # Include account_name in serialization
            "balance": self.balance,
            "interest_rate": self.interest_rate
        }

    @classmethod
    def from_dict(cls, data):
        account = cls(data["account_type"], data.get("account_name"))  # Deserialize account_name
        account.balance = data["balance"]
        account.interest_rate = data["interest_rate"]
        return account
