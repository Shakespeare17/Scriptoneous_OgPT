#!/bin/sh

# Function to extract information from a file and save to an SQLite database
extract_info() {
    input_file="$1"
    db_file="${input_file}_info.db"

    # Check if the file exists
    if [ -f "$input_file" ]; then
        # Get the file type
        file_type=$(file -b "$input_file")

        # Create an SQLite database file
        sqlite3 "$db_file" <<EOF
CREATE TABLE IF NOT EXISTS extracted_info (
    id INTEGER PRIMARY KEY,
    file_type TEXT,
    email_addresses TEXT,
    urls TEXT,
    full_names TEXT,
    phone_numbers TEXT,
    street_addresses TEXT
);
EOF

        # Extract email addresses using grep and a regular expression
        email_addresses=$(grep -Eio '\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b' "$input_file")

        # Extract URLs using grep and a regular expression
        urls=$(grep -Eio 'https?://[^[:space:]]+' "$input_file")

        # Extract full names using grep and a regular expression
        full_names=$(grep -Eio '[A-Z][a-z]+ [A-Z][a-z]+' "$input_file")

        # Extract phone numbers using grep and a regular expression
        phone_numbers=$(grep -Eio '\b[0-9]{3}-[0-9]{3}-[0-9]{4}\b' "$input_file")

        # Extract street addresses using grep and a regular expression
        street_addresses=$(grep -Eio '[0-9]+ [A-Za-z]+ [A-Za-z]+, [A-Za-z]+ [0-9]{5}' "$input_file")

        # Insert the extracted information into the SQLite database
        sqlite3 "$db_file" <<EOF
INSERT INTO extracted_info (file_type, email_addresses, urls, full_names, phone_numbers, street_addresses)
VALUES ('$file_type', '$email_addresses', '$urls', '$full_names', '$phone_numbers', '$street_addresses');
EOF

        echo "Information extracted and saved to $db_file."
    else
        echo "File does not exist."
    fi
}

# Main script execution starts here

# Check if a file path is provided as an argument
if [ -z "$1" ]; then
    echo "Please provide a file path."
else
    # Call the function to extract information
    extract_info "$1"
fi