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
            account_type = input("Account type (savings/checking): ").lower()
            if account_type in ["savings", "checking"]:
                if bank.create_account(username, password, account_type):
                    print("Account created successfully!")
                else:
                    print("Username already exists.")
            else:
                print("Invalid account type.")
        elif choice == "3":
            save_data(bank)
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

def logged_in_menu(bank, username):
    while True:
        print(f"\nWelcome, {username}!")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Logout")
        choice = input("Enter your choice: ")

        if choice == "1":
            amount = float(input("Enter amount to deposit: "))
            if bank.deposit(username, amount):
                print("Deposit successful!")
            else:
                print("Deposit failed. Check username or account.")
        elif choice == "2":
            amount = float(input("Enter amount to withdraw: "))
            if bank.withdraw(username, amount):
                print("Withdrawal successful!")
            else:
                print("Withdrawal failed. Check username, account, or balance.")
        elif choice == "3":
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