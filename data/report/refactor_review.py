import os
import csv
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# You need Pillow installed for image display:
# pip install pillow

FOLDERTOSEARCH = "../results"


def all_tests_passed(testreport_path):
    if not os.path.exists(testreport_path):
        return None

    with open(testreport_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        tests = list(reader)
        if not tests:
            return None

        for row in tests:
            outcome = row.get('outcome')
            if outcome is None:
                return None
            if outcome.lower() != 'passed':
                return False
        return True


def find_folders(base_path='examples'):
    valid_folders = []
    print(f"Searching folders under: {base_path}")
    for root, dirs, files in os.walk(base_path):
        parts = root.split(os.sep)
        if len(parts) < 2:
            continue
        folder_name = parts[-1]
        print(f"Checking folder: {root} (folder_name: {folder_name})")
        if folder_name.count('_') >= 2:
            results_files = [f for f in files if f.endswith('_results.csv')]
            if not results_files:
                print(f"  No *_results.csv found in {root}")
                continue
            testreport_path = os.path.join(root, results_files[0])
            print(f"  Found results CSV: {testreport_path}")
            if all_tests_passed(testreport_path):
                uml_folder = os.path.join(root, 'uml')
                if os.path.isdir(uml_folder):
                    png_files = [f for f in os.listdir(uml_folder)
                                 if f.lower().endswith('.png') and f.lower().startswith("classes")]
                    if png_files:
                        print(f"  Found valid UML folder with PNGs: {uml_folder}")
                        valid_folders.append((uml_folder, png_files))
                    else:
                        print(f"  UML folder has no PNG files.")
                else:
                    print(f"  No UML folder here.")
            else:
                print(f"  Tests not passed or CSV indicates failures.")
    return valid_folders


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

        self.yes_btn = tk.Button(self.frame_buttons, text="Yes", width=10, command=self.yes)
        self.yes_btn.pack(side=tk.LEFT, padx=5)

        self.no_btn = tk.Button(self.frame_buttons, text="No", width=10, command=self.no)
        self.no_btn.pack(side=tk.LEFT, padx=5)

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
                    continue  # Try next image
                return
            else:
                self.folder_index += 1
                self.png_index = 0

        # All images reviewed
        messagebox.showinfo("Done", "All images reviewed!")
        self.on_close()

    def record_result(self, passed):
        uml_folder, png_files = self.folders[self.folder_index]
        filename = png_files[self.png_index]
        self.results.append({
            'filename': filename,
            'passed': passed,
            'reason': 'human'
        })
        self.png_index += 1

        # Save result to the same folder as the report (parent of uml)
        parent_folder = os.path.dirname(uml_folder)
        self.save_results(parent_folder)

        self.load_image()

    def yes(self):
        self.record_result(True)

    def no(self):
        self.record_result(False)

    def save_results(self, output_dir):
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, 'refactor_result.csv')

        try:
            with open(output_file, 'w', newline='') as csvfile:
                fieldnames = ['filename', 'passed', 'reason']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for r in self.results:
                    writer.writerow(r)
            print(f"Refactor results saved in {output_file}")
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save results: {e}")
            print(f"Error saving file: {e}")

    def on_close(self):
        if self.results:
            if self.folder_index < len(self.folders):
                uml_folder, _ = self.folders[self.folder_index]
            else:
                uml_folder, _ = self.folders[-1]
            parent_folder = os.path.dirname(uml_folder)
            self.save_results(parent_folder)
        self.destroy()


def main():
    folders = find_folders(FOLDERTOSEARCH)
    if not folders:
        print("No valid folders with passed tests and UML PNGs found.")
        return

    app = RefactorReviewer(folders)
    app.mainloop()


if __name__ == "__main__":
    main()

