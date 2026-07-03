from typing import List, Dict

class User:
    def __init__(self, user_id: str, name: str) -> None:
        self.user_id = user_id
        self.name = name
        self.balance = 0.0

    def update_balance(self, amount: float) -> None:
        self.balance += amount

class Expense:
    def __init__(self, expense_id: str, description: str, amount: float, paid_by: User) -> None:
        self.expense_id = expense_id
        self.description = description
        self.amount = amount
        self.paid_by = paid_by

    def split_expense(self, users: List[User]) -> Dict[str, float]:
        share = self.amount / len(users)
        self.paid_by.update_balance(-self.amount)  # Update payer's balance
        for user in users:
            user.update_balance(share)
        return {user.name: user.balance for user in users}

class Group:
    def __init__(self, group_id: str) -> None:
        self.group_id = group_id
        self.users = []
        self.expenses = []

    def add_user(self, user: User) -> None:
        self.users.append(user)

    def add_expense(self, expense: Expense) -> None:
        expense.split_expense(self.users)
        self.expenses.append(expense)

    def get_balances(self) -> Dict[str, float]:
        return {user.name: user.balance for user in self.users}

# Function to create user
def create_user(name: str) -> User:
    return User(user_id=name.lower(), name=name)

# Function to create expense
def create_expense(description: str, amount: float, paid_by: User) -> Expense:
    return Expense(expense_id=description.lower(), description=description, amount=amount, paid_by=paid_by)

# Function to get group summary
def get_group_summary(group: Group) -> Dict[str, float]:
    return group.get_balances()