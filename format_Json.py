import sys
import json

def correct_and_pretty_print_json(json_string):
    try:
        json_data = json.loads(json_string)
        corrected_json = json.dumps(json_data, indent=4, sort_keys=True)
        print(corrected_json)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}")

        # Extract the valid part of the JSON
        valid_json = json_string[:e.pos]
        try:
            json_data = json.loads(valid_json)
            corrected_json = json.dumps(json_data, indent=4, sort_keys=True)
            print(f"Valid JSON portion:\n{corrected_json}")
        except json.JSONDecodeError as e:
            print(f"Unable to correct JSON: {e}")

# Usage example
if len(sys.argv) != 2:
    print("Usage: python script.py <json_file>")
    sys.exit(1)

json_file = sys.argv[1]

try:
    with open(json_file) as f:
        json_string = f.read()
except FileNotFoundError:
    print(f"File not found: {json_file}")
    sys.exit(1)

correct_and_pretty_print_json(json_string)