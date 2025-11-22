#!/bin/bash

# Configuration
ARCHIVE_DIR="archives"
LOG_FILE="archive_log.txt"

# Function to display usage
usage() {
    echo "Usage:"
    echo "  $0 <YYYY-MM-DD>           - Archive expense file for the given date"
    echo "  $0 search <YYYY-MM-DD>    - Search and display archived expense file"
    echo ""
    echo "Examples:"
    echo "  $0 2025-11-07"
    echo "  $0 search 2025-11-07"
}

# Function to validate date format
validate_date() {
    local date=$1
    
    # Check format YYYY-MM-DD
    if [[ ! $date =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
        return 1
    fi
    
    # Validate date is real (using date command)
    if ! date -d "$date" >/dev/null 2>&1; then
        return 1
    fi
    
    return 0
}

# Function to create archive directory if it doesn't exist
ensure_archive_dir() {
    if [ ! -d "$ARCHIVE_DIR" ]; then
        mkdir -p "$ARCHIVE_DIR"
        echo "Created archive directory: $ARCHIVE_DIR"
    fi
}

# Function to log archive operations
log_operation() {
    local message=$1
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] $message" >> "$LOG_FILE"
}

# Function to archive expense file
archive_expense() {
    local date=$1
    local expense_file="expenses_${date}.txt"
    
    # Check if expense file exists
    if [ ! -f "$expense_file" ]; then
        echo "Error: Expense file '$expense_file' not found."
        echo "No expenses recorded for date: $date"
        return 1
    fi
    
    # Ensure archive directory exists
    ensure_archive_dir
    
    # Move file to archives
    mv "$expense_file" "$ARCHIVE_DIR/"
    
    if [ $? -eq 0 ]; then
        echo "✓ Successfully archived: $expense_file"
        echo "  Location: $ARCHIVE_DIR/$expense_file"
        log_operation "ARCHIVE: Moved $expense_file to $ARCHIVE_DIR/"
        return 0
    else
        echo "✗ Error: Failed to archive $expense_file"
        log_operation "ERROR: Failed to archive $expense_file"
        return 1
    fi
}

# Function to search and display archived expense
search_archive() {
    local date=$1
    local expense_file="expenses_${date}.txt"
    local archive_path="$ARCHIVE_DIR/$expense_file"
    
    # Check if archived file exists
    if [ ! -f "$archive_path" ]; then
        echo "Error: No archived expense file found for date: $date"
        echo "Searched location: $archive_path"
        return 1
    fi
    
    # Display the archived expense file
    echo "=========================================================="
    echo "   ARCHIVED EXPENSES FOR: $date"
    echo "=========================================================="
    echo ""
    echo "ID   | Item Name                | Timestamp           | Amount"
    echo "-----|--------------------------|---------------------|--------"
    
    while IFS='|' read -r id item timestamp amount; do
        printf "%-4s | %-24s | %-19s | \$%.2f\n" "$id" "$item" "$timestamp" "$amount"
    done < "$archive_path"
    
    echo ""
    echo "=========================================================="
    
    # Calculate total
    local total=0
    while IFS='|' read -r id item timestamp amount; do
        total=$(echo "$total + $amount" | bc)
    done < "$archive_path"
    
    echo "Total Expenses: \$$total"
    echo "=========================================================="
    
    log_operation "SEARCH: Displayed archived expenses for $date"
    return 0
}

# Main script logic
main() {
    # Check if no arguments provided
    if [ $# -eq 0 ]; then
        echo "Error: No arguments provided."
        echo ""
        usage
        exit 1
    fi
    
    # Handle search command
    if [ "$1" == "search" ]; then
        if [ $# -ne 2 ]; then
            echo "Error: Search requires a date argument."
            echo ""
            usage
            exit 1
        fi
        
        local date=$2
        
        # Validate date format
        if ! validate_date "$date"; then
            echo "Error: Invalid date format. Use YYYY-MM-DD (e.g., 2025-11-07)"
            exit 1
        fi
        
        search_archive "$date"
        exit $?
    fi
    
    # Handle archive command (default)
    if [ $# -ne 1 ]; then
        echo "Error: Invalid number of arguments."
        echo ""
        usage
        exit 1
    fi
    
    local date=$1
    
    # Validate date format
    if ! validate_date "$date"; then
        echo "Error: Invalid date format. Use YYYY-MM-DD (e.g., 2025-11-07)"
        exit 1
    fi
    
    archive_expense "$date"
    exit $?
}

# Run main function
main "$@"
