import os
import difflib

def compare_file_contents(file1, file2):
    with open(file1, 'r', encoding='utf-8', errors='replace') as f1, \
         open(file2, 'r', encoding='utf-8', errors='replace') as f2:
        text1 = f1.read()
        text2 = f2.read()
    seq = difflib.SequenceMatcher(None, text1, text2)
    return round((1 - seq.ratio()) * 100, 2)


def get_all_files(folder_path):
    files = {}
    for root, _, filenames in os.walk(folder_path):
        for f in filenames:
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, folder_path)
            files[rel_path] = full_path
    return files

def compare_tests_in_all_dirs(root_dir):
    for subdir, dirs, _ in os.walk(root_dir):
        if "base_folder" in dirs and "refactored_folder" in dirs:
            base_test_dir = os.path.join(subdir, "base_folder", "test")
            refactored_test_dir = os.path.join(subdir, "refactored_folder", "test_refactored")

            if os.path.isdir(base_test_dir) and os.path.isdir(refactored_test_dir):
                print(f"\n Comparing in: {subdir}")
                base_files = get_all_files(base_test_dir)
                refactored_files = get_all_files(refactored_test_dir)

                common_files = set(base_files) & set(refactored_files)
                
                #remove all starting with __
                common_files = {f for f in common_files if not f.startswith('__')}

                if not common_files:
                    print("  No matching test files found.")
                    continue

                for rel_path in sorted(common_files):
                    base_file = base_files[rel_path]
                    refactored_file = refactored_files[rel_path]
                    diff = compare_file_contents(base_file, refactored_file)
                    print(f"  {rel_path}: {diff}% different")

# Example usage:
# compare_tests_in_all_dirs("/path/to/root_dir")
compare_tests_in_all_dirs("../../data")
