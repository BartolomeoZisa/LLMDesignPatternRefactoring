import os
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')  # Use TkAgg backend for matplotlib
import matplotlib.pyplot as plt
from collections import defaultdict
import math

ROOTDIR = "../../examples/"
NAMEDIR = "llm2"  # example: "metrics"

def find_namedir_and_collect_csvs(root_dir, name_dir):
    results = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if os.path.basename(dirpath) == name_dir:
            parent_name = os.path.basename(os.path.dirname(dirpath))

            for sub in os.listdir(dirpath):
                sub_path = os.path.join(dirpath, sub)
                if os.path.isdir(sub_path):
                    combined_df = pd.DataFrame()
                    for file in os.listdir(sub_path):
                        if file.endswith('.csv'):
                            csv_path = os.path.join(sub_path, file)
                            try:
                                df = pd.read_csv(csv_path)
                                combined_df = pd.concat([combined_df, df], ignore_index=True)
                            except Exception as e:
                                print(f"Could not read {csv_path}: {e}")

                    if not combined_df.empty:
                        # e.g., 'icecream.gpt1'
                        key = f"{parent_name}.{sub}"
                        results.append((key, combined_df))
    return results

def plot_histograms(histogram_data):
    grouped = defaultdict(list)
    for name, df in histogram_data:
        parent, sub = name.split('.')
        grouped[parent].append((sub, df))

    for parent_name, sub_dfs in grouped.items():
        num_subs = len(sub_dfs)

        # Automatically determine rows and cols (aim for square-ish layout)
        ncols = min(3, num_subs)  # Limit max cols to 3 for readability
        nrows = math.ceil(num_subs / ncols)

        fig, axes = plt.subplots(nrows, ncols, figsize=(4 * ncols, 3 * nrows), sharey=True)
        axes = axes.flatten() if num_subs > 1 else [axes]

        fig.suptitle(f'Outcome Distribution for {parent_name}', fontsize=16)

        for idx, (sub_name, df) in enumerate(sub_dfs):
            ax = axes[idx]
            if 'outcome' in df.columns:
                outcome_counts = df['outcome'].value_counts()
                colors = outcome_counts.index.map(lambda x: 'green' if x.lower() == 'passed' else 'red')
                outcome_counts.plot(kind='bar', color=colors, ax=ax)
                ax.set_title(f'{sub_name}')
                ax.set_xlabel('Outcome')
                ax.set_ylabel('Count')
                ax.set_xticklabels(outcome_counts.index, rotation=0)
            else:
                ax.set_title(f'{sub_name} (No outcome col)')
                ax.axis('off')

        # Hide unused subplots
        for j in range(len(sub_dfs), len(axes)):
            axes[j].axis('off')

        plt.tight_layout(pad=1.0, rect=[0, 0, 1, 0.95])  # Reduce pad and tweak the layout
        plt.show()


def main(root_dir, name_dir):
    data = find_namedir_and_collect_csvs(root_dir, name_dir)
    if not data:
        print("No matching data found.")
    else:
        # Sort by parent and sub
        data.sort(key=lambda x: (x[0].split('.')[0], x[0].split('.')[1]))

        # Grouped printout
        grouped = defaultdict(list)
        for name, df in data:
            parent = name.split('.')[0]
            grouped[parent].append((name, df))

        for parent, entries in grouped.items():
            print(f"\n{parent}:")
            for name, df in entries:
                print(f"  {name} - {len(df)} rows")

        plot_histograms(data)

if __name__ == "__main__":
    main(ROOTDIR, NAMEDIR)
