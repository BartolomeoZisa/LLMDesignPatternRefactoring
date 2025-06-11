import pandas as pd

csv_file_path = '../report/report.csv'
output_file_path = '../report/summary.csv'

# Read CSV
df = pd.read_csv(csv_file_path)

# Normalize text data
df['All Tests Passed'] = df['All Tests Passed'].str.strip().str.capitalize()
df['Applies Design Pattern'] = df['Applies Design Pattern'].str.strip().str.capitalize()

# Define group keys
group_keys = ['Pattern', 'Example File', 'Standard/Custom']

# Group and aggregate (exclude grouping columns explicitly)
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
        'Total Iterations': total,
        'All Tests Passed Count': passed,
        '% All Tests Passed': round(passed / total * 100, 2),
        'Applies Design Pattern Yes': yes,
        '% Applies Design Pattern Yes': round(yes / total * 100, 2),
        'Applies Design Pattern No': no,
        '% Applies Design Pattern No': round(no / total * 100, 2),
        'Applies Design Pattern Flawed': flawed,
        '% Applies Design Pattern Flawed': round(flawed / total * 100, 2),
    })

# Create DataFrame
summary = pd.DataFrame(summary_data)

# Save to CSV
summary.to_csv(output_file_path, index=False)

print(f"Summary written to {output_file_path}")




