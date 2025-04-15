from explore import explore_folder_for_triples
from promptcreator import PromptCreator
from codetester import CodeTester
import os

FOLDERPREFIX = "copilot"
PROMPTFILE = "../prompt.txt"
PATTERNDESCRIPTIONPATH = "../patternGOFjson"

if __name__ == "__main__":
    project_root = "../../examples"
    matches = explore_folder_for_triples(project_root)
    print(f"Found {len(matches)} matches:")
    
    for i, (base_files, refactored_tests, pattern_name, parentfolder) in enumerate(matches):
        print(f"\nMatch #{i+1}")
        print("Base files:")
        for f in base_files:
            print(f"  {f}")
        print("test files:")
        for f in refactored_tests:
            print(f"  {f}")
        print(f"Pattern name: {pattern_name}")
        print(f"Folder: {parentfolder}")
        
        # TODO generalize for multiple files
        # For now assume only one file in base_files and refactored_tests, and delete __init__.py
        base_files = [f for f in base_files if "__init__.py" not in f]
        refactored_tests = [f for f in refactored_tests if "__init__.py" not in f]
        
        # Creating a prompt for each match
        prompt_creator = PromptCreator(
            prompt_template_path=PROMPTFILE,
            code_path=base_files[0],  # Assuming base_files is a list of code files
            tests_path=refactored_tests[0],  # Assuming refactored_tests is a list of test files
            design_pattern_name=pattern_name[0],  # Assuming pattern_name is a list of design pattern names
            design_pattern_description_folder=PATTERNDESCRIPTIONPATH
        )
        
        # You might need to adjust the paths for the design pattern descriptions or other files
        prompt = prompt_creator.generate_prompt()
        
        print("\nGenerated Prompt:")
        print(prompt)
        print("length of prompt:", len(prompt.split(" ")))
        
        # Process the current pattern until explicitly skipped
        while True:
            print("\nEnter the refactored code (type 'DONE' to finish current refactor, or 'SKIP' to move to next pattern):")
            refactored_code = ""
            
            # Collect multi-line input
            while True:
                line = input()
                if line.strip() == "SKIP":
                    refactored_code = "SKIP"
                    break
                elif line.strip() == "DONE":
                    break
                refactored_code += line + "\n"
            
            # Check if user wants to skip to the next pattern
            if refactored_code == "SKIP":
                print("Skipping to the next pattern...")
                break
            
            print("lenght of refactored code:", len(refactored_code.split(" ")))

            # Process the refactored code
            codeTester = CodeTester(
                code=refactored_code,
                testcode=prompt_creator.tests,
                filename=os.path.basename(base_files[0]),
                target_dir_path=os.path.join(parentfolder, "llm"),
                name_prefix=FOLDERPREFIX,
            )
            codeTester.set_next_available_name()
            codeTester.create_structure()
            codeTester.run_tests()
            
            print("\nYou can enter another refactored version or type 'SKIP' to move to the next pattern.")

        
        