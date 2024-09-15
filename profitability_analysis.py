import matplotlib.pyplot as plt

# Business Profitability and Break-even Analysis Program

def calculate_gross_profit(revenue: float, cogs: float) -> float:
    return revenue - cogs

def calculate_operating_profit(gross_profit: float, operating_expenses: float) -> float:
    return gross_profit - operating_expenses

def calculate_net_profit(operating_profit: float, interest: float, taxes: float) -> float:
    return operating_profit - interest - taxes

def calculate_profit_margin(profit: float, revenue: float) -> float:
    return (profit / revenue) * 100

def calculate_break_even_units(fixed_costs: float, price_per_unit: float, variable_cost_per_unit: float) -> float:
    return fixed_costs / (price_per_unit - variable_cost_per_unit)

def calculate_break_even_revenue(break_even_units: float, price_per_unit: float) -> float:
    return break_even_units * price_per_unit

def plot_break_even_chart(fixed_costs: float, variable_cost_per_unit: float, price_per_unit: float, break_even_units: float):
    units = range(0, int(break_even_units * 2) + 1)
    total_costs = [fixed_costs + (variable_cost_per_unit * unit) for unit in units]
    total_revenue = [price_per_unit * unit for unit in units]
    plt.figure(figsize=(10, 6))
    plt.plot(units, total_costs, label='Total Costs', color='red')
    plt.plot(units, total_revenue, label='Total Revenue', color='green')
    plt.axvline(x=break_even_units, color='blue', linestyle='--', label='Break-even Point')
    plt.text(break_even_units, fixed_costs + (variable_cost_per_unit * break_even_units), f'  BEP: {break_even_units:.2f} units', color='blue')
    plt.axhline(y=fixed_costs, color='orange', linestyle='--', label='Fixed Costs')
    plt.title('Break-even Analysis')
    plt.xlabel('Units Sold')
    plt.ylabel('Amount ($)')
    plt.legend()
    plt.grid(True)
    plt.show()

def sensitivity_analysis(fixed_costs: float, price_per_unit: float, variable_cost_per_unit: float):
    price_change_percent = float(input("Enter percentage change in price per unit: "))
    variable_cost_change_percent = float(input("Enter percentage change in variable cost per unit: "))
    fixed_cost_change_percent = float(input("Enter percentage change in fixed costs: "))
    new_price_per_unit = price_per_unit * (1 + price_change_percent / 100)
    new_variable_cost_per_unit = variable_cost_per_unit * (1 + variable_cost_change_percent / 100)
    new_fixed_costs = fixed_costs * (1 + fixed_cost_change_percent / 100)
    new_break_even_units = calculate_break_even_units(new_fixed_costs, new_price_per_unit, new_variable_cost_per_unit)
    new_break_even_revenue = calculate_break_even_revenue(new_break_even_units, new_price_per_unit)
    print("\n--- Sensitivity Analysis Results ---")
    print(f"New Price per Unit: ${new_price_per_unit:.2f}")
    print(f"New Variable Cost per Unit: ${new_variable_cost_per_unit:.2f}")
    print(f"New Fixed Costs: ${new_fixed_costs:,.2f}")
    print(f"New Break-even Point: {new_break_even_units:,.2f} units")
    print(f"New Break-even Revenue: ${new_break_even_revenue:,.2f}")
    plot_break_even_chart(new_fixed_costs, new_variable_cost_per_unit, new_price_per_unit, new_break_even_units)

def main():
    revenue = float(input("Enter total revenue: "))
    cogs = float(input("Enter cost of goods sold (COGS): "))
    operating_expenses = float(input("Enter total operating expenses: "))
    interest = float(input("Enter interest expenses: "))
    taxes = float(input("Enter taxes: "))
    fixed_costs = float(input("Enter total fixed costs: "))
    price_per_unit = float(input("Enter price per unit: "))
    variable_cost_per_unit = float(input("Enter variable cost per unit: "))
    gross_profit = calculate_gross_profit(revenue, cogs)
    operating_profit = calculate_operating_profit(gross_profit, operating_expenses)
    net_profit = calculate_net_profit(operating_profit, interest, taxes)
    gross_margin = calculate_profit_margin(gross_profit, revenue)
    operating_margin = calculate_profit_margin(operating_profit, revenue)
    net_margin = calculate_profit_margin(net_profit, revenue)
    break_even_units = calculate_break_even_units(fixed_costs, price_per_unit, variable_cost_per_unit)
    break_even_revenue = calculate_break_even_revenue(break_even_units, price_per_unit)
    print("\n--- Business Profitability and Break-even Analysis ---")
    print(f"Gross Profit: ${gross_profit:,.2f}")
    print(f"Operating Profit: ${operating_profit:,.2f}")
    print(f"Net Profit: ${net_profit:,.2f}")
    print(f"Gross Profit Margin: {gross_margin:.2f}%")
    print(f"Operating Profit Margin: {operating_margin:.2f}%")
    print(f"Net Profit Margin: {net_margin:.2f}%")
    print(f"Break-even Point: {break_even_units:,.2f} units")
    print(f"Break-even Revenue: ${break_even_revenue:,.2f}")
    plot_break_even_chart(fixed_costs, variable_cost_per_unit, price_per_unit, break_even_units)
    sensitivity_analysis(fixed_costs, price_per_unit, variable_cost_per_unit)

if __name__ == "__main__":
    main()
