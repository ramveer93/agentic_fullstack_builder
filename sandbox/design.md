# Expense Splitting Application Design

## Overview

The Expense Splitting Application will consist of three main components:
1. **Backend Module**: Responsible for handling the business logic, data storage, and user management.
2. **Frontend Module**: A Gradio interface for user interaction to input expenses and view balances.
3. **Testing Module**: Unit tests for validating the backend module's logic.

## Assignments

- **Backend Engineer**: Implement the backend module.
- **Frontend Engineer**: Develop the frontend using Gradio.
- **Test Engineer**: Write unit tests for the backend module.

---

## Backend Module Design

### Classes

#### 1. User
- **Attributes**:
  - `user_id: str`
  - `name: str`
  - `balance: float`
- **Methods**:
  - `__init__(self, user_id: str, name: str) -> None`
  - `update_balance(self, amount: float) -> None`

#### 2. Expense
- **Attributes**:
  - `expense_id: str`
  - `description: str`
  - `amount: float`
  - `paid_by: User`
- **Methods**:
  - `__init__(self, expense_id: str, description: str, amount: float, paid_by: User) -> None`
  - `split_expense(self, users: List[User]) -> Dict[str, float]`

#### 3. Group
- **Attributes**:
  - `group_id: str`
  - `users: List[User]`
  - `expenses: List[Expense]`
- **Methods**:
  - `__init__(self, group_id: str) -> None`
  - `add_user(self, user: User) -> None`
  - `add_expense(self, expense: Expense) -> None`
  - `get_balances(self) -> Dict[str, float]`

### Other Functions

- `create_user(name: str) -> User`
- `create_expense(description: str, amount: float, paid_by: User) -> Expense`
- `get_group_summary(group: Group) -> Dict[str, float]`

---

## Frontend Module Design (Gradio Application)

### Gradio Interface

#### Functions

- `create_user_interface() -> gr.Interface`
  - Parameters: `user_name: str`
  - Output: `User details`

- `add_expense_interface() -> gr.Interface`
  - Parameters: 
    - `description: str`
    - `amount: float`
    - `paid_by: str (User name)`
  - Outputs: `Updated balances`
  
- `view_balances_interface() -> gr.Interface`
  - Parameters: None
  - Output: `List of users and their current balances`

### Main App Function

- `main_app() -> None`
  - Description: Launches the Gradio app with the above interfaces.

### Gradio Component Considerations

- Important kwargs in `gr.Interface`:
  - Use `inputs` and `outputs` as lists containing the types: `gr.Text`, `gr.Number`, etc.
  - The `title` and `description` parameters for informative UI.
  - Use `live=True` for real-time updates when necessary.
  
---

## Testing Module Design

### Unit Tests

- **Test Cases for User Class**
  - `test_user_initialization() -> None`
  - `test_update_balance_increase() -> None`
  - `test_update_balance_decrease() -> None`

- **Test Cases for Expense Class**
  - `test_expense_initialization() -> None`
  - `test_split_expense_equal() -> None`
  
- **Test Cases for Group Class**
  - `test_add_user() -> None`
  - `test_add_expense() -> None`
  - `test_get_balances() -> None`

### Test Execution

- `run_tests() -> None`
  - Description: Executes all unit tests and checks assertions.

---

This design outlines the structure and responsibilities of each module and engineer required to implement the expense splitting application. Each engineer will create their respective components in the same sandbox directory, adhering to the design specifications outlined above.