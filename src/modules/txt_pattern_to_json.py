import json
import re
import os

INPUTFOLDER = "../patternGOFtxtclean"
OUTPUTFOLDER = "../patternGOFjson"

def parse_text_to_json(input_file, output_file, ignore_headers=None):
    if ignore_headers is None:
        ignore_headers = []

    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Remove unwanted lines like book title or page numbers
    filtered_lines = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue  # skip empty lines
        if stripped.isdigit():
            continue  # skip page numbers like "160"
        if "Design Patterns: Elements of Reusable Object-Oriented Software" in stripped:
            continue  # skip book title
        filtered_lines.append(line)

    print("approximate num of words", sum(len(line.split()) for line in filtered_lines))
    content = ''.join(filtered_lines)

    # List of all possible headers in expected order
    headers = [
        "Intent",
        "Also Known As",
        "Motivation",
        "Applicability",
        "Structure",
        "Participants",
        "Collaborations",
        "Consequences",
        "Implementation",
        "Sample Code",
        "Known Uses"
    ]

    # Use regex to split content into sections based on headers
    pattern = r"(?P<header>" + "|".join(re.escape(h) for h in headers) + r")\n"
    splits = list(re.finditer(pattern, content))

    data = {}

    for i, match in enumerate(splits):
        header = match.group("header")
        if header in ignore_headers:
            continue

        start = match.end()
        end = splits[i + 1].start() if i + 1 < len(splits) else len(content)
        section_text = content[start:end].strip()
        data[header] = section_text

    # Write to JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

    print(f"Parsed JSON saved to {output_file}")

if __name__ == "__main__":
    # Parse every file in the folder
    input_folder = INPUTFOLDER
    output_folder = OUTPUTFOLDER
    ignore_headers = ["Also Known As", "Applicability", "Known Uses", "Consequences"]
    os.makedirs(output_folder, exist_ok=True)
    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            input_file = os.path.join(input_folder, filename)
            output_file = os.path.join(output_folder, filename.replace(".txt", ".json"))
            parse_text_to_json(input_file, output_file, ignore_headers=ignore_headers)
