import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

def create_pie_charts(csv_file, name_column, value_columns, output_name_column, output_dir="../report/charts"):
    df = pd.read_csv(csv_file)
    os.makedirs(output_dir, exist_ok=True)

    label_color_map = {
        "Applies Design Pattern Yes": "#2E7D32",   # dark green
        "Applies Design Pattern No": "#C62828",    # dark red
        "Applies Design Pattern Flawed": "#F9A825" # dark gold
    }

    short_labels = ["Yes", "No", "Flawed"]  # concise legend labels

    for i, row in df.iterrows():
        name = str(row[name_column])
        output_name = str(row[output_name_column]).split('.')[0]

        filtered = [(label, row[label]) for label in value_columns if row[label] != 0]
        if not filtered:
            continue

        labels, data = zip(*filtered)
        colors_to_use = [label_color_map[label] for label in labels]

        subdir = os.path.join(output_dir, name)
        os.makedirs(subdir, exist_ok=True)

        fig, ax = plt.subplots(figsize=(7, 5))

        wedges, texts, autotexts = ax.pie(
            data,
            colors=colors_to_use,
            startangle=90,
            wedgeprops=dict(edgecolor='black', linewidth=2),
            autopct=lambda pct: f'{pct:.1f}%',
            pctdistance=1.3,
            labeldistance=1.15
        )

        for autotext in autotexts:
            autotext.set_color('#000000')
            autotext.set_fontsize(18)
            autotext.set_weight('bold')
            autotext.set_fontfamily('DejaVu Sans')

        # Create handles for the legend with short labels
        full_colors = [label_color_map[label] for label in value_columns]

        handles = [plt.Line2D([0], [0], marker='o', color='w',
                              markerfacecolor=color, markersize=12,
                              markeredgecolor='black', markeredgewidth=1)
                   for color in full_colors]

        ax.legend(handles=handles, labels=short_labels, title="Design Pattern",
                  loc='center left', bbox_to_anchor=(1.05, 0.5),
                  fontsize=14, title_fontsize=16,
                  frameon=True, fancybox=True,
                  borderpad=1, borderaxespad=1,
                  edgecolor='gray', facecolor='white', shadow=True)

        plt.tight_layout()
        chart_path = os.path.join(subdir, f"{output_name}.png")
        plt.savefig(chart_path, bbox_inches='tight')
        plt.close()
        print(f"Saved chart: {chart_path}")

if __name__ == "__main__":
    csv_file = "../report/summary.csv"
    name_column = "Model Name"
    value_columns = ["Applies Design Pattern Yes", "Applies Design Pattern No", "Applies Design Pattern Flawed"]
    output_name_column = "Example File"

    create_pie_charts(csv_file, name_column, value_columns, output_name_column)












