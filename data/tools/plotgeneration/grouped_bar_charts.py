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
        #remove 'summary' from model name if present
        if model_name.endswith('_summary'):
            model_name = model_name[:-8]

        filepath = os.path.join(folder_path, filename)
        df = pd.read_csv(filepath)

        # Convert percentage columns
        for col in ['Applied', 'Passed Tests', 'Perfect', 'Comment Density']:
            if col in df.columns:
                df[col] = df[col].str.replace('%', '').astype(float)

        # Convert numeric metrics
        for col in ['LOC', 'Response Length']:
            if col in df.columns:
                df[col] = df[col].astype(float)

        # Group by Pattern and compute mean
        grouped = df.groupby('Pattern')[['Applied', 'Passed Tests', 'Perfect', 'LOC', 'Response Length', "Comment Density"]].mean()
        summary_data[model_name] = grouped

# Metrics and titles
metrics = ['Applied', 'Passed Tests', 'Perfect', 'LOC', 'Comment Density']
titles = {
    'Applied': 'Applies Pattern',
    'Passed Tests': 'Passes Tests',
    'Perfect': 'Applies Pattern and Passes Tests',
    'LOC': 'Lines of Code (LOC)',
    'Response Length': 'Response Length',
    'Comment Density': 'Comment Density'
}

# Collect all patterns across all models
pattern_set = set().union(*[df.index for df in summary_data.values()])
pattern_list = sorted(pattern_set)

# Function to extract metric matrix
def get_metric_matrix(metric):
    data = []
    model_names = list(summary_data.keys())
    for pattern in pattern_list:
        row = []
        for model in model_names:
            if pattern in summary_data[model].index and metric in summary_data[model].columns:
                value = summary_data[model].loc[pattern][metric]
            else:
                value = 0
            row.append(value)
        data.append(row)
    return pd.DataFrame(data, index=pattern_list, columns=model_names)

# Plot grouped bar charts
x = np.arange(len(pattern_list))  # label locations
width = 0.2  # bar width

for metric in metrics:
    metric_df = get_metric_matrix(metric)
    fig, ax = plt.subplots(figsize=(10, 7.5))  # Slightly taller

    for i, model in enumerate(metric_df.columns):
        ax.bar(x + i * width, metric_df[model], width, label=model)

    ax.set_ylabel(f'{titles[metric]}', fontsize=18)
    ax.set_title(f'{titles[metric]} by Pattern and Model', fontsize=20)
    ax.set_xticks(x + width * (len(metric_df.columns) - 1) / 2)
    ax.set_xticklabels(pattern_list, fontsize=16)
    ax.tick_params(axis='y', labelsize=16)

    # Set y-limit only for percentage-based metrics
    if metric in ['Applied', 'Passed Tests', 'Perfect']:
        ax.set_ylim(0, 115)

    ax.legend(loc='upper left', fontsize=16)
    plt.tight_layout()

    # Save plot
    filename = metric.lower().replace(' ', '_') + '.png'
    filepath = os.path.join(output_path, filename)
    plt.savefig(filepath)
    plt.close()



