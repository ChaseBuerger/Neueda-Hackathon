from user import User
from account import Account

class Bank:
    def __init__(self):
        self.users = {}  # Maps username to User objects
        self.accounts = {}  # Maps username to Account objects

    def create_account(self, username, password, account_type):
        if username in self.users:
            print("Username already exists.")
            return False
        user = User(username, password)
        account = Account(account_type)
        self.users[username] = user
        self.accounts[username] = account
        return True

    def login(self, username, password):
        user = self.users.get(username)
        if user and user.password == password:
            return True
        return False

    def get_account(self, username):
        return self.accounts.get(username)

    def deposit(self, username, amount):
        account = self.get_account(username)
        if not account:
            return "Account not found."
        if amount <= 0:
            return "Deposit amount must be greater than zero."
        account.deposit(amount)
        return "Deposit successful."

    def withdraw(self, username, amount):
        account = self.get_account(username)
        if not account:
            return "Account not found."
        if amount <= 0:
            return "Withdrawal amount must be greater than zero."
        if amount > account.balance:
            return f"Insufficient balance. Current balance: {account.balance:.2f}"
        account.withdraw(amount)
        return "Withdrawal successful."

    def save_to_data(self):
        return {
            "users": {username: user.to_dict() for username, user in self.users.items()},
            "accounts": {username: account.to_dict() for username, account in self.accounts.items()}
        }

    def load_from_data(self, data):
        self.users = {username: User.from_dict(user_data) for username, user_data in data.get("users", {}).items()}
        self.accounts = {username: Account.from_dict(account_data) for username, account_data in data.get("accounts", {}).items()}
