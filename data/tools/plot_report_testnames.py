from collections import defaultdict
import os
import pandas as pd
import matplotlib.pyplot as plt
import json
import sys

BASEDIR = "../results/"

PARENTFOLDER = sys.argv[1] if len(sys.argv) > 1 else "geminiflash2.5_1"   # This is the name of the parent folder you want to use for grouping results.
#gpt4o-mini

def gather_full_test_results(base_dir=BASEDIR):
    # Structure: { parentfoldername: { patternexample: { 'tests': { test_name: {passed, failed} }, 'errors': int } } }
    result = defaultdict(lambda: defaultdict(lambda: {'tests': defaultdict(lambda: {'passed': 0, 'failed': 0}), 'errors': 0}))

    # Get the parent folder name based on the provided base_dir.
    # This will be the name of the directory specified in BASEDIR.

    for root, dirs, files in os.walk(base_dir):
        for filename in files:
            parent_folder_name = os.path.basename(os.path.dirname(root))
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
                        result[parent_folder_name][patternexample]['errors'] += 1
                        continue

                    if 'test' in df.columns and 'outcome' in df.columns:
                        for _, row in df.iterrows():
                            test_name = row['test'].split("::")[-1]
                            outcome = row['outcome']
                            if outcome in ['passed', 'failed']:
                                result[parent_folder_name][patternexample]['tests'][test_name][outcome] += 1
                except Exception as e:
                    print(f"Error reading {csv_path}: {e}")

    return result



def plot_stacked_test_results(results_dict, parent_folder_name, save_plots=False, save_dir="../report/test_plots"):
    for patternexample, data in results_dict.items():
        tests = data['tests']
        errors = data['errors']

        test_names = list(tests.keys())
        passed_counts = [tests[t]['passed'] for t in test_names]
        failed_counts = [tests[t]['failed'] for t in test_names]
        error_counts = [errors] * len(test_names)

        bottom_failed = passed_counts
        bottom_error = [p + f for p, f in zip(passed_counts, failed_counts)]

        fig_width = max(10, 0.75 * len(test_names))  # dynamic width
        plt.figure(figsize=(fig_width, 6))
        plt.bar(test_names, passed_counts, label='Passed', color='mediumseagreen', width=0.6)
        plt.bar(test_names, failed_counts, bottom=bottom_failed, label='Failed', color='lightcoral', width=0.6)
        plt.bar(test_names, error_counts, bottom=bottom_error, label='Errors', color='gray', alpha=0.5, width=0.6)

        max_y = max([p + f + e for p, f, e in zip(passed_counts, failed_counts, error_counts)])
        plt.ylim(0, max_y + 2)

        plt.xlabel("Test Name", fontsize=12)
        plt.ylabel("Number of Test Runs", fontsize=12)
        plt.title(f"Test results for pattern example: {patternexample}", fontsize=14)
        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.yticks(fontsize=10)
        plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
        plt.tight_layout()


        if save_plots:
            output_folder = os.path.join(save_dir, parent_folder_name)
            os.makedirs(output_folder, exist_ok=True)
            output_path = os.path.join(output_folder, f"{patternexample}.png")
            plt.savefig(output_path)
            plt.close()
            print(f"Saved plot to {output_path}")
        else:
            plt.show()



if __name__ == "__main__":
    results = gather_full_test_results(BASEDIR)
    plot_stacked_test_results(results[PARENTFOLDER], PARENTFOLDER, save_plots=True)

    




