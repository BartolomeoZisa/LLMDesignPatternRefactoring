import os

class PromptCreator:
    def __init__(
        self,
        prompt_template_path="",
        code_path="",
        design_pattern_name="",
        design_pattern_description_folder="",
        tests_path=""
    ):
        # Paths
        self.prompt_template_path = prompt_template_path
        self.code_path = code_path
        self.tests_path = tests_path
        self.design_pattern_description_folder = design_pattern_description_folder
        self.design_pattern_name = design_pattern_name

        # Content
        self.prompt_template = self.read_file(prompt_template_path)
        self.code = self.read_file(code_path)
        self.tests = self.read_file(tests_path)
        self.design_pattern_description_path = os.path.join(
            self.design_pattern_description_folder, f"{design_pattern_name}.txt"
        ) if design_pattern_name else ""
        self.design_pattern_description = self.read_file(self.design_pattern_description_path)

    def read_file(self, file_path):
        """Helper method to read the content of a file."""
        try:
            with open(file_path, 'r') as file:
                return file.read()
        except FileNotFoundError:
            print(f"Error: The file at {file_path} was not found.")
            return ""
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return ""

    def set_prompt_template(self, prompt_template_path):
        self.prompt_template_path = prompt_template_path
        self.prompt_template = self.read_file(prompt_template_path)

    def set_code(self, code_path):
        self.code_path = code_path
        self.code = self.read_file(code_path)

    def set_tests(self, tests_path):
        self.tests_path = tests_path
        self.tests = self.read_file(tests_path)

    def set_design_pattern(self, name):
        self.design_pattern_name = name
        self.design_pattern_description_path = os.path.join(
            self.design_pattern_description_folder, f"{name}.txt"
        )
        self.design_pattern_description = self.read_file(self.design_pattern_description_path)

    def generate_prompt(self):
        return self.prompt_template.format(
            code=self.code,
            design_pattern_name=self.design_pattern_name,
            design_pattern_description=self.design_pattern_description,
            tests=self.tests
        )





