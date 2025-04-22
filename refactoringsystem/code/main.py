from explore import explore_folder_for_triples
from promptcreator import PromptCreator
from codetester import CodeTester
from responseStrategies import ResponseFromCLI, OpenAIResponse
import os
import config


if __name__ == "__main__":
    matches = explore_folder_for_triples(config.PROJECT_ROOT)
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

        if config.ASKSKIP:
            user_input = input("Do you want to skip this pattern? (y/n): ").strip().lower()
            if user_input == 'y':
                print("Skipping this pattern.")
                continue
            elif user_input == 'n':
                print("Continuing with this pattern.")
            elif user_input != 'n':
                print("Invalid input. Please enter 'y' or 'n'.")
                continue

        base_files = [f for f in base_files if "__init__.py" not in f]
        refactored_tests = [f for f in refactored_tests if "__init__.py" not in f]

        prompt_creator = PromptCreator(
            prompt_template_path=config.PROMPTFILE,
            code_path=base_files[0],
            tests_path=refactored_tests[0],
            design_pattern_name=pattern_name[0],
            design_pattern_description_folder=config.PATTERNDESCRIPTIONPATH
        )

        prompt = prompt_creator.generate_prompt()

        with open(config.WRITTEN_PROMPT_FILE, "w") as f:
            f.write(prompt)

        prompt_len = len(prompt.split(" ")) 
        print("length of prompt:", prompt_len)

        for _ in range(config.NUMITERATIONS):
            response = OpenAIResponse()
            refactored_code = response.process(prompt)
            response_len = response.length(refactored_code)
            print("length of response:", response_len)
            print("total length:", prompt_len + response_len)

            codeTester = CodeTester(
                code=refactored_code,
                testcode=prompt_creator.tests,
                filename=os.path.basename(base_files[0]),
                target_dir_path=os.path.join(parentfolder, config.REFACTOREDCODEDIR),
                name_prefix=config.FOLDERPREFIX,
            )
            codeTester.set_next_available_name()
            codeTester.create_structure()
            codeTester.run_tests()

            print("\nYou can enter another refactored version or type 'SKIP' to move to the next pattern.")

        
        