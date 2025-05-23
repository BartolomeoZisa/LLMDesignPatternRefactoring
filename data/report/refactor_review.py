import os
import csv
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from graphutils import *
import json
import glob
import networkx as nx

# --- CONFIG ---
FOLDERTOSEARCH = "../results"
VALIDATIONCSV = "validation.csv"

# --- UTILS ---
def all_tests_passed(testreport_path):
    if not os.path.exists(testreport_path):
        return None
    with open(testreport_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        tests = list(reader)
        if not tests:
            return None
        for row in tests:
            if row.get("outcome", "").lower() != "passed":
                return False
        return True

# --- 1. DISCOVER CANDIDATES ---
def find_candidate_folders(base_path):
    folders = []
    print(f"Searching folders under: {base_path}")
    for root, dirs, files in os.walk(base_path):
        folder_name = os.path.basename(root)
        if folder_name.count("_") >= 2:
            result_files = [f for f in files if f.endswith("_results.csv")]
            if not result_files:
                continue
            test_report = os.path.join(root, result_files[0])
            uml_folder = os.path.join(root, "uml")
            if os.path.isdir(uml_folder):
                png_files = [f for f in os.listdir(uml_folder)
                             if f.lower().endswith(".png") and f.lower().startswith("classes")]
                if png_files:
                    folders.append({
                        "uml_folder": uml_folder,
                        "png_files": png_files,
                        "report": test_report,
                        "parent": root
                    })
    return folders

# --- 2. APPLY FILTERS / CRITERIA ---
def filter_folders_by_criteria(folders, criteria_funcs):
    qualified = []
    for folder_info in folders:
        failed_funcs = []

        for func in criteria_funcs:
            try:
                if not func(folder_info):
                    failed_funcs.append(func.__name__)
            except Exception as e:
                failed_funcs.append(f"{func.__name__} (error: {e})")

        if not failed_funcs:
            qualified.append((folder_info["uml_folder"], folder_info["png_files"]))
        else:
            output_path = os.path.join(os.path.dirname(folder_info["uml_folder"]), "validation.csv")
            try:
                with open(output_path, "w", newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=["filename", "passed", "reason"])
                    writer.writeheader()
                    reason_text = ", ".join(f"failed: {name}" for name in failed_funcs)
                    for img in folder_info["png_files"]:
                        writer.writerow({
                            "filename": img,
                            "passed": False,
                            "reason": reason_text
                        })
                print(f"Auto-saved failure result in {output_path}")
            except Exception as e:
                print(f"Failed to save auto result for {output_path}: {e}")
    return qualified

# --- 3. GUI REVIEW TOOL ---
class RefactorReviewer(tk.Tk):
    def __init__(self, folders):
        super().__init__()
        self.title("Refactor Reviewer")
        self.folders = folders
        self.folder_index = 0
        self.png_index = 0
        self.results = []

        self.label = tk.Label(self, text="", font=("Arial", 14))
        self.label.pack(pady=10)

        self.image_label = tk.Label(self)
        self.image_label.pack()

        self.frame_buttons = tk.Frame(self)
        self.frame_buttons.pack(pady=10)

        tk.Button(self.frame_buttons, text="Yes", width=10, command=self.yes).pack(side=tk.LEFT, padx=5)
        tk.Button(self.frame_buttons, text="No", width=10, command=self.no).pack(side=tk.LEFT, padx=5)

        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.load_image()

    def load_image(self):
        while self.folder_index < len(self.folders):
            uml_folder, png_files = self.folders[self.folder_index]
            if self.png_index < len(png_files):
                png_file = png_files[self.png_index]
                full_path = os.path.join(uml_folder, png_file)
                self.label.config(text=f"Folder: {uml_folder}\nImage: {png_file}")
                try:
                    img = Image.open(full_path)
                    img.thumbnail((800, 600))
                    self.photo = ImageTk.PhotoImage(img)
                    self.image_label.config(image=self.photo)
                except Exception as e:
                    print(f"Failed to load image {full_path}: {e}")
                    self.png_index += 1
                    continue
                return
            else:
                self.folder_index += 1
                self.png_index = 0
        messagebox.showinfo("Done", "All images reviewed!")
        self.on_close()

    def record_result(self, passed):
        uml_folder, png_files = self.folders[self.folder_index]
        filename = png_files[self.png_index]
        output_dir = os.path.dirname(uml_folder)
        output_file = os.path.join(output_dir, VALIDATIONCSV)

        try:
            with open(output_file, "w", newline="") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=["filename", "passed", "reason"])
                writer.writeheader()
                writer.writerow({
                    "filename": filename,
                    "passed": passed,
                    "reason": "human"
                })
            print(f"Saved validation for: {filename} in {output_file}")
        except Exception as e:
            print(f"Error saving validation for {filename}: {e}")

        self.png_index += 1
        self.load_image()


    def yes(self):
        self.record_result(True)

    def no(self):
        self.record_result(False)

    def save_results(self, output_dir):
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, VALIDATIONCSV)
        try:
            with open(output_file, "w", newline="") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=["filename", "passed", "reason"])
                writer.writeheader()
                for r in self.results:
                    writer.writerow(r)
            print(f"Refactor results saved in {output_file}")
        except Exception as e:
            print(f"Error saving file: {e}")
            
    def on_close(self):
        self.destroy()

