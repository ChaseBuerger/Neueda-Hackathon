from user import User
from account import Account

class Bank:
    def __init__(self):
        self.users = {}  # Maps username to User objects
        self.accounts = {}  # Maps username to a dictionary of Account objects keyed by account name

    def create_account(self, username, password, account_type, account_name, initial_deposit):
        if username not in self.users:
            user = User(username, password)
            self.users[username] = user
        user_accounts = self.accounts.setdefault(username, {})
        if account_name in user_accounts:
            return f"Account {account_name} already exists."
        account = Account(account_type, account_name)
        account.deposit(initial_deposit)
        user_accounts[account_name] = account
        return f"Account {account_name} created successfully."

    def login(self, username, password):
        user = self.users.get(username)
        if user and user.password == password:
            return True
        return False

    def get_account(self, username, account_name):
        user_accounts = self.accounts.get(username, {})
        return user_accounts.get(account_name)

    def deposit(self, username, account_name, amount):
        try:
            account = self.get_account(username, account_name)
            if not account:
                raise ValueError(f"Account {account_name} not found.")
            if amount <= 0:
                raise ValueError("Deposit amount must be greater than zero.")
            account.deposit(amount)
            return f"Deposit successful to account {account_name}. Current balance: ${account.get_balance():.2f}"
        except ValueError as e:
            print(str(e))

    def withdraw(self, username, account_name, amount):
        account = self.get_account(username, account_name)
        if not account:
            return f"Account {account_name} not found."
        if amount <= 0:
            return "Withdrawal amount must be greater than zero."
        if amount > account.balance:
            return f"Insufficient balance in account {account_name}. Current balance: ${account.balance:.2f}"
        account.withdraw(amount)
        return f"Withdrawal successful from account {account_name}. Current balance: ${account.get_balance():.2f}"

    def save_to_data(self):
        return {
            "users": {username: user.to_dict() for username, user in self.users.items()},
            "accounts": {
                username: {name: account.to_dict() for name, account in accounts.items()}
                for username, accounts in self.accounts.items()
            }
        }

    def load_from_data(self, data):
        self.users = {username: User.from_dict(user_data) for username, user_data in data.get("users", {}).items()}
        self.accounts = {
            username: {name: Account.from_dict(account_data) for name, account_data in accounts.items()}
            for username, accounts in data.get("accounts", {}).items()
        }

    def simulate_growth(self, username, account_name, months):
        try:
            account = self.get_account(username, account_name)
            if not account:
                raise ValueError(f"Account {account_name} not found.")
            if account.account_type != "savings":
                raise ValueError("Interest simulation is only applicable for savings accounts.")
            
            projected_balance = account.balance
            for _ in range(months):
                projected_balance += projected_balance * account.interest_rate
            return f"Projected balance for account {account_name} after {months} months: ${projected_balance:.2f}"
        except ValueError as e:
            print(str(e))

    def apply_interest_to_all(self, months=1):
        for username, accounts in self.accounts.items():
            for account in accounts.values():
                account.apply_interest(months)
