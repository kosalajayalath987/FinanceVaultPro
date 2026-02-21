FinanceVaultPro - Petty Cash Management

A robust, enterprise-grade Petty Cash Management System built with Python and MySQL. Features a real-time DR/CR (Debit/Credit) ledger, automated PDF voucher generation, and comprehensive audit reporting for corporate financial control.

✨ Features
* **Real-time Ledger:** Track expenses and top-ups instantly.
* **Automated Vouchers:** Generates PDF Debit Vouchers for every expense.
* **Audit Ready:** Export full transaction history to PDF.
* **KPI Dashboard:** Visual summary of current liquidity and session totals.

🚀 Getting Started
1. Install MySQL and ensure it's running on `localhost`.
2. Clone the repo: `git clone https://github.com/kosalajayalath987/FinanceVaultPro.git`
3. Install dependencies: 'requirements.txt.`
4. Run the app: `python main.py.`


🛠️ Tech Stack
* **Language:** Python 3.x
* **GUI Framework:** Tkinter
* **Database:** MySQL
* **Reporting:** ReportLab (PDF Generation)

🧪 Guided Test Walkthrough
* Once the app is running, try these steps to verify the DR/CR logic:
* Top-up (Credit): Select Credit (Top-up) from the Mode dropdown, enter "Initial Funding" and an amount (e.g., 5000). Click Post.
* Observe: The "Current Liquidity" KPI should turn green and increase.
* Expense (Debit): Select Debit (Expense), enter "Office Supplies", an amount (e.g., 200), and choose an Authorizer. Click Post.
* Observe: A PDF voucher is instantly generated in the /output folder.
* Audit: Click Full Audit PDF in the sidebar to generate a complete transaction history report.
