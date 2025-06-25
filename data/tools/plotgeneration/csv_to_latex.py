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

