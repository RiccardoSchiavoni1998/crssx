import shutil
import json
import os

def copy_json_file(source_file, destination_file):
    try:
        path = os.path.dirname(os.path.abspath(__file__)) + r"\optimization\results_opt"
        print(path)
        source_file = os.path.join(path, source_file)
        destination_file = os.path.join(path, destination_file)

        # Check if the destination file already exists
        if os.path.exists(destination_file):
            print(f"File '{destination_file}' already exists. Overwriting...")

        # Read the content of the JSON file
        with open(source_file, 'r') as file:
            json_data = json.load(file)

        # Create a copy of the content
        copied_data = json_data

        # Save the copy as a new JSON file, overwriting the existing file if it exists
        with open(destination_file, 'w') as file:
            json.dump(copied_data, file, indent=4)

        print(f"JSON file '{source_file}' copied to '{destination_file}' successfully.")

    except FileNotFoundError:
        print("File not found.")

    except json.decoder.JSONDecodeError:
        print("Error decoding the JSON file.")

# Example usage
source_file = 'stern_results.json'
destination_file = 'results_0.json'

copy_json_file(source_file, destination_file)