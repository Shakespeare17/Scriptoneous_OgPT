#!/bin/bash

# Function to extract information from a file
extract_info() {
    input_file="$1"
    output_file="${input_file}_info.txt"

    # Check if the file exists
    if [ -f "$input_file" ]; then
        # Get the file type
        file_type=$(file -b "$input_file")

        # Display the file type
        echo "File Type: $file_type" > "$output_file"

        # Extract email addresses using grep and a regular expression
        echo "Email Addresses:" >> "$output_file"
        grep -Eio '\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b' "$input_file" >> "$output_file"

        # Extract URLs using grep and a regular expression
        echo "URLs:" >> "$output_file"
        grep -Eio 'https?://[^[:space:]]+' "$input_file" >> "$output_file"

        # Extract full names using grep and a regular expression
        echo "Full Names:" >> "$output_file"
        grep -Eio '[A-Z][a-z]+ [A-Z][a-z]+' "$input_file" >> "$output_file"

        # Extract phone numbers using grep and a regular expression
        echo "Phone Numbers:" >> "$output_file"
        grep -Eio '\b[0-9]{3}-[0-9]{3}-[0-9]{4}\b' "$input_file" >> "$output_file"

        # Extract street addresses using grep and a regular expression
        echo "Street Addresses:" >> "$output_file"
        grep -Eio '[0-9]+ [A-Za-z]+ [A-Za-z]+, [A-Za-z]+ [0-9]{5}' "$input_file" >> "$output_file"

        echo "Information extracted and saved to $output_file."
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