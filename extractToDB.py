import sys
import re
import sqlite3

def extract_info(input_file):
    db_file = f"{input_file}_info.db"

    # Check if the file exists
    try:
        with open(input_file) as file:
            file_content = file.read()
    except FileNotFoundError:
        print("File does not exist.")
        return

    # Get the file type
    file_type = file_content.strip().split("\n", 1)[0]

    # Extract email addresses using regex
    email_addresses = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', file_content)
    email_count = {}
    unique_emails = []
    for email in email_addresses:
        if email not in email_count:
            email_count[email] = 1
            unique_emails.append(email)
        else:
            email_count[email] += 1

    # Extract URLs using regex
    urls = re.findall(r'https?://[^ \n]+', file_content)
    url_count = {}
    unique_urls = []
    for url in urls:
        if url not in url_count:
            url_count[url] = 1
            unique_urls.append(url)
        else:
            url_count[url] += 1

    # Extract full names using regex
    full_names = re.findall(r'[A-Z][a-z]+ [A-Z][a-z]+', file_content)
    full_name_count = {}
    unique_full_names = []
    for name in full_names:
        if name not in full_name_count:
            full_name_count[name] = 1
            unique_full_names.append(name)
        else:
            full_name_count[name] += 1

    # Extract phone numbers using regex
    phone_numbers = re.findall(r'\b[0-9]{3}-[0-9]{3}-[0-9]{4}\b', file_content)
    phone_number_count = {}
    unique_phone_numbers = []
    for number in phone_numbers:
        if number not in phone_number_count:
            phone_number_count[number] = 1
            unique_phone_numbers.append(number)
        else:
            phone_number_count[number] += 1

    # Extract street addresses using regex
    street_addresses = re.findall(r'[0-9]+ [A-Za-z]+ [A-Za-z]+, [A-Za-z]+ [0-9]{5}', file_content)
    street_address_count = {}
    unique_street_addresses = []
    for address in street_addresses:
        if address not in street_address_count:
            street_address_count[address] = 1
            unique_street_addresses.append(address)
        else:
            street_address_count[address] += 1

    # Connect to SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create table for email addresses
    cursor.execute('''CREATE TABLE IF NOT EXISTS email_addresses
                    (email TEXT PRIMARY KEY, count INTEGER)''')
    # Insert email data into table
    for email in unique_emails:
        count = email_count[email]
        cursor.execute('INSERT INTO email_addresses VALUES (?, ?)', (email, count))

    # Create table for URLs
    cursor.execute('''CREATE TABLE IF NOT EXISTS urls
                    (url TEXT PRIMARY KEY, count INTEGER)''')
    # Insert URL data into table
    for url in unique_urls:
        count = url_count[url]
        cursor.execute('INSERT INTO urls VALUES (?, ?)', (url, count))

    # Create table for full names
    cursor.execute('''CREATE TABLE IF NOT EXISTS full_names
                    (name TEXT PRIMARY KEY, count INTEGER)''')
    # Insert full name data into table
    for name in unique_full_names:
        count = full_name_count[name]
        cursor.execute('INSERT INTO full_names VALUES (?, ?)', (name, count))

    # Create table for phone numbers
    cursor.execute('''CREATE TABLE IF NOT EXISTS phone_numbers
                    (number TEXT PRIMARY KEY, count INTEGER)''')
    # Insert phone number data into table
    for number in unique_phone_numbers:
        count = phone_number_count[number]
        cursor.execute('INSERT INTO phone_numbers VALUES (?, ?)', (number, count))

    # Create table for street addresses
    cursor.execute('''CREATE TABLE IF NOT EXISTS street_addresses
                    (address TEXT PRIMARY KEY, count INTEGER)''')
    # Insert street address data into table
    for address in unique_street_addresses:
        count = street_address_count[address]
        cursor.execute('INSERT INTO street_addresses VALUES (?, ?)', (address, count))

    # Commit changes and close the connection
    conn.commit()
    conn.close()

    print("Extraction completed.")