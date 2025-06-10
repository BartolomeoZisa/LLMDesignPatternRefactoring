import os
import json

def ask_example_type(folder_path):
    while True:
        choice = input(f"Folder '{folder_path}' contains 'pattern.txt'. Choose example_type (custom/standard): ").strip().lower()
        if choice in {"custom", "standard"}:
            return choice
        print("Invalid choice. Please type 'custom' or 'standard'.")

def update_info_json(folder_path, example_type):
    info_path = os.path.join(folder_path, "info.json")
    info = {}

    if os.path.exists(info_path):
        with open(info_path, "r") as f:
            try:
                info = json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: 'info.json' in {folder_path} is invalid JSON. Overwriting.")

    info["example_type"] = example_type

    with open(info_path, "w") as f:
        json.dump(info, f, indent=2)
        print(f"Updated 'info.json' in {folder_path}.")

def process_directory(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if "pattern.txt" in filenames:
            example_type = ask_example_type(dirpath)
            update_info_json(dirpath, example_type)

if __name__ == "__main__":
    root = input("Enter the root directory to search: ").strip()
    if os.path.isdir(root):
        process_directory(root)
    else:
        print("Provided path is not a valid directory.")
