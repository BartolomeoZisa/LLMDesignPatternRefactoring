import os
import csv
import json
import pytest
import sys
import subprocess


class CodeTester:
    def __init__(self, code_path: str, test_code_path: str, test_dir_path: str):
        """
        Initializes the CodeTester instance.

        :param code_path: The path to the Python code to be refactored and tested.
        :param test_code_path: The path to the test code to be used for testing the refactored code.
        :param test_dir_path: The path where the directory, which contains various executions and the test, will be created.
        """
        self.code_path = code_path
        self.test_code_path = test_code_path
        self.test_dir_path = test_dir_path  # Combined path for target directory and test directory

        #FILENAME SEEMS USELESS
     
    def create_test_directory(self):
        """
        Creates a directory structure for the test files.
        """
        # Create the directory structure
        test_dir = os.path.join(self.test_dir_path, "test_refactored")
        os.makedirs(test_dir, exist_ok=True)

        # Save the test code
        test_code_file = os.path.join(test_dir, os.path.basename(self.test_code_path))
        with open(test_code_file, 'w') as f:
            with open(self.test_code_path, 'r') as test_file:
                test_code = test_file.read()
                f.write(test_code)
        
        # Add __init__.py to the test directory
        init_file = os.path.join(test_dir, "__init__.py")
        with open(init_file, 'w') as f:
            pass

    def run_tests(self):
        test_dir = os.path.join(self.test_dir_path, "test_refactored")
        report_path = os.path.join(self.test_dir_path, f"{os.path.basename(self.test_dir_path)}_report.json")

        curr_dir = os.getcwd()
        # print(f"Running tests in {test_dir} and saving report to {report_path}, from {curr_dir}")

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

        # print(f"Using PYTHONPATH: {env['PYTHONPATH']}")
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

        # print(f"Restored sys.path: {sys.path}")
        self.save_results_to_csv(report_path)

    def save_results_to_csv(self, report_path):
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

            csv_filename = os.path.join(self.test_dir_path, f"{os.path.basename(self.test_dir_path)}_test_results.csv")
            with open(csv_filename, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=["test", "outcome", "duration"])
                writer.writeheader()
                writer.writerows(test_results)

        except Exception as e:
            print(f"Error saving results to CSV: {e}")

