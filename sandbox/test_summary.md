```python
import unittest
from backend import User, Expense, Group, create_user, create_expense


class TestUser(unittest.TestCase):
    def test_user_initialization(self):
        user = create_user('Alice')
        self.assertEqual(user.name, 'Alice')
        self.assertEqual(user.balance, 0.0)

    def test_update_balance_increase(self):
        user = create_user('Bob')
        user.update_balance(50.0)
        self.assertEqual(user.balance, 50.0)

    def test_update_balance_decrease(self):
        user = create_user('Charlie')
        user.update_balance(-30.0)
        self.assertEqual(user.balance, -30.0)


class TestExpense(unittest.TestCase):
    def test_expense_initialization(self):
        user = create_user('Alice')
        expense = create_expense('Dinner', 100, user)
        self.assertEqual(expense.description, 'Dinner')
        self.assertEqual(expense.amount, 100)
        self.assertEqual(expense.paid_by, user)

    def test_split_expense_equal(self):
        user1 = create_user('Alice')
        user2 = create_user('Bob')
        user3 = create_user('Charlie')
        expense = create_expense('Dinner', 90, user1)
        group = Group('group1')
        group.add_user(user1)
        group.add_user(user2)
        group.add_user(user3)
        group.add_expense(expense)
        self.assertEqual(user1.balance, -90.0)
        self.assertEqual(user2.balance, 30.0)
        self.assertEqual(user3.balance, 30.0)


class TestGroup(unittest.TestCase):
    def test_add_user(self):
        group = Group('group1')
        user = create_user('Alice')
        group.add_user(user)
        self.assertEqual(len(group.users), 1)

    def test_add_expense(self):
        group = Group('group1')
        user = create_user('Alice')
        group.add_user(user)
        expense = create_expense('Coffee', 50, user)
        group.add_expense(expense)
        self.assertEqual(len(group.expenses), 1)

    def test_get_balances(self):
        group = Group('group1')
        user1 = create_user('Alice')
        user2 = create_user('Bob')
        group.add_user(user1)
        group.add_user(user2)
        expense = create_expense('Lunch', 40, user1)
        group.add_expense(expense)
        self.assertEqual(group.get_balances(), {'Alice': -40.0, 'Bob': 20.0})


if __name__ == '__main__':
    unittest.main()
```