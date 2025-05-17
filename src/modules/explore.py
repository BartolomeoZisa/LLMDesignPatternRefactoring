import os
from typing import List, Tuple

def explore_folder_for_triples(root_path: str) -> List[Tuple[List[str], List[str], List[str], str]]:
    """
    Recursively explores folders and returns tuples of:
    - List of base_folder/base/*.py files
    - List of refactored_folder/test_refactored/*.py files
    - List of strings from pattern.txt (one string per line)
    - The root folder where the triple was found
    """
    results = []

    for dirpath, dirnames, filenames in os.walk(root_path):
        if "base_folder" in dirnames and "refactored_folder" in dirnames and "pattern.txt" in filenames:
            base_py_path = os.path.join(dirpath, "base_folder", "base")
            refactored_py_path = os.path.join(dirpath, "refactored_folder", "test_refactored")
            pattern_path = os.path.join(dirpath, "pattern.txt")

            if os.path.isdir(base_py_path) and os.path.isdir(refactored_py_path):
                base_files = [
                    os.path.join(base_py_path, f)
                    for f in os.listdir(base_py_path)
                    if f.endswith(".py") and os.path.isfile(os.path.join(base_py_path, f))
                ]

                refactored_tests = [
                    os.path.join(refactored_py_path, f)
                    for f in os.listdir(refactored_py_path)
                    if f.endswith(".py") and os.path.isfile(os.path.join(refactored_py_path, f))
                ]

                if base_files and refactored_tests:
                    with open(pattern_path, 'r') as pattern_file:
                        pattern_lines = [line.strip() for line in pattern_file.readlines()]  # Read each line and strip extra whitespace
                    
                    results.append((base_files, refactored_tests, pattern_lines, dirpath))

    return results



