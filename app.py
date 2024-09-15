import tkinter as tk
from tkinter import messagebox

class ProfitabilityApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Profitability Analysis")
        self.geometry("400x400")

        # Revenue input
        self.revenue_label = tk.Label(self, text="Enter total revenue:")
        self.revenue_label.pack()
        self.revenue_input = tk.Entry(self)
        self.revenue_input.pack()

        # COGS input
        self.cogs_label = tk.Label(self, text="Enter cost of goods sold (COGS):")
        self.cogs_label.pack()
        self.cogs_input = tk.Entry(self)
        self.cogs_input.pack()

        # Fixed costs input
        self.fixed_costs_label = tk.Label(self, text="Enter total fixed costs:")
        self.fixed_costs_label.pack()
        self.fixed_costs_input = tk.Entry(self)
        self.fixed_costs_input.pack()

        # Calculate button
        self.calculate_button = tk.Button(self, text="Calculate", command=self.calculate_profitability)
        self.calculate_button.pack()

        # Result display
        self.result_label = tk.Label(self, text="Results will be shown here")
        self.result_label.pack()

    def calculate_profitability(self):
        try:
            revenue = float(self.revenue_input.get())
            cogs = float(self.cogs_input.get())
            fixed_costs = float(self.fixed_costs_input.get())

            # Profitability calculations
            gross_profit = revenue - cogs
            net_profit = gross_profit - fixed_costs
            profit_margin = (net_profit / revenue) * 100

            self.result_label.config(text=f"Gross Profit: ${gross_profit:.2f}\nNet Profit: ${net_profit:.2f}\nProfit Margin: {profit_margin:.2f}%")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for all fields.")

if __name__ == "__main__":
    app = ProfitabilityApp()
    app.mainloop()
