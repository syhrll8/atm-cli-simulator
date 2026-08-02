# ATM CLI Simulator

A small command-line ATM: check balance, deposit, withdraw, quit.

## Problem

I had a working ATM menu loop from a Python exercise notebook, but it wasn't something I'd call finished. It had no input validation beyond a basic amount check, no tests, and all the logic was tangled together with `print()`/`input()` calls — so there was no way to verify the balance rules actually worked without manually clicking through the menu every time.

## Approach

I split the project into two pieces:

- **`ATMAccount`** — holds the balance and enforces the rules (no negative starting balance, deposits/withdrawals must be positive, can't withdraw more than the balance). This part has zero `print()` or `input()` calls, which is what makes it testable.
- **`run_atm_menu()`** — the interactive loop. It only handles displaying the menu and reading input; all the actual banking logic is delegated to `ATMAccount`.

Separating "the rules" from "the menu" was the main design decision. It's a small project, but it's the same pattern that matters at any scale: business logic that doesn't depend on how the user is talking to it is logic you can actually test.

## What I learned

- Custom exceptions (`InvalidAmountError`, `InsufficientFundsError`) are clearer than generic `ValueError`s or silent `print("error")` — the caller can tell exactly what went wrong and handle it if they need to.
- A function that both prompts a user *and* enforces business rules is hard to unit test. Once I pulled the rules out into their own class, testing took about 15 minutes.
- Validating that a string is a parseable number (`_prompt_amount`) is a different concern from validating that the number makes business sense (positive, sufficient funds) — keeping those separate made both easier to get right.

## How to run it

```bash
python atm.py
```

## How to run the tests

```bash
python -m unittest test_atm.py -v
```

15 tests, covering: initialization (default/custom/negative starting balance), deposits (valid, zero, negative, balance-unchanged-on-failure), withdrawals (valid, exact-balance, over-balance, zero, negative, balance-unchanged-on-failure), and multi-step sequences.

## Honest scope note

This is a portfolio/learning project, not a production banking system — there's no persistence (balance resets every run), no multi-account support, and no concurrency handling. It's meant to demonstrate that I can take a rough exercise and turn it into something tested and documented, not that I've built a real ATM.
