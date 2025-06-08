import subprocess
import os
import sys
import shutil
from src.modules.explore import explore_folder_for_triples
import src.modules.config as config
 
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

        base_files = [f for f in base_files if "__init__.py" not in f]
        refactored_tests = [f for f in refactored_tests if "__init__.py" not in f]

        code_path = base_files[0]
        test_path = refactored_tests[0]
        pattern = pattern_name[0]

        #save in parentfolder sibling (substitute examples with results)
        save_folder = os.path.join(parentfolder.replace("examples", "results"), config.SAVEFOLDERPATH)

        # Call RefactorFrontEnd
        refactor_cmd = [
            sys.executable, "refactorer.py",
            code_path,
            test_path,
            pattern,
            config.PROMPTFILE,
            save_folder,
            "--temperature", str(config.TEMPERATURE),
            "--model_name", config.MODEL_NAME,
            "--max_length", str(config.MAX_LENGTH),
            "--strategy", config.STRATEGY,
            "--ignore_keys", ",".join(config.IGNOREHEADERS)
        ]

        try:
            print("[INFO] Running refactor step...")
            result = subprocess.run(refactor_cmd, capture_output=True, text=True, check=True)
            refactored_file_path = result.stdout.strip().splitlines()[-1]  # last line = path
            print(result.stdout.strip())
            print(result.stderr.strip())
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Refactor step failed:\n{e.stderr}")
            print("STDOUT:")
            print(e.stdout)  # if available
            print("STDERR:")
            print(e.stderr)  # print stderr even if it's Non
            continue

        # === UML generation ===
        '''
        print("[INFO] Generating UML in DOT, PlantUML, and Mermaid formats...")

        # uml_output_dir is parent of parent of refactored_file_path + "uml"
        refactored_parent = os.path.dirname(os.path.dirname(refactored_file_path))
        uml_output_dir = os.path.join(refactored_parent, "uml")
        os.makedirs(uml_output_dir, exist_ok=True)


        # Define the desired formats and corresponding file extensions
        formats = {
            "dot": ".dot",
            "puml": ".puml",
            "mmd": ".mmd",
            "png": ".png"
        }

        for fmt, ext in formats.items():
            try:
                # Build the pyreverse command for each format
                uml_cmd = [
                    "pyreverse",
                    "--output", fmt,                  # select output format
                    "--output-directory", uml_output_dir,  # set output dir
                    "-p", os.path.splitext(os.path.basename(refactored_file_path))[0],  # project name
                    os.path.dirname(refactored_file_path)  # input module/package
                ]
                print(f"[INFO] Running pyreverse for format '{fmt}'...")
                subprocess.run(uml_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print(f"[INFO] {fmt.upper()} UML saved to {uml_output_dir}{ext}")
            except subprocess.CalledProcessError as e:
                print(f"[ERROR] UML generation for format '{fmt}' failed:\n{e.stderr}")
        '''

        # Construct path to test file (already known)
        refactored_test_path = test_path

        # Call TesterFrontEnd
        tester_cmd = [
            sys.executable, "tester.py", 
            refactored_file_path,
            refactored_test_path
        ]

        try:
            print("[INFO] Running test step...")
            subprocess.run(tester_cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Test step failed:\n{e.stderr}")
            continue

        print("\nDone with this pattern.\nYou can enter another refactored version or type 'SKIP' to move to the next pattern.")

if __name__ == "__main__":
    for _ in range(config.NUMITERATIONS):
        main()



        
        