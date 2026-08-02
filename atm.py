"""
atm.py — A small, tested command-line ATM simulator.

Started as a notebook exercise (ATM practice.ipynb): a menu loop with
check-balance / deposit / withdraw / quit. This version turns that into
something that actually holds up: input validation on every path,
clear error messages instead of silent failures, and a core (ATMAccount)
that's separated from the CLI loop so it can be unit tested without
mocking stdin.

Run it:
    python atm.py

Run the tests:
    python -m unittest test_atm.py -v
"""

from __future__ import annotations


class InsufficientFundsError(Exception):
    """Raised when a withdrawal exceeds the current balance."""


class InvalidAmountError(Exception):
    """Raised when a deposit/withdrawal amount is not a positive number."""


class ATMAccount:
    """Holds the balance and enforces the rules for deposits and withdrawals.

    Kept separate from any print()/input() calls so it can be tested
    directly, without needing to simulate a user typing at a menu.
    """

    def __init__(self, starting_balance: float = 0.0):
        if starting_balance < 0:
            raise InvalidAmountError("Starting balance cannot be negative.")
        self._balance = float(starting_balance)

    @property
    def balance(self) -> float:
        return self._balance

    def deposit(self, amount: float) -> float:
        """Add `amount` to the balance. Returns the new balance.

        Raises InvalidAmountError if amount is not a positive number.
        """
        if amount <= 0:
            raise InvalidAmountError("Deposit amount must be greater than zero.")
        self._balance += amount
        return self._balance

    def withdraw(self, amount: float) -> float:
        """Remove `amount` from the balance. Returns the new balance.

        Raises InvalidAmountError if amount is not a positive number.
        Raises InsufficientFundsError if amount exceeds the current balance.
        """
        if amount <= 0:
            raise InvalidAmountError("Withdrawal amount must be greater than zero.")
        if amount > self._balance:
            raise InsufficientFundsError(
                f"Cannot withdraw RM{amount:.2f} — current balance is RM{self._balance:.2f}."
            )
        self._balance -= amount
        return self._balance


def _prompt_amount(action: str) -> float:
    """Prompt for an amount and keep asking until it's a valid number.

    Only handles "is this parseable as a float" here — business rules
    (positive, sufficient funds) are enforced by ATMAccount, not here.
    """
    while True:
        raw = input(f"Enter amount to {action}: RM").strip()
        try:
            return float(raw)
        except ValueError:
            print(f"'{raw}' isn't a valid number. Please enter digits, e.g. 50 or 50.00.")


def run_atm_menu(account: ATMAccount | None = None) -> None:
    """The interactive CLI loop. Delegates all balance logic to ATMAccount."""
    if account is None:
        account = ATMAccount()

    menu_text = (
        "\n=== ATM Menu ===\n"
        "1. Check Balance\n"
        "2. Deposit\n"
        "3. Withdraw\n"
        "4. Quit"
    )

    while True:
        print(menu_text)
        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            print(f"Your current balance is: RM{account.balance:.2f}")

        elif choice == "2":
            amount = _prompt_amount("deposit")
            try:
                new_balance = account.deposit(amount)
                print(f"Deposited RM{amount:.2f}. New balance: RM{new_balance:.2f}")
            except InvalidAmountError as e:
                print(f"Error: {e}")

        elif choice == "3":
            amount = _prompt_amount("withdraw")
            try:
                new_balance = account.withdraw(amount)
                print(f"Withdrew RM{amount:.2f}. New balance: RM{new_balance:.2f}")
            except (InvalidAmountError, InsufficientFundsError) as e:
                print(f"Error: {e}")

        elif choice == "4":
            print("Thank you for using the ATM.")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 4.")


if __name__ == "__main__":
    run_atm_menu()
