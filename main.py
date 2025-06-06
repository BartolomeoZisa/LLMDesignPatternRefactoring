import subprocess
import os
import sys
import concurrent.futures
from typing import List, Optional, Tuple
from src.modules.explore import explore_folder_for_triples
import src.modules.config as config


def filter_init_py(files: List[str]) -> List[str]:
    """Exclude '__init__.py' files from a list."""
    return [f for f in files if "__init__.py" not in f]


class RefactorPipeline:
    def __init__(
        self,
        base_files: List[str],
        refactored_tests: List[str],
        pattern_name: str,
        parent_folder: str,
    ):
        self.base_files = filter_init_py(base_files)
        self.refactored_tests = filter_init_py(refactored_tests)
        self.pattern_name = pattern_name
        self.parent_folder = parent_folder
        self.code_path = self.base_files[0]
        self.test_path = self.refactored_tests[0]
        self.save_folder = os.path.join(
            parent_folder.replace("examples", "results"), config.SAVEFOLDERPATH
        )
        os.makedirs(self.save_folder, exist_ok=True)

    def run_subprocess(self, cmd: List[str], capture_output=True) -> Tuple[int, str, str]:
        """Run subprocess command with error handling."""
        try:
            result = subprocess.run(
                cmd,
                capture_output=capture_output,
                text=True,
                check=True,
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Command {' '.join(cmd)} failed:\n{e.stderr.strip()}")
            return e.returncode, e.stdout, e.stderr

    def run_refactor(self) -> Optional[str]:
        """Run the refactorer script and return path to refactored file."""
        cmd = [
            sys.executable,
            "refactorer.py",
            self.code_path,
            self.test_path,
            self.pattern_name,
            config.PROMPTFILE,
            self.save_folder,
            "--temperature",
            str(config.TEMPERATURE),
            "--model_name",
            config.MODEL_NAME,
            "--max_length",
            str(config.MAX_LENGTH),
            "--strategy",
            config.STRATEGY,
        ]
        print("[INFO] Running refactor step...")
        retcode, stdout, _ = self.run_subprocess(cmd)
        if retcode != 0:
            return None
        # Assume the last line of stdout is the refactored file path
        refactored_path = stdout.strip().splitlines()[-1]
        return refactored_path

    def generate_uml(self, refactored_file_path: str) -> None:
        """Generate UML diagrams in multiple formats using pyreverse."""
        print("[INFO] Generating UML diagrams...")
        uml_output_dir = os.path.join(os.path.dirname(os.path.dirname(refactored_file_path)), "uml")
        os.makedirs(uml_output_dir, exist_ok=True)

        base_name = os.path.splitext(os.path.basename(refactored_file_path))[0]
        code_dir = os.path.dirname(refactored_file_path)

        formats = ["dot", "puml", "mmd", "png"]

        for fmt in formats:
            cmd = [
                "pyreverse",
                "--output",
                fmt,
                "--output-directory",
                uml_output_dir,
                "-p",
                base_name,
                code_dir,
            ]
            print(f"[INFO] Running pyreverse for format '{fmt}'...")
            retcode, _, stderr = self.run_subprocess(cmd)
            if retcode == 0:
                print(f"[INFO] UML ({fmt.upper()}) saved to {uml_output_dir}")
            else:
                print(f"[ERROR] UML generation failed for '{fmt}':\n{stderr.strip()}")

    def run_tests(self, refactored_file_path: str) -> bool:
        """Run tests on the refactored code."""
        cmd = [sys.executable, "tester.py", refactored_file_path, self.test_path]
        print("[INFO] Running tests...")
        retcode, _, stderr = self.run_subprocess(cmd, capture_output=False)
        if retcode != 0:
            print(f"[ERROR] Test step failed:\n{stderr.strip()}")
            return False
        return True


def main():
    matches = explore_folder_for_triples(config.PROJECT_ROOT)
    print(f"Found {len(matches)} matches:")

    for i, (base_files, refactored_tests, pattern_name, parent_folder) in enumerate(matches, start=1):
        print(f"\nMatch #{i}")
        print("Base files:")
        for f in base_files:
            print(f"  {f}")
        print("Test files:")
        for f in refactored_tests:
            print(f"  {f}")
        print(f"Pattern name: {pattern_name}")
        print(f"Folder: {parent_folder}")

        if config.ASKSKIP:
            user_input = input("Do you want to skip this pattern? (y/n): ").strip().lower()
            if user_input == "y":
                print("Skipping this pattern.")
                continue
            elif user_input != "n":
                print("Invalid input. Please enter 'y' or 'n'.")
                continue

        pipeline = RefactorPipeline(base_files, refactored_tests, pattern_name[0], parent_folder)
        refactored_path = pipeline.run_refactor()
        if not refactored_path:
            continue

        #pipeline.generate_uml(refactored_path)
        
        if not pipeline.run_tests(refactored_path):
            continue

        print("\nDone with this pattern.")
        print("You can enter another refactored version or type 'SKIP' to move to the next pattern.")


def main_wrapper(_):
    main()


if __name__ == "__main__":
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(main_wrapper, i) for i in range(config.NUMITERATIONS)]

        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"[ERROR] One iteration failed: {e}")



        
        