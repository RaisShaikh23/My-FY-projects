💳 Banking System - Python CLI Project
A simple command-line based banking application written in Python. This project simulates a secure mini-banking system where users can create an account, credit/debit money, and check their account balance with basic password authentication.

📌 Features
✅ Create Account: User can create a new bank account with a secure password.
🔒 Password Protection: Each account is protected with a personal PIN (password).
🧾 Unique Password File Per Account: Each user’s password is stored in a dedicated .txt file named after their account number (e.g., 101_password.txt).
💰 Credit Functionality: Add funds to your account.
💸 Debit Functionality: Withdraw money only if sufficient balance is available.
📊 Transaction Log: All transactions are stored in a .csv file per user.
📁 File-Based Storage: Account data is stored locally using text and CSV files.
🕒 Timestamps: All operations display the current time.
🧱 File Structure
When a user account is created, the system generates:

account_no_account.csv: Stores transaction history (credit/debit as signed integers).
account_no_password.txt: Stores the user's password for verification.
➡️ Each account has its own password file, uniquely named based on the account number. Example: rs0230_account.csv ← stores transactions rs0230_password.txt ← stores password (linked to same account)

⚙️ How It Works
User enters their account number and PIN.
The program checks if their account and password files exist:
If they don’t exist, it prompts them to create an account.
If they exist, it verifies the PIN.
A menu-driven interface allows the user to:
1: Create Account
2: Credit Balance
3: Debit Balance
4: View Final Balance & Transaction History
Any other key: Exit
All operations require password verification before proceeding.

🧠 Benefits
Simple to understand and extend (perfect for beginners).
No external libraries — runs on core Python.
Teaches file handling, basic input validation, and secure access control.
Clear separation of functionalities in class methods.
⚠️ Limitations
❌ Passwords are stored in plain text, which is not secure for real-world use.
❌ No encryption or database — uses basic file I/O.
❌ No input sanitization for account number or password complexity.
❌ Cannot handle concurrent access or multiple users at the same time.
🚀 How To Run
Make sure you have Python 3.x installed.
Save the code in a .py file, e.g., bank_system.py.
Run it in your terminal:
