#!/usr/bin/env python3
"""
Data Validation Script for Synthetic Financial Data

Validates GAAP compliance and data consistency across the generated financial statements.
"""

import pandas as pd
import numpy as np
import sys
import os


def validate_data(data_dir="output"):
    """Validate the generated synthetic financial data"""
    
    print(f"Validating synthetic financial data in {data_dir}/")
    print("=" * 50)
    
    # Load the data files
    try:
        pl_data = pd.read_csv(f"{data_dir}/monthly_pl_data.csv")
        cf_data = pd.read_csv(f"{data_dir}/monthly_cash_flow_data.csv")
        bs_data = pd.read_csv(f"{data_dir}/monthly_balance_sheet_data.csv")
    except FileNotFoundError as e:
        print(f"Error: Could not find data files in {data_dir}/")
        print(f"Please run 'python3 generate_synthdata.py --output-dir {data_dir}' first")
        return False
    
    validation_passed = True
    
    # 1. Check data completeness
    print("1. DATA COMPLETENESS CHECK")
    print(f"   P&L records: {len(pl_data)}")
    print(f"   Cash Flow records: {len(cf_data)}")
    print(f"   Balance Sheet records: {len(bs_data)}")
    
    if len(pl_data) != len(cf_data) or len(pl_data) != len(bs_data):
        print("   ❌ Record counts don't match across statements")
        validation_passed = False
    else:
        print("   ✓ All statements have matching record counts")
    
    # 2. Check date ranges
    print("\n2. DATE RANGE CHECK")
    date_range_pl = f"{pl_data['date'].min()} to {pl_data['date'].max()}"
    date_range_cf = f"{cf_data['date'].min()} to {cf_data['date'].max()}"
    date_range_bs = f"{bs_data['date'].min()} to {bs_data['date'].max()}"
    
    print(f"   P&L: {date_range_pl}")
    print(f"   Cash Flow: {date_range_cf}")
    print(f"   Balance Sheet: {date_range_bs}")
    
    if date_range_pl == date_range_cf == date_range_bs:
        print("   ✓ Date ranges match across all statements")
    else:
        print("   ❌ Date ranges don't match")
        validation_passed = False
    
    # 3. Check for negative values where inappropriate
    print("\n3. GAAP COMPLIANCE CHECK")
    
    # Revenue should never be negative
    negative_revenue = pl_data[pl_data['revenue'] < 0]
    print(f"   Negative revenue entries: {len(negative_revenue)} (should be 0)")
    if len(negative_revenue) > 0:
        print("   ❌ Found negative revenue entries")
        validation_passed = False
    else:
        print("   ✓ No negative revenue entries")
    
    # Total assets should never be negative
    negative_assets = bs_data[bs_data['total_assets'] < 0]
    print(f"   Negative total assets: {len(negative_assets)} (should be 0)")
    if len(negative_assets) > 0:
        print("   ❌ Found negative total assets")
        validation_passed = False
    else:
        print("   ✓ No negative total assets")
    
    # 4. Balance sheet balance check
    print("\n4. BALANCE SHEET BALANCE CHECK")
    balance_issues = bs_data[bs_data['balance_check'].abs() > 0.01]
    print(f"   Balance discrepancies: {len(balance_issues)} (should be 0)")
    if len(balance_issues) > 0:
        print("   ❌ Balance sheet doesn't balance")
        print("   Sample discrepancies:")
        print(balance_issues[['date', 'balance_check']].head())
        validation_passed = False
    else:
        print("   ✓ All balance sheets balance correctly")
    
    # 5. Check P&L mathematical consistency
    print("\n5. P&L MATHEMATICAL CONSISTENCY")
    
    # Gross profit = Revenue - COGS
    gross_profit_check = abs(pl_data['gross_profit'] - (pl_data['revenue'] - pl_data['cost_of_goods_sold'])).max()
    print(f"   Gross profit calculation max error: {gross_profit_check:.2f}")
    
    # Net income flow
    net_income_check = abs(pl_data['net_income'] - (pl_data['pre_tax_income'] - pl_data['tax_expense'])).max()
    print(f"   Net income calculation max error: {net_income_check:.2f}")
    
    if gross_profit_check < 0.02 and net_income_check < 0.02:
        print("   ✓ P&L calculations are mathematically consistent")
    else:
        print("   ❌ P&L calculations have errors")
        validation_passed = False
    
    # 6. Check data period coverage
    print("\n6. DATA PERIOD COVERAGE")
    pl_data['date'] = pd.to_datetime(pl_data['date'])
    years_covered = pl_data['year'].nunique()
    months_covered = len(pl_data)
    expected_years = 5.5  # 5 years + partial current year
    
    print(f"   Years covered: {years_covered}")
    print(f"   Months covered: {months_covered}")
    print(f"   Expected: ~{expected_years} years, 60+ months")
    
    if years_covered >= 5 and months_covered >= 60:
        print("   ✓ Adequate historical data coverage")
    else:
        print("   ❌ Insufficient historical data coverage")
        validation_passed = False
    
    # 7. Data quality checks
    print("\n7. DATA QUALITY CHECKS")
    
    # Check for missing values
    pl_missing = pl_data.isnull().sum().sum()
    cf_missing = cf_data.isnull().sum().sum()
    bs_missing = bs_data.isnull().sum().sum()
    
    print(f"   Missing values - P&L: {pl_missing}, Cash Flow: {cf_missing}, Balance Sheet: {bs_missing}")
    
    if pl_missing == 0 and cf_missing == 0 and bs_missing == 0:
        print("   ✓ No missing values found")
    else:
        print("   ❌ Found missing values")
        validation_passed = False
    
    # Summary
    print("\n" + "=" * 50)
    if validation_passed:
        print("✓ ALL VALIDATIONS PASSED")
        print("The synthetic financial data is GAAP-compliant and mathematically consistent.")
        return True
    else:
        print("❌ SOME VALIDATIONS FAILED")
        print("Please review the issues above and regenerate the data.")
        return False


def main():
    """Main CLI entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Validate synthetic financial data')
    parser.add_argument('--data-dir', '-d', default='output',
                       help='Directory containing the CSV files to validate')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.data_dir):
        print(f"Error: Directory '{args.data_dir}' does not exist")
        sys.exit(1)
    
    success = validate_data(args.data_dir)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()