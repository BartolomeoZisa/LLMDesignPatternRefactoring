import os
from filereader import FileReader, TxtReader, JsonReader  

class PromptCreator:
    def __init__(
        self,
        prompt_template_path="",
        code_path="",
        design_pattern_name="",
        design_pattern_description_folder="",
        tests_path="",
        ignore_keys=None
    ):
        self.file_reader = FileReader(TxtReader())

        # Paths
        self.prompt_template_path = prompt_template_path
        self.code_path = code_path
        self.tests_path = tests_path
        self.design_pattern_description_folder = design_pattern_description_folder
        self.design_pattern_name = design_pattern_name
        self.ignore_keys = ignore_keys if ignore_keys else []

        # Content
        self.prompt_template = self.read_txt_file(prompt_template_path)
        self.code = self.read_txt_file(code_path)
        self.tests = self.read_txt_file(tests_path)
        self.design_pattern_description_path = self._resolve_description_path(design_pattern_name)
        self.design_pattern_description = self.read_design_pattern_description()

    def _resolve_description_path(self, pattern_name):
        """Find the description file (.json preferred, fallback to .txt)."""
        if not pattern_name or not self.design_pattern_description_folder:
            return ""

        json_path = os.path.join(self.design_pattern_description_folder, f"{pattern_name}.json")
        txt_path = os.path.join(self.design_pattern_description_folder, f"{pattern_name}.txt")

        if os.path.exists(json_path):
            return json_path
        elif os.path.exists(txt_path):
            return txt_path
        else:
            print(f"Warning: No description file found for {pattern_name}")
            return ""

    def read_txt_file(self, path):
        self.file_reader.set_strategy(TxtReader())
        return self.file_reader.read(path) if path else ""

    def read_json_file(self, path):
        self.file_reader.set_strategy(JsonReader(ignore_keys=self.ignore_keys))
        return self.file_reader.read(path) if path else ""

    def read_design_pattern_description(self):
        if self.design_pattern_description_path.endswith(".json"):
            return self.read_json_file(self.design_pattern_description_path)
        return self.read_txt_file(self.design_pattern_description_path)

    def set_prompt_template(self, prompt_template_path):
        self.prompt_template_path = prompt_template_path
        self.prompt_template = self.read_txt_file(prompt_template_path)

    def set_code(self, code_path):
        self.code_path = code_path
        self.code = self.read_txt_file(code_path)

    def set_tests(self, tests_path):
        self.tests_path = tests_path
        self.tests = self.read_txt_file(tests_path)

    def set_design_pattern(self, name):
        self.design_pattern_name = name
        self.design_pattern_description_path = self._resolve_description_path(name)
        self.design_pattern_description = self.read_design_pattern_description()

    def generate_prompt(self):
        return self.prompt_template.format(
            code=self.code,
            design_pattern_name=self.design_pattern_name,
            design_pattern_description=self.design_pattern_description,
            tests=self.tests
        )






