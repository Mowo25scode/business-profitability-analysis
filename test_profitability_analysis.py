import unittest
from profitability_analysis import (calculate_gross_profit, calculate_operating_profit, 
                                    calculate_net_profit, calculate_profit_margin,
                                    calculate_break_even_units, calculate_break_even_revenue)

class TestProfitabilityAnalysis(unittest.TestCase):
    def test_calculate_gross_profit(self):
        self.assertEqual(calculate_gross_profit(500000, 300000), 200000)
    def test_calculate_operating_profit(self):
        self.assertEqual(calculate_operating_profit(200000, 100000), 100000)
    def test_calculate_net_profit(self):
        self.assertEqual(calculate_net_profit(100000, 15000, 25000), 60000)
    def test_calculate_profit_margin(self):
        self.assertAlmostEqual(calculate_profit_margin(200000, 500000), 40.0)
    def test_calculate_break_even_units(self):
        self.assertEqual(calculate_break_even_units(80000, 50, 30), 4000)
    def test_calculate_break_even_revenue(self):
        self.assertEqual(calculate_break_even_revenue(4000, 50), 200000)

if __name__ == "__main__":
    unittest.main()
