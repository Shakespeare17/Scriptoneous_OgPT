#!/bin/bash

# Recursively loop through all files in current directory and its subdirectories
find . -type f | while read file; do
  # Remove commas, apostrophes, and double-dashes from filename
  new_name=$(echo "$file" | sed -e "s/[,']//g" -e "s/--/-/g")
  # Replace spaces with hyphens
  new_name=$(echo "$new_name" | tr ' ' '-')
  # Convert uppercase file extensions to lowercase
  extension=$(echo "$new_name" | awk -F '.' '{print $NF}')
  new_extension=$(echo "$extension" | tr '[:upper:]' '[:lower:]')
  new_name=$(echo "$new_name" | sed "s/\.$extension/\.$new_extension/")
  # Rename file
  mv "$file" "$new_name"
done