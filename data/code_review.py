import tkinter as tk
from tkinter import filedialog, messagebox
from pygments import lex
from pygments.lexers import PythonLexer
import os
import glob
import json


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

        self.file_index = 0
        self.files = []
        self.results = {}

        self.label = tk.Label(master, text="Select a folder to begin.", font=("Arial", 14))
        self.label.pack(pady=5)

        # Scrollbar and Text Frame
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

        self.load_button = tk.Button(button_frame, text="Load Folder", command=self.load_folder)
        self.load_button.pack(side=tk.LEFT, padx=5)

        self.yes_button = tk.Button(button_frame, text="Yes (Good)", command=lambda: self.mark_file("yes"), state=tk.DISABLED)
        self.yes_button.pack(side=tk.LEFT, padx=5)

        self.no_button = tk.Button(button_frame, text="No (Needs Fixing)", command=lambda: self.mark_file("no"), state=tk.DISABLED)
        self.no_button.pack(side=tk.LEFT, padx=5)

    def load_folder(self):
        folder = filedialog.askdirectory()
        if not folder:
            return
        self.files = glob.glob(os.path.join(folder, "*.py"))
        self.file_index = 0
        self.results = {}
        if not self.files:
            messagebox.showerror("Error", "No .py files found.")
            return
        self.label.config(text=f"Loaded {len(self.files)} files.")
        self.show_file()

    def show_file(self):
        if self.file_index >= len(self.files):
            self.label.config(text="Review complete.")
            self.text.config(state=tk.NORMAL)
            self.text.delete("1.0", tk.END)
            self.text.config(state=tk.DISABLED)
            self.yes_button.config(state=tk.DISABLED)
            self.no_button.config(state=tk.DISABLED)
            self.save_results()
            return

        current_file = self.files[self.file_index]
        with open(current_file, "r", encoding="utf-8") as f:
            code = f.read()

        self.text.highlight_code(code)
        self.label.config(text=f"Reviewing: {os.path.basename(current_file)}")
        self.yes_button.config(state=tk.NORMAL)
        self.no_button.config(state=tk.NORMAL)

    def mark_file(self, decision):
        file_name = os.path.basename(self.files[self.file_index])
        self.results[file_name] = decision
        self.file_index += 1
        self.show_file()

    def save_results(self):
        with open("code_review_results.json", "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=4)
        messagebox.showinfo("Done", "All files reviewed. Results saved to code_review_results.json")


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("900x700")
    app = CodeReviewApp(root)
    root.mainloop()




