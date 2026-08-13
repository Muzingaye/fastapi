import pytest
from calculations import BankAccount, add, subtract


@pytest.mark.parametrize("num1, num2, result", [
    (3, 2, 5),
    (7, 1, 8),
    (12, 4, 16),
])
def test_add(num1, num2, result):
    assert result == add(num1, num2)

def test_subtract():
    assert -4 == subtract(4, 8)


@pytest.fixture
def account():
    return BankAccount("Muzi", 100)


def test_bank_set_initial_account(account):
    assert account.balance == 100



def test_deposit(account):
    account.deposit(50)
    assert account.get_balance() == 150


def test_withdraw(account):
    account.withdraw(30)
    assert account.get_balance() == 70


def test_collect_interest(account):
    account.collect_interest(0.05)
    assert account.get_balance() == 105


def test_collect_interest_multiple_times(account):
    account.collect_interest(0.10)
    account.collect_interest(0.10)
    assert account.get_balance() == 121


def test_deposit_negative_amount(account):
    with pytest.raises(ValueError):
        account.deposit(-10)


def test_withdraw_more_than_balance(account):
    with pytest.raises(ValueError):
        account.withdraw(150)


def test_withdraw_negative_amount(account):
    with pytest.raises(ValueError):
        account.withdraw(-20)


def test_negative_interest_rate(account):
    with pytest.raises(ValueError):
        account.collect_interest(-0.05)