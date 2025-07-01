import os
import json
import re

def count_code_and_comment_lines(file_path):
    """
    Count logical code lines and comment lines (single-line + multiline strings).
    Returns a tuple: (code_lines, comment_lines)
    """
    code_lines = 0
    comment_lines = 0
    in_multiline_comment = False

    triple_quote_pattern = re.compile(r"^[ \t]*([\"']{3})")  # Detects triple quotes

    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
        for line in f:
            stripped = line.strip()

            if not stripped:
                continue  # Skip blank lines

            if in_multiline_comment:
                comment_lines += 1
                if re.search(r'([\'"]{3})', stripped):  # End of multiline comment
                    in_multiline_comment = False
                continue

            match = triple_quote_pattern.match(stripped)
            if match:
                if stripped.count(match.group(1)) == 1:  # Only one triple quote: starts multiline
                    in_multiline_comment = True
                    comment_lines += 1
                    continue
                else:
                    # Single-line docstring: '''something'''
                    comment_lines += 1
                    continue

            if stripped.startswith("#"):
                comment_lines += 1
                continue

            code_lines += 1  # Count as logical code line

    return code_lines, comment_lines


def get_code_files(folder):
    """Get all .py files in the refactored folder, excluding test_refactored."""
    code_files = []
    for root, _, files in os.walk(folder):
        if os.path.basename(root) == "test_refactored":
            continue  # skip test_refactored folder
        for f in files:
            if f.endswith(".py"):
                code_files.append(os.path.join(root, f))
    return code_files


def process_all_refactored_dirs(root_dir):
    """
    For each 'refactored' folder in the directory tree, count logical lines of code
    and comment lines. Write both to the corresponding parameters.json.
    """
    for subdir, dirs, _ in os.walk(root_dir):
        if "refactored" in dirs:
            refactored_path = os.path.join(subdir, "refactored")
            code_files = get_code_files(refactored_path)

            total_code_lines = 0
            total_comment_lines = 0

            for f in code_files:
                code, comments = count_code_and_comment_lines(f)
                total_code_lines += code
                total_comment_lines += comments

            param_file = os.path.join(subdir, "parameters.json")

            # Load or initialize parameter data
            if os.path.exists(param_file):
                with open(param_file, 'r', encoding='utf-8') as f:
                    try:
                        data = json.load(f)
                    except json.JSONDecodeError:
                        data = {}
            else:
                data = {}

            # Update both metrics
            data["lines_of_code"] = total_code_lines
            data["comment_lines"] = total_comment_lines

            with open(param_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)

            print(f"Updated {param_file} with lines_of_code = {total_code_lines}, comment_lines = {total_comment_lines}")


# Example usage:
process_all_refactored_dirs("../../data/results")

