import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import sqlite3
import matplotlib.pyplot as plt

class ProfitabilityApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Profitability Analysis")
        self.geometry("500x600")

        # Initialize Database
        self.conn = sqlite3.connect('profitability_analysis.db')
        self.create_table()

        # Create Frames for Multi-Page Interface
        self.frames = {}
        for F in (InputPage, ResultPage, HistoryPage, GraphPage):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("InputPage")

    def create_table(self):
        """Create results table if it doesn't exist."""
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                revenue REAL,
                cogs REAL,
                variable_costs REAL,
                fixed_costs REAL,
                gross_profit REAL,
                net_profit REAL,
                profit_margin REAL,
                break_even_units REAL,
                break_even_revenue REAL
            )
        ''')
        self.conn.commit()

    def show_frame(self, page_name):
        """Show a frame for the given page name."""
        frame = self.frames[page_name]
        frame.tkraise()

    def save_to_db(self, revenue, cogs, variable_costs, fixed_costs, gross_profit, net_profit, profit_margin, break_even_units, break_even_revenue):
        """Save the analysis results to the SQLite database."""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO results (revenue, cogs, variable_costs, fixed_costs, gross_profit, net_profit, profit_margin, break_even_units, break_even_revenue)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (revenue, cogs, variable_costs, fixed_costs, gross_profit, net_profit, profit_margin, break_even_units, break_even_revenue))
        self.conn.commit()


class InputPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Input Page Elements
        tk.Label(self, text="Profitability and Break-even Analysis", font=("Arial", 18)).pack(pady=10)

        tk.Label(self, text="Enter total revenue:").pack()
        self.revenue_input = tk.Entry(self)
        self.revenue_input.pack()

        tk.Label(self, text="Enter cost of goods sold (COGS):").pack()
        self.cogs_input = tk.Entry(self)
        self.cogs_input.pack()

        tk.Label(self, text="Enter variable costs per unit:").pack()
        self.variable_costs_input = tk.Entry(self)
        self.variable_costs_input.pack()

        tk.Label(self, text="Enter total fixed costs:").pack()
        self.fixed_costs_input = tk.Entry(self)
        self.fixed_costs_input.pack()

        self.calculate_button = tk.Button(self, text="Calculate", command=self.calculate_profitability)
        self.calculate_button.pack(pady=10)

        self.result_button = tk.Button(self, text="View Results", command=lambda: controller.show_frame("ResultPage"))
        self.result_button.pack(pady=5)

        self.history_button = tk.Button(self, text="View History", command=lambda: controller.show_frame("HistoryPage"))
        self.history_button.pack(pady=5)

        self.graph_button = tk.Button(self, text="View Graph", command=lambda: controller.show_frame("GraphPage"))
        self.graph_button.pack(pady=5)

    def calculate_profitability(self):
        try:
            revenue = float(self.revenue_input.get())
            cogs = float(self.cogs_input.get())
            variable_costs = float(self.variable_costs_input.get())
            fixed_costs = float(self.fixed_costs_input.get())

            if revenue <= 0 or cogs < 0 or variable_costs < 0 or fixed_costs < 0:
                raise ValueError("Please enter positive values.")

            # Profitability calculations
            gross_profit = revenue - cogs
            net_profit = gross_profit - fixed_costs
            profit_margin = (net_profit / revenue) * 100

            # Break-even analysis
            price_per_unit = revenue  # assuming 1 unit sold for simplicity
            if price_per_unit > variable_costs:
                break_even_units = fixed_costs / (price_per_unit - variable_costs)
                break_even_revenue = break_even_units * price_per_unit
            else:
                raise ValueError("Price per unit must be greater than variable costs.")

            # Save results to the database
            self.controller.save_to_db(revenue, cogs, variable_costs, fixed_costs, gross_profit, net_profit, profit_margin, break_even_units, break_even_revenue)

            # Pass the results to ResultPage
            result_page = self.controller.frames["ResultPage"]
            result_page.update_results(gross_profit, net_profit, profit_margin, break_even_units, break_even_revenue)

            # Pass the values to GraphPage for graphing
            graph_page = self.controller.frames["GraphPage"]
            graph_page.plot_graph(fixed_costs, variable_costs, price_per_unit, break_even_units)

            # Show results page
            self.controller.show_frame("ResultPage")

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid positive numbers for all fields.")


class ResultPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        tk.Label(self, text="Profitability Results", font=("Arial", 18)).pack(pady=10)
        self.results_label = tk.Label(self, text="", font=("Arial", 12))
        self.results_label.pack(pady=10)

        self.back_button = tk.Button(self, text="Back to Input", command=lambda: controller.show_frame("InputPage"))
        self.back_button.pack(pady=5)

    def update_results(self, gross_profit, net_profit, profit_margin, break_even_units, break_even_revenue):
        """Update the result label with the latest calculation."""
        self.results_label.config(text=f"Gross Profit: ${gross_profit:.2f}\nNet Profit: ${net_profit:.2f}\n"
                                       f"Profit Margin: {profit_margin:.2f}%\n"
                                       f"Break-even Point: {break_even_units:.2f} units\n"
                                       f"Break-even Revenue: ${break_even_revenue:.2f}")


class GraphPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        tk.Label(self, text="Break-even Chart", font=("Arial", 18)).pack(pady=10)
        self.graph_button = tk.Button(self, text="Back to Input", command=lambda: controller.show_frame("InputPage"))
        self.graph_button.pack(pady=5)

    def plot_graph(self, fixed_costs, variable_costs, price_per_unit, break_even_units):
        """Plot a break-even chart using Matplotlib."""
        units = list(range(0, int(break_even_units * 2) + 1))

        # Calculate total costs and total revenue for each unit count
        total_costs = [fixed_costs + (variable_costs * u) for u in units]
        total_revenue = [price_per_unit * u for u in units]

        plt.figure(figsize=(10, 6))
        plt.plot(units, total_costs, label="Total Costs", color="red")
        plt.plot(units, total_revenue, label="Total Revenue", color="green")
        plt.axvline(x=break_even_units, color="blue", linestyle="--", label="Break-even Point")
        plt.title("Break-even Analysis")
        plt.xlabel("Units Sold")
        plt.ylabel("Amount ($)")
        plt.legend()
        plt.grid(True)
        plt.show()


class HistoryPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        tk.Label(self, text="Previous Results", font=("Arial", 18)).pack(pady=10)

        self.history_text = tk.Text(self, width=50, height=20)
        self
