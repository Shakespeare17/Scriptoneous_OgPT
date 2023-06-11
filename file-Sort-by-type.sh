#!/bin/bash

# Create folders for each file type
for file in *; do
    if [[ -f "$file" ]]; then
        extension="${file##*.}"
        mkdir -p "$extension"
    fi
done

# Move files into corresponding folders
for file in *; do
    if [[ -f "$file" ]]; then
        extension="${file##*.}"
        mv "$file" "$extension"
    fi
done