

#look for folders that contain *_test_results.csv that are empty or have outcome failed

import os
import csv
import shutil

def find_failed_test_folders(base_path):
    folders = []
    print(f"Searching folders under: {base_path}")
    for root, dirs, files in os.walk(base_path):
        result_files = [f for f in files if f.endswith("_test_results.csv")]
        if not result_files:
            continue
        test_report = os.path.join(root, result_files[0])
        
        if not os.path.exists(test_report):
            continue
        
        try:
            with open(test_report, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                rows = list(reader)
                if not rows or any(row["outcome"].lower() == "failed" for row in rows):
                    folders.append({
                        "report": test_report,
                        "parent": root
                    })
        except Exception as e:
            print(f"Error reading {test_report}: {e}")
    
    return folders


def main():
    base_path = "../results"
    failed_folders = find_failed_test_folders(base_path)
    
    if not failed_folders:
        print("No folders with failed tests found.")
        return
    
    for folder in failed_folders:
        print(f"Failed test folder: {folder['parent']}, Report: {folder['report']}")
        # Optionally, you can copy these folders to a specific location
        # shutil.copytree(folder['parent'], f"failed_tests/{os.path.basename(folder['parent'])}")


if __name__ == "__main__":
    main()