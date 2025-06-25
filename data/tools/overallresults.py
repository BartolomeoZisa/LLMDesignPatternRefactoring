import os
import csv
from collections import defaultdict

def parse_percentage(value):
    return float(value.strip().replace('%', ''))

def process_file(filepath):
    pattern_stats = defaultdict(lambda: defaultdict(list))
    overall_stats = defaultdict(list)

    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pattern = row['Pattern']
            applied = parse_percentage(row['Applied'])
            passed = parse_percentage(row['Passed Tests'])
            perfect = parse_percentage(row['Perfect'])

            # Grouped stats by pattern
            pattern_stats[pattern]['Applied'].append(applied)
            pattern_stats[pattern]['Passed'].append(passed)
            pattern_stats[pattern]['Perfect'].append(perfect)

            # Overall stats
            overall_stats['Applied'].append(applied)
            overall_stats['Passed'].append(passed)
            overall_stats['Perfect'].append(perfect)

    return pattern_stats, overall_stats

def compute_averages(stats):
    return {k: round(sum(v)/len(v), 2) if v else 0 for k, v in stats.items()}

def main(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            filepath = os.path.join(folder_path, filename)
            pattern_stats, overall_stats = process_file(filepath)

            print(f"\n📄 File: {filename}\n")

            print("Average Percentage by Pattern:")
            for pattern, stats in pattern_stats.items():
                averages = compute_averages(stats)
                print(f"  {pattern}: Applied: {averages['Applied']}%, Passed Tests: {averages['Passed']}%, Perfect: {averages['Perfect']}%")

            overall_avg = compute_averages(overall_stats)
            print("\nOverall Averages in File:")
            print(f"  Applied: {overall_avg['Applied']}%, Passed Tests: {overall_avg['Passed']}%, Perfect: {overall_avg['Perfect']}%")

if __name__ == "__main__":
    folder_path = "../report/per_model_summaries"  # Your folder path here
    main(folder_path)

