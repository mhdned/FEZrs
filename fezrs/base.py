from pathlib import Path

from .file_handler import OpenFiles


class Base:
    def __init__(self, files: OpenFiles):
        self.files = files

    def calculate(self, extra_params: dict):
        pass

    def export(self, file_path: Path, title: str):
        pass
