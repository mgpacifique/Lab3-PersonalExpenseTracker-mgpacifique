#!/usr/bin/env python3
"""
Personal Expenses Tracker
A command-line application to manage daily expenses, track balance, and generate expense reports.
"""

import os
import sys
from datetime import datetime
import re


class ExpenseTracker:
    """Main class for managing personal expenses and balance."""
    
    def __init__(self):
        """Initialize the expense tracker."""
        self.balance_file = "balance.txt"
        self.archive_log = "archive_log.txt"
        self.ensure_files_exist()
    
    def ensure_files_exist(self):
        """Ensure required files exist."""
        if not os.path.exists(self.balance_file):
            with open(self.balance_file, 'w') as f:
                f.write("1000.00")
        
        if not os.path.exists("archives"):
            os.makedirs("archives")
    
    def read_balance(self):
        """Read current balance from balance.txt file."""
        try:
            with open(self.balance_file, 'r') as f:
                balance = float(f.read().strip())
                return balance
        except (FileNotFoundError, ValueError) as e:
            print(f"Error reading balance: {e}")
            return 0.0
    
    def write_balance(self, balance):
        """Write updated balance to balance.txt file."""
        try:
            with open(self.balance_file, 'w') as f:
                f.write(f"{balance:.2f}")
        except IOError as e:
            print(f"Error writing balance: {e}")
    
    def calculate_total_expenses(self):
        """Calculate total expenses from all expense files."""
        total = 0.0
        expense_files = [f for f in os.listdir('.') if f.startswith('expenses_') and f.endswith('.txt')]
        
        for filename in expense_files:
            try:
                with open(filename, 'r') as f:
                    for line in f:
                        parts = line.strip().split('|')
                        if len(parts) >= 4:
                            amount = float(parts[3])
                            total += amount
            except (FileNotFoundError, ValueError, IndexError):
                continue
        
        return total
    
    def display_menu(self):
        """Display the main menu."""
        print("\n" + "=" * 50)
        print("   PERSONAL EXPENSES TRACKER")
        print("=" * 50)
        print("\n1. Check Remaining Balance")
        print("2. View Expenses")
        print("3. Add New Expense")
        print("4. Exit")
        print("\n" + "=" * 50)
    
    def check_balance(self):
        """Feature 2: Check remaining balance and optionally add money."""
        current_balance = self.read_balance()
        total_expenses = self.calculate_total_expenses()
        available_balance = current_balance
        
        print("\n" + "=" * 50)
        print("   BALANCE REPORT")
        print("=" * 50)
        print(f"\nCurrent Balance:        ${current_balance:,.2f}")
        print(f"Total Expenses to Date: ${total_expenses:,.2f}")
        print(f"Available Balance:      ${available_balance:,.2f}")
        print("\n" + "=" * 50)
        
        # Ask if user wants to add money
        add_money = input("\nWould you like to add money to your balance? (y/n): ").strip().lower()
        
        if add_money == 'y':
            while True:
                try:
                    amount_str = input("Enter amount to add: $")
                    amount = float(amount_str)
                    
                    if amount <= 0:
                        print("Error: Amount must be a positive number.")
                        continue
                    
                    new_balance = current_balance + amount
                    self.write_balance(new_balance)
                    
                    print(f"\n✓ Success! ${amount:.2f} added to your balance.")
                    print(f"New Balance: ${new_balance:,.2f}")
                    break
                    
                except ValueError:
                    print("Error: Please enter a valid number.")
    
    def get_next_expense_id(self, date):
        """Get the next sequential ID for an expense on a given date."""
        filename = f"expenses_{date}.txt"
        
        if not os.path.exists(filename):
            return 1
        
        max_id = 0
        try:
            with open(filename, 'r') as f:
                for line in f:
                    parts = line.strip().split('|')
                    if len(parts) >= 1:
                        expense_id = int(parts[0])
                        max_id = max(max_id, expense_id)
        except (FileNotFoundError, ValueError):
            pass
        
        return max_id + 1
    
    def validate_date(self, date_str):
        """Validate date format YYYY-MM-DD."""
        pattern = r'^\d{4}-\d{2}-\d{2}$'
        if not re.match(pattern, date_str):
            return False
        
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False
    
    def add_expense(self):
        """Feature 3: Add a new expense."""
        # Display available balance prominently
        available_balance = self.read_balance()
        print("\n" + "=" * 50)
        print(f"   AVAILABLE BALANCE: ${available_balance:,.2f}")
        print("=" * 50)
        
        # Get expense date
        while True:
            date_str = input("\nEnter date (YYYY-MM-DD, e.g., 2025-11-07): ").strip()
            
            if self.validate_date(date_str):
                break
            else:
                print("Error: Invalid date format. Please use YYYY-MM-DD.")
        
        # Get item name
        while True:
            item_name = input("Enter item name: ").strip()
            if item_name:
                break
            else:
                print("Error: Item name cannot be empty.")
        
        # Get amount
        while True:
            try:
                amount_str = input("Enter amount paid: $")
                amount = float(amount_str)
                
                if amount <= 0:
                    print("Error: Amount must be a positive number.")
                    continue
                
                break
            except ValueError:
                print("Error: Please enter a valid number.")
        
        # Display confirmation
        print("\n" + "-" * 50)
        print("EXPENSE DETAILS:")
        print(f"Date:   {date_str}")
        print(f"Item:   {item_name}")
        print(f"Amount: ${amount:.2f}")
        print("-" * 50)
        
        confirmation = input("\nConfirm this expense? (y/n): ").strip().lower()
        
        if confirmation != 'y':
            print("Expense cancelled.")
            return
        
        # Check if sufficient balance
        if amount > available_balance:
            print("\n✗ Error: Insufficient balance! Cannot save expense.")
            print(f"Available: ${available_balance:.2f}, Required: ${amount:.2f}")
            return
        
        # Generate expense ID
        expense_id = self.get_next_expense_id(date_str)
        
        # Capture current timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Save expense to file
        filename = f"expenses_{date_str}.txt"
        try:
            with open(filename, 'a') as f:
                f.write(f"{expense_id}|{item_name}|{timestamp}|{amount:.2f}\n")
            
            # Update balance
            new_balance = available_balance - amount
            self.write_balance(new_balance)
            
            print(f"\n✓ Success! Expense saved with ID #{expense_id}")
            print(f"Remaining Balance: ${new_balance:,.2f}")
            
        except IOError as e:
            print(f"Error saving expense: {e}")
    
    def search_by_item_name(self):
        """Search expenses by item name."""
        search_term = input("\nEnter item name to search: ").strip().lower()
        
        expense_files = [f for f in os.listdir('.') if f.startswith('expenses_') and f.endswith('.txt')]
        
        if not expense_files:
            print("\nNo expense records found.")
            return
        
        found = False
        print("\n" + "=" * 80)
        print("   SEARCH RESULTS")
        print("=" * 80)
        print(f"{'ID':<5} {'Date':<12} {'Item':<25} {'Timestamp':<20} {'Amount':>10}")
        print("-" * 80)
        
        for filename in expense_files:
            # Extract date from filename
            date = filename.replace('expenses_', '').replace('.txt', '')
            
            try:
                with open(filename, 'r') as f:
                    for line in f:
                        parts = line.strip().split('|')
                        if len(parts) >= 4:
                            expense_id, item_name, timestamp, amount = parts[0], parts[1], parts[2], parts[3]
                            
                            if search_term in item_name.lower():
                                print(f"{expense_id:<5} {date:<12} {item_name:<25} {timestamp:<20} ${float(amount):>9.2f}")
                                found = True
            except (FileNotFoundError, ValueError, IndexError):
                continue
        
        print("=" * 80)
        
        if not found:
            print(f"\nNo expenses found matching '{search_term}'")
    
    def search_by_amount(self):
        """Search expenses by amount."""
        while True:
            try:
                amount_str = input("\nEnter amount to search: $")
                search_amount = float(amount_str)
                break
            except ValueError:
                print("Error: Please enter a valid number.")
        
        expense_files = [f for f in os.listdir('.') if f.startswith('expenses_') and f.endswith('.txt')]
        
        if not expense_files:
            print("\nNo expense records found.")
            return
        
        found = False
        print("\n" + "=" * 80)
        print("   SEARCH RESULTS")
        print("=" * 80)
        print(f"{'ID':<5} {'Date':<12} {'Item':<25} {'Timestamp':<20} {'Amount':>10}")
        print("-" * 80)
        
        for filename in expense_files:
            # Extract date from filename
            date = filename.replace('expenses_', '').replace('.txt', '')
            
            try:
                with open(filename, 'r') as f:
                    for line in f:
                        parts = line.strip().split('|')
                        if len(parts) >= 4:
                            expense_id, item_name, timestamp, amount = parts[0], parts[1], parts[2], parts[3]
                            
                            if abs(float(amount) - search_amount) < 0.01:  # Float comparison
                                print(f"{expense_id:<5} {date:<12} {item_name:<25} {timestamp:<20} ${float(amount):>9.2f}")
                                found = True
            except (FileNotFoundError, ValueError, IndexError):
                continue
        
        print("=" * 80)
        
        if not found:
            print(f"\nNo expenses found with amount ${search_amount:.2f}")
    
    def view_expenses(self):
        """Feature 4: View expenses with search options."""
        while True:
            print("\n" + "=" * 50)
            print("   VIEW EXPENSES")
            print("=" * 50)
            print("\n1. Search by item name")
            print("2. Search by amount")
            print("3. Back to main menu")
            print("\n" + "=" * 50)
            
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == '1':
                self.search_by_item_name()
            elif choice == '2':
                self.search_by_amount()
            elif choice == '3':
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
    
    def run(self):
        """Main program loop."""
        print("\n" + "=" * 50)
        print("   WELCOME TO PERSONAL EXPENSES TRACKER")
        print("=" * 50)
        
        while True:
            self.display_menu()
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == '1':
                self.check_balance()
            elif choice == '2':
                self.view_expenses()
            elif choice == '3':
                self.add_expense()
            elif choice == '4':
                print("\n" + "=" * 50)
                print("   Thank you for using Expense Tracker!")
                print("   All data has been saved.")
                print("=" * 50)
                print()
                sys.exit(0)
            else:
                print("\n✗ Invalid choice. Please enter a number between 1 and 4.")


def main():
    """Entry point for the application."""
    try:
        tracker = ExpenseTracker()
        tracker.run()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