# --- 4. CRITERIA FUNCTIONS EXAMPLES ---
def test_report_passed(info):
    return all_tests_passed(info["report"])

def no_validation(info):
    return not os.path.exists(os.path.join(os.path.dirname(info["parent"]), "validation.csv"))



def check_pattern_in_folder(info):
    """
    For a given folder info dict, parse the .dot graph and check if it contains
    the pattern(s) specified in parameters.json under 'pattern_name' key.
    
    return True if all patterns are found, False otherwise.
    """
    # Locate .dot file (first classes*.dot)
    dot_files = glob.glob(os.path.join(info["uml_folder"], "classes*.dot"))
    if not dot_files:
        print(f"No classes*.dot files found in {info['uml_folder']}")
        return None
    dot_path = dot_files[0]

    # Read parameters.json
    params_path = os.path.join(info["parent"], "parameters.json")
    if not os.path.exists(params_path):
        print(f"No parameters.json found in {info['parent']}")
        return None

    with open(params_path, "r") as f:
        params = json.load(f)

    pattern_names = params.get("pattern_name")
    if not pattern_names:
        print(f"No 'pattern_name' key in {params_path}")
        return None

    if isinstance(pattern_names, str):
        pattern_names = [pattern_names]

    # Load graph from .dot
    graph = GraphParser.read_graph(dot_path)

    if isinstance(graph, nx.MultiDiGraph):
        graph = GraphParser.convert_multidigraph_to_digraph(graph)
    #print(graph)
    visualizer = GraphVisualizer(graph)
    visualizer.draw()

    checker = SubgraphChecker()
    #print(checker.subgraph_classes)
    # Check patterns
    #print(f"Checking patterns: {pattern_names}")
    results = checker.check(graph, pattern_names)

    #print(results)

    #all keys must be true
    for pattern_name, result in results.items():
        if not result:
            print(f"Pattern '{pattern_name}' not found in {dot_path}")
            return False
    return True


# --- 5. MAIN ---
#I should divide the main from the other code, also I should add an option to not check what was already checked
def main():
    candidates = find_candidate_folders(FOLDERTOSEARCH)
    if not candidates:
        print("No folders with results and UML diagrams found.")
        return

    # Choose your active criteria here:
    criteria = [test_report_passed]
    qualified = filter_folders_by_criteria(candidates, criteria)

    if not qualified:
        print("No folders passed all criteria.")
        return

    app = RefactorReviewer(qualified)
    app.mainloop()

if __name__ == "__main__":
    main()



