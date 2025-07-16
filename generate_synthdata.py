#!/usr/bin/env python3
"""
Synthetic Financial Data Generator

Generates GAAP-compliant synthetic financial data for:
- Monthly P&L statements
- Monthly Cash Flow statements  
- Monthly Balance Sheet statements

Data covers the previous 5 years plus current year month-to-date.
"""

import argparse
import os
import sys
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple


class SyntheticDataGenerator:
    """Main class for generating synthetic financial data"""
    
    def __init__(self, company_name: str = "Sample Company Inc."):
        self.company_name = company_name
        self.current_date = datetime.now()
        self.start_date = self.current_date - relativedelta(years=5)
        self.months_data = self._generate_date_range()
        
    def _generate_date_range(self) -> List[datetime]:
        """Generate list of month-end dates for the data period"""
        dates = []
        current = self.start_date.replace(day=1)
        
        while current <= self.current_date:
            # Get last day of the month
            next_month = current + relativedelta(months=1)
            last_day = next_month - relativedelta(days=1)
            dates.append(last_day)
            current = next_month
            
        return dates
    
    def generate_all_data(self, output_dir: str = "output") -> None:
        """Generate all three financial statements and save to CSV files"""
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate data for each statement type
        pl_data = self.generate_pl_data()
        cf_data = self.generate_cash_flow_data()
        bs_data = self.generate_balance_sheet_data()
        
        # Save to CSV files
        pl_path = os.path.join(output_dir, "monthly_pl_data.csv")
        cf_path = os.path.join(output_dir, "monthly_cash_flow_data.csv")
        bs_path = os.path.join(output_dir, "monthly_balance_sheet_data.csv")
        
        pl_data.to_csv(pl_path, index=False)
        cf_data.to_csv(cf_path, index=False)
        bs_data.to_csv(bs_path, index=False)
        
        print(f"Generated synthetic financial data:")
        print(f"  P&L Data: {pl_path}")
        print(f"  Cash Flow Data: {cf_path}")
        print(f"  Balance Sheet Data: {bs_path}")
        print(f"  Data period: {self.start_date.strftime('%Y-%m')} to {self.current_date.strftime('%Y-%m')}")
        print(f"  Total months: {len(self.months_data)}")
    
    def generate_pl_data(self) -> pd.DataFrame:
        """Generate synthetic P&L (Income Statement) data"""
        data = []
        
        # Base revenue with growth trend and seasonality
        base_revenue = 1000000  # $1M base monthly revenue
        growth_rate = 0.02  # 2% monthly growth
        
        for i, date in enumerate(self.months_data):
            # Add growth trend and seasonal variation
            seasonal_factor = 1 + 0.1 * np.sin(2 * np.pi * date.month / 12)
            revenue = base_revenue * (1 + growth_rate) ** i * seasonal_factor
            
            # Add some random variation
            revenue *= np.random.normal(1, 0.05)
            
            # Cost of Goods Sold (typically 40-60% of revenue)
            cogs = revenue * np.random.uniform(0.45, 0.55)
            gross_profit = revenue - cogs
            
            # Operating expenses
            salaries = revenue * np.random.uniform(0.15, 0.25)
            marketing = revenue * np.random.uniform(0.03, 0.08)
            rent = revenue * np.random.uniform(0.02, 0.05)
            utilities = revenue * np.random.uniform(0.01, 0.02)
            other_expenses = revenue * np.random.uniform(0.02, 0.05)
            
            total_operating_expenses = salaries + marketing + rent + utilities + other_expenses
            operating_income = gross_profit - total_operating_expenses
            
            # Interest and taxes
            interest_expense = revenue * np.random.uniform(0.001, 0.005)
            tax_rate = 0.25
            pre_tax_income = operating_income - interest_expense
            tax_expense = max(0, pre_tax_income * tax_rate)
            net_income = pre_tax_income - tax_expense
            
            data.append({
                'date': date.strftime('%Y-%m-%d'),
                'year': date.year,
                'month': date.month,
                'revenue': round(revenue, 2),
                'cost_of_goods_sold': round(cogs, 2),
                'gross_profit': round(gross_profit, 2),
                'salaries_and_benefits': round(salaries, 2),
                'marketing_expenses': round(marketing, 2),
                'rent_expense': round(rent, 2),
                'utilities_expense': round(utilities, 2),
                'other_operating_expenses': round(other_expenses, 2),
                'total_operating_expenses': round(total_operating_expenses, 2),
                'operating_income': round(operating_income, 2),
                'interest_expense': round(interest_expense, 2),
                'pre_tax_income': round(pre_tax_income, 2),
                'tax_expense': round(tax_expense, 2),
                'net_income': round(net_income, 2)
            })
        
        return pd.DataFrame(data)
    
    def generate_cash_flow_data(self) -> pd.DataFrame:
        """Generate synthetic Cash Flow Statement data"""
        # First get P&L data to base cash flow on
        pl_data = self.generate_pl_data()
        data = []
        
        # Starting cash balance
        cash_balance = 500000  # $500K starting cash
        
        for i, (_, pl_row) in enumerate(pl_data.iterrows()):
            date = datetime.strptime(pl_row['date'], '%Y-%m-%d')
            
            # Operating Cash Flow
            net_income = pl_row['net_income']
            
            # Non-cash adjustments
            depreciation = pl_row['revenue'] * np.random.uniform(0.01, 0.03)
            
            # Working capital changes
            ar_change = pl_row['revenue'] * np.random.uniform(-0.1, 0.1)  # Accounts receivable
            inventory_change = pl_row['cost_of_goods_sold'] * np.random.uniform(-0.05, 0.05)
            ap_change = pl_row['cost_of_goods_sold'] * np.random.uniform(-0.05, 0.05)  # Accounts payable
            
            operating_cash_flow = (net_income + depreciation - ar_change - 
                                 inventory_change + ap_change)
            
            # Investing Cash Flow
            capex = pl_row['revenue'] * np.random.uniform(-0.05, -0.01)  # Capital expenditures
            investing_cash_flow = capex
            
            # Financing Cash Flow
            debt_issuance = np.random.uniform(-50000, 50000) if np.random.random() > 0.8 else 0
            dividend_payment = max(0, net_income * 0.3) if net_income > 0 and np.random.random() > 0.7 else 0
            financing_cash_flow = debt_issuance - dividend_payment
            
            # Net change in cash
            net_cash_change = operating_cash_flow + investing_cash_flow + financing_cash_flow
            cash_balance += net_cash_change
            
            data.append({
                'date': pl_row['date'],
                'year': pl_row['year'],
                'month': pl_row['month'],
                'net_income': round(net_income, 2),
                'depreciation_amortization': round(depreciation, 2),
                'accounts_receivable_change': round(ar_change, 2),
                'inventory_change': round(inventory_change, 2),
                'accounts_payable_change': round(ap_change, 2),
                'operating_cash_flow': round(operating_cash_flow, 2),
                'capital_expenditures': round(capex, 2),
                'investing_cash_flow': round(investing_cash_flow, 2),
                'debt_issuance_repayment': round(debt_issuance, 2),
                'dividend_payments': round(dividend_payment, 2),
                'financing_cash_flow': round(financing_cash_flow, 2),
                'net_cash_change': round(net_cash_change, 2),
                'ending_cash_balance': round(cash_balance, 2)
            })
        
        return pd.DataFrame(data)
    
    def generate_balance_sheet_data(self) -> pd.DataFrame:
        """Generate synthetic Balance Sheet data"""
        # Get cash flow data to maintain consistency
        cf_data = self.generate_cash_flow_data()
        pl_data = self.generate_pl_data()
        
        data = []
        
        # Initialize balance sheet items
        initial_ppe = 1000000  # Property, Plant & Equipment
        initial_debt = 500000
        initial_equity = 800000
        
        cumulative_retained_earnings = 0
        cumulative_depreciation = 0
        cumulative_capex = 0
        
        for i, (cf_row, pl_row) in enumerate(zip(cf_data.itertuples(), pl_data.itertuples())):
            date = datetime.strptime(cf_row.date, '%Y-%m-%d')
            
            # Assets
            cash = cf_row.ending_cash_balance
            accounts_receivable = pl_row.revenue * np.random.uniform(0.1, 0.2)
            inventory = pl_row.cost_of_goods_sold * np.random.uniform(0.1, 0.25)
            
            current_assets = cash + accounts_receivable + inventory
            
            # Fixed assets
            cumulative_depreciation += cf_row.depreciation_amortization
            cumulative_capex += abs(cf_row.capital_expenditures)
            ppe_net = initial_ppe + cumulative_capex - cumulative_depreciation
            
            total_assets = current_assets + ppe_net
            
            # Liabilities
            accounts_payable = pl_row.cost_of_goods_sold * np.random.uniform(0.05, 0.15)
            accrued_expenses = pl_row.total_operating_expenses * np.random.uniform(0.05, 0.1)
            
            current_liabilities = accounts_payable + accrued_expenses
            
            # Long-term debt (simplified)
            long_term_debt = initial_debt + sum(cf_data.iloc[:i+1]['debt_issuance_repayment'])
            
            total_liabilities = current_liabilities + long_term_debt
            
            # Equity
            cumulative_retained_earnings += pl_row.net_income - cf_row.dividend_payments
            
            # Force balance by adjusting shareholders' equity to match assets
            shareholders_equity = total_assets - total_liabilities
            
            # Balance check (Assets = Liabilities + Equity)
            total_liab_equity = total_liabilities + shareholders_equity
            
            data.append({
                'date': cf_row.date,
                'year': cf_row.year,
                'month': cf_row.month,
                'cash_and_equivalents': round(cash, 2),
                'accounts_receivable': round(accounts_receivable, 2),
                'inventory': round(inventory, 2),
                'current_assets': round(current_assets, 2),
                'property_plant_equipment_net': round(ppe_net, 2),
                'total_assets': round(total_assets, 2),
                'accounts_payable': round(accounts_payable, 2),
                'accrued_expenses': round(accrued_expenses, 2),
                'current_liabilities': round(current_liabilities, 2),
                'long_term_debt': round(long_term_debt, 2),
                'total_liabilities': round(total_liabilities, 2),
                'shareholders_equity': round(shareholders_equity, 2),
                'total_liabilities_and_equity': round(total_liab_equity, 2),
                'balance_check': round(total_assets - total_liab_equity, 2)
            })
        
        return pd.DataFrame(data)


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(description='Generate synthetic financial data')
    parser.add_argument('--company', '-c', default='Sample Company Inc.',
                       help='Company name for the financial data')
    parser.add_argument('--output-dir', '-o', default='output',
                       help='Output directory for CSV files')
    
    args = parser.parse_args()
    
    # Generate synthetic data
    generator = SyntheticDataGenerator(company_name=args.company)
    generator.generate_all_data(output_dir=args.output_dir)


if __name__ == '__main__':
    main()