# Personal Expenses Tracker

A command-line Personal Finance Tracker application built with vanilla Python that manages daily expenses, tracks balance, and generates expense reports. Includes a companion shell script for file organization and automated archival tasks.

## 📋 Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [File Formats](#file-formats)
- [Testing](#testing)
- [Learning Outcomes](#learning-outcomes)

## ✨ Features

### Python Application (`expenses-tracker.py`)

1. **Main Menu System**
   - Interactive command-line interface
   - Four main options: Check Balance, View Expenses, Add Expense, Exit
   - Continuous loop until user exits
   - Graceful program termination with data persistence

2. **Check Remaining Balance**
   - Display current balance, total expenses, and available balance
   - Option to add money to balance
   - Input validation for amounts
   - Real-time balance updates

3. **Add New Expense**
   - Display available balance before entry
   - Date input with validation (YYYY-MM-DD format)
   - Item name and amount input
   - Confirmation before saving
   - Insufficient balance detection
   - Automatic ID generation per day
   - Timestamp tracking
   - Balance updates after expense

4. **View Expenses**
   - Search by item name (case-insensitive)
   - Search by exact amount
   - Formatted table display of results
   - Shows ID, date, item, timestamp, and amount

### Shell Script (`archive_expenses.sh`)

1. **Archive Expense Files**
   - Move expense files to archives directory
   - Automatic directory creation
   - Timestamp logging of operations
   - Error handling and validation

2. **Search Archived Expenses**
   - Search by date in archives
   - Display formatted expense records
   - Calculate and show totals
   - Timestamp logging of searches

## 📁 Project Structure

```
expenses-tracker/
├── expenses-tracker.py      # Main Python application
├── archive_expenses.sh      # Shell script for archiving
├── balance.txt              # Current balance storage
├── README.md                # Project documentation
├── expenses_YYYY-MM-DD.txt  # Daily expense files (auto-generated)
├── archives/                # Archived expense files directory
│   └── expenses_*.txt
└── archive_log.txt          # Archive operation logs (auto-generated)
```

## 🔧 Requirements

- **Python**: 3.6 or higher
- **Operating System**: Linux/Unix-based system (for shell script)
- **Shell**: Bash
- **Additional Tools**: `bc` (for floating-point calculations in shell script)

## 📥 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/Lab3-expenses-tracker_yourusername.git
   cd Lab3-expenses-tracker_yourusername
   ```

2. **Make the shell script executable**:
   ```bash
   chmod +x archive_expenses.sh
   ```

3. **Verify Python installation**:
   ```bash
   python3 --version
   ```

4. **Initialize balance** (if needed):
   The `balance.txt` file is included with an initial balance of $1000.00.
   You can modify this value directly in the file if desired.

## 🚀 Usage

### Running the Python Application

Start the expense tracker:
```bash
python3 expenses-tracker.py
```

### Menu Options

**1. Check Remaining Balance**
```
Displays:
- Current balance
- Total expenses to date
- Available balance
- Option to add money
```

**2. View Expenses**
```
Sub-menu options:
1. Search by item name
2. Search by amount
3. Back to main menu
```

**3. Add New Expense**
```
Process:
1. Shows available balance
2. Enter date (YYYY-MM-DD)
3. Enter item name
4. Enter amount
5. Confirm expense
6. Validates balance
7. Saves and updates
```

**4. Exit**
```
Saves all data and terminates the program
```

### Using the Shell Script

**Archive an expense file**:
```bash
./archive_expenses.sh 2025-11-07
```

**Search for archived expense**:
```bash
./archive_expenses.sh search 2025-11-07
```

**View help**:
```bash
./archive_expenses.sh
```

### Example Workflow

1. **Start the application**:
   ```bash
   python3 expenses-tracker.py
   ```

2. **Check your balance**:
   - Select option 1
   - View current balance
   - Optionally add money

3. **Add an expense**:
   - Select option 3
   - Enter date: `2025-11-22`
   - Enter item: `Groceries`
   - Enter amount: `45.50`
   - Confirm: `y`

4. **View your expenses**:
   - Select option 2
   - Choose search option
   - Enter search criteria

5. **Archive old expenses**:
   ```bash
   ./archive_expenses.sh 2025-11-22
   ```

6. **Search archived expenses**:
   ```bash
   ./archive_expenses.sh search 2025-11-22
   ```

## 📄 File Formats

### balance.txt
```
1000.00
```
Single line containing the current balance as a decimal number.

### expenses_YYYY-MM-DD.txt
```
1|Groceries|2025-11-22 14:30:00|45.50
2|Coffee|2025-11-22 16:45:00|4.75
3|Lunch|2025-11-22 12:30:00|12.00
```
Format: `ID|ItemName|Timestamp|Amount`
- Each line represents one expense
- Fields are separated by pipe (|) character
- ID is sequential per day
- Timestamp format: YYYY-MM-DD HH:MM:SS
- Amount is decimal with 2 decimal places

### archive_log.txt
```
[2025-11-22 18:30:15] ARCHIVE: Moved expenses_2025-11-07.txt to archives/
[2025-11-22 18:32:45] SEARCH: Displayed archived expenses for 2025-11-07
```
Format: `[Timestamp] Operation: Description`

## 🧪 Testing

### Testing the Python Application

1. **Test balance operations**:
   ```bash
   python3 expenses-tracker.py
   # Select option 1
   # Add money when prompted
   # Verify balance updates
   ```

2. **Test expense addition**:
   - Add expenses with various amounts
   - Test insufficient balance scenario
   - Verify file creation (expenses_YYYY-MM-DD.txt)
   - Check balance deduction

3. **Test expense viewing**:
   - Search by item name (partial matches)
   - Search by amount (exact matches)
   - Verify formatted output

4. **Test date validation**:
   - Try invalid dates (e.g., 2025-13-45)
   - Try incorrect formats (e.g., 11/22/2025)
   - Verify error messages

### Testing the Shell Script

1. **Test archiving**:
   ```bash
   # Create a test expense file first using Python app
   python3 expenses-tracker.py
   # Add expense for today's date
   
   # Archive it
   ./archive_expenses.sh 2025-11-22
   
   # Verify file moved to archives/
   ls -l archives/
   
   # Check log file
   cat archive_log.txt
   ```

2. **Test searching**:
   ```bash
   ./archive_expenses.sh search 2025-11-22
   # Verify formatted output
   ```

3. **Test error handling**:
   ```bash
   # Try archiving non-existent file
   ./archive_expenses.sh 2025-01-01
   
   # Try invalid date format
   ./archive_expenses.sh 2025-13-45
   
   # Try searching non-existent archive
   ./archive_expenses.sh search 1999-01-01
   ```

### Cross-System Testing

Test on different systems to ensure compatibility:
- Ubuntu/Debian
- Fedora/RHEL
- macOS (with bash)
- WSL (Windows Subsystem for Linux)

## 📚 Learning Outcomes

This project demonstrates:

1. **File I/O Operations**
   - Reading from and writing to text files
   - Creating and managing multiple files
   - File existence checking
   - Directory operations

2. **Data Structures**
   - Lists for storing expense records
   - String manipulation and parsing
   - Structured data format (pipe-delimited)

3. **Control Flow**
   - Menu-driven program loops
   - Conditional statements
   - Input validation loops
   - Exception handling

4. **Shell Scripting**
   - Bash script structure
   - Command-line argument parsing
   - File operations in shell
   - Error handling and logging
   - Date validation

5. **Software Engineering Practices**
   - Code organization and modularity
   - Error handling and validation
   - User experience design
   - Documentation
   - Testing strategies

## 🐛 Troubleshooting

### Common Issues

**Issue**: `Permission denied` when running shell script
```bash
# Solution: Make script executable
chmod +x archive_expenses.sh
```

**Issue**: `bc: command not found` error
```bash
# Solution: Install bc
sudo apt-get install bc  # Ubuntu/Debian
sudo yum install bc      # Fedora/RHEL
```

**Issue**: Python script can't find balance.txt
```bash
# Solution: Ensure you're in the correct directory
cd /path/to/expenses-tracker/
python3 expenses-tracker.py
```

**Issue**: Date validation fails
```bash
# Solution: Ensure date command supports -d flag
# On macOS, you may need to install GNU coreutils:
brew install coreutils
# Then use gdate instead of date in the script
```

## 📝 Notes

- All monetary values are stored with 2 decimal places
- Dates must be in YYYY-MM-DD format
- Expense IDs are sequential per day (reset for each date)
- Balance file stores only the current total balance
- Archives directory is created automatically if it doesn't exist
- Archive logs include timestamps for audit purposes

## 👨‍💻 Author

Your Name - GitHub: mgpacifique

## 📄 License

This project is part of an academic assignment for African Leadership University.

---

**African Leadership University**  
BSE Year 1 Trimester 2  
Introduction to Python Programming and Databases  
Lab 3: Personal Expenses Tracker
