# synthdata-copilot
Using Copilot Agent to generate synthetic data generation scripts

## Overview
This project generates GAAP-compliant synthetic financial data for testing and development purposes. It produces three key financial statements:

1. **Monthly P&L (Profit & Loss) Statement** - Revenue, expenses, and net income
2. **Monthly Cash Flow Statement** - Operating, investing, and financing cash flows
3. **Monthly Balance Sheet** - Assets, liabilities, and equity

## Features
- Generates 5+ years of historical data plus current year month-to-date
- GAAP-compliant financial statement structure
- Realistic financial relationships and ratios
- Consistent data across all three statements
- Minimal external dependencies
- Command-line interface
- Extensible for future scenario injection

## Installation
```bash
# Clone the repository
git clone https://github.com/busse/synthdata-copilot.git
cd synthdata-copilot

# Install dependencies
pip install -r requirements.txt
```

## Usage
```bash
# Generate synthetic data with default settings
python3 generate_synthdata.py

# Specify company name and output directory
python3 generate_synthdata.py --company "Acme Corp" --output-dir my_data

# Show help
python3 generate_synthdata.py --help
```

## Output Files
The script generates three CSV files in the output directory:
- `monthly_pl_data.csv` - Profit & Loss statement data
- `monthly_cash_flow_data.csv` - Cash flow statement data  
- `monthly_balance_sheet_data.csv` - Balance sheet data

## Data Structure
Each file contains monthly data with the following common fields:
- `date` - End of month date (YYYY-MM-DD)
- `year` - Year
- `month` - Month number
- Plus statement-specific financial metrics

## Future Enhancements
This system is designed to be extensible for scenario injection such as:
- Revenue fluctuations
- Expense spikes
- Market conditions
- Economic events

## Requirements
- Python 3.7+
- pandas >= 1.5.0
- numpy >= 1.24.0
