

---

# `refactorer.py` – Automated Code Refactoring Tool

## Overview

`refactorer.py` is a command-line tool designed to assist with automated code refactoring by leveraging language models (such as OpenAI's GPT). It generates a custom prompt based on a given design pattern and source code, submits the prompt to a selected language model, and saves the refactored output along with metadata.

---

## Features

* Generates prompts for code transformation using design patterns.
* Supports OpenAI-based models (e.g., GPT-4).
* Modular strategy-based architecture for LLM integration.
* Automatically creates organized folders with outputs.
* Saves prompt, refactored code, and metadata for reproducibility.

---

## Dependencies

* Python 3.8+
* `promptcreator` module
* `responseStrategies` module (e.g., `OpenAIResponse`)
* `config` module with `PATTERNDESCRIPTIONPATH`

---

## Usage

```bash
python3 refactorer.py [-h] [--temperature TEMPERATURE] [--model_name MODEL_NAME] [--max_length MAX_LENGTH] [--strategy {openai,oolama}]
                     code_path refactored_tests_path pattern_name prompt_file_path save_folder_path
```

### Arguments

| Argument                | Type  | Description                                                                          |
| ----------------------- | ----- | ------------------------------------------------------------------------------------ |
| `code_path`             | str   | Path to the source code file to be refactored.                                       |
| `refactored_tests_path` | str   | Path to the existing test file for reference.                                        |
| `pattern_name`          | str   | Name of the design pattern to apply (e.g., Singleton, Observer).                     |
| `prompt_file_path`      | str   | Path to the prompt template to be used.                                              |
| `save_folder_path`      | str   | Directory where output files will be stored.                                         |
| `--temperature`         | float | Sampling temperature for model generation (default: 1.0).                            |
| `--model_name`          | str   | Name of the model to use (default: `gpt-4o-mini-2024-07-18`).                        |
| `--max_length`          | int   | Maximum number of tokens allowed in the output (default: 2048).                      |
| `--strategy`            | str   | Strategy to use for LLM response. Supported: `openai`, `oolama` (default: `openai`). |

---

## Outputs

* `prompt.txt` – The generated LLM prompt.
* `refactored/<filename>` – The refactored source code.
* `parameters.json` – Metadata about the run (input paths, settings, etc.).

All outputs are saved in a timestamped directory named as:

```
<source_filename>_<pattern>_<model_name>_<timestamp>
```

---

## Class: `RefactorFrontEnd`

### Methods

* **`__init__`**: Initializes refactoring configuration and parameters.
* **`generate_prompt()`**: Builds a prompt using `PromptCreator`.
* **`prepare_save_directory()`**: Creates output folders with timestamp.
* **`get_response_strategy()`**: Selects and returns the model strategy.
* **`generate_refactored_code()`**: Submits the prompt to the model and stores the response.
* **`save_outputs()`**: Saves all output files.
* **`run()`**: Executes the full workflow (prompt → response → save).

---

## Notes

* Currently, only the `openai` strategy is implemented.
* The `oolama` strategy raises `NotImplementedError`.
* Prompt and refactoring logic rely on external modules (`PromptCreator`, `OpenAIResponse`).


