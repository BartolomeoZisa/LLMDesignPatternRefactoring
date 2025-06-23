import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Input and output paths
folder_path = '../report/per_model_summaries'
output_path = '../report/grouped_bar_charts'
os.makedirs(output_path, exist_ok=True)

# Data structure to store summaries
summary_data = {}

# Read and process each CSV
for filename in os.listdir(folder_path):
    if filename.endswith(".csv"):
        model_name = os.path.splitext(filename)[0]
        filepath = os.path.join(folder_path, filename)
        df = pd.read_csv(filepath)

        # Remove % signs and convert to float
        for col in ['Applied', 'Passed Tests', 'Perfect']:
            df[col] = df[col].str.replace('%', '').astype(float)

        # Group by Pattern and compute mean
        grouped = df.groupby('Pattern')[['Applied', 'Passed Tests', 'Perfect']].mean()
        summary_data[model_name] = grouped

# Combine data into one DataFrame per metric
metrics = ['Applied', 'Passed Tests', 'Perfect']
titles = {
    'Applied': 'Applies Pattern',
    'Passed Tests': 'Passes Tests',
    'Perfect': 'Applies Pattern and Passes Tests'
}

pattern_set = set().union(*[df.index for df in summary_data.values()])
pattern_list = sorted(pattern_set)

# Function to extract metric matrix
def get_metric_matrix(metric):
    data = []
    model_names = list(summary_data.keys())
    for pattern in pattern_list:
        row = []
        for model in model_names:
            value = summary_data[model].loc[pattern][metric] if pattern in summary_data[model].index else 0
            row.append(value)
        data.append(row)
    return pd.DataFrame(data, index=pattern_list, columns=model_names)

# Plot and save grouped bar charts
x = np.arange(len(pattern_list))  # label locations
width = 0.2  # bar width

for metric in metrics:
    metric_df = get_metric_matrix(metric)
    fig, ax = plt.subplots(figsize=(10, 7.5))  # Slightly taller

    for i, model in enumerate(metric_df.columns):
        ax.bar(x + i * width, metric_df[model], width, label=model)

    ax.set_ylabel(f'{titles[metric]} (%)', fontsize=18)   # Y-label bigger
    ax.set_title(f'{titles[metric]} by Pattern and Model', fontsize=20)  # Title bigger
    ax.set_xticks(x + width * (len(metric_df.columns) - 1) / 2)
    ax.set_xticklabels(pattern_list, fontsize=16)        # X tick labels bigger
    ax.tick_params(axis='y', labelsize=16)                # Y tick labels bigger
    ax.set_ylim(0, 115)                                   # Y-axis limit
    ax.legend(loc='upper left', fontsize=16)             # Legend font bigger
    plt.tight_layout()

    # Save to file
    filename = metric.lower().replace(' ', '_') + '.png'
    filepath = os.path.join(output_path, filename)
    plt.savefig(filepath)
    plt.close()



