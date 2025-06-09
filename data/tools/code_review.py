import tkinter as tk
from tkinter import filedialog, messagebox
from pygments import lex
from pygments.lexers import PythonLexer
import os
import glob
import json
import csv

BASEPATH = "../results"
SKIP_REVIEWED = True  # Set to True to skip already reviewed files

def find_candidate_folders(base_path):
    folders = []
    print(f"Searching folders under: {base_path}")
    for root, dirs, files in os.walk(base_path):
        result_files = [f for f in files if f.endswith("_results.csv")]
        parameters_files = [f for f in files if f.endswith("parameters.json")]
        if not result_files or not parameters_files:
            continue
        test_report = os.path.join(root, result_files[0])
        parameters = os.path.join(root, parameters_files[0])
        refactored_folder = os.path.join(root, "refactored") 
        folders.append({
            "report": test_report,
            "parameters": parameters,
            "refactored_folder": refactored_folder,
            "parent": root
        })
    return folders

class HighlightText(tk.Text):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Define commonly used Pygments token tags manually
        self.token_colors = {
            "Token.Keyword": "#ff79c6",        # pink
            "Token.Name": "#f8f8f2",           # white
            "Token.Comment": "#6272a4",        # gray-blue
            "Token.String": "#f1fa8c",         # yellow
            "Token.Number": "#bd93f9",         # purple
            "Token.Operator": "#ffb86c",       # orange
            "Token.Name.Function": "#50fa7b",  # green
            "Token.Name.Class": "#8be9fd",     # cyan
        }

        for tag, color in self.token_colors.items():
            self.tag_configure(tag, foreground=color)

    def highlight_code(self, code):
        self.config(state=tk.NORMAL)
        self.delete("1.0", tk.END)

        idx = "1.0"
        for token, content in lex(code, PythonLexer()):
            self.insert(idx, content)
            tag_name = str(token)

            if tag_name in self.token_colors and content.strip():
                end_idx = self.index(f"{idx}+{len(content)}c")
                self.tag_add(tag_name, idx, end_idx)

            idx = self.index(f"{idx}+{len(content)}c")

        self.config(state=tk.DISABLED)


class CodeReviewApp:
    def __init__(self, master):
        self.master = master
        master.title("Code Review Tool")

        self.candidate_folders = find_candidate_folders(BASEPATH)
        self.folder_index = 0
        self.file_index = 0
        self.files = []
        self.current_folder = None

        self.label = tk.Label(master, text="Loading candidate folders...", font=("Arial", 14))
        self.label.pack(pady=5)

        frame = tk.Frame(master)
        frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=5)

        self.text = HighlightText(frame, wrap="none", font=("Courier", 12),
                                  bg="#282a36", fg="#f8f8f2", insertbackground="white")
        self.text.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        scrollbar = tk.Scrollbar(frame, command=self.text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text.config(yscrollcommand=scrollbar.set)

        button_frame = tk.Frame(master)
        button_frame.pack(pady=5)

        self.yes_button = tk.Button(button_frame, text="Yes (Good)", command=lambda: self.mark_file("yes"), state=tk.DISABLED)
        self.yes_button.pack(side=tk.LEFT, padx=5)
        self.flawed_button = tk.Button(button_frame, text="Flawed", command=lambda: self.mark_file("flawed"), state=tk.DISABLED)
        self.flawed_button.pack(side=tk.LEFT, padx=5)

        self.no_button = tk.Button(button_frame, text="No (Needs Fixing)", command=lambda: self.mark_file("no"), state=tk.DISABLED)
        self.no_button.pack(side=tk.LEFT, padx=5)

        self.load_next_folder()

    def load_next_folder(self):
        if self.folder_index >= len(self.candidate_folders):
            self.label.config(text="All folders reviewed.")
            self.text.config(state=tk.NORMAL)
            self.text.delete("1.0", tk.END)
            self.text.config(state=tk.DISABLED)
            self.yes_button.config(state=tk.DISABLED)
            self.no_button.config(state=tk.DISABLED)
            self.flawed_button.config(state=tk.DISABLED)
            messagebox.showinfo("Done", "All folders reviewed.")
            return

        self.current_folder = self.candidate_folders[self.folder_index]
        refactored_path = self.current_folder["refactored_folder"]
        all_files = glob.glob(os.path.join(refactored_path, "*.py"))
        self.files = [f for f in all_files if "__init__.py" not in f]

        # Load reviewed files from CSV if SKIP_REVIEWED is enabled
        if SKIP_REVIEWED:
            reviewed_files = set()
            csv_path = os.path.join(self.current_folder["parent"], "code_review.csv")
            if os.path.isfile(csv_path):
                with open(csv_path, newline='', encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        reviewed_files.add(row["file"])
                self.files = [f for f in self.files if os.path.basename(f) not in reviewed_files]

        self.file_index = 0
        self.folder_index += 1

        if not self.files:
            self.load_next_folder()
        else:
            self.label.config(text=f"Loaded {len(self.files)} files from: {refactored_path}")
            self.show_file()


    def show_file(self):
        if self.file_index >= len(self.files):
            self.load_next_folder()
            return

        current_file = self.files[self.file_index]
        with open(current_file, "r", encoding="utf-8") as f:
            code = f.read()

        self.text.highlight_code(code)
        self.label.config(text=f"Reviewing: {os.path.basename(current_file)}")
        self.yes_button.config(state=tk.NORMAL)
        self.no_button.config(state=tk.NORMAL)
        self.flawed_button.config(state=tk.NORMAL)

    def mark_file(self, decision):
        current_file = self.files[self.file_index]
        file_name = os.path.basename(current_file)
        result_row = {"file": file_name, "applies_pattern": decision}
        self.save_result_to_csv(result_row)
        self.file_index += 1
        self.show_file()

    def save_result_to_csv(self, row):
        if not self.current_folder:
            return

        csv_path = os.path.join(self.current_folder["parent"], "code_review.csv")
        file_exists = os.path.isfile(csv_path)

        with open(csv_path, "a", newline='', encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["file", "applies_pattern"])
            if not file_exists:
                writer.writeheader()
            writer.writerow(row)



if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("900x700")
    app = CodeReviewApp(root)
    root.mainloop()




