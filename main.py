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

def main():
    bank = Bank()
    load_data(bank)
    while True:
        print("\nWelcome to the Bank CLI")
        print("1. Login")
        print("2. Create Account")
        print("3. Deposit")
        print("4. Withdraw")
        print("5. Show Balance")  # New option added
        print("6. Exit")  # Updated exit option number
        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Username: ")
            password = input("Password: ")
            if bank.login(username, password):
                print("Login successful!")
            else:
                print("Invalid credentials.")
        elif choice == "2":
            username = input("Choose a username: ")
            password = input("Choose a password: ")
            account_type = input("Account type (savings/checking): ").lower()
            if account_type in ["savings", "checking"]:
                if bank.create_account(username, password, account_type):
                    print("Account created successfully!")
                else:
                    print("Username already exists.")
            else:
                print("Invalid account type.")
        elif choice == "3":
            username = input("Username: ")
            amount = float(input("Enter amount to deposit: "))
            message = bank.deposit(username, amount)
            print(message)
        elif choice == "4":
            username = input("Username: ")
            amount = float(input("Enter amount to withdraw: "))
            message = bank.withdraw(username, amount)
            print(message)
        elif choice == "5":  # New option logic
            username = input("Username: ")
            account = bank.get_account(username)  # Retrieve the Account object
            if account:
                print(f"Your balance is: ${account.get_balance()}")  # Use get_balance method
            else:
                print("Account not found or not logged in.")
        elif choice == "6":  # Updated exit option number
            save_data(bank)
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
