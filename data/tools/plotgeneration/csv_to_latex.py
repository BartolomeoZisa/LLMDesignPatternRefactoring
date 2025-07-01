import pandas as pd
import os
import glob

INPUT = "../report/per_model_summaries"

# Optional: auto-generate caption based on filename
def generate_caption(filename):
    base = os.path.basename(filename)
    name, _ = os.path.splitext(base)
    return f"\\caption{{{name.replace('_', ' ').title()}}}"

if os.path.isdir(INPUT):
    csv_files = glob.glob(os.path.join(INPUT, "*.csv"))
    df_list = [(pd.read_csv(f), f) for f in csv_files]

    #ignore specified columns
    ignore_columns = ['Perfect', 'CL', 'Response Length']

    for i, (df, filepath) in enumerate(df_list):
        # Remove ignored columns if they exist
        df = df.drop(columns=[col for col in ignore_columns if col in df.columns], errors='ignore')

        # Sort by 'Pattern' and 'Standard/Custom'
        df.sort_values(by=['Pattern', 'Standard/Custom'], inplace=True)

        # Add a column for the file name
        df['Example File'] = os.path.basename(filepath)

        # Save the modified DataFrame back to the list
        df_list[i] = (df, filepath)

    for df, filepath in df_list:
        latex_table = df.to_latex(index=False, escape=True, float_format="%.2f")

        wrapped_table = (
            "\\begin{table}[h]\n"
            "\\centering\n"
            "\\makebox[\\linewidth][c]{\n"
            "\\resizebox{1.1\\textwidth}{!}{%\n"
            + latex_table + "\n}%\n}\n"
            + generate_caption(filepath) + "\n"
            "\\end{table}\n"
        )

        print(wrapped_table)

else:
    df = pd.read_csv(INPUT)
    latex_table = df.to_latex(index=False, escape=True, float_format="%.2f")
    wrapped_table = (
        "\\begin{table}[h]\n"
        "\\centering\n"
        "\\makebox[\\linewidth][c]{\n"
        "\\resizebox{1.1\\textwidth}{!}{%\n"
        + latex_table + "\n}%\n}\n"
        "\\caption{Summary Table}\n"
        "\\end{table}\n"
    )
    print(wrapped_table)

