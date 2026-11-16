"""Paybook Sync Open Banking API Connector & ERPNext Bank Reconciliation Engine."""

import hashlib
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field


@dataclass
class PaybookBankTransaction:
    paybook_txn_id: str
    account_number_mask: str
    booking_date: str          # YYYY-MM-DD
    description: str
    amount: float              # Positive for deposits, negative for withdrawals
    currency: str = "INR"
    suggested_gl_account: Optional[str] = None


@dataclass
class BankStatementMatchResult:
    paybook_txn_id: str
    erp_payment_entry_id: Optional[str]
    booking_date: str
    amount: float
    match_status: str          # EXACT_MATCH_RECONCILED, UNMATCHED_BANK_FEED, SUSPICIOUS_DUPLICATE


class PaybookOpenBankingEngine:
    """Connects Paybook Sync open banking feeds with ERPNext General Ledger bank accounts."""

    EXPENSE_RULE_MAP = {
        "AMAZON WEB SERVICES": "5110 - Cloud Infrastructure Expenses",
        "UBER": "5120 - Local Travel & Conveyance",
        "SWIGGY": "5130 - Office Meals & Refreshments",
        "SALARY": "2110 - Payroll Payable",
        "GST PAYMENT": "2210 - GST Payable"
    }

    def categorize_transaction(self, txn: PaybookBankTransaction) -> str:
        desc_upper = txn.description.upper()
        for keyword, gl_acc in self.EXPENSE_RULE_MAP.items():
            if keyword in desc_upper:
                txn.suggested_gl_account = gl_acc
                return gl_acc
        txn.suggested_gl_account = "5999 - Uncategorized Bank Expenses"
        return txn.suggested_gl_account

    def reconcile_with_ledger_entries(
        self,
        bank_txns: List[PaybookBankTransaction],
        erp_payment_entries: List[Dict[str, Any]]
    ) -> List[BankStatementMatchResult]:
        # erp_payment_entries format: [{"name": "PE-001", "date": "2026-03-01", "paid_amount": 500.0}]
        results = []
        matched_pe_ids = set()

        for b_txn in bank_txns:
            self.categorize_transaction(b_txn)
            matched_pe = None

            for pe in erp_payment_entries:
                if pe["name"] in matched_pe_ids:
                    continue
                # Match on exact absolute amount and same date
                if pe["date"] == b_txn.booking_date and abs(pe["paid_amount"] - abs(b_txn.amount)) < 0.01:
                    matched_pe = pe["name"]
                    matched_pe_ids.add(pe["name"])
                    break

            if matched_pe:
                status = "EXACT_MATCH_RECONCILED"
            else:
                status = "UNMATCHED_BANK_FEED"

            results.append(BankStatementMatchResult(
                paybook_txn_id=b_txn.paybook_txn_id,
                erp_payment_entry_id=matched_pe,
                booking_date=b_txn.booking_date,
                amount=b_txn.amount,
                match_status=status
            ))

        return results
