import gradio as gr
from backend import create_user, create_expense, Group

class ExpenseManager:
    def __init__(self):
        self.group = Group('Default Group')

    def add_user(self, name: str):
        user = create_user(name)
        self.group.add_user(user)
        return f"User '{name}' added successfully!"

    def add_expense(self, description: str, amount: float, paid_by: str):
        user = next((u for u in self.group.users if u.name == paid_by), None)
        if user:
            expense = create_expense(description, amount, user)
            self.group.add_expense(expense)
            return self.group.get_balances()
        return "User not found."

    def view_balances(self):
        return self.group.get_balances()

expense_manager = ExpenseManager()

with gr.Blocks() as app:
    gr.Markdown("# Expense Splitting Application")
    with gr.Tab("Add User"):
        user_name = gr.Textbox(label="User Name")
        add_user_btn = gr.Button("Add User")
        user_output = gr.Textbox(label="", interactive=False)
        add_user_btn.click(expense_manager.add_user, inputs=user_name, outputs=user_output)
    with gr.Tab("Add Expense"):
        expense_desc = gr.Textbox(label="Expense Description")
        expense_amount = gr.Number(label="Amount")
        paid_by = gr.Textbox(label="Paid By (User Name)")
        add_expense_btn = gr.Button("Add Expense")
        expense_output = gr.Textbox(label="", interactive=False)
        add_expense_btn.click(expense_manager.add_expense, inputs=[expense_desc, expense_amount, paid_by], outputs=expense_output)
    with gr.Tab("View Balances"):
        view_balances_btn = gr.Button("Refresh Balances")
        balances_output = gr.Textbox(label="", interactive=False)
        view_balances_btn.click(expense_manager.view_balances, outputs=balances_output)

if __name__ == "__main__":
    app.launch()