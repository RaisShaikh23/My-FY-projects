# 🏦 Bank Account Management System (Console-Based)

This project is a simple **console-based bank account management system** written in Python. It allows users to create a bank account file, credit and debit money, and view transaction history. All transactions are saved to a local `.csv` file associated with the user's account number.

---

## 🔧 Key Features

- 📁 **Account File Creation:** Generates a new CSV file for each account based on account number.
- 💰 **Credit Functionality:** Allows users to deposit money with date & time logged.
- 🧾 **Debit Functionality:** Lets users withdraw money (only if sufficient balance is available).
- 📜 **Transaction History:** Displays a list of all previous transactions and shows the current balance.
- 🗃 **File-based Storage:** All transactions are stored in a persistent CSV file.

---

## ⚙️ How It Works

1. **Create an Account:**
   - A new `.csv` file named `<account_number>_account.csv` is created.
   - If the file already exists, a message is shown to the user.

2. **Credit Money:**
   - Takes integer input for deposit amount.
   - Appends the amount to the CSV file.
   - Displays the credited amount and timestamp.

3. **Debit Money:**
   - Reads all previous transactions from the CSV file.
   - Ensures the debit amount does not exceed available balance.
   - Appends the negative amount to the file and confirms the debit.

4. **View Final Summary:**
   - Prints all transaction history.
   - Shows the current account balance with the last update timestamp.

---

## ✅ Benefits

- Beginner-friendly Python project.
- No external libraries required.
- File persistence ensures data is not lost between program runs.
- Realistic logic for balance checking and transaction tracking.

---

## ⚠️ Limitations

- No user authentication or password protection.
- Data stored in plain text (`.csv`) without encryption.
- No GUI — only terminal-based interactions.
- Does not support multiple accounts being accessed simultaneously in the same session.

---

## 🛠️ Technologies Used

- 🐍 Python 3.x (Standard Library)
- 💾 File I/O (`open()`, `write()`, `read()`)
- ⏱ Time module (`time.ctime()` for timestamps)

---
## Persional Experience :
i was revising classes and def in python , than i saw 10 to 15 line basic bank system class in my previous codes .
while  i was rewriting it , i just felt there should be some updation at that movement i just ran it.
It take me 2 and half day to make some modification , even after my code need some more mmodification like 'password'.
I will definetly try to make it more perfect more efficient.

