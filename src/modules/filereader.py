import json
from abc import ABC, abstractmethod

# === Strategy Interface ===
class ReaderStrategy(ABC):
    @abstractmethod
    def read(self, filepath, **kwargs) -> str:
        pass

# === Concrete Strategy for TXT ===
class TxtReader(ReaderStrategy):
    def read(self, filepath, **kwargs) -> str:
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read()

# === Concrete Strategy for JSON (returns flat text) ===
class JsonReader(ReaderStrategy):
    def __init__(self, ignore_keys=None):
        self.ignore_keys = ignore_keys if ignore_keys else []

    def read(self, filepath) -> str:
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)

        if self.ignore_keys:
            def remove_keys(obj):
                if isinstance(obj, dict):
                    return {k: remove_keys(v) for k, v in obj.items() if k not in self.ignore_keys}
                elif isinstance(obj, list):
                    return [remove_keys(item) for item in obj]
                else:
                    return obj
            data = remove_keys(data)

        flat_lines = []

        def flatten(obj, prefix=''):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    flatten(v, f'{prefix}{k}.')
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    flatten(item, f'{prefix}{i}.')
            else:
                key = prefix.rstrip('.')
                flat_lines.append(f"{key}\n{obj}")

        flatten(data)
        return '\n'.join(flat_lines)

# === Context Class ===
class FileReader:
    def __init__(self, strategy: ReaderStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: ReaderStrategy):
        self._strategy = strategy

    def read(self, filepath, **kwargs) -> str:
        return self._strategy.read(filepath, **kwargs)

