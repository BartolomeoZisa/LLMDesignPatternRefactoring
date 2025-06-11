import os
import csv
import json
import pandas as pd

RESULTS_DIR = "../results"
OUTPUT_DIR = "../report/report.csv"

example_types = {
    "roundhole": "standard",
    "gridmovement": "custom",
    "calculator": "custom",
    "icecream": "custom",
    "cafecito": "custom",
    "sword": "standard",
    "stall": "custom",
    "traffic_light": "custom",
    "elevator": "standard",
    "validator": "standard",
    "graphtraversal": "custom",
    "vector": "custom",
    "monster": "custom",
    "wand": "custom",
    "car": "standard"
}


def load_code_review(path):
    """Load code_review.csv into a dictionary: {filename -> 'yes'/'no'/'flawed'}"""
    review_map = {}
    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            filename = os.path.basename(row["file"])
            value = row["applies_pattern"].strip().lower()
            if value in {"yes", "no", "flawed"}:
                review_map[filename] = value
            else:
                review_map[filename] = "unknown"
    return review_map

def all_tests_passed(test_result_path):
    """Return True if all tests passed, False if any failed, None if unreadable."""
    try:
        with open(test_result_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)
            if not rows:
                return None
            return all(row["outcome"].lower() == "passed" for row in rows)
    except Exception as e:
        print(f"Error reading {test_result_path}: {e}")
        return None

def parse_json_metadata(json_path):
    """Extract metadata from parameters.json."""
    with open(json_path) as f:
        data = json.load(f)

    code_file = os.path.basename(data.get("code_path", ""))
    base_name = os.path.splitext(code_file)[0].lower()

    return {
        "pattern_name": data.get("pattern_name", "Unknown"),
        "code_file": code_file,
        "model_name": data.get("model_name", "Unknown"),
        "timestamp": data.get("timestamp", ""),
        "type": example_types.get(base_name, "unknown")
    }


def generate_summary(json_path, test_csv_path, code_review_path, output_path):
    review_data = load_code_review(code_review_path)
    meta = parse_json_metadata(json_path)
    test_result = all_tests_passed(test_csv_path)

    applies_pattern_status = review_data.get(meta["code_file"], "unknown")

    row = {
        "Pattern": meta["pattern_name"].capitalize(),
        "Example File": meta["code_file"],
        "Standard/Custom": meta["type"],
        "Iteration": None,
        "All Tests Passed": "Yes" if test_result else "No",
        "Applies Design Pattern": applies_pattern_status.capitalize(),
        "Model Name": meta["model_name"],
        "Timestamp": meta["timestamp"]
    }

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    # Append to CSV
    df = pd.DataFrame([row])
    if not os.path.exists(output_path):
        df.to_csv(output_path, index=False)
    else:
        df.to_csv(output_path, mode="a", header=False, index=False)

    #print(f"Added {meta['code_file']} @ {meta['timestamp']} to {output_path}")

def sort_and_reassign_iterations(csv_path=OUTPUT_DIR):
    """Sort CSV by example file and timestamp, and reassign iteration numbers."""
    df = pd.read_csv(csv_path)

    # Sort by 'Example File' and 'Timestamp'
    df.sort_values(by=["Pattern","Example File", "Timestamp"], inplace=True)

    # Reassign Iteration numbers within each Example File group
    df["Iteration"] = df.groupby("Example File").cumcount() + 1

    # Reorder columns
    cols = ["Pattern", "Example File", "Standard/Custom", "Iteration",
            "All Tests Passed", "Applies Design Pattern", "Model Name", "Timestamp"]
    df = df[cols]

    df.to_csv(csv_path, index=False)
    print(f"Sorted and updated iterations in {csv_path}")

# Example batch processor (edit paths as needed)
def process_all_iterations(base_dir, output_path=OUTPUT_DIR):
    """
    Automatically detect and process all iterations under base_dir.
    Each iteration should contain:
    - parameters.json
    - *_test_results.csv
    - code_review.csv
    """

    if os.path.exists(output_path):
        os.remove(output_path)

    for root, dirs, files in os.walk(base_dir):
        if root.endswith("__"):
            continue
        if root.endswith("refactored"):
            continue
        result_csv = next((f for f in files if f.endswith("_test_results.csv")), None)
        json_file = next((f for f in files if f == "parameters.json"), None)
        review_file = next((f for f in files if f == "code_review.csv"), None)

        if result_csv and json_file and review_file:
            json_path = os.path.join(root, json_file)
            test_csv_path = os.path.join(root, result_csv)
            review_path = os.path.join(root, review_file)
            generate_summary(json_path, test_csv_path, review_path, output_path)

    if not os.path.exists(output_path):
        print(f"No valid iterations found in {base_dir}.")
        return

    sort_and_reassign_iterations(output_path)


if __name__ == "__main__":
    process_all_iterations(RESULTS_DIR)