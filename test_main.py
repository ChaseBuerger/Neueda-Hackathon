import unittest
from unittest.mock import patch, MagicMock
from bank import Bank
from main import logged_in_menu

# filepath: c:\Users\Administrator\Desktop\training\Neueda-Hackathon\test_main.py

class TestBankApplication(unittest.TestCase):
    def setUp(self):
        self.bank = MagicMock(spec=Bank)
        self.username = "test_user"
        self.bank.accounts = {
            self.username: {
                "savings1": MagicMock(account_type="savings", balance=1000.0, get_balance=lambda: 1000.0),
                "checking1": MagicMock(account_type="checking", balance=500.0, get_balance=lambda: 500.0),
            }
        }
        # Mock save_to_data to return a JSON-serializable dictionary
        self.bank.save_to_data.return_value = {
            self.username: {
                "savings1": {"account_type": "savings", "balance": 1000.0},
                "checking1": {"account_type": "checking", "balance": 500.0},
            }
        }

    @patch("builtins.input", side_effect=["1", "savings1", "200", "5"])  # Deposit to savings1
    @patch("builtins.print")
    def test_deposit(self, mock_print, mock_input):
        self.bank.deposit.return_value = "Deposit successful to account savings1. Current balance: $1200.00"
        logged_in_menu(self.bank, self.username)
        self.bank.deposit.assert_called_with(self.username, "savings1", 200.0)
        mock_print.assert_any_call("Deposit successful to account savings1. Current balance: $1200.00")

    @patch("builtins.input", side_effect=["2", "checking1", "100", "5"])  # Withdraw from checking1
    @patch("builtins.print")
    def test_withdraw(self, mock_print, mock_input):
        self.bank.withdraw.return_value = "Withdrawal successful from account checking1. Current balance: $400.00"
        logged_in_menu(self.bank, self.username)
        self.bank.withdraw.assert_called_with(self.username, "checking1", 100.0)
        mock_print.assert_any_call("Withdrawal successful from account checking1. Current balance: $400.00")

    @patch("builtins.input", side_effect=["3", "5"])  # Show balances
    @patch("builtins.print")
    def test_show_balances(self, mock_print, mock_input):
        logged_in_menu(self.bank, self.username)
        mock_print.assert_any_call("Your accounts and balances:")
        mock_print.assert_any_call("savings1: $1000.00")
        mock_print.assert_any_call("checking1: $500.00")

    @patch("builtins.input", side_effect=["4", "new_account", "savings", "300", "5"])  # Create account
    @patch("builtins.print")
    def test_create_account(self, mock_print, mock_input):
        self.bank.create_account.return_value = "Account created successfully."
        logged_in_menu(self.bank, self.username)
        self.bank.create_account.assert_called_with(self.username, None, "savings", "new_account", 300.0)
        mock_print.assert_any_call("Account created successfully.")

    @patch("builtins.input", side_effect=["6", "savings1", "12", "5"])  # Simulate growth for 12 months
    @patch("builtins.print")
    def test_simulate_growth(self, mock_print, mock_input):
        self.bank.simulate_growth.return_value = "Projected balance for account savings1 after 12 months: $1126.83"
        logged_in_menu(self.bank, self.username)
        self.bank.simulate_growth.assert_called_with(self.username, "savings1", 12)
        mock_print.assert_any_call("Projected balance for account savings1 after 12 months: $1126.83")
        

    @patch("builtins.input", side_effect=["1", "nonexistent_account", "200", "5"])  # Deposit to non-existent account
    @patch("builtins.print")
    def test_deposit_to_nonexistent_account(self, mock_print, mock_input):
        self.bank.deposit.side_effect = ValueError("Account does not exist.")
        logged_in_menu(self.bank, self.username)
        mock_print.assert_any_call("Account does not exist.")

    @patch("builtins.input", side_effect=["2", "savings1", "2000", "5"])  # Withdraw more than balance
    @patch("builtins.print")
    def test_withdraw_insufficient_funds(self, mock_print, mock_input):
        self.bank.withdraw.side_effect = ValueError("Insufficient funds.")
        logged_in_menu(self.bank, self.username)
        mock_print.assert_any_call("Insufficient funds.")

    @patch("builtins.input", side_effect=["4", "savings1", "savings", "-100", "200", "5"])
    @patch("builtins.print")
    def test_create_account_negative_balance(self, mock_print, mock_input):
        self.bank.create_account.return_value = "Account created successfully."
        logged_in_menu(self.bank, self.username)
        self.bank.create_account.assert_called_with(self.username, None, "savings", "savings1", 200.0)
        mock_print.assert_any_call("Initial deposit must be a positive number.")
        mock_print.assert_any_call("Account created successfully.")

    @patch("builtins.input", side_effect=["6", "nonexistent_account", "12", "5"])  # Simulate growth for non-existent account
    @patch("builtins.print")
    def test_simulate_growth_nonexistent_account(self, mock_print, mock_input):
        self.bank.simulate_growth.side_effect = ValueError("Account does not exist.")
        logged_in_menu(self.bank, self.username)
        mock_print.assert_any_call("Account does not exist.")

    @patch("builtins.input", side_effect=["invalid_option"])  # Invalid menu option
    @patch("builtins.print")
    def test_invalid_menu_option(self, mock_print, mock_input):
        logged_in_menu(self.bank, self.username)
        mock_print.assert_any_call("Invalid option. Please try again.")

    @patch("builtins.input", side_effect=["invalid", "5"])  # Invalid option, then exit
    @patch("builtins.print")
    def test_invalid_menu_option(self, mock_print, mock_input):
        logged_in_menu(self.bank, self.username)
        mock_print.assert_any_call("Invalid choice. Try again.")
        mock_print.assert_any_call("Logging out...")

    @patch("builtins.input", side_effect=["5"])  # Logout
    @patch("builtins.print")
    def test_logout(self, mock_print, mock_input):
        logged_in_menu(self.bank, self.username)
        mock_print.assert_any_call("Logging out...")

if __name__ == "__main__":
    unittest.main()