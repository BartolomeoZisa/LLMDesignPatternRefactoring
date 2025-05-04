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

        filename = os.path.basename(self.refactored_code_path)
        target_dir = os.path.dirname(self.refactored_code_path)

        code_tester = CodeTester(
            code=open(self.refactored_code_path).read(),
            testcode=open(self.refactored_test_path).read(),
            filename=filename,
            target_dir_path=target_dir,
            name_prefix = config.FOLDERPREFIX,
        )

        code_tester.set_next_available_name()
        code_tester.create_structure()
        code_tester.run_tests()
