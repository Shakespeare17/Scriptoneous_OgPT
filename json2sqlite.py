import sys
import json
import sqlite3

def create_table(cursor, table_name, columns):
    column_list = ', '.join([f"{column} TEXT" for column in columns])
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({column_list})")

def insert_data(cursor, table_name, data):
    placeholders = ', '.join(['?' for _ in data.keys()])
    values = tuple(data.values())
    cursor.execute(f"INSERT INTO {table_name} VALUES ({placeholders})", values)

def convert_json_to_sqlite(json_data, db_name, table_name):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        create_table(cursor, table_name, json_data[0].keys())

        for entry in json_data:
            insert_data(cursor, table_name, entry)

        conn.commit()

def correct_json(json_string):
    try:
        return json.loads(json_string)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}")
        if e.msg == "Expecting property name enclosed in double quotes":
            pos = e.pos
            json_string = json_string[:pos] + '"' + json_string[pos:]
        elif e.msg == "Expecting property name":
            pos = e.pos
            json_string = json_string[:pos] + '"' + json_string[pos:]
            json_string = json_string[:pos+1] + '":' + json_string[pos+1:]
        elif e.msg == "Expecting ':' delimiter":
            pos = e.pos
            json_string = json_string[:pos] + ':' + json_string[pos:]
        elif e.msg == "Expecting ',' delimiter":
            pos = e.pos
            json_string = json_string[:pos] + ',' + json_string[pos:]
        else:
            print("Unable to correct JSON.")
            sys.exit(1)

        print("Attempting to correct JSON...")
        try:
            return json.loads(json_string)
        except json.JSONDecodeError as e:
            print(f"Unable to correct JSON: {e}")
            sys.exit(1)

# Usage example
if len(sys.argv) != 4:
    print("Usage: python script.py <json_file> <db_name> <table_name>")
    sys.exit(1)

json_file = sys.argv[1]
db_name = sys.argv[2]
table_name = sys.argv[3]

try:
    with open(json_file) as f:
        json_string = f.read()
except FileNotFoundError:
    print(f"File not found: {json_file}")
    sys.exit(1)

try:
    json_data = correct_json(json_string)
except json.JSONDecodeError:
    print(f"Unable to parse JSON: {json_file}")
    sys.exit(1)

convert_json_to_sqlite(json_data, db_name, table_name)