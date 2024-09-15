import tkinter as tk
from tkinter import messagebox, filedialog
import sqlite3


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
        for F in (InputPage, ResultPage, HistoryPage):
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
                fixed_costs REAL,
                gross_profit REAL,
                net_profit REAL,
                profit_margin REAL
            )
        ''')
        self.conn.commit()

    def show_frame(self, page_name):
        """Show a frame for the given page name."""
        frame = self.frames[page_name]
        frame.tkraise()

    def save_to_db(self, revenue, cogs, fixed_costs, gross_profit, net_profit, profit_margin):
        """Save the analysis results to the SQLite database."""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO results (revenue, cogs, fixed_costs, gross_profit, net_profit, profit_margin)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (revenue, cogs, fixed_costs, gross_profit, net_profit, profit_margin))
        self.conn.commit()


class InputPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Input Page Elements
        tk.Label(self, text="Profitability Analysis", font=("Arial", 18)).pack(pady=10)

        tk.Label(self, text="Enter total revenue:").pack()
        self.revenue_input = tk.Entry(self)
        self.revenue_input.pack()

        tk.Label(self, text="Enter cost of goods sold (COGS):").pack()
        self.cogs_input = tk.Entry(self)
        self.cogs_input.pack()

        tk.Label(self, text="Enter total fixed costs:").pack()
        self.fixed_costs_input = tk.Entry(self)
        self.fixed_costs_input.pack()

        self.calculate_button = tk.Button(self, text="Calculate", command=self.calculate_profitability)
        self.calculate_button.pack(pady=10)

        self.result_button = tk.Button(self, text="View Results", command=lambda: controller.show_frame("ResultPage"))
        self.result_button.pack(pady=5)

        self.history_button = tk.Button(self, text="View History", command=lambda: controller.show_frame("HistoryPage"))
        self.history_button.pack(pady=5)

    def calculate_profitability(self):
        try:
            revenue = float(self.revenue_input.get())
            cogs = float(self.cogs_input.get())
            fixed_costs = float(self.fixed_costs_input.get())

            if revenue <= 0 or cogs < 0 or fixed_costs < 0:
                raise ValueError("Please enter positive values.")

            # Profitability calculations
            gross_profit = revenue - cogs
            net_profit = gross_profit - fixed_costs
            profit_margin = (net_profit / revenue) * 100

            # Save results to the database
            self.controller.save_to_db(revenue, cogs, fixed_costs, gross_profit, net_profit, profit_margin)

            # Pass the results to ResultPage
            result_page = self.controller.frames["ResultPage"]
            result_page.update_results(gross_profit, net_profit, profit_margin)

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

    def update_results(self, gross_profit, net_profit, profit_margin):
        """Update the result label with the latest calculation."""
        self.results_label.config(text=f"Gross Profit: ${gross_profit:.2f}\nNet Profit: ${net_profit:.2f}\nProfit Margin: {profit_margin:.2f}%")


class HistoryPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        tk.Label(self, text="Previous Results", font=("Arial", 18)).pack(pady=10)

        self.history_text = tk.Text(self, width=50, height=20)
        self.history_text.pack(pady=10)

        self.load_history()

        self.back_button = tk.Button(self, text="Back to Input", command=lambda: controller.show_frame("InputPage"))
        self.back_button.pack(pady=5)

    def load_history(self):
        """Load previous results from the SQLite database and display them."""
        self.history_text.delete(1.0, tk.END)  # Clear existing content

        cursor = self.controller.conn.cursor()
        cursor.execute('SELECT * FROM results ORDER BY id DESC')
        rows = cursor.fetchall()

        if rows:
            for row in rows:
                self.history_text.insert(tk.END, f"Revenue: ${row[1]:.2f}, COGS: ${row[2]:.2f}, "
                                                 f"Fixed Costs: ${row[3]:.2f}\n"
                                                 f"Gross Profit: ${row[4]:.2f}, Net Profit: ${row[5]:.2f}, "
                                                 f"Profit Margin: {row[6]:.2f}%\n\n")
        else:
            self.history_text.insert(tk.END, "No results found.")


if __name__ == "__main__":
    app = ProfitabilityApp()
    app.mainloop()
