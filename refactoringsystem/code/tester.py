import os
import argparse
import config
from codetester import CodeTester

class TesterFrontEnd:
    def __init__(self, refactored_code_path, refactored_test_path):
        self.refactored_code_path = refactored_code_path
        self.refactored_test_path = refactored_test_path

    def run(self):
        if not os.path.exists(self.refactored_code_path):
            raise FileNotFoundError(f"Code path does not exist: {self.refactored_code_path}")
        if not os.path.exists(self.refactored_test_path):
            raise FileNotFoundError(f"Test path does not exist: {self.refactored_test_path}")

        #target_dir is the parent directory of dir_name
        test_dir_path = os.path.dirname(os.path.dirname(self.refactored_code_path))
        

        code_tester = CodeTester(
            code_path=self.refactored_code_path,
            test_code_path=self.refactored_test_path,
            test_dir_path = test_dir_path,
        )

        code_tester.create_test_directory()
        code_tester.run_tests()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run tests on refactored code.")
    parser.add_argument("refactored_code_path", help="Path to the refactored code file")
    parser.add_argument("refactored_test_path", help="Path to the refactored test file")
    args = parser.parse_args()

    tester = TesterFrontEnd(args.refactored_code_path, args.refactored_test_path)
    tester.run()