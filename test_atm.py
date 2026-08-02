"""
Unit tests for atm.py's ATMAccount — the part of the original notebook
exercise that actually had business logic worth testing (deposits,
withdrawals, balance rules). The CLI loop (run_atm_menu) is intentionally
left untested here since it's just input()/print() plumbing around
ATMAccount; this is what "tested" means for this project, not a claim
that every line has coverage.
"""

import unittest

from atm import ATMAccount, InsufficientFundsError, InvalidAmountError


class TestATMAccountInitialization(unittest.TestCase):
    def test_default_starting_balance_is_zero(self):
        account = ATMAccount()
        self.assertEqual(account.balance, 0.0)

    def test_custom_starting_balance(self):
        account = ATMAccount(starting_balance=100)
        self.assertEqual(account.balance, 100.0)

    def test_negative_starting_balance_raises(self):
        with self.assertRaises(InvalidAmountError):
            ATMAccount(starting_balance=-50)


class TestDeposit(unittest.TestCase):
    def setUp(self):
        self.account = ATMAccount(starting_balance=100)

    def test_deposit_increases_balance(self):
        new_balance = self.account.deposit(50)
        self.assertEqual(new_balance, 150)
        self.assertEqual(self.account.balance, 150)

    def test_deposit_zero_raises(self):
        with self.assertRaises(InvalidAmountError):
            self.account.deposit(0)

    def test_deposit_negative_raises(self):
        with self.assertRaises(InvalidAmountError):
            self.account.deposit(-10)

    def test_balance_unchanged_after_failed_deposit(self):
        try:
            self.account.deposit(-10)
        except InvalidAmountError:
            pass
        self.assertEqual(self.account.balance, 100)


class TestWithdraw(unittest.TestCase):
    def setUp(self):
        self.account = ATMAccount(starting_balance=100)

    def test_withdraw_decreases_balance(self):
        new_balance = self.account.withdraw(30)
        self.assertEqual(new_balance, 70)
        self.assertEqual(self.account.balance, 70)

    def test_withdraw_exact_balance_allowed(self):
        new_balance = self.account.withdraw(100)
        self.assertEqual(new_balance, 0)

    def test_withdraw_more_than_balance_raises(self):
        with self.assertRaises(InsufficientFundsError):
            self.account.withdraw(150)

    def test_withdraw_zero_raises(self):
        with self.assertRaises(InvalidAmountError):
            self.account.withdraw(0)

    def test_withdraw_negative_raises(self):
        with self.assertRaises(InvalidAmountError):
            self.account.withdraw(-20)

    def test_balance_unchanged_after_failed_withdrawal(self):
        try:
            self.account.withdraw(150)
        except InsufficientFundsError:
            pass
        self.assertEqual(self.account.balance, 100)


class TestSequenceOfOperations(unittest.TestCase):
    def test_deposit_then_withdraw(self):
        account = ATMAccount()
        account.deposit(200)
        account.withdraw(75)
        self.assertEqual(account.balance, 125)

    def test_multiple_deposits(self):
        account = ATMAccount()
        account.deposit(10)
        account.deposit(20)
        account.deposit(30)
        self.assertEqual(account.balance, 60)


if __name__ == "__main__":
    unittest.main()
