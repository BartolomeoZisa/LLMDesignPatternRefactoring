import subprocess
import os
import sys
from explore import explore_folder_for_triples
import config

def main():
    matches = explore_folder_for_triples(config.PROJECT_ROOT)
    print(f"Found {len(matches)} matches:")

    for i, (base_files, refactored_tests, pattern_name, parentfolder) in enumerate(matches):
        print(f"\nMatch #{i+1}")
        print("Base files:")
        for f in base_files:
            print(f"  {f}")
        print("Test files:")
        for f in refactored_tests:
            print(f"  {f}")
        print(f"Pattern name: {pattern_name}")
        print(f"Folder: {parentfolder}")

        if config.ASKSKIP:
            user_input = input("Do you want to skip this pattern? (y/n): ").strip().lower()
            if user_input == 'y':
                print("Skipping this pattern.")
                continue
            elif user_input != 'n':
                print("Invalid input. Please enter 'y' or 'n'.")
                continue

        base_files = [f for f in base_files if "__init__.py" not in f]
        refactored_tests = [f for f in refactored_tests if "__init__.py" not in f]

        code_path = base_files[0]
        test_path = refactored_tests[0]
        pattern = pattern_name[0]

        # Call RefactorFrontEnd
        refactor_cmd = [
            sys.executable, "refactor_frontend.py",  # Adjust if file is named differently
            code_path,
            test_path,
            pattern,
            config.PROMPTFILE,
            config.SAVEFOLDERPATH,
            "--temperature", str(config.TEMPERATURE),
            "--model_name", config.MODEL_NAME,
            "--max_length", str(config.MAX_LENGTH),
            "--strategy", config.STRATEGY
        ]

        try:
            print("[INFO] Running refactor step...")
            result = subprocess.run(refactor_cmd, capture_output=True, text=True, check=True)
            refactored_file_path = result.stdout.strip().splitlines()[-1]  # last line = path
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Refactor step failed:\n{e.stderr}")
            continue

        # Construct path to test file (already known)
        refactored_test_path = test_path

        # Call TesterFrontEnd
        tester_cmd = [
            sys.executable, "tester_frontend.py",  # Adjust if file is named differently
            refactored_file_path,
            refactored_test_path
        ]

        try:
            print("[INFO] Running test step...")
            subprocess.run(tester_cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Test step failed:\n{e.stderr}")
            continue

        print("\nDone with this pattern.\nYou can enter another refactored version or type 'SKIP' to move to the next pattern.")

if __name__ == "__main__":
    main()

        
        