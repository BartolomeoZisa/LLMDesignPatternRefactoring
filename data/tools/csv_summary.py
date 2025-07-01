import pandas as pd
import os

csv_file_path = '../report/report.csv'
summary_output_file_path = '../report/summary.csv'
per_model_dir = '../report/per_model_summaries'

# Create output directory if it doesn't exist
os.makedirs(per_model_dir, exist_ok=True)

# Read CSV
df = pd.read_csv(csv_file_path)

# Normalize text data
df['All Tests Passed'] = df['All Tests Passed'].str.strip().str.capitalize()
df['Applies Design Pattern'] = df['Applies Design Pattern'].str.strip().str.capitalize()

# Define group keys
group_keys = ['Pattern', 'Example File', 'Standard/Custom', 'Model Name']

# Group and aggregate for overall summary
summary_data = []
for group_values, group_df in df.groupby(group_keys):
    total = len(group_df)
    passed = (group_df['All Tests Passed'] == 'Yes').sum()
    yes = (group_df['Applies Design Pattern'] == 'Yes').sum()
    no = (group_df['Applies Design Pattern'] == 'No').sum()
    flawed = (group_df['Applies Design Pattern'] == 'Flawed').sum()

    summary_data.append({
        'Pattern': group_values[0],
        'Example File': group_values[1],
        'Standard/Custom': group_values[2],
        'Model Name': group_values[3],
        'Total Iterations': total,
        'All Tests Passed Count': passed,
        'Applies Design Pattern Yes': yes,
        'Applies Design Pattern No': no,
        'Applies Design Pattern Flawed': flawed,
    })

# Save overall summary
summary_df = pd.DataFrame(summary_data)
summary_df.to_csv(summary_output_file_path, index=False)
print(f"Summary written to {summary_output_file_path}")

# Create per-model CSVs
for model_name, model_df in df.groupby('Model Name'):
    model_summary_data = []
    for group_values, group_df in model_df.groupby(['Pattern', 'Example File', 'Standard/Custom']):
        total = len(group_df)
        passed = (group_df['All Tests Passed'] == 'Yes').sum()
        applied = (group_df['Applies Design Pattern'] == 'Yes').sum()
        not_applied = (group_df['Applies Design Pattern'] == 'No').sum()
        flawed = (group_df['Applies Design Pattern'] == 'Flawed').sum()
        perfect = ((group_df['All Tests Passed'] == 'Yes') & (group_df['Applies Design Pattern'] == 'Yes')).sum()
        LOC = group_df['lines_of_code'].mean() 
        response_length = group_df['response_length'].mean()
        CL = group_df['comment_lines'].mean() if 'comment_lines' in group_df.columns else 0

        model_summary_data.append({
            'Example File': group_values[1],
            'Type': group_values[2],
            'Pattern': group_values[0],
            'Passed Tests': f"{round(passed / total * 100, 2)} %",
            'Applied': f"{round(applied / total * 100, 2)} %",
            'Flawed': f"{round(flawed / total * 100, 2)} %",
            'Not Applied': f"{round(not_applied / total * 100, 2)} %",
            'Perfect': f"{round(perfect / total * 100, 2)} %",
            'LOC': f"{round(LOC, 2)}",
            'Response Length': f"{round(response_length,2)}",
            'CL' : f"{round(CL, 2)}",
            'Comment Density': f"{round((CL / (LOC+CL)) * 100, 2)} %"
        })


    # Create and save per-model summary CSV
    per_model_df = pd.DataFrame(model_summary_data)
    #order by 'Pattern' and 'Standard/Custom'
    per_model_df.sort_values(by=['Pattern', 'Type'], inplace=True)
    model_file_name = f"{model_name.replace(' ', '_').lower()}_summary.csv"
    per_model_output_path = os.path.join(per_model_dir, model_file_name)
    per_model_df.to_csv(per_model_output_path, index=False)
    print(f"Per-model summary written to {per_model_output_path}")




