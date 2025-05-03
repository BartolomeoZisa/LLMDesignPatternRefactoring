import argparse
import os
import datetime
import json
from promptcreator import PromptCreator
from responseStrategies import OpenAIResponse
import config

class RefactorFrontEnd:
    def __init__(self, code_path, refactored_tests_path, pattern_name, prompt_file_path,
                 temperature, model_name, max_length, strategy, save_folder_path):
        self.code_path = code_path
        self.refactored_tests_path = refactored_tests_path
        self.pattern_name = pattern_name
        self.prompt_file_path = prompt_file_path
        self.temperature = temperature
        self.model_name = model_name
        self.max_length = max_length
        self.strategy = strategy.lower()
        self.save_folder_path = save_folder_path
        self.full_save_path = ""
        self.refactored_code = ""
        self.prompt = ""
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        if self.strategy not in ["openai", "oolama"]:
            raise ValueError(f"Unsupported strategy: {self.strategy}")

    def generate_prompt(self):
        print("[INFO] Generating prompt...")
        prompt_creator = PromptCreator(
            prompt_template_path=self.prompt_file_path,
            code_path=self.code_path,
            tests_path=self.refactored_tests_path,
            design_pattern_name=self.pattern_name,
            design_pattern_description_folder=config.PATTERNDESCRIPTIONPATH
        )
        self.prompt = prompt_creator.generate_prompt()
        print(f"[INFO] Prompt length: {len(self.prompt.split())} words")

    def prepare_save_directory(self):
        base_name = os.path.splitext(os.path.basename(self.code_path))[0]
        folder_name = f"{base_name}_{self.pattern_name}_{self.model_name}_{self.timestamp}"
        self.full_save_path = os.path.join(self.save_folder_path, folder_name)
        os.makedirs(os.path.join(self.full_save_path, "refactored"), exist_ok=True)

    def get_response_strategy(self):
        if self.strategy == "openai":
            return OpenAIResponse(
                model_name=self.model_name,
                temperature=self.temperature,
                max_length=self.max_length
            )
        elif self.strategy == "oolama":
            raise NotImplementedError("Oolama strategy is not yet implemented.")

    def generate_refactored_code(self):
        print(f"[INFO] Using strategy: {self.strategy}")
        response = self.get_response_strategy()
        self.refactored_code = response.process(self.prompt)

        prompt_len = len(self.prompt.split())
        response_len = response.length(self.refactored_code)
        print(f"[INFO] Response length: {response_len} words")
        print(f"[INFO] Total token length: {prompt_len + response_len}")

    def save_outputs(self):
        with open(os.path.join(self.full_save_path, "prompt.txt"), "w") as f:
            f.write(self.prompt)

        refactored_file = os.path.join(self.full_save_path, "refactored", "refactored_code.py")
        with open(refactored_file, "w") as f:
            f.write(self.refactored_code)

        metadata = {
            "code_path": self.code_path,
            "refactored_tests_path": self.refactored_tests_path,
            "pattern_name": self.pattern_name,
            "prompt_file_path": self.prompt_file_path,
            "temperature": self.temperature,
            "model_name": self.model_name,
            "max_length": self.max_length,
            "strategy": self.strategy,
            "timestamp": self.timestamp
        }

        with open(os.path.join(self.full_save_path, "parameters.json"), "w") as f:
            json.dump(metadata, f, indent=4)

        print(f"[INFO] Files saved to: {self.full_save_path}")

    def run(self):
        self.generate_prompt()
        self.prepare_save_directory()
        self.generate_refactored_code()
        self.save_outputs()
        print("[INFO] Done.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate refactoring prompt and process response.")
    parser.add_argument("code_path", help="Path to the original code file")
    parser.add_argument("refactored_tests_path", help="Path to the test file")
    parser.add_argument("pattern_name", help="Design pattern name")
    parser.add_argument("prompt_file_path", help="Path to prompt template file")
    parser.add_argument("save_folder_path", help="Folder where the output will be saved")
    parser.add_argument("--temperature", type=float, default=1.0, help="Temperature for LLM")
    parser.add_argument("--model_name", type=str, default="gpt-4o-mini-2024-07-18", help="Model name")
    parser.add_argument("--max_length", type=int, default=2048, help="Max token length")
    parser.add_argument("--strategy", type=str, default="openai", choices=["openai", "oolama"],
                        help="Strategy to use for LLM response")

    args = parser.parse_args()

    frontend = RefactorFrontEnd(
        code_path=args.code_path,
        refactored_tests_path=args.refactored_tests_path,
        pattern_name=args.pattern_name,
        prompt_file_path=args.prompt_file_path,
        temperature=args.temperature,
        model_name=args.model_name,
        max_length=args.max_length,
        strategy=args.strategy,
        save_folder_path=args.save_folder_path
    )
    frontend.run()


