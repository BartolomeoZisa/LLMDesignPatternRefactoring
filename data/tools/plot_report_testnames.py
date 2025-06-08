from collections import defaultdict
import os
import pandas as pd
import matplotlib.pyplot as plt
import json

BASEDIR = "../results/"


def gather_full_test_results(base_dir="results"):
    # Structure: { patternexample: { 'tests': { test_name: {passed, failed} }, 'errors': int } }
    result = defaultdict(lambda: {'tests': defaultdict(lambda: {'passed': 0, 'failed': 0}), 'errors': 0})

    for root, dirs, files in os.walk(base_dir):
        for filename in files:
            if filename.endswith("test_results.csv"):
                csv_path = os.path.join(root, filename)
                
                # Locate parameters.json in the same directory or a parent directory
                params_path = os.path.join(root, "parameters.json")
                patternexample = None

                if os.path.isfile(params_path):
                    try:
                        with open(params_path, 'r') as f:
                            params = json.load(f)
                        code_path = params.get("code_path", "")
                        patternexample = os.path.splitext(os.path.basename(code_path))[0]
                    except Exception as e:
                        print(f"Error reading parameters.json at {params_path}: {e}")

                if patternexample is None:
                    print(f"Warning: Could not determine patternexample for {csv_path}")
                    continue

                try:
                    df = pd.read_csv(csv_path)
                    
                    if df.empty:
                        print(f"Empty CSV treated as error: {csv_path}")
                        result[patternexample]['errors'] += 1
                        continue

                    if 'test' in df.columns and 'outcome' in df.columns:
                        for _, row in df.iterrows():
                            test_name = row['test'].split("::")[-1]
                            outcome = row['outcome']
                            if outcome in ['passed', 'failed']:
                                result[patternexample]['tests'][test_name][outcome] += 1
                except Exception as e:
                    print(f"Error reading {csv_path}: {e}")

    return result


def plot_stacked_test_results(results_dict):
    for patternexample, data in results_dict.items():
        tests = data['tests']
        errors = data['errors']

        test_names = list(tests.keys())
        passed_counts = [tests[t]['passed'] for t in test_names]
        failed_counts = [tests[t]['failed'] for t in test_names]
        error_counts = [errors] * len(test_names)  # add all errors on top of every bar

        # Compute bottoms for stacking
        bottom_failed = passed_counts
        bottom_error = [p + f for p, f in zip(passed_counts, failed_counts)]

        plt.figure(figsize=(10, 5))
        plt.bar(test_names, passed_counts, label='Passed', color='mediumseagreen')
        plt.bar(test_names, failed_counts, bottom=bottom_failed, label='Failed', color='lightcoral')
        plt.bar(test_names, error_counts, bottom=bottom_error, label='Errors', color='gray', alpha=0.5)

        plt.xlabel("Test Name")
        plt.ylabel("Number of Test Runs")
        plt.title(f"Test Results for Pattern Example: {patternexample}")
        plt.xticks(rotation=45, ha='right')
        plt.legend()
        plt.tight_layout()
        plt.show()



if __name__ == "__main__":
    
    results = gather_full_test_results(BASEDIR)
    plot_stacked_test_results(results)



