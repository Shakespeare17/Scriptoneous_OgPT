#!/bin/bash

# Backup source and destination directories
source_dir="/path/to/source"
destination_dir="/path/to/backup"

# Perform backup using rsync
rsync -avz --delete "$source_dir" "$destination_dir"