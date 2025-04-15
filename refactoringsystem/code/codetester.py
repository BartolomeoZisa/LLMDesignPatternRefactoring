import os
import re
import csv
import json
import pytest
import sys
import subprocess


class CodeTester:
    

    def __init__(self, code: str, testcode: str, filename: str, target_dir_path: str, name_prefix: str):
        """
        Initializes the CodeTester instance.

        :param code: The Python code to be refactored and tested.
        :param testcode: The test code to be used for testing the refactored code.
        :param filename: The filename for the refactored Python code, should be the same the one used in the test code.
        :param target_dir_path: The path where the directory structure should be created.
        :param name_prefix: The prefix to be used for naming the directories (e.g., 'gpt', 'claude').
        """
        self.code = code
        self.testcode = testcode
        self.filename = filename
        self.target_dir_path = target_dir_path
        self.name_prefix = name_prefix

    def get_next_available_name(self):
        """
        Checks the current directories in the target_dir_path to find the next available name like 'gpt1', 'gpt2', etc.
        """
        #if the target_dir_path doesn't exist, create it
        if not os.path.exists(self.target_dir_path):
            os.makedirs(self.target_dir_path)

        # List all directories in the target path
        existing_dirs = os.listdir(self.target_dir_path)

        # Pattern to match directories like 'gpt1', 'gpt2', etc.
        pattern = re.compile(rf"^{self.name_prefix}(\d+)$")
        
        # Extract numbers from matching directories
        existing_numbers = []
        for dir_name in existing_dirs:
            match = pattern.match(dir_name)
            if match:
                existing_numbers.append(int(match.group(1)))
        
        # If no directories exist, return the first available name
        if not existing_numbers:
            return f"{self.name_prefix}1"
        
        # Return the next available number (i.e., max(existing_numbers) + 1)
        next_number = max(existing_numbers) + 1
        return f"{self.name_prefix}{next_number}"
    
    #TODO: shouldn't use set_next_avaible_name

    def set_next_available_name(self):
        """
        Sets the next available name for the directory based on the existing directories in target_dir_path.
        """
        self.name = self.get_next_available_name()

    def create_structure(self):
        """
        Creates the directory structure: targetdirpath/name{i}/refactored/ and test_refactored/
        where name{i} is dynamically determined like 'gpt1', 'gpt2', etc.
        """
        # Generate the next available name (e.g., 'gpt1', 'gpt2', etc.)
        name_i = self.name

        base_path = os.path.join(self.target_dir_path, name_i)
        
        # Create the main directories
        refactored_path = os.path.join(base_path, "refactored")
        test_refactored_path = os.path.join(base_path, "test_refactored")
        
        # Ensure the directories are created
        os.makedirs(refactored_path, exist_ok=True)
        os.makedirs(test_refactored_path, exist_ok=True)
        
        # Create init.py files to mark directories as Python packages
        with open(os.path.join(refactored_path, "__init__.py"), 'w') as f:
            pass  # Empty __init__.py
        with open(os.path.join(test_refactored_path, "__init__.py"), 'w') as f:
            pass  # Empty __init__.py

        # Write the refactored code to filename.py in the refactored directory
        refactored_filename = os.path.join(refactored_path, f"{self.filename}")
        with open(refactored_filename, 'w') as f:
            f.write(self.code)

        # Create a basic test file (this can be extended)
        test_filename = os.path.join(test_refactored_path, f"test_{self.name}_{self.filename}")
        test_code = self.testcode
        with open(test_filename, 'w') as f:
            f.write(test_code)

    def run_tests(self):
        name_i = self.name
        test_dir = os.path.join(self.target_dir_path, name_i, "test_refactored")
        report_path = os.path.join(self.target_dir_path, name_i, f"{name_i}_report.json")

        curr_dir = os.getcwd() 
        #print(f"Running tests in {test_dir} and saving report to {report_path}, from {curr_dir}")

        # Build the command to run pytest via subprocess
        pytest_cmd = [
            sys.executable, "-m", "pytest",
            test_dir,
            "--json-report",
            f"--json-report-file={report_path}",
            "--import-mode=importlib",
        ]

        # Save original sys.path and set up environment
        save_path = sys.path.copy()
        parent_dir = os.path.dirname(test_dir)
        sys.path.insert(0, parent_dir)
        
        # Copy current environment and add PYTHONPATH
        env = os.environ.copy()
        env["PYTHONPATH"] = parent_dir + os.pathsep + env.get("PYTHONPATH", "")
        
        #print(f"Using PYTHONPATH: {env['PYTHONPATH']}")
        print(f"Running command: {' '.join(pytest_cmd)}")

        try:
            result = subprocess.run(pytest_cmd, env=env, capture_output=True, text=True)
            print("Test run output:\n", result.stdout)
            if result.stderr:
                print("Test run errors:\n", result.stderr)
        except Exception as e:
            print(f"Error running tests: {e}")
        finally:
            sys.path = save_path.copy()

        #print(f"Restored sys.path: {sys.path}")
        self.save_results_to_csv(report_path, name_i)


    def save_results_to_csv(self, report_path, name_i):
        try:
            with open(report_path, 'r') as f:
                report = json.load(f)

            test_results = []
            for test in report.get("tests", []):
                test_results.append({
                    'test': test.get("nodeid", ""),
                    'outcome': test.get("outcome", ""),
                    'duration': test.get("duration", 0),
                })

            csv_filename = os.path.join(self.target_dir_path, name_i, f"{name_i}_test_results.csv")
            with open(csv_filename, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=["test", "outcome", "duration"])
                writer.writeheader()
                writer.writerows(test_results)

        except Exception as e:
            print(f"Error saving results to CSV: {e}")
