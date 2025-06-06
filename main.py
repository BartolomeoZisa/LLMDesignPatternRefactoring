import subprocess
import os
import sys
import shutil
from src.modules.explore import explore_folder_for_triples
import src.modules.config as config
import concurrent.futures


class RefactorPipeline:
    def __init__(self, base_files, refactored_tests, pattern_name, parentfolder):
        self.base_files = [f for f in base_files if "__init__.py" not in f]
        self.refactored_tests = [f for f in refactored_tests if "__init__.py" not in f]
        self.pattern_name = pattern_name[0]
        self.parentfolder = parentfolder
        self.code_path = self.base_files[0]
        self.test_path = self.refactored_tests[0]
        self.save_folder = os.path.join(parentfolder.replace("examples", "results"), config.SAVEFOLDERPATH)
        os.makedirs(self.save_folder, exist_ok=True)

    def run_refactor(self):
        refactor_cmd = [
            sys.executable, "refactorer.py",
            self.code_path,
            self.test_path,
            self.pattern_name,
            config.PROMPTFILE,
            self.save_folder,
            "--temperature", str(config.TEMPERATURE),
            "--model_name", config.MODEL_NAME,
            "--max_length", str(config.MAX_LENGTH),
            "--strategy", config.STRATEGY
        ]

        try:
            print("[INFO] Running refactor step...")
            result = subprocess.run(refactor_cmd, capture_output=True, text=True, check=True)
            refactored_file_path = result.stdout.strip().splitlines()[-1]
            return refactored_file_path
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Refactor step failed:\n{e.stderr}")
            return None

    def generate_uml(self, refactored_file_path):
        print("[INFO] Generating UML in DOT, PlantUML, and Mermaid formats...")

        refactored_parent = os.path.dirname(os.path.dirname(refactored_file_path))
        uml_output_dir = os.path.join(refactored_parent, "uml")
        os.makedirs(uml_output_dir, exist_ok=True)

        formats = {
            "dot": ".dot",
            "puml": ".puml",
            "mmd": ".mmd",
            "png": ".png"
        }

        for fmt, ext in formats.items():
            try:
                uml_cmd = [
                    "pyreverse",
                    "--output", fmt,
                    "--output-directory", uml_output_dir,
                    "-p", os.path.splitext(os.path.basename(refactored_file_path))[0],
                    os.path.dirname(refactored_file_path)
                ]
                print(f"[INFO] Running pyreverse for format '{fmt}'...")
                subprocess.run(uml_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print(f"[INFO] {fmt.upper()} UML saved to {uml_output_dir}{ext}")
            except subprocess.CalledProcessError as e:
                print(f"[ERROR] UML generation for format '{fmt}' failed:\n{e.stderr}")

    def run_tests(self, refactored_file_path):
        tester_cmd = [
            sys.executable, "tester.py",
            refactored_file_path,
            self.test_path
        ]

        try:
            print("[INFO] Running test step...")
            subprocess.run(tester_cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Test step failed:\n{e.stderr}")
            return False
        return True


def main():
    matches = explore_folder_for_triples(config.PROJECT_ROOT)
    print(f"Found {len(matches)} matches:")

    for i, (base_files, refactored_tests, pattern_name, parentfolder) in enumerate(matches):
        print(f"\nMatch #{i+1}")
        print("Base files:")
        for f in base_files:
            print(f"  {f}")
        print("Test files:")
        for f in refactored_tests:
            print(f"  {f}")
        print(f"Pattern name: {pattern_name}")
        print(f"Folder: {parentfolder}")

        if config.ASKSKIP:
            user_input = input("Do you want to skip this pattern? (y/n): ").strip().lower()
            if user_input == 'y':
                print("Skipping this pattern.")
                continue
            elif user_input != 'n':
                print("Invalid input. Please enter 'y' or 'n'.")
                continue

        pipeline = RefactorPipeline(base_files, refactored_tests, pattern_name, parentfolder)

        refactored_file_path = pipeline.run_refactor()
        if not refactored_file_path:
            continue

        #pipeline.generate_uml(refactored_file_path)

        success = pipeline.run_tests(refactored_file_path)
        if not success:
            continue

        print("\nDone with this pattern.\nYou can enter another refactored version or type 'SKIP' to move to the next pattern.")



if __name__ == "__main__":
    for i in range(config.ITERATIONS):
        main()


        
        