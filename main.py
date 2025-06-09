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
    
    # Validate account type
    while True:
        account_type = input("Account type (savings/checking): ").lower()
        if account_type in ["savings", "checking"]:
            break
        print("Invalid account type. Please enter 'savings' or 'checking'.")
    
    # Validate initial deposit
    while True:
        try:
            initial_deposit = float(input("Enter initial deposit amount: "))
            if initial_deposit < 0:
                print("Initial deposit must be a positive number.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid dollar amount.")
    
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
        print("6. Simulate Growth")
        choice = input("Enter your choice: ")

        if choice == "1":  # Deposit logic
            user_accounts = bank.accounts.get(username, {})
            if not user_accounts:
                print("No accounts found. Please create an account first.")
                continue
            print("Your accounts:")
            for account_name in user_accounts.keys():
                print(f"- {account_name}")
            account_name = input("Enter account name: ")
            if account_name not in user_accounts:
                print("Account does not exist.")  # Ensure this matches the test expectation
                continue

            # Validate deposit amount
            while True:
                try:
                    amount = float(input("Enter amount to deposit: "))
                    if amount <= 0:
                        print("Deposit amount must be greater than zero.")
                        continue
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid dollar amount.")

            result = bank.deposit(username, account_name, amount)
            print(result)

        elif choice == "2":  # Withdraw logic
            user_accounts = bank.accounts.get(username, {})
            if not user_accounts:
                print("No accounts found. Please create an account first.")
                continue
            print("Your accounts:")
            for account_name in user_accounts.keys():
                print(f"- {account_name}")
            account_name = input("Enter account name: ")
            if account_name not in user_accounts:
                print("Invalid account name. Try again.")
                continue
            
            # Validate withdrawal amount
            while True:
                try:
                    amount = float(input("Enter amount to withdraw: "))
                    if amount <= 0:
                        print("Withdrawal amount must be greater than zero.")
                        continue
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid dollar amount.")
            
            try:
                result = bank.withdraw(username, account_name, amount)
                print(result)
            except ValueError as e:
                print(str(e))  # Print the error message (e.g., "Insufficient funds.")

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

        elif choice == "6":  # Simulate growth
            user_accounts = bank.accounts.get(username, {})
            if not user_accounts:
                print("No accounts found. Please create an account first.")
                continue
            print("Your accounts:")
            for account_name in user_accounts.keys():
                print(f"- {account_name}")
            account_name = input("Enter account name: ")
            if account_name not in user_accounts:
                print("Account does not exist.")  # Ensure this matches the test expectation
                continue

            account = user_accounts[account_name]
            if account.account_type != "savings":
                print("Growth simulation is only applicable for savings accounts.")
                continue

            while True:
                try:
                    months = int(input("Enter number of months to simulate: "))
                    if months <= 0:
                        print("Number of months must be greater than zero.")
                        continue
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid number of months.")

            result = bank.simulate_growth(username, account_name, months)
            print(result)

        else:
            print("Invalid choice. Try again.")
            
        # Save data after each operation
        save_data(bank)

def main():
    bank = Bank()
    load_data(bank)
    main_menu(bank)

if __name__ == "__main__":
    main()