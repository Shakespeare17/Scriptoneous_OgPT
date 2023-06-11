#!/bin/bash

# Iterate over PDF files in the current directory
for file in *.pdf; do
    if [[ -f "$file" ]]; then
        # Extract the name from the first page of the PDF
        name=$(pdfgrep -m 1 "." "$file" | head -n 1)

        # Remove invalid characters from the name
        name=$(echo "$name" | sed 's/[^a-zA-Z0-9_-]/_/g')

        # Rename the file
        if [[ -n "$name" ]]; then
            new_name="${name}.pdf"
            mv "$file" "$new_name"
            echo "Renamed '$file' to '$new_name'"
        else
            echo "No name found in '$file'"
        fi
    fi
done