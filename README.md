# Frappe Paybook Open Banking Aggregator & Live Feed Engine

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![FinTech](https://img.shields.io/badge/Open%20Banking-Paybook%20Sync-teal.svg)](https://paybook.com)

Integrates Paybook Sync and Account Aggregator Open Banking APIs into Frappe, automatically pulling daily bank transaction feeds and reconciling them against ERPNext Payment Entries.

## Features
- **Automated Expense Categorization:** Rules engine classifies transaction descriptions into chart-of-accounts expense ledgers (AWS, Uber, GST, etc.).
- **Zero-Touch Bank Reconciliation:** Matches live bank clearing dates and debits against ERPNext Payment Entries.
- **Account Aggregator Support:** Seamlessly supports multi-bank feeds across HDFC, ICICI, SBI, and international accounts.

## Tests
```bash
python3 -m unittest discover tests
```
