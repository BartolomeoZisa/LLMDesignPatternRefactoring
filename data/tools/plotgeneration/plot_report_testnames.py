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
                    
                    simple_names = df['test'].apply(lambda x: x.split("::")[-1]).unique()

                    # 2) build a raw‐to‐tests mapping to find collisions
                    raw2tests = defaultdict(list)
                    for name in simple_names:
                        stripped = name.replace("test_", "", 1)
                        raw = ''.join(w[0].upper() for w in stripped.split('_'))
                        raw2tests[raw].append(name)

                    # 3) build your final mapping: original full simple_name -> unique acronym
                    acronyms = {}
                    for raw, tests in raw2tests.items():
                        if len(tests) == 1:
                            # no collision
                            acronyms[tests[0]] = f"{raw}"
                        else:
                            # collision: suffix _1, _2, ... 
                            for idx, name in enumerate(tests, start=1):
                                acronyms[name] = f"{raw}_{idx}"

                    # 4) now aggregate
                    for _, row in df.iterrows():
                        simple = row['test'].split("::")[-1]
                        key = acronyms.get(simple, f"UNKN")
                        outcome = row['outcome']
                        if outcome in ('passed', 'failed'):
                            result[parent_folder_name][patternexample]['tests'][key][outcome] += 1

                except Exception as e:
                    print(f"Error reading {csv_path}: {e}")

    return result



def plot_stacked_test_results(results_dict, parent_folder_name, save_plots=False, save_dir="../../report/test_plots"):
    for patternexample, data in results_dict.items():
        tests = data['tests']
        errors = data['errors']

        test_names = list(tests.keys())
        passed_counts = [tests[t]['passed'] for t in test_names]
        failed_counts = [tests[t]['failed'] for t in test_names]
        error_counts = [errors] * len(test_names)

        bottom_failed = passed_counts
        bottom_error = [p + f for p, f in zip(passed_counts, failed_counts)]

        # === Fixed layout for 15 test slots ===
        total_slots = 15
        x_positions = [i * (total_slots / len(test_names)) for i in range(len(test_names))]
        bar_width = 0.6
        fig_width = 10  # fixed figure width as if for 15 bars

        plt.figure(figsize=(fig_width, 6))
        plt.bar(x_positions, passed_counts, label='Passed', color='mediumseagreen', width=bar_width)
        plt.bar(x_positions, failed_counts, bottom=bottom_failed, label='Failed', color='lightcoral', width=bar_width)
        plt.bar(x_positions, error_counts, bottom=bottom_error, label='Errors', color='gray', alpha=0.5, width=bar_width)

        max_y = max([p + f + e for p, f, e in zip(passed_counts, failed_counts, error_counts)])
        plt.ylim(0, max_y)

        plt.ylabel("Test Runs", fontsize=20)
        plt.xticks(x_positions, test_names, rotation=45, ha='right', fontsize=16)
        plt.yticks(fontsize=16)
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


def plot_stacked_test_results_horizontal(results_dict, parent_folder_name, save_plots=False, save_dir="../../report/test_plots"):
    for patternexample, data in results_dict.items():
        tests = data['tests']
        errors = data['errors']

        test_names = list(tests.keys())
        passed_counts = [tests[t]['passed'] for t in test_names]
        failed_counts = [tests[t]['failed'] for t in test_names]
        error_counts = [errors] * len(test_names)

        fig_height = max(8, 0.5 * len(test_names))
        plt.figure(figsize=(14, fig_height))

        y_pos = range(len(test_names))

        plt.barh(y_pos, passed_counts, label='Passed', color='mediumseagreen', height=0.6)
        plt.barh(y_pos, failed_counts, left=passed_counts, label='Failed', color='lightcoral', height=0.6)
        plt.barh(y_pos, error_counts, left=[p + f for p, f in zip(passed_counts, failed_counts)], label='Errors', color='gray', alpha=0.5, height=0.6)

        plt.yticks(y_pos, test_names, fontsize=18)
        plt.xlabel("Number of Test Runs", fontsize=22, fontweight='bold', labelpad=15)  # space below xlabel
        plt.title(f"Test results for pattern example: {patternexample}", fontsize=26, fontweight='bold', pad=25)  # space above title

        plt.legend(loc='center left', bbox_to_anchor=(1.02, 0.5), fontsize=18, borderaxespad=0)

        max_total = max([p + f + e for p, f, e in zip(passed_counts, failed_counts, error_counts)])
        plt.xlim(0, max_total + 2)  # padding on right side

        plt.subplots_adjust(left=0.3)  # space on left for y labels
        plt.tight_layout()

        if save_plots:
            output_folder = os.path.join(save_dir, parent_folder_name)
            os.makedirs(output_folder, exist_ok=True)
            output_path = os.path.join(output_folder, f"{patternexample}.png")
            plt.savefig(output_path, bbox_inches='tight')  # bbox_inches to fit legend
            plt.close()
            print(f"Saved plot to {output_path}")
        else:
            plt.show()



if __name__ == "__main__":
    results = gather_full_test_results(BASEDIR)
    plot_stacked_test_results(results[PARENTFOLDER], PARENTFOLDER, save_plots=True)

    




