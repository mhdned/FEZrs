# Import module and files
from fezrs.utils.file_handler import FileHandler

class BaseTool:
    """
    A base class for FEZrs tools that process different spectral bands.

    This class provides a foundation for implementing various spectral analysis tools.
    It handles the initialization of file paths using the FileHandler and enforces the 
    implementation of core methods in subclasses.

    Attributes:
        files_handler (FileHandler): An instance of FileHandler that manages the spectral band files.
    """
    def __init__(self, **band_file_path):
        """
            ## constructor method
        """
        self.files_handler = FileHandler(**band_file_path)

    def validate(self):
        raise NotImplementedError("Subclasses should implement this method")

    def calculate(self):
        raise NotImplementedError("Subclasses should implement this method")

    def export(self, file_path):
        raise NotImplementedError("Subclasses should implement this method")
