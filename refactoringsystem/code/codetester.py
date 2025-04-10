import os
import re
import csv
import pytest


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

    def create_structure(self):
        """
        Creates the directory structure: targetdirpath/name{i}/refactored/ and test_refactored/
        where name{i} is dynamically determined like 'gpt1', 'gpt2', etc.
        """
        # Generate the next available name (e.g., 'gpt1', 'gpt2', etc.)
        name_i = self.get_next_available_name()

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
        refactored_filename = os.path.join(refactored_path, f"{self.filename}.py")
        with open(refactored_filename, 'w') as f:
            f.write(self.code)

        # Create a basic test file (this can be extended)
        test_filename = os.path.join(test_refactored_path, f"test_{self.filename}.py")
        test_code = self.testcode
        with open(test_filename, 'w') as f:
            f.write(test_code)


    def run_tests(self):
        """
        Runs pytest on the generated test files and saves the result to a CSV file.
        """
        test_dir = os.path.join(self.target_dir_path, f"{self.name_prefix}{self.counter - 1}/test_refactored")
        
        # Run pytest on the test files in the test_refactored directory
        pytest_args = [test_dir]
        result = pytest.main(pytest_args)

        # Convert the pytest result to a CSV format
        self.save_results_to_csv(result)

    #TODO could use a strategy to save to different formats
    def save_results_to_csv(self, result):
        """
        Saves pytest results to a CSV file.
        """
        test_results = []
        for item in result:
            test_results.append({
                'test': item.nodeid,
                'outcome': item.outcome,
                'duration': item.duration,
            })
        
        csv_filename = os.path.join(self.target_dir_path, f"{self.name_prefix}{self.counter - 1}_test_results.csv")
        with open(csv_filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["test", "outcome", "duration"])
            writer.writeheader()
            writer.writerows(test_results)