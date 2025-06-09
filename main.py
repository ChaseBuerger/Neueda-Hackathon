import json
from bank import Bank

DATA_FILE = "data.json"

def load_data(bank):
    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
            bank.load_from_data(data)
    except FileNotFoundError:
        print("No existing data found. Starting fresh.")

def save_data(bank):
    with open(DATA_FILE, "w") as file:
        json.dump(bank.save_to_data(), file)

def main_menu(bank):
    while True:
        print("\nWelcome to the Bank CLI")
        print("1. Login")
        print("2. Create Account")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Username: ")
            password = input("Password: ")
            if bank.login(username, password):
                print("Login successful!")
                logged_in_menu(bank, username)
            else:
                print("Invalid credentials.")
        elif choice == "2":
            username = input("Choose a username: ")
            password = input("Choose a password: ")
            result = add_account(bank, username, password)
            print(result)
        elif choice == "3":
            save_data(bank)
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

def add_account(bank, username, password=None):
    account_name = input("Enter account name: ")
    account_type = input("Account type (savings/checking): ").lower()
    initial_deposit = float(input("Enter initial deposit amount: "))
    if account_type not in ["savings", "checking"]:
        return "Invalid account type."
    result = bank.create_account(username, password, account_type, account_name, initial_deposit)
    return result

def logged_in_menu(bank, username):
    while True:
        print(f"\nWelcome, {username}!")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Show Balances")
        print("4. Create Account")
        print("5. Logout")
        choice = input("Enter your choice: ")

        if choice == "1":  # Deposit logic
            account_name = input("Enter account name: ")
            amount = float(input("Enter amount to deposit: "))
            result = bank.deposit(username, account_name, amount)
            print(result)
        elif choice == "2":  # Withdraw logic
            account_name = input("Enter account name: ")
            amount = float(input("Enter amount to withdraw: "))
            result = bank.withdraw(username, account_name, amount)
            print(result)
        elif choice == "3":  # Show balances for all accounts
            user_accounts = bank.accounts.get(username, {})
            if user_accounts:
                print("Your accounts and balances:")
                for account_name, account in user_accounts.items():
                    print(f"{account_name}: ${account.get_balance():.2f}")
            else:
                print("No accounts found.")
        elif choice == "4":  # Create account logic
            result = add_account(bank, username)
            print(result)
        elif choice == "5":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Try again.")

def main():
    bank = Bank()
    load_data(bank)
    main_menu(bank)

if __name__ == "__main__":
    main()