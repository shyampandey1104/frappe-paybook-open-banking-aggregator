import unittest
from paybook_sync.engine import PaybookOpenBankingEngine, PaybookBankTransaction

class TestPaybookOpenBanking(unittest.TestCase):
    def test_auto_categorization(self):
        engine = PaybookOpenBankingEngine()
        txn = PaybookBankTransaction(
            paybook_txn_id="PB-TXN-101",
            account_number_mask="*9912",
            booking_date="2026-03-01",
            description="DEBIT - AMAZON WEB SERVICES CLOUD BILL",
            amount=-12500.0
        )
        acc = engine.categorize_transaction(txn)
        self.assertEqual(acc, "5110 - Cloud Infrastructure Expenses")

    def test_ledger_reconciliation(self):
        engine = PaybookOpenBankingEngine()
        bank_txns = [
            PaybookBankTransaction("PB-01", "*9912", "2026-03-01", "Uber trip", -450.0),
            PaybookBankTransaction("PB-02", "*9912", "2026-03-02", "Unknown vendor payment", -1200.0)
        ]
        erp_entries = [
            {"name": "PE-2026-01", "date": "2026-03-01", "paid_amount": 450.0}
        ]

        recon = engine.reconcile_with_ledger_entries(bank_txns, erp_entries)
        self.assertEqual(recon[0].match_status, "EXACT_MATCH_RECONCILED")
        self.assertEqual(recon[0].erp_payment_entry_id, "PE-2026-01")
        self.assertEqual(recon[1].match_status, "UNMATCHED_BANK_FEED")

if __name__ == "__main__":
    unittest.main()
