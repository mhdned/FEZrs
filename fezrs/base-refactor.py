from abc import ABC
from pathlib import Path
from typing import Union
from uuid import uuid4
import matplotlib.pyplot as plt

BandPathType = Union[str, Path]


class BaseTool(ABC):

    def __init__(self, **bands_path: dict[str, BandPathType]):
        self.__output = None
        self.__tool_name = self.__class__.__name__.replace("Calculator", "")
        pass

    def __validate(self):
        raise NotImplementedError("Subclasses should implement this method")

    def process(self):
        self.__validate()
        raise NotImplementedError("Subclasses should implement this method")

    def __export_file(
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
    ):
        filename_prefix = self.__tool_name

        # Check output property is not empty
        if self.__output is None:
            raise ValueError("Data not computed.")

        # Check the output path is exist and if not create that directory(ies)
        output_path = Path(output_path)
        output_path.mkdir(parents=True, exist_ok=True)

        # Run plot methods
        fig, ax = plt.subplots(figsize=figsize)
        im = ax.imshow(self.__output, cmap=colormap)
        plt.grid(grid)

        # Arguments conditions
        if not show_axis:
            ax.axis("off")

        if show_colorbar:
            fig.colorbar(im, ax=ax)

        if title:
            plt.title(f"{title}-FEZrs")

        # Export file
        filename = f"{output_path}/{filename_prefix}_{uuid4().hex}.png"
        fig.savefig(filename, dpi=dpi, bbox_inches=bbox_inches)

        # Close plt and return value
        plt.close(fig)
        return filename

    def execute(self, output_path: BandPathType, **export_file_kwargs):
        self.__validate()
        self.process()
        self.__export_file(output_path, **export_file_kwargs)
