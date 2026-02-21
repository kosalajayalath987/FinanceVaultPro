#### *** FinanceVaultPro - Petty Cash Management ***

A robust, enterprise-grade Petty Cash Management System built with Python and MySQL. Features a real-time DR/CR (Debit/Credit) ledger, automated PDF voucher generation, and comprehensive audit reporting for corporate financial control.

### **📂 Project Structure**

    ├── assets/
    ├── output/              
    ├── .gitignore          
    ├── database_setup.py    
    ├── main.py             
    ├── requirements.txt     
    └── README.md           
    

### **✨ Features**
* **Real-time Ledger:** Track expenses and top-ups instantly.
* **Automated Vouchers:** Generates PDF Debit Vouchers for every expense.
* **Audit Ready:** Export full transaction history to PDF.
* **KPI Dashboard:** Visual summary of current liquidity and session totals.


### **🚀 Getting Started**
1. Install MySQL and ensure it's running on `localhost`.
2. Clone the repo: `git clone https://github.com/kosalajayalath987/FinanceVaultPro.git`
3. Install dependencies: 'requirements.txt.`
4. Run the app: `python main.py.`

### **🛠️ Tech Stack**
* **Language:** Python 3.x
* **GUI Framework:** Tkinter
* **Database:** MySQL
* **Reporting:** ReportLab / fpdf (PDF Generation)


### **🧪 Guided Test Walkthrough**
* Once the app is running, try these steps to verify the DR/CR logic:
* Top-up (Credit): Select Credit (Top-up) from the Mode dropdown, enter "Initial Funding" and an amount (e.g., 5000). Click Post.
* Observe: The "Current Liquidity" KPI should turn green and increase.
* Expense (Debit): Select Debit (Expense), enter "Office Supplies", an amount (e.g., 200), and choose an Authorizer. Click Post.
* Observe: A PDF voucher is instantly generated in the /output folder.
* Audit: Click Full Audit PDF in the sidebar to generate a complete transaction history report.


### **🗄️ Database Structure**

## **Users**
Column | Type |	Constraints | Description|
:----  |:---- |:----|:----
user_id	INT |Primary Key, Auto-Inc | Unique identifier for each system user.|
username |VARCHAR |UNIQUE |Unique login name.|
password_hash |VARCHAR	|NOT NULL |Bcrypt hashed password for secure login.|
role |VARCHAR |NOT NULL	|User permissions (Admin, Custodian, etc.)|

## **Funds**
Column |Type |Constraints |Description |
:----  |:---- |:----|:----
fund_id |INT |Primary Key, Auto-Inc |Unique identifier for the fund.|
user_id |INT |Foreign Key |Links to users.user_id (the fund owner).|
fund_name |VARCHAR |NOT NULL |Descriptive name for the fund.|
balance	|DECIMAL |DEFAULT 0.00|The current liquid amount available.|

## **Transactions**
Column |Type |Constraints |Description
:----  |:---- |:----|:----
tx_id  |INT |Primary Key, Auto-Inc |Unique identifier for the transaction.
fund_id|INT |Foreign Key |Links to funds.fund_id.
amount |DECIMAL |NOT NULL |The monetary value of the transaction.
description |VARCHAR|-	|Narration or reason for the movement.
created_at |TIMESTAMP |DEFAULT NOW() |Automatic date and time of record.

    


        












