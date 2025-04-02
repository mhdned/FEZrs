# Import package and libraries
from pathlib import Path
from typing import Union

# Import module and files
from fezrs.utils.file_handler import FileHandler
from fezrs.utils.type_handler import PathLike

class BaseTool:
    """
    ## BaseTool (class)
    A base class for FEZrs tools that process different spectral bands.

    ### Description:
    This class provides a foundation for implementing various spectral analysis tools.
    It handles the initialization of file paths using the FileHandler and enforces the 
    implementation of core methods in subclasses.

    ### Attributes:
        files_handler (FileHandler): An instance of FileHandler that manages the spectral band files.
    """
    def __init__(self, **band_file_path: dict[str, Union[str, Path]]):
        """
        ## __init__ (method)
        Initialize the BaseTool class
        
        ### Args:
        band_file_path (dict[str, Union[str, Path]]): A dictionary mapping band names to file paths.
        
        """
        self.files_handler = FileHandler(**band_file_path)

    def validate(self):
        raise NotImplementedError("Subclasses should implement this method")

    def calculate(self):
        raise NotImplementedError("Subclasses should implement this method")

    def export_file(self, file_path: PathLike):
        raise NotImplementedError("Subclasses should implement this method")
    def run(self, output_path: PathLike, **export_kwargs):
        """
        ## run (Method)
        Runs the full pipeline: validation, calculation, and exporting the image.

        ### Args:
            output_path (str or Path): Directory where the file will be saved.
            **export_kwargs: Additional arguments to customize the export (e.g., figsize, colormap).
        """
        self.validate()
        self.calculate()
        self.export_file(output_path, **export_kwargs)
