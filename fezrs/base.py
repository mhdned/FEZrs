# Import packages and libraries
from abc import ABC
from pathlib import Path
from uuid import uuid4
import matplotlib.pyplot as plt

# Import module and files
from fezrs.utils.file_handler import FileHandler
from fezrs.utils.type_handler import BandPathType, BandPathsType


# Definition abstract class
class BaseTool(ABC):

    def __init__(self, **bands_path: BandPathsType):
        self._output = None
        self.__tool_name = self.__class__.__name__.replace("Calculator", "")

        self.files_handler = FileHandler(**bands_path)

    def _validate(self):
        raise NotImplementedError("Subclasses should implement this method")

    def process(self):
        self._validate()
        raise NotImplementedError("Subclasses should implement this method")

    def _customize_export_file(self, ax):
        pass

    def _export_file(
        self,
        output_path: BandPathType,
        title: str | None = None,
        figsize: tuple = (10, 10),
        show_axis: bool = False,
        colormap: str = None,
        show_colorbar: bool = False,
        filename_prefix: str = "Tool_output",
        dpi: int = 500,
        bbox_inches: str = "tight",
        grid: bool = True,
        nrows: int = 1,
        ncols: int = 1,
    ):
        filename_prefix = self.__tool_name

        # Check output property is not empty
        if self._output is None:
            raise ValueError("Data not computed.")

        # Check the output path is exist and if not create that directory(ies)
        output_path = Path(output_path)
        output_path.mkdir(parents=True, exist_ok=True)

        # Run plot methods
        fig, ax = plt.subplots(figsize=figsize, nrows=nrows, ncols=ncols)
        im = ax.imshow(self._output, cmap=colormap)
        plt.grid(grid)

        # Arguments conditions
        if not show_axis:
            ax.axis("off")

        if show_colorbar:
            fig.colorbar(im, ax=ax)

        if title:
            plt.title(f"{title}-FEZrs")

        self._customize_export_file(ax)

        # Export file
        filename = f"{output_path}/{filename_prefix}_{uuid4().hex}.png"
        fig.savefig(filename, dpi=dpi, bbox_inches=bbox_inches)

        # Close plt and return value
        plt.close(fig)
        return filename

    def execute(
        self,
        output_path: BandPathType,
        title: str | None = None,
        figsize: tuple = (10, 10),
        show_axis: bool = False,
        colormap: str = None,
        show_colorbar: bool = False,
        filename_prefix: str = "Tool_output",
        dpi: int = 500,
        bbox_inches: str = "tight",
        grid: bool = True,
        nrows: int = None,
        ncols: int = None,
    ):
        self._validate()
        self.process()
        self._export_file(
            output_path,
            title,
            figsize,
            show_axis,
            colormap,
            show_colorbar,
            filename_prefix,
            dpi,
            bbox_inches,
            grid,
        )
        return self
